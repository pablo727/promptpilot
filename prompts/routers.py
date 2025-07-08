from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework.reverse import reverse
from rest_framework.response import Response

from .views import PromptViewSet, PromptRatingViewSet
from users.views import UserViewSet


class PromptPilotView(APIRootView):

    def get_view_name(self):
        return "Prompt Pilot API"

    def get(self, request, *args, **kwargs):
        api_root_dict = {}

        for prefix, viewset, basename in self.api_root_dict:
            try:
                url = reverse(
                    f"{basename}-list", request=request, format=kwargs.get("format")
                )
                api_root_dict[prefix] = url
            except Exception as e:
                print(f"Error resolving {basename}-list: {e}")
                continue
        return Response(api_root_dict)


class PromptPilotRouter(DefaultRouter):
    APIRootView = PromptPilotView

    def get_api_root_view(self, api_urls=None):
        return self.APIRootView.as_view(api_root_dict=self.registry)


router = PromptPilotRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"prompts", PromptViewSet, basename="prompt")
router.register(r"ratings", PromptRatingViewSet, basename="promptrating")
