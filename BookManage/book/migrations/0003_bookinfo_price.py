# Generated by Django 2.2.5 on 2023-03-24 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20230324_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinfo',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
