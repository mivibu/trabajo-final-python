def calcular_emisiones_carbono ( consumos_kwh, factor_emision=0.4 ):

    """ 
calcula las emisiones de carbono a partir del consumo en kwh.
Eleva ValueError si el consumo es negativo.
    """
    if consumos_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")
    return consumos_kwh * factor_emision

def obtener_metricas_consumo (registros):
    """
    Obtenemos las metricas de consumo de una lista de registros para calcular emisiones totales
    """
    total_global_emisiones = 0.0 # esto es un acumulador
    emisiones_por_planta = {}
    planta_mayor_consumo = None
    mayor_emision = -1 
    
    for registro in registros: 
      planta = registro.get("planta", "Planta Desconocida")
      consumo = registro.get("consumo_kwh", 0.0)
      
      emisiones = calcular_emisiones_carbono(consumo)
      total_global_emisiones += emisiones

      if planta not in emisiones_por_planta:
            emisiones_por_planta[planta] = 0.0
            emisiones_por_planta[planta] += emisiones

    for planta, emisiones in emisiones_por_planta.items():
        
        if emisiones > mayor_emision:
            mayor_emision = emisiones
            planta_mayor_consumo = planta

    return {
        "total_global_emisiones": total_global_emisiones,
        "planta_mayor_consumo": planta_mayor_consumo,
        "emisiones_por_planta": emisiones_por_planta
    }

