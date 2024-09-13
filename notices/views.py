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
        serializer.save(id_user=self.request.user, responsible=self.request.user)

    def update(self, request, *args, **kwargs):
        notice = self.get_object()

        if not notice.is_approved and (request.user == notice.id_user or request.user.is_admin):
            serializer = NoticeSerializer(notice, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if notice.is_approved and not request.user.is_admin:
            return Response({'error': 'Apenas o administrador pode editar um aviso aprovado.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        notice = self.get_object()

        if request.user != notice.id_user and not request.user.is_admin:
            return Response({'error': 'Você não tem permissão para deletar este aviso.'}, status=status.HTTP_403_FORBIDDEN)

        if notice.is_approved and not request.user.is_admin:
            return Response({'error': 'Apenas administradores podem deletar avisos aprovados.'}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

    def approve_notice(self, request, pk=None):
        notice = get_object_or_404(Notice, pk=pk)

        if not request.user.is_admin:
            return Response({'error': 'Apenas administradores podem aprovar avisos.'}, status=status.HTTP_403_FORBIDDEN)

        notice.is_approved = True
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
