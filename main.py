"""Ejecución demostrativa con más de diez operaciones simuladas."""
from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorSoftwareFJ
from excepciones import SoftwareFJError, DatosInvalidosError

def ejecutar_pruebas():
    gestor = GestorSoftwareFJ()
    print("=" * 65)
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 65)

    def ejecutar(numero, descripcion, accion):
        print(f"\nPRUEBA {numero}: {descripcion}")
        try:
            resultado = accion()
        except SoftwareFJError as error:
            gestor.logger.error("Prueba %s - %s: %s", numero, descripcion, error)
            print("ERROR CONTROLADO:", error)
        except Exception as error:
            gestor.logger.exception("Error inesperado en prueba %s", numero)
            print("ERROR INESPERADO:", error)
        else:
            print("RESULTADO:", resultado)
        finally:
            print("Fin de la prueba.")

    ejecutar(1, "Registrar cliente válido",
             lambda: gestor.registrar_cliente(
                 Cliente("C001", "Laura Gómez", "12345678", "laura@email.com", "3001234567")))
    ejecutar(2, "Intentar registrar correo inválido",
             lambda: Cliente("C002", "Pedro Ruiz", "87654321", "correo-invalido", "3007654321"))
    ejecutar(3, "Intentar registrar documento duplicado",
             lambda: gestor.registrar_cliente(
                 Cliente("C003", "Laura Gómez Dos", "12345678", "laura2@email.com", "3001112233")))
    ejecutar(4, "Buscar cliente existente",
             lambda: gestor.buscar_cliente("12345678").describir())
    ejecutar(5, "Buscar cliente inexistente",
             lambda: gestor.buscar_cliente("99999999"))
    ejecutar(6, "Agregar servicio de sala",
             lambda: gestor.agregar_servicio(
                 ReservaSala("S001", "Sala Ejecutiva", 50000, 12)))
    ejecutar(7, "Agregar alquiler de equipos",
             lambda: gestor.agregar_servicio(
                 AlquilerEquipo("S002", "Computador portátil", 30000, 5)))
    ejecutar(8, "Agregar asesoría especializada",
             lambda: gestor.agregar_servicio(
                 AsesoriaEspecializada("S003", "Asesoría tecnológica", 80000, "Tecnología")))
    ejecutar(9, "Buscar servicio inexistente",
             lambda: gestor.buscar_servicio("S999"))
    ejecutar(10, "Crear reserva válida",
             lambda: gestor.crear_reserva("R001", "12345678", "S001", 2, {"personas": 8}))
    ejecutar(11, "Confirmar reserva",
             lambda: gestor.buscar_reserva("R001").confirmar().value)
    ejecutar(12, "Procesar reserva con impuesto y descuento",
             lambda: f"${gestor.buscar_reserva('R001').procesar(0.19, 0.10):,.2f}")
    ejecutar(13, "Intentar procesar nuevamente una reserva procesada",
             lambda: gestor.buscar_reserva("R001").procesar())
    ejecutar(14, "Intentar crear reserva para servicio no disponible",
             lambda: (setattr(gestor.buscar_servicio("S002"), "disponible", False),
                      gestor.crear_reserva("R002", "12345678", "S002", 1, {"unidades": 1})))
    ejecutar(15, "Crear y cancelar una reserva pendiente",
             lambda: gestor.crear_reserva("R003", "12345678", "S003", 1,
                                           {"modalidad": "virtual"}).cancelar().value)
    ejecutar(16, "Consultar reserva inexistente",
             lambda: gestor.buscar_reserva("R999"))
    ejecutar(17, "Validar capacidad superior a la permitida",
             lambda: gestor.buscar_servicio("S001").calcular_costo(2, personas=20))

    print("\n" + "=" * 65)
    print("RESUMEN")
    print("Clientes registrados:", len(gestor.listar_clientes()))
    print("Servicios registrados:", len(gestor.listar_servicios()))
    print("Reservas creadas:", len(gestor.listar_reservas()))
    print("Los eventos y errores se registran en logs/sistema.log")
    print("=" * 65)

if __name__ == "__main__":
    ejecutar_pruebas()
