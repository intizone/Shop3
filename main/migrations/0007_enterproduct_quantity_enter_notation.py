# Generated by Django 5.0.2 on 2024-02-09 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_enterproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterproduct',
            name='quantity_enter_notation',
            field=models.SmallIntegerField(choices=[(0, 'Ayrish'), (1, 'Qo`shish')], default=0),
        ),
    ]
