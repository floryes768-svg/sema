from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trabajo, EntregaTrabajo
from clases.models import Clase

@login_required
def index(request):
    if request.user.rol == 'maestro':
        clases = Clase.objects.filter(maestro=request.user)
        trabajos = Trabajo.objects.filter(clase__in=clases)
    else:
        clases = request.user.clases_unidas.all()
        trabajos = Trabajo.objects.filter(clase__in=clases)
    return render(request, 'trabajos/index.html', {'trabajos': trabajos})

@login_required
def crear_trabajo(request):
    if request.user.rol != 'maestro':
        return redirect('trabajos:index')
    clases = Clase.objects.filter(maestro=request.user)
    if request.method == 'POST':
        clase_id = request.POST['clase']
        titulo = request.POST['titulo']
        descripcion = request.POST.get('descripcion', '')
        fecha_entrega = request.POST.get('fecha_entrega', '')
        clase = get_object_or_404(Clase, id=clase_id)
        imagen = request.FILES.get('imagen')
        Trabajo.objects.create(
            clase=clase,
            titulo=titulo,
            descripcion=descripcion,
            fecha_entrega=fecha_entrega,
            imagen=imagen
        )
        return redirect('trabajos:index')
    return render(request, 'trabajos/crear.html', {'clases': clases})

@login_required
def detalle_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    entregas = EntregaTrabajo.objects.filter(trabajo=trabajo)
    ya_entrego = None
    if request.user.rol == 'alumno':
        ya_entrego = entregas.filter(alumno=request.user).first()
    if request.method == 'POST' and request.user.rol == 'alumno':
        if not ya_entrego:
            comentario = request.POST.get('comentario', '')
            EntregaTrabajo.objects.create(
                trabajo=trabajo,
                alumno=request.user,
                comentario=comentario
            )
        return redirect('trabajos:detalle', trabajo_id=trabajo_id)
    return render(request, 'trabajos/detalles.html', {
        'trabajo': trabajo,
        'entregas': entregas,
        'ya_entrego': ya_entrego
    })

@login_required
def calificar_entrega(request, entrega_id):
    if request.user.rol != 'maestro':
        return redirect('trabajos:index')
    entrega = get_object_or_404(EntregaTrabajo, id=entrega_id)
    if request.method == 'POST':
        calificacion = request.POST['calificacion']
        entrega.calificacion = calificacion
        entrega.save()
        return redirect('trabajos:detalle', trabajo_id=entrega.trabajo.id)
    return render(request, 'trabajos/calificar.html', {'entrega': entrega})