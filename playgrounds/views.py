from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PromptTestRunSerializer
from .models import Prompt
from .services.factory import get_llm_service


class RunPromptView(APIView):
    def post(self, request):
        prompt_id = request.data.get("prompt")
        llm = request.data.get("llm")
        variables = request.data.get("input_variables", {})

        prompt = Prompt.objects.get(id=prompt_id)
        service = get_llm_services(llm)
        run_data = service.run_prompt(prompt.content, variables)

        test_run = PromptTestRun.objects.create(
            prompt=prompt,
            user=request.user,
            input_variables=variables,
            llm_used=llm,
            result=run_data["result"],
            tokens_used=run_data.get("tokens_used"),
        )
        serializer = PromptTestRunSerializer(test_run)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
