from django.db import models

class VerCamiones(models.Model):
    id = models.IntegerField(primary_key=True)
    placa = models.CharField(max_length=10)
    estado = models.CharField(max_length=100)
    id_instalacion = models.IntegerField()

    class Meta:
        managed = False  # Django no intentará crear, modificar ni borrar esta vista
        db_table = 'ver_camiones'  # Nombre exacto de la vista en MySQL

