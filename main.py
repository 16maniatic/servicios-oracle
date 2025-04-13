import os
import subprocess
import msvcrt

def clear():
    os.system('cls')

def key(space, enter):
    print(f"\n{space}")
    print(f"{enter}")
    
    while True:
        if msvcrt.kbhit():
            tecla = msvcrt.getch()
            if tecla == b' ':
                return "menu"
            elif tecla == b'\r':
                return "salir"

def controller(action, service):
    try:
        command = f"net {action} {service}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{action.capitalize()} del servicio '{service}' completado.")
        else:
            print(f"\033[31mError al {action} el servicio '{service}':\n{result.stderr}\033[0m")

    except Exception as e:
        print(f"\033[31mOcurrió un error: {e}\033[0m")

def stop_services():
    print("\n=== Deteniendo servicios de Oracle ===")
    services = [
        "OracleServiceXE",
        "OracleOraDB21Home2TNSListener"
    ]
    for service in services:
        controller("stop", service)
    
    action = key("Presiona ESPACIO para volver al menú principal...", 
                          "Presiona ENTER para salir...")
    return action

def start_services():
    print("\n=== Iniciando servicios de Oracle ===")
    services = [
        "OracleServiceXE",
        "OracleOraDB21Home2TNSListener"
    ]
    for service in services:
        controller("start", service) 
    
    action = key("Presiona ESPACIO para volver al menú principal...", 
                          "Presiona ENTER para salir...")
    return action

def restart_services():
    print("\n=== Reiniciando servicios de Oracle ===")
    services = [
        "OracleServiceXE",
        "OracleOraDB21Home2TNSListener"
    ]
    
    for service in services:
        controller("stop", service)
    
    for service in services:
        controller("start", service)
    
    action = key("Presiona ESPACIO para volver al menú principal...", 
                          "Presiona ENTER para salir...")
    return action

def delete_services():
    print("\n=== ADVERTENCIA: Borrado de servicios de Oracle ===")
    confirm = input("¿Estás seguro de que deseas continuar? (s/n): ")
    if confirm.lower() == 's':
        services = [
            "OracleServiceORCL",
            "OracleOraDB11g_home1TNSListener",
            "OracleJobSchedulerORCL"
        ]
        for service in services:
            controller("stop", service)
            try:
                command = f"sc delete {service}"
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Servicio '{service}' eliminado correctamente.")
                else:
                    print(f"\033[31mError al eliminar el servicio '{service}':\n{result.stderr}\033[0m")
            except Exception as e:
                print(f"\033[31mOcurrió un error: {e}\033[0m")
                
        print("\033[31mSe recomienda reiniciar el sistema para completar la desinstalación.\033[0m")
    else:
        print("\033[31mOperación cancelada.\033[0m")
    
    action = key("Presiona ESPACIO para volver al menú principal...", 
                          "Presiona ENTER para salir...")
    return action

def menu():
    while True:
        clear()
        print("GESTIÓN DE SERVICIOS ORACLE")
        print("*" * 27)
        print("1. Reiniciar servicios de Oracle")
        print("2. Detener servicios de Oracle")
        print("3. Iniciar servicios de Oracle")
        print("4. Borrar completamente los servicios de Oracle")
        print("\033[31m(SOLO SI LO HAS DESINSTALADO Y/O QUIERES CAMBIAR LA VERSION INSTALADA)\033[0m")
        print("5. Salir")
        
        option = input("Selecciona una opción (1-5): ")
        
        if option == "1":
            action = restart_services()
            if action == "salir":
                break
        elif option == "2":
            action = stop_services()
            if action == "salir":
                break
        elif option == "3":
            action = start_services()
            if action == "salir":
                break
        elif option == "4":
            action = delete_services()
            if action == "salir":
                break
        elif option == "5":
            print("\nSaliendo del programa...")
            break
        else:
            print("\nOpción no válida. Intenta de nuevo.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    menu()
    