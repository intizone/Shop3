# Generated by Django 5.0.2 on 2024-02-21 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_enterproduct_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='enterproduct',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='productimage',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='productreview',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]