# Generated by Django 3.2.3 on 2021-05-23 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_alter_customer_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(related_name='related_customer', to='mainapp.Order'),
        ),
    ]
