#!/usr/bin/env python3

import subprocess
import logging
from tabulate import tabulate
import shutil

# Configuración del logging
logging.basicConfig(filename='audit_network.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Códigos de color ANSI
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
NC = '\033[0m'  # Sin color

# Función para ejecutar comandos con manejo de errores
def execute_command(command):
    try:
        result = subprocess.run(command, shell=False, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_msg = f"Error al ejecutar {' '.join(command)}: {e.stderr.strip()}"
        logging.error(error_msg)
        return error_msg

# Verificación de dependencias
def check_dependencies():
    dependencies = ['ip', 'ss', 'ufw', 'docker']
    missing_deps = []
    for dep in dependencies:
        if shutil.which(dep) is None:
            missing_deps.append(dep)
    if missing_deps:
        error_msg = f"{RED}Dependencias faltantes: {', '.join(missing_deps)}{NC}"
        print(error_msg)
        logging.error(f"Faltan dependencias: {', '.join(missing_deps)}")
        return False
    return True

# Listar interfaces de red
def list_interfaces():
    print(f"\n{BLUE}Interfaces de red y su estado:{NC}")
    interfaces = execute_command(["ip", "-br", "link", "show"])
    table = []
    for line in interfaces.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            state = f"{GREEN}{parts[1]}{NC}" if parts[1] == "UP" else f"{RED}{parts[1]}{NC}"
            table.append([parts[0], state])
    print(tabulate(table, headers=["Interface", "Estado"], tablefmt="grid"))
    logging.info("Se listaron las interfaces de red")

# Mostrar direcciones IP
def show_ip_addresses():
    print(f"\n{BLUE}Direcciones IP asignadas a cada interfaz:{NC}")
    ips = execute_command(["ip", "-br", "addr", "show"])
    table = []
    for line in ips.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            table.append([parts[0], f"{YELLOW}{parts[2]}{NC}"])
    print(tabulate(table, headers=["Interface", "Dirección IP"], tablefmt="grid"))
    logging.info("Se mostraron las direcciones IP")

# Mostrar tabla de enrutamiento
def show_routing_table():
    print(f"\n{BLUE}Tabla de enrutamiento actual:{NC}")
    routes = execute_command(["ip", "route", "show"])
    table = [[f"{GREEN}{line}{NC}"] for line in routes.splitlines()]
    print(tabulate(table, headers=["Ruta"], tablefmt="grid"))
    logging.info("Se mostró la tabla de enrutamiento")

# Mostrar reglas del firewall (UFW)
def show_firewall_rules():
    print(f"\n{BLUE}Reglas del firewall (UFW):{NC}")
    try:
        rules = execute_command(["sudo", "ufw", "status", "numbered"])
        table = [[f"{YELLOW}{line}{NC}"] for line in rules.splitlines() if line.startswith("[")]
        print(tabulate(table, headers=["Regla de UFW"], tablefmt="grid"))
        logging.info("Se mostraron las reglas del firewall")
    except FileNotFoundError:
        error_msg = f"{RED}UFW no está instalado en este sistema.{NC}"
        print(error_msg)
        logging.error("UFW no está instalado en este sistema.")

# Listar conexiones abiertas
def list_open_connections():
    print(f"\n{BLUE}Conexiones de red abiertas:{NC}")
    connections = execute_command(["ss", "-tuln"])
    table = []
    for line in connections.splitlines()[1:]:  # Omitir primera línea (encabezado)
        parts = line.split()
        if len(parts) >= 5:
            table.append([f"{GREEN}{parts[0]}{NC}", f"{YELLOW}{parts[4]}{NC}", f"{YELLOW}{parts[5]}{NC}"])
    print(tabulate(table, headers=["Estado", "Dirección Local", "Dirección Remota"], tablefmt="grid"))
    logging.info("Se listaron las conexiones abiertas")

# Auditoría de redes Docker
def list_docker_nets():
    print(f"\n{BLUE}Redes de Docker:{NC}")
    if shutil.which('docker') is None:
        print(f"{RED}Docker no está instalado.{NC}")
        logging.error("Docker no está instalado.")
        return
    
    nets = execute_command(['docker', 'network', 'ls'])
    table = []
    for line in nets.splitlines()[1:]:
        net = line.split()
        if len(net) >= 2:
            netname = net[1]
            table.append([f"{GREEN}{netname}{NC}", f"", f""])
            inspect_result = execute_command(['docker', 'network', 'inspect', netname])
            for item in inspect_result.splitlines():
                if '"Name":' in item:
                    hostname = item.split(":")[1].strip().strip('"').strip(',')
                    table.append(["", f"{YELLOW}{hostname}{NC}", ""])
                if '"IPv4Address":' in item:
                    hostip = item.split(":")[1].strip().strip('"').strip(',')
                    table[-1][2] = f"{YELLOW}{hostip}{NC}"
    print(tabulate(table, headers=["Nombre de Red", "Nombre de Host", "IP de Host"], tablefmt="grid"))
    logging.info("Se listaron las redes de Docker")

# Menú interactivo
def print_menu():
    print(f"\n{GREEN}Menú de Auditoría de Configuración de Red:{NC}")
    print("1. Listar interfaces de red")
    print("2. Mostrar direcciones IP")
    print("3. Mostrar tabla de enrutamiento")
    print("4. Mostrar reglas del firewall")
    print("5. Listar conexiones abiertas")
    print("6. Listar redes de Docker")
    print("7. Ejecutar todas las auditorías")
    print("8. Salir")

def main():
    print(f"{GREEN}Iniciando Auditoría de Configuración de Red{NC}")
    logging.info("Iniciando auditoría de configuración de red")

    # Verificación de dependencias antes de comenzar
    if not check_dependencies():
        print(f"{RED}No se puede continuar debido a dependencias faltantes.{NC}")
        return

    while True:
        print_menu()
        choice = input(f"{YELLOW}Ingrese su elección: {NC}")

        if choice == "1":
            list_interfaces()
        elif choice == "2":
            show_ip_addresses()
        elif choice == "3":
            show_routing_table()
        elif choice == "4":
            show_firewall_rules()
        elif choice == "5":
            list_open_connections()
        elif choice == "6":
            list_docker_nets()
        elif choice == "7":
            list_interfaces()
            show_ip_addresses()
            show_routing_table()
            show_firewall_rules()
            list_open_connections()
            list_docker_nets()
        elif choice == "8":
            print(f"{GREEN}Saliendo. Gracias por usar la herramienta de auditoría de configuración de red.{NC}")
            break
        else:
            print(f"{RED}Elección no válida. Intente de nuevo.{NC}")

    logging.info("Auditoría de configuración de red completada")

if __name__ == "__main__":
    main()
