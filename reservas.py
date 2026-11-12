from datetime import datetime
from excepciones import ReservaError, OperacionNoPermitidaError, ValidacionError


class Reserva:
    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, codigo, cliente, servicio, duracion, **parametros):
        if not codigo or not isinstance(codigo, str):
            raise ValidacionError("El código de reserva es obligatorio.")
        if duracion <= 0:
            raise ValidacionError("La duración debe ser mayor que cero.")
        self.codigo = codigo
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)
        self.parametros = parametros
        self.estado = "PENDIENTE"
        self.fecha_creacion = datetime.now()

    def confirmar(self):
        if self.estado != "PENDIENTE":
            raise OperacionNoPermitidaError("Solo se puede confirmar una reserva pendiente.")
        self.servicio.validar_disponibilidad()
        self.servicio.validar_parametros(**self.parametros)
        self.estado = "CONFIRMADA"
        return f"Reserva {self.codigo} confirmada."

    def cancelar(self):
        if self.estado not in ("PENDIENTE", "CONFIRMADA"):
            raise OperacionNoPermitidaError("La reserva no se puede cancelar en su estado actual.")
        self.estado = "CANCELADA"
        return f"Reserva {self.codigo} cancelada."

    def procesar(self, descuento=0, impuesto=0):
        if self.estado != "CONFIRMADA":
            raise ReservaError("La reserva debe estar confirmada antes de procesarse.")
        try:
            total = self.servicio.calcular_costo(self.duracion, descuento, impuesto)
        except (TypeError, ValueError) as error:
            raise ReservaError("No fue posible calcular el costo de la reserva.") from error
        else:
            if total < 0:
                raise ReservaError("El cálculo produjo un total inconsistente.")
            self.estado = "PROCESADA"
            return total
        finally:
            # Punto de cierre para auditoría o liberación de recursos.
            pass

    def __str__(self):
        return (f"{self.codigo} | {self.cliente.nombre} | {self.servicio.nombre} | "
                f"{self.estado} | Duración: {self.duracion}")
