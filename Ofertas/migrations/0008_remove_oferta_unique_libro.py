# Generated by Django 5.2.1 on 2025-05-26 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ofertas', '0007_rename_nombre_oferta_titulo'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='oferta',
            name='unique_libro',
        ),
    ]
