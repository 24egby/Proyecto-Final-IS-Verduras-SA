from django.contrib.auth.decorators import login_required
from Verduras_SA.decorators import group_required
from .models import  VerCamiones, VerBodegas, VerRegistroSalidaGranja
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
@group_required("CoorBodega")
def home_coord_bodega(request):
    return render(request, "home_coordinador_bodega.html")

#Gestion Camiones
@login_required
@group_required("CoorBodega")
def gestion_Camiones(request): 
    user = request.user
    user_id = user.id 
    id_insta = obtener_id_instalacion(user_id)
    camiones = VerCamiones.objects.filter(id_instalacion=id_insta) 
    return render(request, 'gestion_Camiones_C.html', {'camiones': camiones, 'id_instalacion':id_insta})

@login_required
@group_required("CoorBodega")
def actualizar_Estado_Camion(request):
    if request.method == "POST":
        id_camion = request.POST.get("id")
        estado = request.POST.get("estado")
        cursor = connection.cursor()
        cursor.callproc("cambiar_estado_camion", [id_camion, estado])
        connection.commit()
        return JsonResponse({"ok": True})
    
#Generar salida de camiones
@login_required
@group_required("CoorBodega")
def gestion_Salida_Camiones(request):
    user = request.user
    user_id = user.id 
    id_insta = obtener_id_instalacion(user_id)
    camiones = VerCamiones.objects.filter(id_instalacion=id_insta, estado="En garaje") 
    return render(request, 'gestion_Salida_Camiones.html', {'camiones': camiones, 'id_instalacion':id_insta})

@login_required
@group_required("CoorBodega")
def generar_Salida_Granja(request, id):
    user = request.user
    user_id = user.id 
    id_insta = obtener_id_instalacion(user_id)
    try:
        with connection.cursor() as cursor:
            cursor.callproc('crear_registro_salida_granja', [id,id_insta])
            messages.success(request, "✅ Salida generada exitosamente.")
    except Exception as e:
        messages.error(request,f"Error:{e}")
    return redirect("Salida-Camiones")

@login_required
@group_required("CoorBodega")
def generar_Salida_Venta(request):
    return 0

@login_required
@group_required("CoorBodega")
def gestion_Ingreso_Camiones(request):
    user = request.user
    user_id = user.id 
    id_insta = obtener_id_instalacion(user_id)
    nombre_bodega = VerBodegas.objects.filter(id=id_insta).values_list('nombre', flat=True).first()
    registros = VerRegistroSalidaGranja.objects.filter(bodega=nombre_bodega).exclude(estado="Finalizado")
    return render(request, 'gestion_recepciones_camiones.html', {"registros":registros})