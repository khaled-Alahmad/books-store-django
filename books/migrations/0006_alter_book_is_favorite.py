# Generated by Django 4.2.2 on 2023-06-26 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_book_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
