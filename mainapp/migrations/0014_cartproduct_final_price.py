# Generated by Django 3.2.3 on 2021-05-23 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20210523_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
