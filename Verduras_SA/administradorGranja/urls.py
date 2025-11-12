from django.urls import path
import administradorBodega.views as VAB

#Rutas Gerente
urlpatterns = [
    path('', VAB.home_admin_bodega, name="Admin-Bodega"),
    
    #Gestion Empleados
    path('Gestion-Empleados', VAB.gestion_empleados, name="Gestion-Empleados"),
    path('Gestion-Empleados/Agregar-Empleado', VAB.crear_Empleado, name="Agregar-Empleado"),
    path('Gestion-Empleados/Eliminar-Empleado/<int:id_admin>/', VAB.eliminar_Empleado, name="Eliminar-Empleado"),
    path('Gestion-Empleados/Actualizar-Empleado/<int:id>/', VAB.actualizar_Empleado, name='Actualizar-Empleado'),

]