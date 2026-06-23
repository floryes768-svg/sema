from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Clase, Materia

@login_required
def index(request):
    if request.user.rol == 'maestro':
        todas = Materia.objects.filter(maestro=request.user)
        nombres_vistos = []
        materias = []
        for m in todas:
            if m.nombre.lower() not in nombres_vistos:
                nombres_vistos.append(m.nombre.lower())
                materias.append(m)
        return render(request, 'clases/index.html', {'materias': materias})
    else:
        clases = request.user.clases_unidas.all()
        return render(request, 'clases/index.html', {'clases': clases})

@login_required
def crear_clase(request):
    if request.user.rol != 'maestro':
        return redirect('clases:index')
    if request.method == 'POST':
        nombre = request.POST['nombre']
        especialidad = request.POST['especialidad']
        descripcion = request.POST.get('descripcion', '')
        semestre = request.POST.get('semestre', '1-2')

        
        materia, _ = Materia.objects.get_or_create(
            nombre=nombre,
            especialidad=especialidad,
            maestro=request.user
        )

        
        Clase.objects.create(
            nombre=nombre,
            especialidad=especialidad,
            descripcion=descripcion,
            semestre=semestre,
            maestro=request.user,
            materia=materia
        )
        return redirect('clases:index')

    semestres = Clase.SEMESTRE_CHOICES
    return render(request, 'clases/crear.html', {'semestres': semestres})

@login_required
def unirse_clase(request):
    if request.user.rol != 'alumno':
        return redirect('clases:index')
    error = None
    if request.method == 'POST':
        codigo = request.POST['codigo'].upper()
        try:
            clase = Clase.objects.get(codigo=codigo)
            clase.alumnos.add(request.user)
            return redirect('clases:index')
        except Clase.DoesNotExist:
            error = 'Código incorrecto, intenta de nuevo'
    return render(request, 'clases/unirse.html', {'error': error})

@login_required
def detalle_clase(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    alumnos = clase.alumnos.all()
    return render(request, 'clases/detalle.html', {'clase': clase, 'alumnos': alumnos})

@login_required
def detalle_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id, maestro=request.user)
    grupos = materia.grupos.all()
    return render(request, 'clases/detalle_materia.html', {'materia': materia, 'grupos': grupos})

@login_required
def editar_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id, maestro=request.user)
    if request.method == 'POST':
        materia.nombre = request.POST['nombre']
        materia.especialidad = request.POST['especialidad']
        materia.save()
        # Actualizar también los grupos relacionados
        materia.grupos.update(nombre=materia.nombre, especialidad=materia.especialidad)
        return redirect('clases:index')
    return render(request, 'clases/editar_materia.html', {'materia': materia})

@login_required
def eliminar_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id, maestro=request.user)
    if request.method == 'POST':
        materia.delete()
        return redirect('clases:index')
    return render(request, 'clases/confirmar_eliminar.html', {
        'objeto': materia.nombre,
        'cancel_url': 'clases:index'
    })

@login_required
def editar_grupo(request, clase_id):
    grupo = get_object_or_404(Clase, id=clase_id, maestro=request.user)
    if request.method == 'POST':
        grupo.semestre = request.POST['semestre']
        grupo.descripcion = request.POST.get('descripcion', '')
        grupo.save()
        return redirect('clases:index')
    semestres = Clase.SEMESTRE_CHOICES
    return render(request, 'clases/editar_grupo.html', {'grupo': grupo, 'semestres': semestres})

@login_required
def eliminar_grupo(request, clase_id):
    grupo = get_object_or_404(Clase, id=clase_id, maestro=request.user)
    materia = grupo.materia
    if request.method == 'POST':
        grupo.delete()
        if materia and materia.grupos.count() == 0:
            materia.delete()
        return redirect('clases:index')
    return render(request, 'clases/confirmar_eliminar.html', {
        'objeto': f"{grupo.nombre} — {grupo.get_semestre_display()}",
        'cancel_url': 'clases:index'
    })
   
@login_required
def especialidades_materia(request, nombre):
    materias = Materia.objects.filter(
        maestro=request.user,
        nombre__iexact=nombre
    )
    return render(request, 'clases/especialidades.html', {
        'nombre': nombre,
        'materias': materias
    })