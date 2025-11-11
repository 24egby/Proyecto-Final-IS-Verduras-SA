from django.db import models

class VerEmpleados(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_completo = models.CharField(max_length=100)
    correo = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50)
    id_instalacion = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'ver_empleados'