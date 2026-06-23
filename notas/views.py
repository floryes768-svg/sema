from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Nota
from clases.models import Clase
from usuarios.models import Usuario

@login_required
def index(request):
    if request.user.rol == 'maestro':
        clases = Clase.objects.filter(maestro=request.user)
    else:
        clases = request.user.clases_unidas.all()
        notas = Nota.objects.filter(alumno=request.user)
        return render(request, 'notas/index.html', {'notas': notas, 'clases': clases})
    return render(request, 'notas/index.html', {'clases': clases})

@login_required
def agregar_nota(request, clase_id):
    if request.user.rol != 'maestro':
        return redirect('notas:index')
    clase = get_object_or_404(Clase, id=clase_id, maestro=request.user)
    alumnos = clase.alumnos.all()
    if request.method == 'POST':
        alumno_id = request.POST['alumno']
        titulo = request.POST['titulo']
        descripcion = request.POST.get('descripcion', '')
        calificacion = request.POST['calificacion']
        alumno = get_object_or_404(Usuario, id=alumno_id)
        Nota.objects.create(
            alumno=alumno,
            clase=clase,
            titulo=titulo,
            descripcion=descripcion,
            calificacion=calificacion
        )
        return redirect('notas:index')
    return render(request, 'notas/agregar.html', {'clase': clase, 'alumnos': alumnos})

@login_required
def editar_nota(request, nota_id):
    if request.user.rol != 'maestro':
        return redirect('notas:index')
    nota = get_object_or_404(Nota, id=nota_id)
    if request.method == 'POST':
        nota.titulo = request.POST['titulo']
        nota.descripcion = request.POST.get('descripcion', '')
        calificacion = float(request.POST['calificacion'])
        if 1 <= calificacion <= 10:
            nota.calificacion = calificacion
        nota.save()
        return redirect('notas:index')
    return render(request, 'notas/editar.html', {'nota': nota})