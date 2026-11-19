"""Gestión del ciclo de vida de una reserva."""
from enum import Enum
from entidad import Entidad
from excepciones import (ReservaInvalidaError, EstadoReservaError,
                         ServicioNoDisponibleError, ProcesamientoReservaError)

class EstadoReserva(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"

class Reserva(Entidad):
    def __init__(self, identificador, cliente, servicio, duracion, parametros=None):
        super().__init__(identificador)
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("La reserva requiere cliente y servicio.")
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as exc:
            raise ReservaInvalidaError("La duración debe ser numérica.") from exc
        if duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser mayor que cero.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.parametros = dict(parametros or {})
        self.estado = EstadoReserva.PENDIENTE
        self.costo_total = None

    def confirmar(self):
        if self.estado is not EstadoReserva.PENDIENTE:
            raise EstadoReservaError("Solo se pueden confirmar reservas pendientes.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible.")
        self.servicio.validar_parametros(**self.parametros)
        self.estado = EstadoReserva.CONFIRMADA
        return self.estado

    def cancelar(self):
        if self.estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise EstadoReservaError("La reserva no se puede cancelar en su estado actual.")
        self.estado = EstadoReserva.CANCELADA
        return self.estado

    def procesar(self, impuesto=0.0, descuento=0.0):
        if self.estado is not EstadoReserva.CONFIRMADA:
            raise EstadoReservaError("Solo se pueden procesar reservas confirmadas.")
        try:
            self.costo_total = self.servicio.calcular_costo(
                self.duracion, impuesto, descuento, **self.parametros
            )
            self.estado = EstadoReserva.PROCESADA
            return self.costo_total
        except Exception as exc:
            raise ProcesamientoReservaError("No fue posible procesar la reserva.") from exc

    def describir(self):
        return (f"Reserva {self.identificador} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Estado: {self.estado.value}")

    def __str__(self):
        return self.describir()
