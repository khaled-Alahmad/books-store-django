# Generated by Django 4.2.2 on 2023-06-25 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auther',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('publication_date', models.CharField(max_length=4)),
                ('audience', models.CharField(max_length=100)),
                ('page_count', models.IntegerField()),
                ('series', models.CharField(max_length=100)),
                ('isbn', models.CharField(max_length=100)),
                ('edition', models.CharField(max_length=100)),
                ('format', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('is_favorite', models.CharField(max_length=100)),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='books.auther')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateField()),
                ('customer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='books.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SimilarBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_books', to='books.book')),
                ('similar_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchaser_name', models.CharField(max_length=100)),
                ('purchase_date', models.DateField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('book', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='books.order')),
            ],
        ),
        migrations.CreateModel(
            name='BooksFavorites',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_favorite', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='books.customer')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='books.category'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='books.publisher'),
        ),
    ]