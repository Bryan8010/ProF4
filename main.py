import logging
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from gestor import GestorSoftwareFJ


def configurar_logs():
    logging.basicConfig(
        filename="software_fj.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8"
    )
    logging.getLogger("SoftwareFJ").info("========== Inicio del sistema ==========")


def ejecutar_operacion(numero, descripcion, accion):
    """Aísla cada operación: un fallo no detiene las siguientes."""
    logger = logging.getLogger("SoftwareFJ")
    print(f"\nOPERACIÓN {numero}: {descripcion}")
    try:
        resultado = accion()
    except Exception as error:
        logger.exception("Error en operación %s: %s", numero, error)
        print(f"ERROR CONTROLADO: {error}")
    else:
        logger.info("Operación %s ejecutada correctamente.", numero)
        if resultado is not None:
            print(resultado)
    finally:
        print("Fin de la operación.")


def main():
    configurar_logs()
    sistema = GestorSoftwareFJ()

    # 1. Registro válido de cliente
    ejecutar_operacion(1, "Registrar cliente válido",
        lambda: sistema.registrar_cliente(Cliente("C001", "Laura Gómez", "laura@email.com", "3001234567")))

    # 2. Registro inválido: correo incorrecto
    ejecutar_operacion(2, "Registrar cliente con correo inválido",
        lambda: sistema.registrar_cliente(Cliente("C002", "Carlos Pérez", "correo-invalido", "3101234567")))

    # 3. Segundo cliente válido
    ejecutar_operacion(3, "Registrar segundo cliente válido",
        lambda: sistema.registrar_cliente(Cliente("C003", "Andrés Ruiz", "andres@email.com", "3111234567")))

    # 4. Crear servicios de los tres tipos
    def crear_servicios():
        sistema.registrar_servicio(ReservaSala("S001", "Sala de reuniones", 50000, 12))
        sistema.registrar_servicio(AlquilerEquipo("E001", "Proyector", 35000, 5))
        sistema.registrar_servicio(Asesoria("A001", "Asesoría tecnológica", 80000, "Software"))
        return "Tres servicios registrados correctamente."
    ejecutar_operacion(4, "Crear sala, equipo y asesoría", crear_servicios)

    # 5. Crear servicio inválido
    ejecutar_operacion(5, "Crear servicio con tarifa negativa",
        lambda: ReservaSala("S002", "Sala inválida", -1000, 10))

    # 6. Reserva de sala correcta
    def reserva_sala():
        r = sistema.crear_reserva("R001", "C001", "S001", 2, personas=8)
        r.confirmar()
        return f"{r} | Total: ${r.procesar(descuento=10, impuesto=19):,.2f}"
    ejecutar_operacion(6, "Crear, confirmar y procesar reserva de sala", reserva_sala)

    # 7. Reserva de equipo correcta
    def reserva_equipo():
        r = sistema.crear_reserva("R002", "C003", "E001", 3, cantidad=2)
        r.confirmar()
        return f"{r} | Total: ${r.procesar(impuesto=19):,.2f}"
    ejecutar_operacion(7, "Alquilar equipos", reserva_equipo)

    # 8. Reserva de sala que supera la capacidad
    def reserva_invalida():
        r = sistema.crear_reserva("R003", "C001", "S001", 1, personas=30)
        return r.confirmar()
    ejecutar_operacion(8, "Intentar reservar sala con exceso de personas", reserva_invalida)

    # 9. Reserva de asesoría
    def reserva_asesoria():
        r = sistema.crear_reserva("R004", "C003", "A001", 1.5, tema="Seguridad informática")
        r.confirmar()
        return f"{r} | Total: ${r.procesar(descuento=5, impuesto=19):,.2f}"
    ejecutar_operacion(9, "Reservar asesoría especializada", reserva_asesoria)

    # 10. Intentar procesar una reserva sin confirmarla
    def procesar_sin_confirmar():
        r = sistema.crear_reserva("R005", "C001", "A001", 1, tema="Redes")
        return r.procesar()
    ejecutar_operacion(10, "Procesar reserva pendiente", procesar_sin_confirmar)

    # 11. Buscar cliente inexistente
    ejecutar_operacion(11, "Buscar cliente inexistente",
        lambda: sistema.buscar_cliente("NO-EXISTE"))

    # 12. Cancelar una reserva pendiente
    def cancelar():
        r = sistema.crear_reserva("R006", "C001", "A001", 1, tema="Programación")
        return r.cancelar()
    ejecutar_operacion(12, "Cancelar reserva pendiente", cancelar)

    print("\n========== RESUMEN DE RESERVAS ==========")
    for elemento in sistema.listar_reservas():
        print(elemento)
    print("\nEl sistema terminó las operaciones sin detenerse.")
    print("Consulta software_fj.log para revisar los eventos y errores.")


if __name__ == "__main__":
    main()
