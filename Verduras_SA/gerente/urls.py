from django.urls import path
import gerente.views as VG

#Rutas Gerente
urlpatterns = [
    path('', VG.home_gerente, name="Gerente"),
    
    #Gestion Granjas
    path('Gestion-Granjas', VG.gestion_Granjas, name="Gestion-Granjas"),
    path('Gestion-Granjas/Crear-Granja', VG.crear_Granja, name="Crear-Granja"),
    path('Gestion-Granjas/Eliminar-Granja/<int:id>/', VG.eliminar_Granja, name='Eliminar-Granja'),
    
    #Gestion Admins
    path('Gestion-Admin', VG.gestion_Admins, name="Gestion-Admins"),
    path('Gestion-Admin/Agregar-Admin', VG.crear_Admins, name="Agregar-Admin"),
    path('Gestion-Admin/Obtener-Instalaciones/', VG.obtener_instalaciones, name='Obtener-Instalaciones'),
    path('Gestion-Admin/Eliminar-Admin/<int:id_admin>/', VG.eliminar_admin, name="Eliminar-Admin"),
    
    #Vista Coords
    path('Vista-Coords', VG.vista_coordinadores, name="Vista-Coords"),
    
    #Gestion Productos
    path('Gestion-Productos', VG.gestion_Productos, name="Gestion-Productos"),
    path('Gestion-Productos/Eliminar-Producto/<int:id>/', VG.eliminar_producto, name="Eliminar-Producto"),
    path("Gestion-Productos/Agregar-Producto/", VG.agregar_producto, name="Agregar-Producto"),
    
    #Gestion Bodegas
    path('Gestion-Bodegas', VG.gestion_Bodegas, name="Gestion-Bodegas"),
    path('Gestion-Bodegas/Crear-Bodega', VG.crear_Bodega, name="Crear-Bodega"),
    path('Gestion-Bodegas/Eliminar-Bodega/<int:id>/', VG.eliminar_Granja, name='Eliminar-Bodega'),
    
]