# Generated by Django 4.2.2 on 2023-06-25 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_orderdetails_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='is_favorite',
            field=models.CharField(choices=[('important', 'مهم'), ('excluded', 'استبعاد'), ('none', 'بدون تمييز')], max_length=20),
        ),
    ]