from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
# Registering messages as a nested ressource
conversations_router.register(r'messages', MessageViewSet, basename='conversation-message')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify', TokenVerifyView.as_view(), name='token_verify')
]