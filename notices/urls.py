from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet

router = DefaultRouter()
router.register(r'notices', NoticeViewSet, basename='notice')

urlpatterns = [
    path('', include(router.urls)),  # Inclui as rotas padrão do DRF para Notice
    path('notices/<uuid:pk>/approve/', NoticeViewSet.as_view({'patch': 'approve_notice'}), name='approve-notice'),
    path('notices/user/', NoticeViewSet.as_view({'get': 'user_notices'}), name='user-notices'),  # Rota personalizada
]
