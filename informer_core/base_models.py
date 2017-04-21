from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from ool import VersionField, VersionedMixin
import uuid

class BaseInformerModel(VersionedMixin, models.Model):
    
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name = _('UID'), editable=False)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('Пользователь'), on_delete=models.CASCADE)
    
    revision = models.DateTimeField(verbose_name = _('Обновлено'), auto_now=True)
    
    system = models.CharField(verbose_name = _('Программа создатель'),
                            max_length=100,
                            default=settings.PROGRAM_NAME+' '+settings.INFORMER_VERSION,
                            blank=True
                            )
    
    version = VersionField(verbose_name = _('Версия Object Optimistic Lock'))
    
    REQUIRED_FIELDS = ['uid','user']

    class Meta:
        abstract = True
        
    def get_username(self):
        return self.user
    
    
    