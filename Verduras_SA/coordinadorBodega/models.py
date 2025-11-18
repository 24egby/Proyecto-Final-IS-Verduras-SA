from django.db import models

class VerCamiones(models.Model):
    id = models.IntegerField(primary_key=True)
    placa = models.CharField(max_length=10)
    estado = models.CharField(max_length=100)
    id_instalacion = models.IntegerField()

    class Meta:
        managed = False 
        db_table = 'ver_camiones' 

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

class VerRegistroSalidaGranja(models.Model):
    id = models.IntegerField(primary_key=True)
    producto = models.CharField(max_length=100)
    bodega = models.CharField(max_length=100)
    granja = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    camion = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    class Meta:
        managed = False   
        db_table = 'ver_registro_salida_granja' 

class VerRegistroSalidaVenta(models.Model):
    id = models.IntegerField(primary_key=True)
    producto = models.CharField(max_length=100)
    bodega = models.CharField(max_length=100)
    calidad = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    camion = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    class Meta:
        managed = False   
        db_table = 'ver_registro_salida_venta' 

class VerProductos(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre_producto = models.CharField(max_length=50)
    bodega = models.CharField(max_length=50)
    direccion_bodega = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ver_productos'

class VerInventario(models.Model):
    id = models.IntegerField(primary_key=True)
    id_producto = models.IntegerField()
    excelente = models.IntegerField()
    bueno = models.IntegerField()
    defectuoso = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ver_inventario'