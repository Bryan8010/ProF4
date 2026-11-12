from abc import ABC, abstractmethod
from excepciones import ValidacionError, ServicioNoDisponibleError


class Servicio(ABC):
    def __init__(self, codigo, nombre, tarifa_base, disponible=True):
        if not codigo or not isinstance(codigo, str):
            raise ValidacionError("El código del servicio es obligatorio.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ValidacionError("La tarifa base debe ser un número positivo.")
        self._codigo = codigo.strip()
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise ValidacionError("La disponibilidad debe ser True o False.")
        self._disponible = estado

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    # Sobrecarga simulada en Python mediante parámetros opcionales.
    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0):
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ValidacionError("La cantidad o duración debe ser positiva.")
        if not 0 <= descuento <= 100:
            raise ValidacionError("El descuento debe estar entre 0 y 100.")
        if not 0 <= impuesto <= 100:
            raise ValidacionError("El impuesto debe estar entre 0 y 100.")
        subtotal = self._calcular_subtotal(float(cantidad))
        return round(subtotal * (1 - descuento / 100) * (1 + impuesto / 100), 2)

    @abstractmethod
    def _calcular_subtotal(self, cantidad):
        pass

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs):
        pass


class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValidacionError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def _calcular_subtotal(self, horas):
        return self._tarifa_base * horas

    def describir(self):
        return f"Sala: {self.nombre} | ${self._tarifa_base:.2f}/hora | Capacidad: {self.capacidad}"

    def validar_parametros(self, **kwargs):
        personas = kwargs.get("personas")
        if not isinstance(personas, int) or personas <= 0:
            raise ValidacionError("Debe indicar una cantidad válida de personas.")
        if personas > self.capacidad:
            raise ValidacionError("La cantidad de personas supera la capacidad de la sala.")


class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, tarifa_dia, unidades, disponible=True):
        super().__init__(codigo, nombre, tarifa_dia, disponible)
        if not isinstance(unidades, int) or unidades < 0:
            raise ValidacionError("Las unidades disponibles deben ser un entero no negativo.")
        self.unidades = unidades

    def _calcular_subtotal(self, dias):
        return self._tarifa_base * dias

    def describir(self):
        return f"Equipo: {self.nombre} | ${self._tarifa_base:.2f}/día | Unidades: {self.unidades}"

    def validar_parametros(self, **kwargs):
        cantidad = kwargs.get("cantidad")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValidacionError("La cantidad de equipos debe ser un entero positivo.")
        if cantidad > self.unidades:
            raise ServicioNoDisponibleError("No hay suficientes unidades del equipo.")
        self.unidades -= cantidad


class Asesoria(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValidacionError("Debe especificar la especialidad de la asesoría.")
        self.especialidad = especialidad.strip()

    def _calcular_subtotal(self, horas):
        return self._tarifa_base * horas

    def describir(self):
        return f"Asesoría: {self.nombre} | Especialidad: {self.especialidad} | ${self._tarifa_base:.2f}/hora"

    def validar_parametros(self, **kwargs):
        tema = kwargs.get("tema")
        if not isinstance(tema, str) or len(tema.strip()) < 3:
            raise ValidacionError("El tema de la asesoría debe tener al menos 3 caracteres.")
