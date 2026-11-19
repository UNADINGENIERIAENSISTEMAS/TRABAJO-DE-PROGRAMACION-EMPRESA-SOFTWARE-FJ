"""Clase abstracta y servicios especializados de Software FJ."""
from abc import abstractmethod
from entidad import Entidad
from excepciones import DatosInvalidosError, CalculoCostoError

class Servicio(Entidad):
    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        nombre = str(nombre).strip()
        if not nombre:
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        try:
            tarifa_base = float(tarifa_base)
        except (TypeError, ValueError) as exc:
            raise DatosInvalidosError("La tarifa base debe ser numérica.") from exc
        if tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor que cero.")
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = bool(disponible)

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, **parametros):
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, **parametros):
        raise NotImplementedError

    def describir(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.nombre} ({self.identificador}) - {estado}"

    @staticmethod
    def _ajustar_costo(subtotal, impuesto=0.0, descuento=0.0):
        try:
            impuesto, descuento = float(impuesto), float(descuento)
        except (TypeError, ValueError) as exc:
            raise CalculoCostoError("Impuesto y descuento deben ser numéricos.") from exc
        if subtotal < 0 or not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise CalculoCostoError("Valores de cálculo fuera de los rangos permitidos.")
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if int(capacidad) <= 0:
            raise DatosInvalidosError("La capacidad debe ser mayor que cero.")
        self.capacidad = int(capacidad)

    def validar_parametros(self, **parametros):
        personas = int(parametros.get("personas", 1))
        if personas <= 0 or personas > self.capacidad:
            raise DatosInvalidosError(f"La cantidad de personas debe estar entre 1 y {self.capacidad}.")
        return True

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, **parametros):
        self.validar_parametros(**parametros)
        if float(duracion) <= 0:
            raise CalculoCostoError("La duración debe ser mayor que cero.")
        subtotal = self.tarifa_base * float(duracion)
        return self._ajustar_costo(subtotal, impuesto, descuento)


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_base, unidades_disponibles, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if int(unidades_disponibles) <= 0:
            raise DatosInvalidosError("Debe existir al menos una unidad disponible.")
        self.unidades_disponibles = int(unidades_disponibles)

    def validar_parametros(self, **parametros):
        unidades = int(parametros.get("unidades", 1))
        if unidades <= 0 or unidades > self.unidades_disponibles:
            raise DatosInvalidosError("La cantidad de equipos solicitada no está disponible.")
        return True

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, **parametros):
        self.validar_parametros(**parametros)
        if float(duracion) <= 0:
            raise CalculoCostoError("La duración debe ser mayor que cero.")
        unidades = int(parametros.get("unidades", 1))
        subtotal = self.tarifa_base * float(duracion) * unidades
        return self._ajustar_costo(subtotal, impuesto, descuento)


class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador, nombre, tarifa_base, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        especialidad = str(especialidad).strip()
        if not especialidad:
            raise DatosInvalidosError("La especialidad es obligatoria.")
        self.especialidad = especialidad

    def validar_parametros(self, **parametros):
        modalidad = parametros.get("modalidad", "virtual")
        if modalidad not in ("virtual", "presencial"):
            raise DatosInvalidosError("La modalidad debe ser virtual o presencial.")
        return True

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, **parametros):
        self.validar_parametros(**parametros)
        if float(duracion) <= 0:
            raise CalculoCostoError("La duración debe ser mayor que cero.")
        subtotal = self.tarifa_base * float(duracion)
        if parametros.get("modalidad", "virtual") == "presencial":
            subtotal *= 1.10
        return self._ajustar_costo(subtotal, impuesto, descuento)

    def describir(self):
        return f"{super().describir()} | Especialidad: {self.especialidad}"
