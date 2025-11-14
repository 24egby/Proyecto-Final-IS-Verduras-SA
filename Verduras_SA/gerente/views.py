from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import VerGranjas, VerBodegas, VerAdmins, VerCoords, VerProductos, VerCoordsInsta, Producto, VerAdminsInsta, VerAdminsDetalle, VerCamiones
from django.contrib import messages
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from Verduras_SA.decorators import group_required

@login_required
@group_required("Gerente")
def home_gerente(request):
    granjas = VerGranjas.objects.all()
    bodegas = VerBodegas.objects.all() 
    admins = VerAdmins.objects.all()
    coords = VerCoords.objects.all()
    productos = VerProductos.objects.all()

    context = {
        "granjas": granjas,
        "bodegas": bodegas,
        "admins": admins,
        "coords": coords,
        "productos": productos,
    }
    return render(request, "home_gerente.html", context)

#Gestion de Granjas
@login_required
@group_required("Gerente")
def gestion_Granjas(request):
    granjas = VerGranjas.objects.all()
    context = {
        "granjas": granjas,
    }
    return render(request, "gestion_Granjas.html", context)

@login_required
@group_required("Gerente")
def crear_Granja(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        dirrecion = request.POST.get('dirrecion')

        if not nombre or not dirrecion:
            messages.error(request, "⚠️ Por favor complete todos los campos.")
            return redirect('Crear-Granja')

        # Normalizar texto para comparar sin mayúsculas o espacios
        nombre_limpio = nombre.strip().lower()
        dirrecion_limpia = dirrecion.strip().lower()

        # Validación: existencia previa
        if VerGranjas.objects.filter(nombre__iexact=nombre_limpio).exists():
            messages.error(request, "❌ Ya existe una granja con ese nombre.")
            return redirect('Crear-Granja')
        elif VerGranjas.objects.filter(direccion__iexact=dirrecion_limpia).exists():
            messages.error(request, "❌ Ya existe una granja con esa dirrecion.")
            return redirect('Crear-Granja')

        # Crear registro si todo es válido
        try:
            with connection.cursor() as cursor:
                cursor.callproc('agregar_instalacion', [nombre, dirrecion, 1, 0])
            messages.success(request, f"✅ La granja '{nombre}' fue registrada correctamente.")
        except Exception as e:
            messages.error(request, f"⚠️ Error al registrar: {e}")

        return redirect('Crear-Granja')

    return render(request, 'crear_Granja.html')

@login_required
@group_required("Gerente")
def eliminar_Granja(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('eliminar_instalacion', [id])
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print("Error eliminando instalación:", e)
        return JsonResponse({'status': 'error'}, status=500)

@login_required
@group_required("Gerente")
def editar_granja(request, id):
    granja = get_object_or_404(VerGranjas, id=id)
    return render(request, 'editar_Granja.html', {'granja': granja})

@login_required
@group_required("Gerente")
def actualizar_granja(request, id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('dirrecion')
        estado = request.POST.get('estado')
        if not nombre or not direccion or not estado:
            messages.error(request, "⚠️ Por favor complete todos los campos.")
            return redirect('Editar-Granja', id=id)
        
        try:
            with connection.cursor() as cursor:
                cursor.callproc('actualizar_granja', [id, nombre, direccion, estado])
            messages.success(request, f"✅ La granja '{nombre}' fue actualizada correctamente.")
        except Exception as e:
            messages.error(request, f"⚠️ Error al actualizar: {e}")
        return redirect('Editar-Granja', id)

#Vista de Coordinadores
@login_required 
@group_required("Gerente")
def vista_coordinadores(request):
    coords = VerCoordsInsta.objects.all()
    return render(request, "vista_Coord.html", {
        "coords": coords,
    })
    
#Gestion de Productos
@login_required
@group_required("Gerente")
def gestion_Productos(request):
    productos = VerProductos.objects.all()
    context = {
        "productos": productos,
    }
    return render(request, "gestion_Productos.html", context)

@login_required
@group_required("Gerente")
def eliminar_producto(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('eliminar_producto', [id])
            messages.success(request, "✅ Producto eliminado exitosamente.")
    except Exception as e:
        messages.error("Error eliminando Producto:", e)
    return redirect("Gestion-Productos")

@login_required
@group_required("Gerente")
def agregar_producto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        try:
            with connection.cursor() as cursor:
                cursor.callproc('agregar_producto', [nombre])
                messages.success(request, "✅ Producto agregado exitosamente.")
        except Exception as e:
            messages.error("Error agregando Producto:", e)
        return redirect("Gestion-Productos")

#Gestion de Administradores
@login_required
@group_required("Gerente")
def gestion_Admins(request):
    admins = VerAdminsInsta.objects.all()
    context = {
        'admins': admins
    }
    return render(request, "gestion_Administradores.html", context)

@login_required
@group_required("Gerente")
def crear_Admins(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        nombre_usuario = request.POST.get("email")
        email = request.POST.get("email")
        password = make_password(request.POST.get("password"))
        tipo_instalacion = request.POST.get("tipo-instalacion")
        id_insta = request.POST.get("instalacion")
        try:
            with connection.cursor() as cursor:
                cursor.callproc('agregar_admin', [nombre.title(), apellido.title(), nombre_usuario, email, password, tipo_instalacion, id_insta])
            messages.success(
                request,
                f"✅ Administrador '{nombre} {apellido}' fue registrado correctamente."
            )
        except Exception as e:
            messages.error(request, f"⚠️ Error al registrar: {e}")
        return redirect('Agregar-Admin')
    return render(request, "crear_Admins.html")

@login_required
@group_required("Gerente")
def obtener_instalaciones(request):
    tipo = request.GET.get("tipo")
    data = []
    match tipo:
        case "Granja":
            pendientes = VerGranjas.objects.filter(administrador="Pendiente")
            data = [{"id": g.id, "instalacion": g.nombre} for g in pendientes]
        case "Bodega":
            pendientes = VerBodegas.objects.filter(administrador="Pendiente")
            data = [{"id": b.id, "instalacion": b.nombre} for b in pendientes]
    return JsonResponse(data, safe=False)

@login_required
@group_required("Gerente")
def eliminar_admin(request, id_admin):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.callproc('eliminar_usuario', [id_admin])
                messages.success(request, "Administrador eliminado correctamente.")
        except Exception as e:
            print("Error eliminando Administrador:", e)
            return redirect("Gestion-Admins")
    return redirect('Gestion-Admins') 

@login_required
@group_required("Gerente")
def actualizar_admin(request, id):
    admin = get_object_or_404(VerAdminsDetalle, id=id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('email')
        correo = request.POST.get('email')
        tipo_instalacion = request.POST.get('tipo-instalacion')
        id_instalacion = request.POST.get('instalacion')
        # Solo actualiza la contraseña si el campo no está vacío
        nueva_pass = request.POST.get('password')
        if nueva_pass:
            password = make_password(nueva_pass)
        else :
            password = None
        try:
            with connection.cursor() as cursor:
                # Crear la bodega con el procedimiento almacenado
                cursor.callproc('actualizar_admin', [id, nombre, apellido, username, correo, tipo_instalacion, id_instalacion, password])
            messages.success(request, "✅ Información del administrador actualizada correctamente.")
        except Exception as e:
            messages.error(request, f"⚠️ Error al actualizar: {e}")
        
        return redirect('Gestion-Admins')
    return render(request, 'editar_admin.html', {'admin': admin})

#Gestion Bodegas
@login_required
@group_required("Gerente")
def gestion_Bodegas(request):
    bodegas = VerBodegas.objects.all()
    context = {
        "bodegas": bodegas,
    }
    return render(request, "gestion_Bodegas.html", context)

@login_required
@group_required("Gerente")
def crear_Bodega(request):
    # Obtener vegetales sin instalación asignada
    vegetales_disponibles = Producto.objects.filter(id_instalacion__isnull=True)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('dirrecion')
        vegetal_id = request.POST.get('vegetal')
        if not nombre or not direccion or not vegetal_id:
            messages.error(request, "⚠️ Por favor complete todos los campos.")
            return redirect('Crear-Bodega')
        nombre_limpio = nombre.strip().lower()
        direccion_limpia = direccion.strip().lower()
        # Validación de duplicados
        if VerBodegas.objects.filter(nombre__iexact=nombre_limpio).exists():
            messages.error(request, "❌ Ya existe una bodega con ese nombre.")
            return redirect('Crear-Bodega')
        elif VerBodegas.objects.filter(direccion__iexact=direccion_limpia).exists():
            messages.error(request, "❌ Ya existe una bodega con esa dirección.")
            return redirect('Crear-Bodega')
        try:
            with connection.cursor() as cursor:
                # Crear la bodega con el procedimiento almacenado
                cursor.callproc('agregar_instalacion', [nombre, direccion, 2, vegetal_id])
            messages.success(
                request,
                f"✅ La Bodega '{nombre}' fue registrada correctamente."
            )
        except Exception as e:
            messages.error(request, f"⚠️ Error al registrar: {e}")
        return redirect('Crear-Bodega')
    return render(request, 'crear_Bodega.html', {
        'vegetales_disponibles': vegetales_disponibles
    })

@login_required
@group_required("Gerente")
def eliminar_Bodega(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('eliminar_instalacion', [id])
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print("Error eliminando instalación:", e)
        return JsonResponse({'status': 'error'}, status=500)

@login_required
@group_required("Gerente")
def editar_Bodega(request, id):
    bodega = get_object_or_404(VerBodegas, id=id)
    productos = Producto.objects.filter(id_instalacion__isnull=True)
    return render(request, 'editar_bodega.html', {
        'bodega': bodega,
        'productos': productos
    })

@login_required
@group_required("Gerente")
def actualizar_Bodega(request, id):
    if request.method == 'POST':
        nombre = request.POST.get("nombre")
        direccion = request.POST.get("direccion")
        producto = request.POST.get("producto")
        estado = request.POST.get("estado")
        
        if not nombre or not direccion or not estado or not producto:
            messages.error(request, "⚠️ Por favor complete todos los campos.")
            return redirect('Editar-Bodega', id=id)
        
        try:
            with connection.cursor() as cursor:
                cursor.callproc('actualizar_bodega', [id, nombre, direccion, estado, producto])
            messages.success(request, f"✅ La bodega '{nombre}' fue actualizada correctamente.")
        except Exception as e:
            messages.error(request, f"⚠️ Error al actualizar: {e}")
        return redirect('Editar-Bodega', id)
    
# Gestion Camiones
@login_required
@group_required("Gerente")
def gestion_Camiones(request, id): 
    camiones = VerCamiones.objects.filter(id_instalacion=id) 
    return render(request, 'gestion_Camiones.html', {'camiones': camiones, 'id_instalacion':id})

@login_required
@group_required("Gerente")
def agregar_camion(request):
    if request.method == 'POST':
        placa = request.POST.get('placa')
        id_instalacion = request.POST.get('id_instalacion')
        try:
            with connection.cursor() as cursor:
                cursor.callproc('agregar_camion', [placa, id_instalacion])
            messages.success(request, f"Camión {placa} agregado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al agregar camión: {e}")
        return redirect('Gestion-Camiones', id=id_instalacion)

@login_required
@group_required("Gerente")
def eliminar_Camion(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('eliminar_camion', [id])
            return JsonResponse({'message': 'Camión eliminado correctamente.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)