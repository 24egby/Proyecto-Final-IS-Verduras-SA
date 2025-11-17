from django.urls import path
import coordinadorBodega.views as VCB

#Rutas Coordinador de Bodega
urlpatterns = [
    path('', VCB.home_coord_bodega, name="Coord-Bodega"),
    
    #Gestion Camiones
    path('Gestion-Camiones/', VCB.gestion_Camiones, name='Gestion-Camiones-c'),
    path('Gestion-Camiones/Actualizar-Camion', VCB.actualizar_Estado_Camion, name='Actualizar-Camion'),
    
    #Salidas de camiones
    path('Salida-Camiones/', VCB.gestion_Salida_Camiones, name='Salida-Camiones'),
    path('Salida-Camiones/Generar-Salida-Granja/<int:id>/', VCB.generar_Salida_Granja, name='Salida-Granja'),
    #path('Salida-Camiones/Generar-Salida-Venta/<int:id>/', VCB.generar_Salida_Venta, name='Salida-Venta'),
    
    
    #Recepciones de camiones
    path('Llegada-Camiones/', VCB.gestion_Ingreso_Camiones, name='Llegada-Camiones'),
    
]