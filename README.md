# Software FJ — Sistema de gestión orientado a objetos

## Requisitos
- Python 3.9 o superior.
- No requiere instalar librerías externas.

## Ejecución
1. Descomprimir `Software_FJ.zip`.
2. Abrir una terminal dentro de la carpeta `Software_FJ`.
3. Ejecutar:

   ```bash
   python main.py
   ```

## Descripción
El sistema administra clientes, servicios y reservas en listas de Python. No utiliza bases de datos.
Los eventos y errores se registran en `software_fj.log`.

## Servicios incluidos
- Reserva de salas por horas.
- Alquiler de equipos por días.
- Asesorías especializadas por horas.

## Pruebas
`main.py` ejecuta doce operaciones, incluyendo registros válidos e inválidos, creación de servicios,
reservas exitosas y fallidas, cancelaciones y búsquedas de clientes inexistentes.

## Principios POO
- Abstracción: `Entidad` y `Servicio`.
- Herencia: `Cliente` y los tres servicios concretos.
- Polimorfismo: cada servicio implementa sus propios métodos abstractos.
- Encapsulación: atributos protegidos y privados, con propiedades de acceso.
- Excepciones: jerarquía propia, validaciones y encadenamiento de errores.

## Nota sobre sobrecarga
Python no implementa sobrecarga tradicional por firma como Java o C++. En este proyecto se demuestra
una alternativa idiomática mediante parámetros opcionales en `calcular_costo(cantidad, descuento, impuesto)`.
