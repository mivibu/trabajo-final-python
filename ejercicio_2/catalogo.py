
import json

#Punto A: StockInvalidoError, Clases: (P)DispositivoEcológico y (H)PanelSolar.

class StockInvalidoError(Exception):
    """Excepción para stock inválido en el catálogo."""


class DispositivoEcologico:
    """
    Clase base para los productos ecológicos del catálogo.

    El stock es un atributo encapsulado solo se puede acceder mediante la
    propiedad ``stock``, que evita valores negativos.

    Attributos:
        codigo: Código único del producto.
        nombre: Nombre comercial.
        precio: Precio unitario.
    """

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        """
        Crea un dispositivo.

        Raises:
            StockInvalidoError: Si el stock es negativo.
        """
        self.codigo: str = codigo
        self.nombre: str = nombre
        self.precio: float = precio
        self.__stock: int = 0
        self.stock = (stock)  # pasa por el setter, así se valida desde el inicio

    @property
    def stock(self) -> int:
        """Devuelve el stock actual."""
        return self.__stock

    @stock.setter
    def stock(self, valor: int):
        """
        Asigna un nuevo stock.

        Raises:
            StockInvalidoError: Si el valor es negativo.
        """
        if valor < 0:
            raise StockInvalidoError(
                f"Stock inválido para '{self.nombre}': {valor} (no puede ser negativo)"
            )
        self.__stock = valor

    def ficha_tecnica(self) -> str:
        """Devuelve la ficha técnica comercial del producto."""
        return (
            f"[{self.codigo}] {self.nombre}\n"
            f"    Precio: ${self.precio:.2f} | Stock: {self.stock} unidades"
        )

    def to_dict(self) -> dict:
        """Devuelve los datos del producto en un diccionario (para el JSON)."""
        return {
            "tipo": self.__class__.__name__,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }

class PanelSolar(DispositivoEcologico):
    """
    Panel solar: dispositivo ecológico con potencia y eficiencia.

    Attributes:
        potencia_watts: Potencia nominal en watts.
        eficiencia: Eficiencia de conversión, en porcentaje.
    """

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int,
                 potencia_watts: int, eficiencia: float) -> None:
        """Crea un panel solar (valida el stock igual que la clase base)."""
        super().__init__(codigo, nombre, precio, stock)
        self.potencia_watts: int = potencia_watts
        self.eficiencia: float = eficiencia

    def ficha_tecnica(self) -> str:
        """Polimorfismo: amplía la ficha base con los datos del panel."""
        return (
            super().ficha_tecnica()
            + f"\n    Potencia: {self.potencia_watts} W | Eficiencia: {self.eficiencia}%"
        )

    def to_dict(self) -> dict:
        """Amplía el diccionario base con los atributos del panel."""
        datos = super().to_dict()
        datos["potencia_watts"] = self.potencia_watts
        datos["eficiencia"] = self.eficiencia
        return datos

#Punto B: GestorInventario (persistencia del catálogo en JSON).
class GestorInventario:
    """Gestiona la persistencia del catálogo de dispositivos."""

    def guardar_catalogo_json(self, lista_dispositivos: list[DispositivoEcologico],
                              ruta_archivo: str):
        """
        Guarda el catálogo en un archivo JSON.

        Args:
            lista_dispositivos: Dispositivos a guardar.
            ruta_archivo: Ruta del archivo, por ejemplo "catalogo_ecotech.json".
        """
        datos: list[dict] = [d.to_dict() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # 1. Instanciamos panel1 fuera del try para asegurar que siempre esté enlazado
    panel1 = PanelSolar("PS-001", "Panel Solar 300W", 45000.0, 10, 300, 18.5)
    print(panel1.ficha_tecnica())

    try:
        # 2. Probamos la excepción de stock inválido de forma aislada
        print("\nIntentando asignar stock negativo...")
        panel1.stock = -5
    except StockInvalidoError as e:
        print(f"Excepción capturada correctamente: {e}")

    # 3. Probamos el gestor de inventario y la persistencia en JSON
    gestor = GestorInventario()
    catalogo = [panel1]

    ruta_salida = "catalogo_ecotech.json"
    gestor.guardar_catalogo_json(catalogo, ruta_salida)
    print(f"\nCatálogo guardado exitosamente en '{ruta_salida}'.")