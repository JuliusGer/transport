from django.db import models


class transport_types(models.Model):
    # type_id = models.IntegerField('id типа транспорта')
    type_name = models.CharField('тип транспорта', max_length=20)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = 'transport_type'
        verbose_name_plural = 'transport_types'


class transport_info(models.Model):
    TYPE_SELECT = (
        (1, 'Самолет'),
        (2, 'Поезд'),
        (3, 'Автобус'),
        (4, 'Легковой автомобиль'),
        (5, 'Водный транспорт'),
        (6, 'Вертолет')
    )
    type_id = models.IntegerField('тип транспорта', choices=TYPE_SELECT, default='4')
    transport_number = models.CharField('номер транспорта', max_length=100)
    owner_id = models.IntegerField('id владельца')
    # prev_owner_id = models.IntegerField('id предыдущего владельца')
    manufacture_date = models.DateField('дата выпуска')
    cur_license_expires = models.DateField('права владельца истекают')
    made_in_country = models.CharField('страна выпуска', max_length=100)

    def __str__(self):
        return self.transport_number

    class Meta:
        verbose_name = 'transport_info'
        verbose_name_plural = 'transport_info'


class transport_owners_info(models.Model):
    owner_name = models.CharField('фио владельца', max_length=200)
    TYPE_SELECT = (
        ('Ж', 'Женский'),
        ('М', 'Мужской'),
    )
    owner_gender = models.CharField('пол владельца', max_length=100, choices=TYPE_SELECT, default='Ж')
    passport = models.CharField('паспорт владельца', max_length=500)
    birth_date = models.DateField('дата рождения владельца',  max_length=100)
    citizenship = models.CharField('гражданство владельца', max_length=100)

    def __str__(self):
        return self.owner_name

    class Meta:
        verbose_name = 'transport_owner_info'
        verbose_name_plural = 'transport_owners_info'