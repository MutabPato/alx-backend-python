from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.SimpleRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)
urlpatterns = router.urls