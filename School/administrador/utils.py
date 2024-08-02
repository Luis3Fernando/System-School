import datetime
from .apis_net_pe import ApisNetPe

APIS_TOKEN = "apis-token-9457.9-gQunoDFhZouZFc9StW9mDcmU42VPg5"

def fecha_actual():
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    fecha_actual = datetime.date.today()
    dia = fecha_actual.day
    mes = meses[fecha_actual.month - 1]
    anio = fecha_actual.year
    return f"{dia} de {mes} del {anio}"

def GetPerson(dni):
    api_consultas = ApisNetPe(APIS_TOKEN)
    return api_consultas.get_person(dni)