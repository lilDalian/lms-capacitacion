from django.shortcuts import render, redirect
from .models import Instructor
from departamentos.models import Departamento
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def permisos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_completo')
        correo = request.POST.get('correo')
        depto_id = request.POST.get('departamento')
        departamento = Departamento.objects.get(id=depto_id)
        Instructor.objects.create(
            nombre_completo=nombre,
            correo=correo,
            departamento=departamento
        )
        return redirect('permisos')
    
    instructores = Instructor.objects.select_related(
        'departamento').all()
    departamentos = Departamento.objects.all()
    
    stats = {
        'total': instructores.count(),
        'activos': instructores.filter(activo=True).count(),
        'programar': instructores.filter(
            puede_programar=True).count(),
        'editar': instructores.filter(
            puede_editar=True).count(),
    }
    
    context = {
        'instructores': instructores,
        'departamentos': departamentos,
        'stats': stats,
    }
    return render(request, 
        'instructores/permisos.html', context)

@require_POST
def toggle_permiso(request, id):
    try:
        data = json.loads(request.body)
        campo = data.get('campo')
        campos_permitidos = [
            'activo','puede_programar',
            'puede_editar','puede_eliminar'
        ]
        if campo not in campos_permitidos:
            return JsonResponse(
                {'status': 'error'}, status=400)
        
        instructor = Instructor.objects.get(id=id)
        valor_actual = getattr(instructor, campo)
        setattr(instructor, campo, not valor_actual)
        instructor.save()
        return JsonResponse({'status': 'success',
            'nuevo_valor': not valor_actual})
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'msg': str(e)}, 
            status=400)
