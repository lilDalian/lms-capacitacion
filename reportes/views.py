import datetime
from django.shortcuts import render
from departamentos.models import Departamento
from practicas.models import PracticaOperativa

def reporte_hh(request):
    # 1. Filtros por GET (Mes y Año)
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    
    hoy = datetime.datetime.now()
    # Valores por defecto: Mes y año actual
    if not mes:
        mes = hoy.month
    else:
        mes = int(mes)
        
    if not anio:
        anio = hoy.year
    else:
        anio = int(anio)

    # 2. Obtener todos los departamentos
    departamentos = Departamento.objects.all()
    
    datos_reporte = []
    
    for depto in departamentos:
        # Filtrar prácticas del departamento en el mes y año específico
        practicas = PracticaOperativa.objects.filter(
            departamento=depto,
            fecha_inicio__year=anio,
            fecha_inicio__month=mes
        )
        
        hc_total = 0  # Total de asistentes (Headcount)
        total_h = 0   # Total de minutos (asistentes * duración)
        
        for practica in practicas:
            # Para cada práctica, contamos cuántas asistencias están registradas
            asistentes = practica.asistenciapractica_set.count()
            
            # Acumulamos el HC y el tiempo (HH)
            hc_total += asistentes
            total_h += (asistentes * practica.duracion_minutos)
            
        # 3. Calculamos el HHC (Horas Hombre de Capacitación) diviendo entre 60
        hhc = total_h / 60.0
        
        # Guardamos en la lista solo si quieres mostrar todos. 
        # (Si quisieras omitir los de 0, podrías poner if hhc > 0:)
        datos_reporte.append({
            'departamento': depto.nombre,
            'total_h': total_h,
            'hc': hc_total,
            'hhc': round(hhc, 2)
        })
        
    # 4. Ordenar por HHC descendente
    datos_reporte.sort(key=lambda x: x['hhc'], reverse=True)
    
    # Listas para pintar los selects en el template
    meses = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]
    
    context = {
        'datos_reporte': datos_reporte,
        'mes_actual': mes,
        'anio_actual': anio,
        'meses': meses,
        'anios': range(2023, hoy.year + 3)
    }
    
    return render(request, 'reportes/reporte_hh.html', context)
