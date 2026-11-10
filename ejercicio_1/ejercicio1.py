
def limpiar_registro_sensor(registro_raw: dict[str, str]):

    """
    Esta función normaliza los datos raw de un sensor individualmente.

    Limpia los espacios en blanco del identificador, convierte la temperatura 
    a un valor numérico de tipo float (eliminando 'C' o '°C'), 
    y asigna 'sin ubicacion' si el campo no existe o está vacío.

    Args:
        registro_raw (dict): Diccionario con los datos del sensor sin procesar.

    Returns:
        dict: Diccionario limpio con el formato correcto.
    """

    #aqui se limpia el identificador
    sensor_id = registro_raw["sensor_id"].strip()
    temperatura = float (registro_raw["temperatura"]. replace("°C", "").replace("C", "").strip())

    ubicacion = registro_raw.get("ubicacion", "").strip() #el strip quita los espacios en blanco.

    if ubicacion == "":
        ubicacion = "sin ubicacion"
    #print(ubicacion)

    registro_limpio = {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }

    return registro_limpio

    
def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):

    """
    Analiza una lista de sensores normalizados para calcular el promedio.

    Compara la temperatura de cada sensor contra un umbral límite, guardan los 
    ID de los que superan ese umbral, y calcula el promedio térmico global de la planta.

    Args:
        lista_sensores_limpios (list): Lista de diccionarios con datos de sensores ya limpios.
        umbral_temperatura (float): Temperatura máxima permitida antes de generar una alerta.

    Returns:
        tuple: (lista_sensores_alerta, promedio_temperaturas) donde la lista contiene los ID
               en alerta y el promedio es un float con todas las temperaturas.
    """


    #utilizo el acumulador para calcular el promedio
    lista_sensores_alerta = []
    suma_temperaturas = 0

    for sensor in lista_sensores_limpios:
        temperatura = sensor["temperatura"]
        sensor_id = sensor["sensor_id"]

        if temperatura > umbral_temperatura:
            lista_sensores_alerta.append(sensor_id)

        suma_temperaturas += temperatura

    if len (lista_sensores_limpios) > 0: #aca mejorar que solo ignore los sensores nulos o vacios
        promedio_temperaturas = suma_temperaturas / len (lista_sensores_limpios) #len es para saber cuantos elementos hay en la lista
    else:
        promedio_temperaturas = 0


    return lista_sensores_alerta, promedio_temperaturas

#bloque principal

sensores_raw = [
{
    "sensor_id": " SENSOR-001 ",
     "temperatura": "25.3 °C", 
     "ubicacion": "Planta Norte"
},

{
    "sensor_id": " SENSOR-002 ",
     "temperatura": "29.5 °C", 
     
},

{
    "sensor_id": " SENSOR-003 ",
     "temperatura": "21.5 °C", 
     "ubicacion": "Planta Norte"
},

{
    "sensor_id": " SENSOR-004 ",
     "temperatura": "42.5 °C", 
     "ubicacion": "oficinas"
},

{
    "sensor_id": " SENSOR-005 ",
     "temperatura": "24.3 °C", 
     "ubicacion": "Laboratorio"
},

{
    "sensor_id": " SENSOR-006 ",
     "temperatura": "38.5 °C",    
},

]



#limpiar los registros

sensores_limpios = []

for registro in sensores_raw:
    sensor_limpio = limpiar_registro_sensor(registro)
    sensores_limpios.append(sensor_limpio)
    #append agrega un elemento al final de la lista

umbral = 35.0

sensores_alerta, promedio_global = generar_resumen_sensores(sensores_limpios, umbral)

#despues agregar el desglose y el reporte de sensores.

# --- IMPRESIÓN DEL REPORTE FINAL ---
print("\n" + "="*35) 
print("   REPORTE FINAL DE SENSORES")
print("="*35)

# se muestran todos los registros de sensores limpios
print("DETALLE DE REGISTROS LIMPIOS:")
for sensor in sensores_limpios:
    print(f"  - ID: {sensor['sensor_id']} | Temp: {sensor['temperatura']} °C | Ubicación: {sensor['ubicacion']}")

#Total de sensores limpios procesados
print(f"\nTotal de sensores analizados: {len(sensores_limpios)}")

#promedio global
print(f"Promedio térmico global: {promedio_global:.2f} °C")

# sensores que superaron el umbral de temperatura
print(f"\n SENSORES EN ALERTA (Mayor a {umbral} °C):")
if len(sensores_alerta) > 0:
    for sensor_id in sensores_alerta:
        print(f"  -> {sensor_id}")
else:
    print("  -> Ningún sensor superó el umbral de alerta.")

print("="*50 + "\n")