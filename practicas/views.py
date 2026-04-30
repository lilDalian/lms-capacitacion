from django.shortcuts import render, redirect
from django.contrib import messages
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
    ).select_related('instructor','departamento')
    
    pendientes = PracticaOperativa.objects.filter(
        estatus='Pendiente'
    ).select_related('instructor','departamento')
    
    completadas = PracticaOperativa.objects.filter(
        estatus='Completado'
    ).select_related('instructor','departamento')
    
    context = {
        'programadas': programadas,
        'pendientes': pendientes,
        'completadas': completadas,
    }
    return render(request, 
        'practicas/lista_practicas.html', context)

def nueva_cedula(request):
    if request.method == 'POST':
        try:
            # 1. Obtener el instructor seleccionado
            instructor_id = request.POST.get('instructor')
            instructor = Instructor.objects.get(id=instructor_id)
            
            # 2. Usar el departamento del instructor seleccionado
            departamento = instructor.departamento
            
            # 3. Leer la duración seleccionada
            duracion = request.POST.get('duracion_minutos')
            
            # 4. Crear la PracticaOperativa
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
            
            # 5. Leer colaboradores del POST
            nombres_colaboradores = request.POST.getlist('colaboradores[]')
            
            for nombre in nombres_colaboradores:
                if nombre.strip():
                    # 6. get_or_create de Colaborador (asignamos "S/N" si es nuevo)
                    colaborador, created = Colaborador.objects.get_or_create(
                        nombre_completo=nombre.strip(),
                        departamento=departamento,
                        defaults={'numero_colaborador': 'S/N'}
                    )
                    
                    # 7. Crear AsistenciaPractica para cada colaborador
                    AsistenciaPractica.objects.create(
                        practica=practica,
                        colaborador=colaborador
                    )
                    
            # 8. Redirigir al dashboard si todo sale bien
            messages.success(request, '✅ Cédula guardada exitosamente')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'❌ Error al guardar: {str(e)}')
            print(f"Error al guardar cédula: {e}")
            
            # En caso de error, necesitamos volver a mandar instructores para el dropdown
            instructores = Instructor.objects.filter(activo=True)
            departamentos = Departamento.objects.all()
            
            context = {
                'instructores': instructores,
                'departamentos': departamentos,
                'error': str(e)
            }
            return render(request, 'practicas/nueva_cedula.html', context)
        
    # GET: Traer instructores activos y departamentos
    instructores = Instructor.objects.filter(activo=True)
    departamentos = Departamento.objects.all()
    
    context = {
        'instructores': instructores,
        'departamentos': departamentos
    }
    
    return render(request, 'practicas/nueva_cedula.html', context)
