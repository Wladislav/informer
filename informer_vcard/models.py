from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _
from informer_core.base_models import BaseInformerModel
from informer_core.base_models import TimeFramedModel
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
#https://github.com/carljm/django-model-utils
from model_utils import Choices
from model_utils.fields import StatusField
from informer_core.utils import INFORMER_STATUS
from django_tz.fields import TimeZoneField
from geoposition.fields import GeopositionField

#https://ru.wikipedia.org/wiki/VCard

class vCard(BaseInformerModel, TimeFramedModel):

    class Meta:
        verbose_name = _('Карточка vCard')
        verbose_name_plural = _('Карточки vCard')
        
    STATUS = INFORMER_STATUS
    CLASS = Choices(('public', _('Публично')), ('private', _('Приватно')), ('confidential', _('Конфедициально')))
    
    label = models.CharField(verbose_name = _('Представление'),
                            max_length=256,
                            default='',
                            blank=True,
                            help_text= _('Основное представление')
                            )
    language = models.CharField(choices=settings.LANGUAGES,
                                verbose_name = _('Язык'),
                                max_length=5,
                                blank=False,
                                default=settings.LANGUAGE_CODE,
                                help_text= _('Язык общения')
                                )
    photo = models.ImageField(verbose_name = _('Фотография'),
                              upload_to='vcard_photo/',
                              blank=True,
                              help_text= _('Фотография в формате jpg, png, gif')
                              )
    logo = models.ImageField(verbose_name = _('Логотип'),
                             upload_to='vcard_logo/',
                             blank=True,
                             help_text= _('Логотип персонального бренда или предприятия')
                             )
    sound = models.FileField(upload_to='vcard_sound/',
                             verbose_name = _('Звук'),
                             blank=True,
                             help_text= _('Голос или музыкальное сопровождение mp3, ogg, wav')
                             )    
    # geo = GeopositionField(verbose_name = _('Геопозиция GPS'),
    #                        blank=True,
    #                        help_text= _('Глобальное позиционирование Nord, West (21.36214, -157.95341)')
    #                        )
    note = models.CharField(verbose_name = _('Заметка'),
                            max_length=256,
                            default='',
                            blank=True,
                            help_text= _('Заметка')
                            )
    url = models.URLField(max_length=256,
                          verbose_name = _('URL'),
                          blank=True,
                          help_text= _('Ссылка в интернете')
                          )
    tz = TimeZoneField(verbose_name = _('Часовой пояс'),
                       default=settings.TIME_ZONE,
                       help_text= _('Выберите из списка')
                       )
    category = models.CharField(verbose_name = _('Категория'),
                            max_length=256,
                            default='',
                            blank=False,
                            help_text= _('Категория информации')
                            )
    # Черновик, Опубликовано, Удалено
    status = StatusField(verbose_name = _('Статус'),
                         help_text= _('Статус объекта')
                         )
    secure = models.CharField(verbose_name = _('Доступ'),
                                    choices=CLASS,
                                    default=CLASS.public,
                                    max_length=20,
                                    help_text= _('Уровень доступа к этой информации')
                                    ) 
    secure_key = models.BinaryField(verbose_name = _('Открытый ключ или сертификат аутентификации'),
                                    blank=True,
                                    help_text= _('Открытый ключ или сертификат аутентификации')
                                    )
    objectname = models.CharField(verbose_name = _('Имя модели'),
                               max_length=5,
                               default='VCARD',
                               blank=False,
                               help_text= _('*')
                               )    
    def __str__(self):
         return 'vCard: %s' % self.label
        
def create_vcard(sender, **kwargs):
     vCard = kwargs["instance"]
     if kwargs["created"]:
         vcard_names = vCard_names(owner=vCard)
         vcard_names.save()

post_save.connect(create_vcard, sender=vCard)

class vCard_phone(models.Model):
    
    class Meta:
        verbose_name = _('vCard Телефон')
        verbose_name_plural = _(' vCard Телефоны')
        
    PHONE_TYPES = Choices(
        ('home',_('По месту проживания')),
        ('work',_('По месту работы')),
        ('voice',_('Для голосового общения')),
        ('fax',_('Для передачи факсов')),
        ('cell',_('Сотовый')),
        ('pager',_('Для передачи сообщений на пейджер')),
        ('bbs',_('Обслуживает электронную доску объявлений')),
        ('car',_('Автомобильный')),
        )
    PHONE_TYPES_APPS = Choices(
        ('msg',_('Поддерживает передачу голосовых сообщений')),
        ('video',_('Поддерживает видеоконференции')),
        ('modem',_('По этому номеру работает модем')),
        ('isdn',_('Предоставляет услуги ISDN'))
        )
    owner = models.ForeignKey(vCard,
                              verbose_name = _('Владелец'),
                              on_delete=models.CASCADE,
                              help_text= _('*')
                              )
    tel = PhoneNumberField(verbose_name = _('Телефон'),
                           blank=True,
                           default='',
                           help_text= _('Телефон с кодом города')
                           )
    type = models.CharField(verbose_name = _('Тип телефона'),
                            choices=PHONE_TYPES,
                            default=PHONE_TYPES.cell,
                            max_length=20,
                            help_text= _('Тип телефона')
                            )
    function = models.CharField(verbose_name = _('Функциональность'),
                                choices=PHONE_TYPES_APPS,
                                default='',
                                max_length=20,
                                help_text= _('Функциональность телефона')
                                )
    prefer = models.BooleanField(verbose_name = _('Предпочтительный'),
                                 default=False,
                                 help_text= _('Рекомендуется как основной')
                                 )
    def __str__(self):
         return 'vCard phone: %s' % self.tel    
    
class vCard_adress(models.Model):
    
    class Meta:
        verbose_name = _('vCard Адрес')
        verbose_name_plural = _(' vCard Адреса')
        
    ADRESS_TYPES = Choices(
        ('dom',_('Местный')),
        ('intl',_('Международный')),
        ('postal',_('Для писем')),
        ('parcel',_('Для посылок')),
        ('home',_('Место проживания')),
        ('work',_('Место работы')),
        )
    owner = models.ForeignKey(vCard,
                              verbose_name = _('Владелец'),
                              on_delete=models.CASCADE,
                              help_text= _('*')
                              )
    adress = models.CharField(verbose_name = _('Адрес'),
                           max_length=256,
                           default='',
                           blank=True,
                           help_text= _('Полный адрес строкой')
                           )
    type = models.CharField(verbose_name = _('Тип адреса'),
                            choices=ADRESS_TYPES,
                            default=ADRESS_TYPES.home,
                            max_length=20,
                            help_text= _('Тип Адреса')
                            )
    geo = GeopositionField(verbose_name = _('GPS'),
                           blank=True,
                           help_text= _('Глобальное позиционирование Nord, West (21.36214, -157.95341)')
                           )
    prefer = models.BooleanField(verbose_name = _('Предпочтительный'),
                                 default=False,
                                 help_text= _('Рекомендуется как основной')
                                 )
    def __str__(self):
         return 'vCard adress: %s' % self.adress    
    
class vCard_email(models.Model):
    
    class Meta:
        verbose_name = _('vCard Email')
        verbose_name_plural = _(' vCard Email')
        
    EMAIL_TYPE = Choices(
        ('home',_('Домашний')),
        ('work',_('Рабочий'))
        )
    owner = models.ForeignKey(vCard,
                              verbose_name = _('Владелец'),
                              on_delete=models.CASCADE,
                              help_text= _('*')
                              )
    
    email = models.EmailField(blank=False,
                              help_text= _('Электронный почтовый адрес')
                              )
    
    type = models.CharField(verbose_name = _('Тип email'),
                            choices=EMAIL_TYPE,
                            default=EMAIL_TYPE.home,
                            max_length=20,
                            help_text= _('Тип электронного почтового адреса')
                            )    
    prefer = models.BooleanField(verbose_name = _('Предпочтительный'),
                                 default=False,
                                 help_text= _('Рекомендуется как основной')
                                 )
    def __str__(self):
         return 'vCard Email: %s' % self.email
        
class vCard_names(models.Model):
    
    class Meta:
        verbose_name = _('vCard Имена')
        verbose_name_plural = _(' vCard Имена')
        
    owner = models.OneToOneField(vCard,
                                 primary_key=True,
                                 verbose_name = _('Владелец'),
                                 on_delete=models.CASCADE,
                                 blank = True,
                                 help_text= _('*')
                                 )
    
    full_name = models.CharField(verbose_name = _('Полное имя'),
                                 max_length=256,
                                 default='',
                                 blank=False,
                                 help_text= _('Полное имя')
                                 )
    bday = models.DateTimeField(verbose_name = _('День рождения'),
                                help_text= _('День рождения или создания'),
                                null=True,
                                blank=True)       
    first_name = models.CharField(verbose_name = _('Имя'),
                                  max_length=256,
                                  default='',
                                  blank=True,
                                  help_text= _('Часть имени: Имя')
                                  )
    second_name = models.CharField(verbose_name = _('Фамилия'),
                                   max_length=256,
                                   default='',
                                   blank=True,
                                   help_text= _('Часть имени: Фамилия')
                                   )
    middle_name = models.CharField(verbose_name = _('Отчество'),
                                   max_length=256,
                                   default='',
                                   blank=True,
                                   help_text= _('Часть имени: Отчество')
                                   )
    prefix = models.CharField(verbose_name = _('Префикс'),
                              max_length=50,
                              default='',
                              blank=True,
                              help_text= _('Префикс имени (Господин, Доктор)')
                              )
    suffix = models.CharField(verbose_name = _('Суффикс'),
                              max_length=50,
                              default='',
                              blank=True,
                              help_text= _('Суффикс имени (Младший)')
                              )
    nickname = models.CharField(verbose_name = _('Ник'),
                                max_length=100,
                                default='',
                                blank=True,
                                help_text= _('Прозвище')
                                )    
    title = models.CharField(verbose_name = _('Должность'),
                             max_length=256,
                             default='',
                             blank=True,
                             help_text= _('Должность на предприятии')
                             )    
    role = models.CharField(verbose_name = _('Роль'),
                            max_length=256,
                            default='',
                            blank=True,
                            help_text= _('Ведущая роль на предприятии')
                            )
    sort_as = models.CharField(verbose_name = _('Сортировка'),
                            max_length=256,
                            default='',
                            blank=True,
                            help_text= _('*')
                            )
    def __str__(self):
         return '%s' % self.full_name

class vCard_impp(models.Model):
    
    class Meta:
        verbose_name = _('vCard Социальная сеть')
        verbose_name_plural = _(' vCard Социальнае сети')
        
    owner = models.ForeignKey(vCard,
                              verbose_name = _('Владелец'),
                              on_delete=models.CASCADE,
                              help_text= _('*')
                              )
    url = models.URLField(max_length=256,
                          verbose_name = _('URL'),
                          blank=False,
                          help_text= _('Ссылка в интернете')
                          )
    prefer = models.BooleanField(verbose_name = _('Предпочтительный'),
                                 default=False,
                                 help_text= _('Рекомендуется как основной')
                                 )
    def __str__(self):
         return 'vCard social: %s' % self.url    
    
class vCard_organization(models.Model):
    
    class Meta:
        verbose_name = _('vCard Организация')
        verbose_name_plural = _(' vCard Организации')
        
    owner = models.ForeignKey(vCard,
                              verbose_name = _('Владелец'),
                              on_delete=models.CASCADE,
                              help_text= _('*')
                              )
    form = models.CharField(verbose_name = _('Правовая форма'),
                           max_length=100,
                           default='',
                           blank=True,
                           help_text= _('Организационно правовая форма предприятия')
                           )
    org = models.CharField(verbose_name = _('Наименование организации'),
                           max_length=256,
                           default='',
                           blank=False,
                           help_text= _('Полное наименование организации')
                           )
    
    any = models.CharField(verbose_name = _('Дополнительно'),
                           max_length=100,
                           default='',
                           blank=True,
                           help_text= _('Дополнительная информация')
                           )    
    prefer = models.BooleanField(verbose_name = _('Предпочтительный'),
                                 default=False,
                                 help_text= _('Рекомендуется как основной')
                                 )
    def __str__(self):
         return 'vCard organization: %s' % self.org     
    
    
class vCard_related(models.Model):

    class Meta:
        verbose_name = _('vCard Связь')
        verbose_name_plural = _(' vCard Связи')
        
    RELATED_TYPE = Choices(
        ('contact',_('Контактируем')),
        ('acquaintance',_('Знакомый/Знакомая')),
        ('friend',_('Друг/Подружка')),
        ('met',_('Встречились')),
        ('co-worker',_('Сотрудник/Сотрудница')),
        ('colleague',_('Коллега')),
        ('co-resident',_('Живем вместе')),
        ('neighbor',_('Сосед')),
        ('child',_('Ребенок')),
        ('parent',_('Родитель')),
        ('sibling',_('Брат/Сестра')),
        ('spouse',_('Супруг(а)')),
        ('kin',_('Родственник')),
        ('muse',_('Муза')),
        ('crush',_('Подавляет')),
        ('date',_('Встречаемся')),
        ('sweetheart',_('Любимый/Любимая')),
        ('me',_('Я сам')),
        ('agent',_('Доверенное лицо')),
        ('emergency',_('Запасной')),
        )
    
    KIND_TYPE = Choices(
        ('individual',_('Индивидульная')),
        ('organization',_('Организация')),
        ('group',_('Группа')),
        ('location',_('Местонахождение')),
    )
        
    owner = models.ForeignKey(vCard,
                              verbose_name = _('Владелец'),
                              on_delete=models.CASCADE,
                              help_text= _('*')
                              )
    relate = models.ForeignKey(vCard,
                               related_name="related_relate",
                               blank=False,
                               null=True,
                               on_delete=models.CASCADE,
                               help_text= _('Связи с другой информацией')
                              )
    type = models.CharField(verbose_name = _('Тип связи'),
                            choices=RELATED_TYPE,
                            default=RELATED_TYPE.contact,
                            max_length=20,
                            help_text= _('Тип связи')
                            )
    king = models.CharField(verbose_name = _('Вид группы'),
                            choices=KIND_TYPE,
                            default=KIND_TYPE.group,
                            max_length=20,
                            help_text= _('Вид группы')
                            )
    # def __str__(self):
    #      return 'vCard organization: %s' % self.org    

class vCard_expertise(models.Model):
    
    class Meta:
        verbose_name = _('vCard Знание')
        verbose_name_plural = _(' vCard Знания')
        
    EXPERTISE_LEVEL = Choices(
        ('beginner',_('Начальный')),
        ('average',_('Средний')),
        ('expert',_('Эксперт')),
        )
    
    owner = models.ForeignKey(vCard, verbose_name = _('Владелец'),
                              on_delete=models.CASCADE,
                              help_text= _('*')
                              )        
    expertise = models.CharField(verbose_name = _('Знание'),
                                 max_length=256,
                                 default='',
                                 blank=False,
                                 help_text= _('Наименование знания')
                                 )
    type = models.CharField(verbose_name = _('Уровень'),
                            choices=EXPERTISE_LEVEL,
                            default=EXPERTISE_LEVEL.average,
                            max_length=20,
                            help_text= _('Уровень экспертности')
                            )
    def __str__(self):
         return 'vCard expertise: %s' % self.expertise
    
class vCard_hobby(models.Model):
    
    class Meta:
        verbose_name = _('vCard Увлечение')
        verbose_name_plural = _(' vCard Увлечения')
        
    HOBBY_LEVEL = Choices(
        ('high',_('Высокий')),
        ('medium',_('Средний')),
        ('low',_('Низкий')),
        )
    
    owner = models.ForeignKey(vCard, verbose_name = _('Владелец'),
                              on_delete=models.CASCADE,
                              help_text= _('*')
                              )
    hobby = models.CharField(verbose_name = _('Увлечение'),
                                 max_length=256,
                                 default='',
                                 blank=False,
                                 help_text= _('Наименование Увлечения')
                                 )    
    expertise = models.CharField(verbose_name = _('Увлечение'),
                                 max_length=256,
                                 default='',
                                 blank=False,
                                 help_text= _('Увлечение')
                                 )
    type = models.CharField(verbose_name = _('Уровень'),
                            choices=HOBBY_LEVEL,
                            default=HOBBY_LEVEL.medium,
                            max_length=20,
                            help_text= _('Уровень экспертности')
                            )
    def __str__(self):
         return 'vCard hobby: %s' % self.hobby
        
class vCard_interest(models.Model):
    
    class Meta:
        verbose_name = _('vCard Интерес')
        verbose_name_plural = _(' vCard Интересы')
        
    INTEREST_LEVEL = Choices(
        ('high',_('Высокий')),
        ('medium',_('Средний')),
        ('low',_('Низкий')),
        )
    
    owner = models.ForeignKey(vCard, verbose_name = _('Владелец'),
                              on_delete=models.CASCADE,
                              help_text= _('*')
                              )        
    interest = models.CharField(verbose_name = _('Интерес'),
                                 max_length=256,
                                 default='',
                                 blank=False,
                                 help_text= _('Наименование интереса')
                                 )
    type = models.CharField(verbose_name = _('Уровень'),
                            choices=INTEREST_LEVEL,
                            default=INTEREST_LEVEL.medium,
                            max_length=20,
                            help_text= _('Уровень эксперности')
                            )
    def __str__(self):
         return 'vCard interest: %s' % self.interest    