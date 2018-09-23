# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, db_column='ID', serialize=False)),
                ('user_id', models.IntegerField(unique=True, verbose_name='ID пользователя', db_column='USER_ID')),
                ('amount', models.FloatField(db_column='AMOUNT', verbose_name='Сумма')),
                ('min_value', models.FloatField(db_column='MIN_VALUE', verbose_name='Нижний порог')),
                ('max_value', models.FloatField(db_column='MAX_VALUE', verbose_name='Верхний порог')),
            ],
            options={
                'verbose_name_plural': 'Счета',
                'ordering': ('user_id',),
                'verbose_name': 'Счёт',
                'db_table': 'ACCOUNT',
            },
        ),
    ]
