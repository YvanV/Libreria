from django.db import models

# Create your models here.

class Oferta(models.Model):
    titulo = models.CharField(max_length=200, null=True, blank=True, default=None)
    autor = models.CharField(max_length=100, null=True, blank=True, default=None)
    precio_en_texto = models.CharField(max_length=20, null=True, blank=True, default=None)
    fecha_ingreso = models.DateField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    pagina = models.IntegerField(null=True, blank=True, default=None)
    secuencia = models.IntegerField(null=True, blank=True, default=None)
    disponibilidad = models.CharField(max_length=50, null=True, blank=True, default=None)
    disponibilidad_anterior = models.CharField(max_length=50, null=True, blank=True, default=None)
    enlace = models.URLField(max_length=200, null=True, blank=True, default=None)
    estado = models.CharField(max_length=10, null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["titulo", "autor"], name="unique_libro"
            )
        ]
    
    def __str__ (self):
        return f"{self.titulo}/{self.autor}"


