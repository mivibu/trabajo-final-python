def calcular_emisiones_carbono(consumos_khm, factor emisiones=0.4 )
*** 
calcula las emisiones de carbono a partir del consumo en khm.
Eleva ValueError si el consumo es negativo.
"""
if consumos_khm < 0:
    raise ValueError("El consumo no puede ser negativo")
return consumos_khm * emisiones

def obtener_metricas_consumo (registros):
    """
    Obtenemos las metricas de consumo de una lista de registros.
    """
    total_global_emisiones = 0.0 
    emisiones_totales = {}
