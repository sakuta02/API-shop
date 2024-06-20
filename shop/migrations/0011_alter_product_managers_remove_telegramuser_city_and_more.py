# Generated by Django 5.0.4 on 2024-04-25 15:12

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_telegramuser_related_shop'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='telegramuser',
            name='city',
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active'),
        ),
    ]
