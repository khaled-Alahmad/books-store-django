# Generated by Django 4.2.2 on 2023-07-14 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_alter_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='customer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='books.customer'),
        ),
    ]
