from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework.reverse import reverse as drf_reverse
from rest_framework.response import Response

from .views import PromptViewSet, PromptRatingViewSet
from users.views import UserViewSet
from playgrounds.views import RunPromptViewSet


class PromptPilotView(APIRootView):
    router = None

    def get_view_name(self):
        return "Prompt Pilot API"

    def get(self, request, *args, **kwargs):
        api_root_dict = {}

        router = self.__class__.router
        if not router:
            return Response({"error": "Router not attached to view."})

        # Grab all registered ViewSets from the router
        for prefix, viewset, basename in router.registry:
            try:
                url = drf_reverse(
                    f"{basename}-list", request=request, format=kwargs.get("format")
                )
                api_root_dict[prefix] = url
            except Exception as e:
                print(f"Error resolving {basename}-list: {e}")

        return Response(api_root_dict)


class PromptPilotRouter(DefaultRouter):
    APIRootView = PromptPilotView

    def get_api_root_view(self, api_urls=None):
        view = super().get_api_root_view(api_urls)
        self.APIRootView.router = self
        return view


router = PromptPilotRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"prompts", PromptViewSet, basename="prompt")
router.register(r"ratings", PromptRatingViewSet, basename="promptrating")
router.register(r"playgrounds_run", RunPromptViewSet, basename="runprompt")
