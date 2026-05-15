import datetime
import json
from collections import Counter
from django.shortcuts import render
from departamentos.models import Departamento
from practicas.models import PracticaOperativa, Colaborador

# ── Tabla oficial de valores de tiempo ────────────────────────────────────────
VALORES_TIEMPO = {
    10: 0.17, 15: 0.25, 20: 0.33,
    25: 0.42, 30: 0.50, 35: 0.58,
    40: 0.67, 45: 0.75, 50: 0.83,
    55: 0.92, 60: 1.00
}


def reporte_hh(request):
    # 1. Filtros por GET (Mes y Año)
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')

    hoy = datetime.datetime.now()
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
        # a) Prácticas del departamento en el mes/año
        practicas = PracticaOperativa.objects.filter(
            departamento=depto,
            fecha_inicio__year=anio,
            fecha_inicio__month=mes
        ).prefetch_related('asistenciapractica_set')

        # b) Contar cuántas prácticas hizo cada colaborador en el mes
        conteo_colaboradores = Counter()  # {colaborador_id: cantidad_practicas}
        nombres_colaboradores = {}        # {colaborador_id: nombre_completo}
        duraciones_por_practica = []      # lista de duraciones para calcular la más común

        for practica in practicas:
            duraciones_por_practica.append(practica.duracion_minutos)
            for asistencia in practica.asistenciapractica_set.all():
                col = asistencia.colaborador
                conteo_colaboradores[col.id] += 1
                nombres_colaboradores[col.id] = col.nombre_completo

        # c) Colaborador con MÁS prácticas en el departamento ese mes
        if conteo_colaboradores:
            col_ref_id, max_practicas = conteo_colaboradores.most_common(1)[0]
            col_ref_nombre = nombres_colaboradores[col_ref_id]
        else:
            max_practicas = 0
            col_ref_nombre = '—'

        # d) Duración más común entre las prácticas del departamento
        if duraciones_por_practica:
            duracion_ref = Counter(duraciones_por_practica).most_common(1)[0][0]
        else:
            duracion_ref = 0

        # e) Total de colaboradores del departamento (headcount real)
        total_colaboradores_depto = Colaborador.objects.filter(
            departamento=depto
        ).count()

        # f) Aplicar fórmula oficial HHC
        if duracion_ref in VALORES_TIEMPO and total_colaboradores_depto > 0 and max_practicas > 0:
            hhc = VALORES_TIEMPO[duracion_ref] * max_practicas / total_colaboradores_depto
        else:
            hhc = 0.0

        datos_reporte.append({
            'departamento': depto.nombre,
            'duracion_ref': duracion_ref,
            'max_practicas': max_practicas,
            'col_referencia': col_ref_nombre,
            'total_colaboradores': total_colaboradores_depto,
            'hhc': round(hhc, 2),
        })

    # 4. Ordenar por HHC descendente
    datos_reporte.sort(key=lambda x: x['hhc'], reverse=True)

    # Convertir a JSON de forma segura para Chart.js
    datos_reporte_json = json.dumps(datos_reporte)

    meses = [
        (1, 'Enero'),     (2, 'Febrero'),   (3, 'Marzo'),
        (4, 'Abril'),     (5, 'Mayo'),       (6, 'Junio'),
        (7, 'Julio'),     (8, 'Agosto'),     (9, 'Septiembre'),
        (10, 'Octubre'),  (11, 'Noviembre'), (12, 'Diciembre')
    ]

    context = {
        'datos_reporte': datos_reporte,
        'datos_reporte_json': datos_reporte_json,
        'mes_actual': mes,
        'anio_actual': anio,
        'meses': meses,
        'anios': range(2023, hoy.year + 3),
    }

    return render(request, 'reportes/reporte_hh.html', context)
