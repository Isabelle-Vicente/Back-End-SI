from django.db import models
from users.models import User
from django.utils import timezone

class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    sharing = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    content = models.TextField()  # Melhor para textos longos
    id_user = models.ForeignKey(User, related_name='user_notices', on_delete=models.DO_NOTHING)  # Verifique o nome aqui
    responsible = models.ForeignKey(User, related_name='responsible_notices', on_delete=models.DO_NOTHING)  # Responsável, que pode mudar para o admin
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    local = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)  # Controla se todos podem ver
    is_approved = models.BooleanField(default=False)  # Apenas admin pode alterar

    class Meta:
        db_table = 'posts'
        managed = True
        
    def __str__(self):
        return self.subject
