from django.db import models


class Animal(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Собака'),
        ('cat', 'Кошка'),
        ('other', 'Другое'),
    ]
    GENDER_CHOICES = [
        ('M', 'Мальчик'),
        ('F', 'Девочка'),
    ]

    name = models.CharField('Кличка', max_length=100)
    species = models.CharField('Вид', max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField('Порода', max_length=100, blank=True)
    age = models.PositiveIntegerField('Возраст (лет)', default=0)
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.get_species_display()})'


class AnimalPhoto(models.Model):
    animal = models.ForeignKey(Animal, related_name='photos',
                               on_delete=models.CASCADE)
    image = models.ImageField('Фото', upload_to='animals/')

    def __str__(self):
        return f'Фото для {self.animal.name}'


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    ]
    HOUSING_CHOICES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
    ]

    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE,
        related_name='applications', null=True, blank=True,
        verbose_name='Пользователь'
    )
    animal = models.ForeignKey(
        Animal, related_name='applications', on_delete=models.CASCADE
    )

    full_name = models.CharField('ФИО', max_length=200)
    phone = models.CharField('Телефон', max_length=30)
    age = models.PositiveIntegerField('Возраст', default=18)
    housing = models.CharField(
        'Тип жилья', max_length=20, choices=HOUSING_CHOICES, default='apartment'
    )
    family_size = models.PositiveIntegerField('Человек в семье', default=1)
    other_animals = models.CharField(
        'Другие животные', max_length=200, blank=True,
        help_text='Если есть — какие. Если нет — оставьте пустым.'
    )
    comment = models.TextField('Комментарий', blank=True)

    status = models.CharField(
        'Статус', max_length=20, choices=STATUS_CHOICES, default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка #{self.pk} на {self.animal.name} от {self.full_name}'