
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notas.models import Nota
from trabajos.models import EntregaTrabajo
from clases.models import Clase

@login_required
def index(request):
    if request.user.rol == 'maestro':
        clases = Clase.objects.filter(maestro=request.user)
        resumen = []
        for clase in clases:
            alumnos = clase.alumnos.all()
            for alumno in alumnos:
                notas = Nota.objects.filter(alumno=alumno, clase=clase)
                entregas = EntregaTrabajo.objects.filter(
                    alumno=alumno,
                    trabajo__clase=clase,
                    calificacion__isnull=False
                )
                promedio_notas = sum([float(n.calificacion) for n in notas]) / len(notas) if notas else None
                promedio_entregas = sum([float(e.calificacion) for e in entregas]) / len(entregas) if entregas else None
                resumen.append({
                    'alumno': alumno,
                    'clase': clase,
                    'notas': notas,
                    'entregas': entregas,
                    'promedio_notas': round(promedio_notas, 2) if promedio_notas else None,
                    'promedio_entregas': round(promedio_entregas, 2) if promedio_entregas else None,
                })
        return render(request, 'calificaciones/index.html', {'resumen': resumen})
    else:
     clases = request.user.clases_unidas.all()
     resumen_alumno = []
     for clase in clases:
        notas = Nota.objects.filter(alumno=request.user, clase=clase)
        entregas = EntregaTrabajo.objects.filter(
            alumno=request.user,
            trabajo__clase=clase,
            calificacion__isnull=False
        )
        promedio_notas = sum([float(n.calificacion) for n in notas]) / notas.count() if notas.count() > 0 else None
        promedio_entregas = sum([float(e.calificacion) for e in entregas]) / entregas.count() if entregas.count() > 0 else None
        resumen_alumno.append({
            'clase': clase,
            'notas': notas,
            'entregas': entregas,
            'promedio_notas': round(promedio_notas, 2) if promedio_notas else None,
            'promedio_entregas': round(promedio_entregas, 2) if promedio_entregas else None,
        })
    return render(request, 'calificaciones/index.html', {'resumen_alumno': resumen_alumno})
        
