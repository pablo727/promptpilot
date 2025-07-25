from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status

from .serializers import PromptTestRunSerializer
from .models import Prompt
from .services.factory import get_llm_service


class RunPromptViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PromptTestRunSerializer

    def create(self, request):
        prompt_id = request.data.get("prompt")
        provider_name = request.data.get("provider") or "ollama"
        if not prompt_id:
            raise ValidationError({"prompt": "This field is required."})
        llm = request.data.get("llm")
        variables = request.data.get("input_variables", {})

        prompt = Prompt.objects.get(id=prompt_id)
        service = get_llm_service(llm)
        run_data = service.run_prompt(prompt.content, variables)

        test_run = self.serializer_class().Meta.model.objects.create(
            prompt=prompt,
            user=request.user,
            input_variables=variables,
            llm_used=llm,
            result=run_data["result"],
            tokens_used=run_data.get("tokens_used"),
            latency_ms=run_data.get("latency_ms"),
        )
        serializer = PromptTestRunSerializer(test_run)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
