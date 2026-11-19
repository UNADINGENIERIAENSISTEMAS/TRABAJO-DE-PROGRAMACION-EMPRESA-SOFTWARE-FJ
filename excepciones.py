"""Excepciones personalizadas del sistema Software FJ."""

class SoftwareFJError(Exception):
    """Excepción base para los errores controlados de la aplicación."""

class DatosInvalidosError(SoftwareFJError): pass
class ClienteDuplicadoError(SoftwareFJError): pass
class ClienteNoEncontradoError(SoftwareFJError): pass
class ServicioDuplicadoError(SoftwareFJError): pass
class ServicioNoEncontradoError(SoftwareFJError): pass
class ServicioNoDisponibleError(SoftwareFJError): pass
class ReservaInvalidaError(SoftwareFJError): pass
class ReservaNoEncontradaError(SoftwareFJError): pass
class EstadoReservaError(SoftwareFJError): pass
class CalculoCostoError(SoftwareFJError): pass
class ProcesamientoReservaError(SoftwareFJError): pass
