from django.contrib.auth.decorators import login_required
from Verduras_SA.decorators import group_required
from .models import VerBodegas, VerProductos
from django.shortcuts import render, redirect
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
@group_required("EmpleBodega")
def home_emple_bodega(request):
    if request.method == "POST":
        user = request.user
        user_id = user.id 
        id_insta = obtener_id_instalacion(user_id)
        producto = VerBodegas.objects.filter(id=id_insta).values_list('producto', flat=True).first()
        id_prod = VerProductos.objects.filter(nombre_producto=producto).values_list("id_producto", flat=True).first()
        estado = request.POST.get("estado")
        cantidad = request.POST.get("cantidad")
        try:
            with connection.cursor() as cursor:
                cursor.callproc('actualizar_inventario_agregando', [id_prod, cantidad, estado])
            messages.success( request, f"✅ Productos agregados al inventario." )
        except Exception as e:
            messages.error(request, f"⚠️ Error al registrar: {e}")
        return redirect('Empleado-Bodega')

    return render(request, "home_empleado.html")
