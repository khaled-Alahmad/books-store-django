# Generated by Django 4.2.2 on 2023-07-14 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_purchase_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cluster',
            field=models.IntegerField(default=0),
        ),
    ]
