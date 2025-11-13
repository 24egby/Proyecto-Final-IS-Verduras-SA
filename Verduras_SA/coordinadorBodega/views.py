from django.contrib.auth.decorators import login_required
from .models import  VerCamiones
from django.shortcuts import render
from django.db import connection

def obtener_id_instalacion(user_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET @o_id_instalacion = 0;")
            cursor.execute(f"CALL obtener_id_instalacion({user_id}, @o_id_instalacion);")
            cursor.execute("SELECT @o_id_instalacion;")
            id_instalacion = cursor.fetchone()[0]
            return id_instalacion if id_instalacion is not None else 0
    except Exception as e:
        return 0

@login_required
def home_coord_bodega(request):
    return render(request, "home_coordinador_bodega.html")



@login_required
def gestion_Camiones(request): 
    user = request.user
    user_id = user.id 
    id_insta = obtener_id_instalacion(user_id)
    camiones = VerCamiones.objects.filter(id_instalacion=id_insta) 
    return render(request, 'gestion_Camiones_C.html', {'camiones': camiones, 'id_instalacion':id_insta})