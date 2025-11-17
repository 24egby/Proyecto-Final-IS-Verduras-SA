from django.urls import path
import empleadoBodega.views as VEB

#Rutas Coordinador de Bodega
urlpatterns = [
    path('', VEB.home_emple_bodega, name="Empleado-Bodega"),
]