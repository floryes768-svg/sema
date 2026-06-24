from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from clases.models import Clase
from .models import Asistencia

@login_required
def pasar_lista(request, clase_id):
    if request.user.rol != 'maestro':
        return redirect('clases:index')
    
    clase = get_object_or_404(Clase, id=clase_id, maestro=request.user)
    alumnos = clase.alumnos.all()
    fecha = request.GET.get('fecha', timezone.now().date().isoformat())

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        for alumno in alumnos:
            estado = request.POST.get(f'estado_{alumno.id}', 'A')
            Asistencia.objects.update_or_create(
                clase=clase,
                alumno=alumno,
                fecha=fecha,
                defaults={'estado': estado}
            )
        return redirect('asistencia:historial', clase_id=clase_id)

    asistencias_hoy = {}
    for a in Asistencia.objects.filter(clase=clase, fecha=fecha):
        asistencias_hoy[a.alumno.id] = a.estado

    return render(request, 'asistencia/pasar_lista.html', {
        'clase': clase,
        'alumnos': alumnos,
        'fecha': fecha,
        'asistencias_hoy': asistencias_hoy,
    })

@login_required
def historial(request, clase_id):
    if request.user.rol != 'maestro':
        return redirect('clases:index')

    clase = get_object_or_404(Clase, id=clase_id, maestro=request.user)
    alumnos = clase.alumnos.all()
    fechas = Asistencia.objects.filter(clase=clase).values_list('fecha', flat=True).distinct().order_by('fecha')
    
    tabla = []
    for alumno in alumnos:
        fila = {'alumno': alumno, 'asistencias': []}
        total_presentes = 0
        for fecha in fechas:
            try:
                a = Asistencia.objects.get(clase=clase, alumno=alumno, fecha=fecha)
                fila['asistencias'].append(a.estado)
                if a.estado == 'P':
                    total_presentes += 1
            except Asistencia.DoesNotExist:
                fila['asistencias'].append('-')
        fila['total'] = total_presentes
        tabla.append(fila)

    return render(request, 'asistencia/historial.html', {
        'clase': clase,
        'fechas': fechas,
        'tabla': tabla,
    })