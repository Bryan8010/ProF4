import logging
from excepciones import ClienteNoEncontradoError, ValidacionError, SoftwareFJError
from entidades import Cliente
from reservas import Reserva


class GestorSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logger = logging.getLogger("SoftwareFJ")

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ValidacionError("Solo se pueden registrar objetos Cliente.")
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ValidacionError("Ya existe un cliente con ese identificador.")
        self.clientes.append(cliente)
        self.logger.info("Cliente registrado: %s", cliente.identificador)

    def buscar_cliente(self, identificador):
        for cliente in self.clientes:
            if cliente.identificador == identificador:
                return cliente
        raise ClienteNoEncontradoError(f"No existe el cliente {identificador}.")

    def registrar_servicio(self, servicio):
        if any(s.codigo == servicio.codigo for s in self.servicios):
            raise ValidacionError("Ya existe un servicio con ese código.")
        self.servicios.append(servicio)
        self.logger.info("Servicio registrado: %s", servicio.codigo)

    def buscar_servicio(self, codigo):
        for servicio in self.servicios:
            if servicio.codigo == codigo:
                return servicio
        raise SoftwareFJError(f"No existe el servicio {codigo}.")

    def crear_reserva(self, codigo, id_cliente, codigo_servicio, duracion, **parametros):
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(codigo_servicio)
        if any(r.codigo == codigo for r in self.reservas):
            raise ValidacionError("El código de reserva ya está registrado.")
        reserva = Reserva(codigo, cliente, servicio, duracion, **parametros)
        self.reservas.append(reserva)
        self.logger.info("Reserva creada: %s", codigo)
        return reserva

    def listar_reservas(self):
        return [str(reserva) for reserva in self.reservas]
