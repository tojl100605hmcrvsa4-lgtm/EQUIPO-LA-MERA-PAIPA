from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Alumno, Reporte


def lista_alumnos(request):
    query = request.GET.get('q')
    if query:
        alumnos = Alumno.objects.filter(
            matricula__icontains=query
        ) | Alumno.objects.filter(
            nombre_completo__icontains=query
        )
    else:
        alumnos = Alumno.objects.all().order_by('grupo', 'nombre_completo')
        
    return render(request, 'reportes/lista_alumnos.html', {
        'alumnos': alumnos,
        'query': query
    })


def detalle_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    reportes = alumno.reportes.all().order_by('-fecha')
    
    return render(request, 'reportes/detalle_alumno.html', {
        'alumno': alumno,
        'reportes': reportes
    })


def crear_alumno(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        nombre_completo = request.POST.get('nombre_completo')
        grupo = request.POST.get('grupo')
        semestre = request.POST.get('semestre')

        if Alumno.objects.filter(matricula=matricula).exists():
            messages.error(request, 'Ya existe un alumno con esa matrícula.')
        else:
            Alumno.objects.create(
                matricula=matricula,
                nombre_completo=nombre_completo,
                grupo=grupo,
                semestre=semestre
            )
            messages.success(request, 'Alumno registrado correctamente.')
            return redirect('lista_alumnos')

    return render(request, 'reportes/crear_alumno.html')


def lista_reportes(request):
    tipo_filtro = request.GET.get('tipo')
    if tipo_filtro:
        reportes = Reporte.objects.filter(tipo=tipo_filtro).order_by('-fecha')
    else:
        reportes = Reporte.objects.all().order_by('-fecha')

    return render(request, 'reportes/lista_reportes.html', {
        'reportes': reportes,
        'tipos_reporte': Reporte.TIPOS_REPORTE,
        'tipo_seleccionado': tipo_filtro
    })


def crear_reporte(request, alumno_id=None):
    alumnos = Alumno.objects.all().order_by('nombre_completo')
    alumno_seleccionado = get_object_or_404(Alumno, id=alumno_id) if alumno_id else None

    if request.method == 'POST':
        id_alumno = request.POST.get('alumno')
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')
        registrado_por = request.POST.get('registrado_por')

        alumno_obj = get_object_or_404(Alumno, id=id_alumno)

        Reporte.objects.create(
            alumno=alumno_obj,
            tipo=tipo,
            descripcion=descripcion,
            registrado_por=registrado_por
        )
        messages.success(request, 'Reporte generado exitosamente.')
        return redirect('detalle_alumno', alumno_id=alumno_obj.id)

    return render(request, 'reportes/crear_reporte.html', {
        'alumnos': alumnos,
        'alumno_seleccionado': alumno_seleccionado,
        'tipos_reporte': Reporte.TIPOS_REPORTE
    })


def eliminar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    alumno_id = reporte.alumno.id
    if request.method == 'POST':
        reporte.delete()
        messages.success(request, 'Reporte eliminado.')
    return redirect('detalle_alumno', alumno_id=alumno_id)

def detalle_alumno(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)

    return render(request, 'reportes/detalle_alumno.html', {
        'alumno': alumno
    })
