# Generated by Django 5.1.3 on 2024-11-16 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_detallecompra'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='carrito',
        ),
    ]
