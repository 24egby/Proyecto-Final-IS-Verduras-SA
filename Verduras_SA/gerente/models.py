from django.db import models

class VerGranjas(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    administrador = models.CharField(max_length=100)
    coordinador = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ver_granjas'

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

class VerAdmins(models.Model):
    nombre_completo = models.CharField(max_length=100)
    correo = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ver_admins'

class VerCoords(models.Model):
    nombre_completo = models.CharField(max_length=100)
    correo = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ver_coords'

class VerProductos(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre_producto = models.CharField(max_length=50)
    bodega = models.CharField(max_length=50)
    direccion_bodega = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ver_productos'

class VerAdminsInsta(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_completo = models.CharField(max_length=100)
    correo = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50)
    lugar_trabajo = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'ver_admins_instalacion'

class VerCoordsInsta(models.Model):
    nombre_completo = models.CharField(max_length=100)
    correo = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50)
    lugar_trabajo = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'ver_coords_instalacion'

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.CharField(max_length=100)
    id_instalacion = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'productos'
        managed = False
    def __str__(self):
        return self.producto

class VerAdminsDetalle(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    usuario = models.CharField(max_length=150)
    correo = models.EmailField(max_length=254)
    tipo = models.CharField(max_length=50)
    id_instalacion = models.IntegerField(null=True, blank=True)
    nombre_instalacion = models.CharField(max_length=150, null=True, blank=True)
    tipo_instalacion = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = False  # Django no intentará crear ni modificar la vista
        db_table = 'info_admin'  # Nombre exacto de la vista en MySQL
        verbose_name = 'Administrador Detalle'
        verbose_name_plural = 'Administradores Detalle'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo})"
    
class VerCamiones(models.Model):
    id = models.IntegerField(primary_key=True)
    placa = models.CharField(max_length=10)
    estado = models.CharField(max_length=100)
    id_instalacion = models.IntegerField()

    class Meta:
        managed = False  
        db_table = 'ver_camiones' 

