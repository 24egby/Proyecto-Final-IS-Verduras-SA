from django.urls import path
import administradorGranja.views as VAG

#Rutas Gerente
urlpatterns = [
    path('', VAG.home_admin_granja, name="Admin-Granja"),
    
    #Gestion Empleados
    path('Gestion-Empleados', VAG.gestion_empleados, name="Gestion-Empleados-G"),
    path('Gestion-Empleados/Agregar-Empleado', VAG.crear_Empleado, name="Agregar-Empleado-G"),
    path('Gestion-Empleados/Eliminar-Empleado/<int:id_admin>/', VAG.eliminar_Empleado, name="Eliminar-Empleado-G"),
    path('Gestion-Empleados/Actualizar-Empleado/<int:id>/', VAG.actualizar_Empleado, name='Actualizar-Empleado-G'),

]