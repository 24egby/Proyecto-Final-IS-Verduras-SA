from django.contrib.auth.decorators import login_required
from Verduras_SA.decorators import group_required
from django.shortcuts import render, redirect
from .models import VerGranjas, VerRegistroSalidaGranja, VerProductos
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection
from .utils import process_image_and_read_plate
from PIL import Image
import numpy as np
import cv2

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

@login_required
@group_required("CoorGranja")
def escaneo_placa_ingreso(request):
    return render(request, 'escaneo_placa.html')

@login_required
@group_required("CoorGranja")
def detectar_placa(request):
    if request.method == 'POST':
        if 'photo' not in request.FILES:
            return JsonResponse({'ok': False, 'error': 'No se recibió la foto'}, status=400)
        photo = request.FILES['photo']
        try:
            img = Image.open(photo).convert('RGB')
            img_np = np.array(img)
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            plate_text = process_image_and_read_plate(img_cv)
            return JsonResponse({'ok': True, 'plate': plate_text})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=500)
        
@login_required
@group_required("CoorGranja")
def gestion_Ingreso_Camiones(request):
    user = request.user
    user_id = user.id 
    id_insta = obtener_id_instalacion(user_id)
    nombre_granja = VerGranjas.objects.filter(id=id_insta).values_list('nombre', flat=True).first()
    print(nombre_granja)
    registros = VerRegistroSalidaGranja.objects.filter(granja=nombre_granja, cantidad=0 , estado="Cargando").exclude(estado="Finalizado")
    return render(request, 'gestion_produccion_granja.html', {"registros":registros})

@login_required
@group_required("CoorGranja")
def actualizar_Ingreso_Camione(request, id):
    try:
        cantidad = request.POST.get("Cantidad")
        with connection.cursor() as cursor:
            cursor.callproc('actualizar_registro_salida_granja', [id, cantidad, 4, "Cargado"])
            messages.success(request, "✅ Cargamento actualizadao.")
    except Exception as e:
            messages.error(request,f"Error:{e}")
    return redirect('Gestion-Ingresos')