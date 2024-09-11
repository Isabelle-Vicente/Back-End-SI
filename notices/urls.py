from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet

router = DefaultRouter()
router.register(r'notices', NoticeViewSet, basename='notice')

urlpatterns = [
    path('', include(router.urls)),  # Inclui as rotas padrão do DRF para Notice
    path('notices/<int:pk>/approve/', NoticeViewSet.as_view({'patch': 'approve_notice'}), name='approve-notice'),
]
