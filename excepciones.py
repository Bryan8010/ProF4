class SoftwareFJError(Exception):
    """Excepción base del sistema."""


class ValidacionError(SoftwareFJError):
    pass


class ClienteNoEncontradoError(SoftwareFJError):
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    pass


class ReservaError(SoftwareFJError):
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    pass
