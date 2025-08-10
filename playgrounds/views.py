import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status

from .serializers import PromptTestRunSerializer
from .models import Prompt
from .services.factory import get_llm_service


logger = logging.getLogger(__name__)


class RunPromptViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PromptTestRunSerializer

    def create(self, request):
        prompt_id = request.data.get("prompt")
        llm = request.data.get("llm", "ollama")
        variables = request.data.get("input_variables", {})

        if not prompt_id:
            raise ValidationError({"prompt": "This field is required."})

        if llm not in ["ollama", "openai"]:
            raise ValidationError({"llm": "Unsupported LLM provider"})

        if not isinstance(variables, dict):
            raise ValidationError({"input_variables": "Must be a dictionary"})

        prompt = get_object_or_404(Prompt, id=prompt_id)
        service = get_llm_service(llm)

        try:
            run_data = service.run_prompt(prompt.content, variables)
        except Exception as e:
            return Response(
                {"detail": f"Failed to run prompt: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        test_run = self.serializer_class().Meta.model.objects.create(
            prompt=prompt,
            user=request.user,
            input_variables=variables,
            llm_used=llm,
            result=run_data["result"],
            tokens_used=run_data.get("tokens_used"),
            latency_ms=run_data.get("latency_ms"),
        )
        logger.info(
            f"Prompt run by user {request.user} on prompt {prompt.id} using {llm}"
        )

        serializer = PromptTestRunSerializer(test_run)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@login_required
def playground_page(request):
    prompts = Prompt.objects.all()
    return render(request, "playgrounds/playground.html", {"prompts": prompts})
