from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Usuario

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        rol = request.POST['rol']
        nombre_completo = request.POST.get('nombre_completo', '')
        correo = request.POST.get('correo', '')
        if Usuario.objects.filter(username=username).exists():
            return render(request, 'usuarios/registro.html', {'error': 'El usuario ya existe'})
        usuario = Usuario.objects.create_user(
            username=username,
            password=password,
            rol=rol,
            nombre_completo=nombre_completo,
            correo=correo
        )
        login(request, usuario)
        return redirect('dashboard')
    return render(request, 'usuarios/registro.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario:
            login(request, usuario)
            return redirect('dashboard')
        return render(request, 'usuarios/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.rol == 'maestro':
        return redirect('maestro_home')
    return redirect('alumno_home')

def maestro_home(request):
    if not request.user.is_authenticated or request.user.rol != 'maestro':
        return redirect('login')
    return render(request, 'usuarios/maestro.html')

def alumno_home(request):
    if not request.user.is_authenticated or request.user.rol != 'alumno':
        return redirect('login')
    return render(request, 'usuarios/alumno.html')

def perfil(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        request.user.nombre_completo = request.POST.get('nombre_completo', '')
        request.user.correo = request.POST.get('correo', '')
        request.user.save()
        return redirect('perfil')
    return render(request, 'usuarios/perfil.html')