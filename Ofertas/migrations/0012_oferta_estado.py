# Generated by Django 5.2.1 on 2025-05-27 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ofertas', '0011_rename_estado_oferta_disponibilidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='oferta',
            name='estado',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
