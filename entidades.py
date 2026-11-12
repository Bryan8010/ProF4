from abc import ABC, abstractmethod
from excepciones import ValidacionError


class Entidad(ABC):
    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValidacionError("El identificador es obligatorio.")
        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        """Devuelve una descripción de la entidad."""


class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.__nombre = self._validar_texto(nombre, "nombre")
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValidacionError(f"El {campo} debe contener al menos 2 caracteres.")
        return valor.strip()

    @staticmethod
    def _validar_correo(correo):
        if not isinstance(correo, str) or "@" not in correo or "." not in correo.split("@")[-1]:
            raise ValidacionError("El correo electrónico no tiene un formato válido.")
        return correo.strip().lower()

    @staticmethod
    def _validar_telefono(telefono):
        numero = str(telefono).strip()
        if not numero.isdigit() or not 7 <= len(numero) <= 15:
            raise ValidacionError("El teléfono debe contener entre 7 y 15 dígitos.")
        return numero

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        return f"Cliente {self.nombre} | ID: {self.identificador} | {self.correo}"
