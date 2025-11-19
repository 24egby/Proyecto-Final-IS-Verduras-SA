from django.urls import path
import coordinadorGranja.views as VCG

#Rutas Coordinador de Bodega
urlpatterns = [
    path('', VCG.home_coord_bodega, name="Coord-Granja"),
    
    #Recepciones de camiones
    path('Llegada-Camiones/', VCG.escaneo_placa_ingreso, name='Llegada-Camiones-CG'),
    path('Llegada-Camiones/Reconocer-Placa', VCG.detectar_placa, name='Reconocer-Placa'),
    
    #Cargar Camiones
    path('Gestion-Ingresos/', VCG.gestion_Ingreso_Camiones, name='Gestion-Ingresos'),
    path('Gestion-Ingresos/Actualizar-Ingreso/<int:id>/', VCG.actualizar_Ingreso_Camione, name='Actualizar-Ingreso-CG'),
]