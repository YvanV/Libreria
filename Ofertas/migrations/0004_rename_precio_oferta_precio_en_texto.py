# Generated by Django 5.2.1 on 2025-05-24 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ofertas', '0003_rename_fecha_salida_oferta_fecha_salida'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oferta',
            old_name='precio',
            new_name='precio_en_texto',
        ),
    ]
