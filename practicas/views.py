from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json
from .models import PracticaOperativa, AsistenciaPractica, Colaborador
from instructores.models import Instructor
from departamentos.models import Departamento


def dashboard(request):
    total_practicas = PracticaOperativa.objects.count()
    programadas = PracticaOperativa.objects.filter(estatus='Programado').count()
    pendientes = PracticaOperativa.objects.filter(estatus='Pendiente').count()
    completadas = PracticaOperativa.objects.filter(estatus='Completado').count()

    context = {
        'total_practicas': total_practicas,
        'programadas': programadas,
        'pendientes': pendientes,
        'completadas': completadas,
    }
    return render(request, 'dashboard.html', context)


def lista_practicas(request):
    programadas = PracticaOperativa.objects.filter(
        estatus='Programado'
    ).select_related('instructor', 'departamento')

    pendientes = PracticaOperativa.objects.filter(
        estatus='Pendiente'
    ).select_related('instructor', 'departamento')

    completadas = PracticaOperativa.objects.filter(
        estatus='Completado'
    ).select_related('instructor', 'departamento')

    context = {
        'programadas': programadas,
        'pendientes': pendientes,
        'completadas': completadas,
    }
    return render(request, 'practicas/lista_practicas.html', context)


def _build_context():
    """Helper: construye el contexto común para GET y POST-error."""
    instructores = Instructor.objects.filter(activo=True).select_related('departamento')
    departamentos = Departamento.objects.all()

    # JSON para filtrado JS — instructores
    instructores_json = json.dumps(list(
        instructores.values('id', 'nombre_completo', 'departamento_id')
    ))

    # JSON para filtrado JS — colaboradores
    colaboradores_json = json.dumps(list(
        Colaborador.objects.values('id', 'nombre_completo', 'departamento_id')
    ))

    return {
        'instructores': instructores,
        'departamentos': departamentos,
        'instructores_json': instructores_json,
        'colaboradores_json': colaboradores_json,
    }


def nueva_cedula(request):
    if request.method == 'POST':
        try:
            instructor_id = request.POST.get('instructor')
            instructor = Instructor.objects.get(id=instructor_id)
            departamento = instructor.departamento
            duracion = request.POST.get('duracion_minutos')

            practica = PracticaOperativa.objects.create(
                departamento=departamento,
                instructor=instructor,
                nombre_curso=request.POST.get('nombre_curso'),
                lugar=request.POST.get('lugar'),
                fecha_inicio=request.POST.get('fecha_inicio'),
                fecha_fin=request.POST.get('fecha_fin'),
                hora_inicio=request.POST.get('hora_inicio'),
                hora_fin=request.POST.get('hora_fin'),
                duracion_minutos=duracion,
                estatus=request.POST.get('estatus'),
                fecha_expiracion=request.POST.get('fecha_expiracion')
            )

            # Leer IDs de colaboradores (no nombres)
            colaborador_ids = request.POST.getlist('colaboradores[]')

            for colab_id in colaborador_ids:
                if colab_id.strip():
                    colaborador = Colaborador.objects.get(id=int(colab_id))
                    AsistenciaPractica.objects.create(
                        practica=practica,
                        colaborador=colaborador
                    )

            messages.success(request, '✅ Práctica guardada exitosamente')
            return redirect('dashboard')

        except Exception as e:
            messages.error(request, f'❌ Error al guardar: {str(e)}')
            print(f"Error al guardar práctica: {e}")
            context = _build_context()
            context['error'] = str(e)
            return render(request, 'practicas/nueva_cedula.html', context)

    # GET
    context = _build_context()
    return render(request, 'practicas/nueva_cedula.html', context)


def detalle_practica(request, id):
    practica = get_object_or_404(PracticaOperativa, id=id)
    asistencias = AsistenciaPractica.objects.filter(
        practica=practica
    ).select_related('colaborador')
    hhc = (asistencias.count() * practica.duracion_minutos) / 60
    context = {
        'practica': practica,
        'asistencias': asistencias,
        'total_asistentes': asistencias.count(),
        'hhc': round(hhc, 2),
    }
    return render(request, 'practicas/detalle_practica.html', context)
