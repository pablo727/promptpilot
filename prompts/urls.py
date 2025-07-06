from rest_framework.routers import DefaultRouter

from .views import PromptViewSet, PromptRatingViewSet

router = DefaultRouter()
router.register(r"prompts", PromptViewSet)
router.register(r"ratings", PromptRatingViewSet)


urlpatterns = router.urls
