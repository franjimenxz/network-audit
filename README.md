
# Auditoría de Configuración de Red, Docker y Firewall (Python)

## Descripción

Este proyecto es un **script en Python** diseñado para auditar y generar informes sobre las configuraciones de red, redes Docker y reglas del firewall en sistemas **Linux**. El script realiza una auditoría completa y muestra información como el estado de las interfaces de red, direcciones IP, tabla de rutas, conexiones abiertas, redes Docker y las reglas de firewall configuradas con UFW.

## Características

- **Auditoría de Redes**:
  - Muestra el estado de las interfaces de red.
  - Muestra las direcciones IP asignadas a cada interfaz.
  - Muestra la tabla de rutas del sistema.
  - Muestra las conexiones abiertas de red.
- **Auditoría de Docker**:
  - Lista las redes de Docker y sus contenedores asociados con direcciones IP.
- **Auditoría de Firewall**:
  - Muestra las reglas configuradas en UFW.
- **Manejo de Errores y Logs**:
  - Registra todas las acciones y errores en un archivo de log (`audit_network.log`).
  - Verifica que todas las dependencias necesarias (como `ip`, `ss`, `ufw`, `docker`) estén instaladas antes de ejecutar.
- **Interfaz Interactiva**:
  - Menú interactivo que permite al usuario seleccionar qué auditorías realizar o ejecutar todas de una vez.

## Dependencias

El script requiere que las siguientes herramientas estén instaladas en el sistema:

- `ip`: Para auditar interfaces de red y la tabla de rutas.
- `ss`: Para listar conexiones de red abiertas.
- `ufw`: Para mostrar las reglas del firewall (opcional).
- `docker`: Para auditar redes de Docker (opcional).
- Python 3.x

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/franjimenxz/network-audit.git
   cd network-audit
   ```

2. **Hacer el script ejecutable**:
   ```bash
   chmod +x network_audit.py
   ```

3. **Ejecutar el script**:
   ```bash
   sudo ./network_audit.py
   ```

## Uso

Al ejecutar el script, verás un menú interactivo con varias opciones para auditar diferentes aspectos de la configuración de red, Docker, y el firewall. Puedes seleccionar una opción para ejecutar una auditoría específica o elegir la opción para ejecutar todas las auditorías a la vez.

### Menú Interactivo:

```plaintext
Menú de Auditoría de Configuración de Red:
1. Listar interfaces de red
2. Mostrar direcciones IP
3. Mostrar tabla de enrutamiento
4. Mostrar reglas del firewall
5. Listar conexiones abiertas
6. Listar redes de Docker
7. Ejecutar todas las auditorías
8. Salir
```

### Ejemplo de Ejecución (Salida):

```plaintext
Iniciando Auditoría de Configuración de Red

Interfaces de red y su estado:
+------------+---------+
| Interface  | Estado  |
+------------+---------+
| lo         | UNKNOWN |
| eth0       | UP      |
+------------+---------+

Direcciones IP asignadas a cada interfaz:
+------------+-------------------+
| Interface  | Dirección IP       |
+------------+-------------------+
| lo         | 127.0.0.1/8       |
| eth0       | 192.168.1.100/24  |
+------------+-------------------+

Tabla de enrutamiento actual:
+--------------------------------+
| Ruta                           |
+--------------------------------+
| default via 192.168.1.1 dev eth0|
| 192.168.1.0/24 dev eth0 scope link |
+--------------------------------+

Conexiones de red abiertas:
+---------+---------------------+-----------------+
| Estado  | Dirección Local      | Dirección Remota|
+---------+---------------------+-----------------+
| LISTEN  | 127.0.0.1:631        | 0.0.0.0:*       |
| LISTEN  | 0.0.0.0:22           | 0.0.0.0:*       |
+---------+---------------------+-----------------+

Reglas del firewall (UFW):
+---------------------------+
| Regla de UFW              |
+---------------------------+
| [ 1] ALLOW IN 80/tcp      |
| [ 2] ALLOW IN 443/tcp     |
+---------------------------+

Redes de Docker:
+--------------+-----------------+---------------+
| Nombre de Red| Nombre de Host   | IP de Host    |
+--------------+-----------------+---------------+
| bridge       | web_app          | 172.17.0.2    |
| bridge       | db               | 172.17.0.3    |
+--------------+-----------------+---------------+
```

## Automatización

Para automatizar la ejecución de este script, puedes añadirlo a **cron** para que se ejecute periódicamente (por ejemplo, cada día a las 2:00 AM):

1. Edita el archivo cron:
   ```bash
   crontab -e
   ```

2. Añade la siguiente línea para ejecutar el script diariamente:
   ```bash
   0 2 * * * /ruta/al/script/network_audit.py
   ```

