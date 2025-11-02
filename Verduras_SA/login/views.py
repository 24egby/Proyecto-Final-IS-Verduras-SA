from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            grupos_usuario = list(user.groups.values_list("name", flat=True))
            if not grupos_usuario:
                error = "No perteneces a ningún grupo válido."
                return redirect("Login")
            grupo = grupos_usuario[0]
            match grupo:
                case "Gerente":
                    return redirect("Gerente")
                case "AdminGranja":
                    return redirect("Admin-Granja")
                case "AdminBodega":
                    return redirect("Admin-Bodega")
                case "CoorGranja":
                    return redirect("Coord-Granja")
                case "CoorBodega":
                    return redirect("Coord-Bodega")
                case "EmpleBodega":
                    return redirect("Empleado-Bodega")
                case "EmpleGranja":
                    return redirect("Empleado-Granja")
                case _:
                    error = "No perteneces a un grupo válido."
                    return redirect("Login")
        else:
            error = "Usuario o contraseña incorrectos."
    return render(request, "index.html", {"error": error})

@login_required
def logout_g(request):
    logout(request)
    return redirect("Login")