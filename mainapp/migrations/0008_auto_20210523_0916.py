# Generated by Django 3.2.3 on 2021-05-23 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20210515_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(blank=True, max_length=1024, null=True)),
                ('status', models.CharField(choices=[('new', 'New order'), ('in_progress', 'Order is processing'), ('is_ready', 'Osrder is ready'), ('completed', 'Order completed')], default='new', max_length=100)),
                ('buying_type', models.CharField(choices=[('self', 'Self pickup'), ('delivery', 'Delivery')], default='self', max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_orders', to='mainapp.customer')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(related_name='related_customer', to='mainapp.Order'),
        ),
    ]