# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto académico desarrollado en Python para demostrar programación orientada a objetos y manejo robusto de excepciones.

## Requisitos
- Python 3.10 o superior.
- No requiere instalar paquetes externos.

## Ejecución
Desde la carpeta del proyecto, ejecutar:

```bash
python main.py
```

En algunos equipos Windows también puede ser:

```bash
py main.py
```

## Contenido
- Clases abstractas `Entidad` y `Servicio`.
- Cliente con validaciones.
- Servicios de reserva de salas, alquiler de equipos y asesorías.
- Gestión de reservas y estados.
- Excepciones personalizadas.
- Registro de eventos y errores en `logs/sistema.log`.
- 17 escenarios demostrativos.

## Consideraciones
La información se conserva en memoria durante la ejecución. No se utiliza una base de datos. El archivo de log sí conserva los registros de eventos y errores.
