from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

INFORMER_STATUS = Choices(
    ('draft',_('Черновик')),
    ('published',_('Опубликовано')),
    ('deleted',_('Удалено'))
    )

