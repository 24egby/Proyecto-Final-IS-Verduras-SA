from django.urls import path
import coordinadorGranja.views as VCG

#Rutas Coordinador de Bodega
urlpatterns = [
    path('', VCG.home_coord_bodega, name="Coord-Granja"),
    
    
    
    #Recepciones de camiones
    #path('Llegada-Camiones/', VCB.gestion_Ingreso_Camiones, name='Llegada-Camiones'),
    
]