# Generated by Django 3.2.9 on 2021-11-26 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['id'], 'verbose_name': 'Обзор', 'verbose_name_plural': 'Обзоры'},
        ),
    ]
