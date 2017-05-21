from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from ool import VersionField, VersionedMixin
import uuid

class TimeFramedModel(models.Model):
    """
    An abstract base class model that provides ``start``
    and ``end`` fields to record a timeframe.

    """
    start = models.DateTimeField(_('Начало'), null=True, blank=True)
    end = models.DateTimeField(_('Окончание'), null=True, blank=True)

    class Meta:
        abstract = True

class BaseInformerModel(VersionedMixin, models.Model):
    
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name = _('UID'), editable=False)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name = _('Пользователь'),
                             on_delete=models.CASCADE,
                             help_text= _('Пользователь как владелец объекта'))
    
    created = models.DateTimeField(verbose_name = _('Создано'), auto_now_add=True, help_text= _('Дата и время создания'), editable=False)
    
    revision = models.DateTimeField(verbose_name = _('Обновлено'), auto_now=True, help_text= _('Дата и время обновления'), editable=False)
    
    system = models.CharField(verbose_name = _('Программа'),
                            max_length=100,
                            default=settings.PROGRAM_NAME+' '+settings.INFORMER_VERSION,
                            blank=True,
                            help_text= _('Программа создатель'),
                            editable=False
                            )
    
    version = VersionField(verbose_name = _('OOL'), help_text= _('Версия оптимистической блокировки объектов'), editable=False)
    
    REQUIRED_FIELDS = ['uid','user']

    class Meta:
        abstract = True
        
    def get_username(self):
        return self.user
    
    
    