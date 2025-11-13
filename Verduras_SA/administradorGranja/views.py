from django.contrib.auth.decorators import login_required
from .models import VerEmpleados, VerEmpleadosDetallados
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from django.contrib.auth.hashers import make_password


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

def verificar_coordinador(id_insta):
    sin_coordinador = 0
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET @resultado = 0;")
            cursor.execute(f"CALL verificar_coord_instalacion({id_insta}, @resultado);")
            cursor.execute("SELECT @resultado;")
            sin_coordinador = cursor.fetchone()[0]
            return sin_coordinador
    except Exception as e:
        return 0

@login_required
def home_admin_granja(request):
    return render(request, "home_admin_granja.html")


#Gestion de Empleados
@login_required
def gestion_empleados(request):
    user = request.user
    user_id = user.id 
    id_insta = obtener_id_instalacion(user_id)
    empleados = VerEmpleados.objects.filter(id_instalacion=id_insta)
    return render(request, "gestion_Empleados_G.html", {'empleados':empleados})

@login_required
def crear_Empleado(request):
    user = request.user
    user_id = user.id 
    id_insta = obtener_id_instalacion(user_id)
    sin_coordinador = verificar_coordinador(id_insta)
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        nombre_usuario = request.POST.get("email")
        email = request.POST.get("email")
        password = make_password(request.POST.get("password"))
        cargo = request.POST.get("cargo")
        try:
            with connection.cursor() as cursor:
                cursor.callproc('agregar_empleado_granja', [nombre.title(), apellido.title(), nombre_usuario, email, password,cargo ,id_insta])
            messages.success(request, f"✅ Empleado '{nombre} {apellido}' fue registrado correctamente.")
        except Exception as e:
            messages.error(request, f"⚠️ Error al registrar: {e}")
        return redirect('Gestion-Empleados-G')
    
    print(sin_coordinador)
    return render(request, 'crear_empleados_G.html', {'sin_coordinador': sin_coordinador})

@login_required
def eliminar_Empleado(request, id_admin):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.callproc('eliminar_usuario', [id_admin])
                messages.success(request, "Empleado eliminado correctamente.")
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("Gestion-Empleados-G")
    return redirect('Gestion-Empleados-G') 

@login_required
def actualizar_Empleado(request, id):
    user = request.user
    user_id = user.id 
    id_insta = obtener_id_instalacion(user_id)
    empleado = get_object_or_404(VerEmpleadosDetallados, id=id)
    sin_coordinador = verificar_coordinador(empleado.id_instalacion)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('email')
        correo = request.POST.get('email')
        tipo_empleado = request.POST.get('cargo')
        nueva_pass = request.POST.get('password')
        if nueva_pass:
            password = make_password(nueva_pass)
        else :
            password = None
        try:
            with connection.cursor() as cursor:
                # Crear la bodega con el procedimiento almacenado
                cursor.callproc('actualizar_empleado_granja', [id, nombre, apellido, username, correo, tipo_empleado, password, id_insta])
            messages.success(request, "✅ Información del empleado actualizada correctamente.")
        except Exception as e:
            messages.error(request, f"⚠️ Error al actualizar: {e}")
        
        return redirect('Actualizar-Empleado-G', id)
        
    return render(request, 'editar_Empleado_G.html', {'empleado': empleado, 'sin_coordinador':sin_coordinador})