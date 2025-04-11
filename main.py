import os
import subprocess
import msvcrt

def limpiar_pantalla():
    os.system('cls')

def esperar_tecla(mensaje_espacio, mensaje_enter):
    print(f"\n{mensaje_espacio}")
    print(f"{mensaje_enter}")
    
    while True:
        if msvcrt.kbhit():
            tecla = msvcrt.getch()
            if tecla == b' ':
                return "menu"
            elif tecla == b'\r':
                return "salir"

def controlar_servicio(accion, servicio):
    try:
        comando = f"net {accion} {servicio}"
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)

        if resultado.returncode == 0:
            print(f"[✔] {accion.capitalize()} del servicio '{servicio}' completado.")
        else:
            print(f"[✘] Error al {accion} el servicio '{servicio}':\n{resultado.stderr}")

    except Exception as e:
        print(f"[!] Ocurrió un error: {e}")

def detener_servicios_oracle():
    print("\n=== Deteniendo servicios de Oracle ===")
    servicios = [
        "OracleServiceXE",
        "OracleOraDB21Home2TNSListener"
    ]
    for servicio in servicios:
        controlar_servicio("stop", servicio)
    
    accion = esperar_tecla("Presiona ESPACIO para volver al menú principal...", 
                          "Presiona ENTER para salir...")
    return accion

def iniciar_servicios_oracle():
    print("\n=== Iniciando servicios de Oracle ===")
    servicios = [
        "OracleServiceXE",
        "OracleOraDB21Home2TNSListener"
    ]
    for servicio in servicios:
        controlar_servicio("start", servicio)
    
    accion = esperar_tecla("Presiona ESPACIO para volver al menú principal...", 
                          "Presiona ENTER para salir...")
    return accion

def reiniciar_servicios_oracle():
    print("\n=== Reiniciando servicios de Oracle ===")
    detener_servicios_oracle()
    
    servicios = [
        "OracleServiceXE",
        "OracleOraDB21Home2TNSListener"
    ]
    for servicio in servicios:
        controlar_servicio("start", servicio)
    
    accion = esperar_tecla("Presiona ESPACIO para volver al menú principal...", 
                          "Presiona ENTER para salir...")
    return accion

def borrar_servicios_oracle():
    print("\n=== ADVERTENCIA: Borrado de servicios de Oracle ===")
    confirmacion = input("¿Estás seguro de que deseas continuar? (s/n): ")
    if confirmacion.lower() == 's':
        servicios = [
            "OracleServiceORCL",
            "OracleOraDB11g_home1TNSListener",
            "OracleJobSchedulerORCL"
        ]
        for servicio in servicios:
            controlar_servicio("stop", servicio)
            try:
                comando = f"sc delete {servicio}"
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                if resultado.returncode == 0:
                    print(f"[✔] Servicio '{servicio}' eliminado correctamente.")
                else:
                    print(f"[✘] Error al eliminar el servicio '{servicio}':\n{resultado.stderr}")
            except Exception as e:
                print(f"[!] Ocurrió un error: {e}")
                
        print("Se recomienda reiniciar el sistema para completar la desinstalación.")
    else:
        print("Operación cancelada.")
    
    accion = esperar_tecla("Presiona ESPACIO para volver al menú principal...", 
                          "Presiona ENTER para salir...")
    return accion

def mostrar_menu():
    while True:
        limpiar_pantalla()
        print("GESTIÓN DE SERVICIOS ORACLE")
        print("*" * 27)
        print("1. Reiniciar servicios de Oracle")
        print("2. Detener servicios de Oracle")
        print("3. Iniciar servicios de Oracle")
        print("4. Borrar completamente los servicios de Oracle")
        print("\033[31m(SOLO SI LO HAS DESINSTALADO Y/O QUIERES CAMBIAR LA VERSION INSTALADA)\033[0m")
        print("5. Salir")
        
        opcion = input("Selecciona una opción (1-5): ")
        
        if opcion == "1":
            accion = reiniciar_servicios_oracle()
            if accion == "salir":
                break
        elif opcion == "2":
            accion = detener_servicios_oracle()
            if accion == "salir":
                break
        elif opcion == "3":
            accion = iniciar_servicios_oracle()
            if accion == "salir":
                break
        elif opcion == "4":
            accion = borrar_servicios_oracle()
            if accion == "salir":
                break
        elif opcion == "5":
            print("\nSaliendo del programa...")
            break
        else:
            print("\nOpción no válida. Intenta de nuevo.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    mostrar_menu()
    