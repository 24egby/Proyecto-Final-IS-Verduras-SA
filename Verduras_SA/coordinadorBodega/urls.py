from django.urls import path
import coordinadorBodega.views as VCB

#Rutas Coordinador de Bodega
urlpatterns = [
    path('', VCB.home_coord_bodega, name="Coord-Bodega"),
    
    path('Gestion-Camiones/', VCB.gestion_Camiones, name='Gestion-Camiones-c'),
    #Gestion Empleados
    #path('Gestion-Empleados', VCB.gestion_empleados, name="Gestion-Empleados-B"),
    #path('Gestion-Empleados/Agregar-Empleado', VCB.crear_Empleado, name="Agregar-Empleado-B"),
    #path('Gestion-Empleados/Eliminar-Empleado/<int:id_admin>/', VCB.eliminar_Empleado, name="Eliminar-Empleado-B"),
    #path('Gestion-Empleados/Actualizar-Empleado/<int:id>/', VCB.actualizar_Empleado, name='Actualizar-Empleado-B'),

]