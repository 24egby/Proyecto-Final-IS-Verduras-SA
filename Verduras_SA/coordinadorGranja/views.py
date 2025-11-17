from django.contrib.auth.decorators import login_required
from Verduras_SA.decorators import group_required
#from .models import  VerCamiones, VerBodegas, VerRegistroSalidaGranja
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
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
@group_required("CoorGranja")
def home_coord_bodega(request):
    return render(request, "home_coordinador_granja.html")
