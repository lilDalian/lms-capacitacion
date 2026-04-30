import os
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_capacitacion.settings")
django.setup()

from departamentos.models import Departamento

def cargar_departamentos():
    departamentos_lista = [
        "Call Center", "Ama de Llaves", "Concierge", 
        "Actividades", "Mantenimiento", "Botones", 
        "Recursos Humanos", "SPA", "Ropería", 
        "Ventas y Bodas", "Recepción", "Áreas Públicas", 
        "Boutique", "Jardinería", "Cocinas", "Calidad", 
        "Lavandería", "Stewards", "A Y B", 
        "Gerencia Operativa", "Grupos y Convenciones", 
        "Seguridad", "T.I.", "Contraloría", "Transportes"
    ]

    print("Iniciando carga de departamentos...")
    
    for depto_nombre in departamentos_lista:
        depto, created = Departamento.objects.get_or_create(nombre=depto_nombre)
        if created:
            print(f"[+] Creado: {depto_nombre}")
        else:
            print(f"[-] Ya existe: {depto_nombre}")

    print("¡Carga de departamentos completada!")

if __name__ == "__main__":
    cargar_departamentos()
