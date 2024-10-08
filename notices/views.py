from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin
from .models import Notice
from .serializers import NoticeSerializer
from rest_framework.decorators import action

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        image_file = self.request.FILES.get('image_file')
        serializer.save(id_user=self.request.user, responsible=self.request.user, image_file=image_file)

    def update(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, image_file=image_file)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Notice.objects.all()
        notice = get_object_or_404(queryset, pk=pk)
        notice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def approve_notice(self, request, pk=None):
        notice = get_object_or_404(Notice, pk=pk)
        notice.is_approved = request.data['is_approved']
        notice.responsible = request.user
        notice.save()
        return Response({'status': 'Aviso aprovado com sucesso!'})

    def user_notices(self, request):
        notices = Notice.objects.filter(id_user=request.user)
        serializer = NoticeSerializer(notices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def approved_notices(self, request):
        notices = Notice.objects.filter(is_approved=True)
        serializer = NoticeSerializer(notices, many=True)
        return Response(serializer.data)
