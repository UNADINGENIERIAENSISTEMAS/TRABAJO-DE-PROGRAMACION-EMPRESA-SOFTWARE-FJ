"""Coordinador de clientes, servicios y reservas."""
import logging
from pathlib import Path
from excepciones import (ClienteDuplicadoError, ClienteNoEncontradoError,
                         ServicioDuplicadoError, ServicioNoEncontradoError,
                         ServicioNoDisponibleError, ReservaNoEncontradaError,
                         ReservaInvalidaError)
from reserva import Reserva

def configurar_logger(ruta=None):
    ruta = Path(ruta or Path(__file__).parent / "logs" / "sistema.log")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        handler = logging.FileHandler(ruta, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
    return logger

class GestorSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logger = configurar_logger()
        self.logger.info("Sistema Software FJ iniciado.")

    def registrar_cliente(self, cliente):
        if any(c.documento == cliente.documento or c.identificador == cliente.identificador
               for c in self.clientes):
            self.logger.warning("Intento de registrar cliente duplicado: %s", cliente.documento)
            raise ClienteDuplicadoError("Ya existe un cliente con ese documento o identificador.")
        self.clientes.append(cliente)
        self.logger.info("Cliente registrado: %s", cliente.documento)
        return cliente

    def buscar_cliente(self, documento):
        for cliente in self.clientes:
            if cliente.documento == str(documento):
                return cliente
        self.logger.warning("Cliente no encontrado: %s", documento)
        raise ClienteNoEncontradoError(f"No existe el cliente con documento {documento}.")

    def agregar_servicio(self, servicio):
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise ServicioDuplicadoError("Ya existe un servicio con ese identificador.")
        self.servicios.append(servicio)
        self.logger.info("Servicio agregado: %s", servicio.identificador)
        return servicio

    def buscar_servicio(self, identificador):
        for servicio in self.servicios:
            if servicio.identificador == str(identificador):
                return servicio
        raise ServicioNoEncontradoError(f"No existe el servicio {identificador}.")

    def crear_reserva(self, identificador, documento_cliente, id_servicio,
                      duracion, parametros=None):
        cliente = self.buscar_cliente(documento_cliente)
        servicio = self.buscar_servicio(id_servicio)
        if not servicio.disponible:
            self.logger.warning("Reserva rechazada: servicio %s no disponible", id_servicio)
            raise ServicioNoDisponibleError("No se puede reservar un servicio no disponible.")
        if any(r.identificador == str(identificador) for r in self.reservas):
            raise ReservaInvalidaError("Ya existe una reserva con ese identificador.")
        reserva = Reserva(identificador, cliente, servicio, duracion, parametros)
        self.reservas.append(reserva)
        self.logger.info("Reserva creada: %s", identificador)
        return reserva

    def buscar_reserva(self, identificador):
        for reserva in self.reservas:
            if reserva.identificador == str(identificador):
                return reserva
        raise ReservaNoEncontradaError(f"No existe la reserva {identificador}.")

    def listar_clientes(self):
        return list(self.clientes)

    def listar_servicios(self):
        return list(self.servicios)

    def listar_reservas(self):
        return list(self.reservas)
