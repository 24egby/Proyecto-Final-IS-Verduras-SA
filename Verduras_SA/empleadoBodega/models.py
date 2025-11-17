from django.db import models

class VerBodegas(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    administrador = models.CharField(max_length=100)
    coordinador = models.CharField(max_length=100)
    producto = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'ver_bodegas'
        
class VerProductos(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre_producto = models.CharField(max_length=50)
    bodega = models.CharField(max_length=50)
    direccion_bodega = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ver_productos'
        
        
        