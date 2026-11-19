"""Modelo de cliente con validación y encapsulación."""
import re
from entidad import Entidad
from excepciones import DatosInvalidosError

class Cliente(Entidad):
    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()
        if len(valor) < 2:
            raise DatosInvalidosError("El nombre debe contener al menos 2 caracteres.")
        self._nombre = valor

    @property
    def documento(self): return self._documento
    @documento.setter
    def documento(self, valor):
        valor = str(valor).strip()
        if not re.fullmatch(r"\d{5,15}", valor):
            raise DatosInvalidosError("El documento debe contener entre 5 y 15 dígitos.")
        self._documento = valor

    @property
    def correo(self): return self._correo
    @correo.setter
    def correo(self, valor):
        valor = str(valor).strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")
        self._correo = valor

    @property
    def telefono(self): return self._telefono
    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        if not re.fullmatch(r"\d{7,15}", valor):
            raise DatosInvalidosError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._telefono = valor

    def describir(self):
        return f"Cliente {self.nombre} | Documento: {self.documento}"

    def __str__(self):
        return self.describir()
