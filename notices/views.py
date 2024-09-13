from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin
from .models import Notice
from .serializers import NoticeSerializer

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Define o usuário criador e responsável no momento da criação do aviso
        serializer.save(id_user=self.request.user, responsible=self.request.user)

    def update(self, request, *args, **kwargs):
        notice = self.get_object()

        # Apenas o criador ou admin podem editar enquanto não aprovado
        if not notice.is_approved and (request.user == notice.id_user or request.user.is_admin):
            serializer = NoticeSerializer(notice, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Se aprovado, só o administrador pode editar
        if notice.is_approved and not request.user.is_admin:
            return Response({'error': 'Apenas o administrador pode editar um aviso aprovado.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def approve_notice(self, request, pk=None):
        notice = get_object_or_404(Notice, pk=pk)

        if not request.user.is_admin:
            return Response({'error': 'Apenas administradores podem aprovar avisos.'}, status=status.HTTP_403_FORBIDDEN)

        notice.is_approved = True
        notice.responsible = request.user  # O admin se torna o responsável
        notice.save()
        return Response({'status': 'Aviso aprovado com sucesso!'})

    def user_notices(self, request):
        # Filtra avisos pertencentes ao usuário autenticado
        notices = Notice.objects.filter(id_user=request.user)
        serializer = NoticeSerializer(notices, many=True)
        return Response(serializer.data)
