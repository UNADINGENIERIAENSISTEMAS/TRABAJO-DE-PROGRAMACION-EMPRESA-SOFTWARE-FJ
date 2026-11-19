"""Clase abstracta base para las entidades del sistema."""
from abc import ABC, abstractmethod

class Entidad(ABC):
    def __init__(self, identificador):
        identificador = str(identificador).strip()
        if not identificador:
            raise ValueError("El identificador no puede estar vacío.")
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible de la entidad."""
        raise NotImplementedError
