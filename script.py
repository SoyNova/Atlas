import eel
import time
import win32gui
import win32api
import win32con
import threading
import random
import os
import winsound
import sys
import ctypes
import win32con
import win32api
from cryptography.fernet import Fernet
import subprocess
import atexit



os.system('cls')

destruct_activated = False
temp_bat = "cleanup.bat"

delay_cps = 5

# username = input("Ingresa tu nombre: ")

eel.init('web')

@eel.expose                    
def say_hello_py(x):
 
    print('Hello from %s' % x)

@eel.expose
def set_cps(cps):
    global delay_cps
    print('CPS set to %s' % cps)
    delay_cps = int(cps)

runningLeft = False
workInMenus = False
runningRight = False
delay_cps_right = 10

anti_detect = False  # Modo anti-detección
jitter_range = 2     # Movimiento aleatorio del mouse (píxeles)
human_variation = 0.017

window = win32gui.FindWindow("LWJGL", None)


def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def eliminar_registros():
    try:
        # Eliminar USN Journal (Requiere Admin)
        os.system("fsutil usn deletejournal /D C:")

        # Eliminar archivos temporales
        os.system("del /Q /F /S %TEMP%\\*.*")
        os.system("del /Q /F /S %APPDATA%\\..\\Local\\Temp\\*.*")

        # Eliminar Prefetch
        os.system("del /Q /F /S C:\\Windows\\Prefetch\\*.*")

        # Limpiar Event Logs
        os.system("wevtutil cl Application")
        os.system("wevtutil cl System")
    except Exception as e:
        print(f"Error limpiando registros: {e}")

def encriptar_y_eliminar_archivo(ruta):
    try:
        # Generar clave de encriptación
        clave = Fernet.generate_key()
        cifrador = Fernet(clave)

        # Leer, encriptar y sobreescribir
        with open(ruta, "rb") as f:
            datos = f.read()
        datos_encriptados = cifrador.encrypt(datos)
        
        # Sobreescribir 3 veces (estándar DoD)
        with open(ruta, "wb") as f:
            for _ in range(3):
                f.write(os.urandom(len(datos_encriptados)))
            f.write(datos_encriptados)
        
        # Eliminar archivo
        os.remove(ruta)
    except Exception as e:
        print(f"Error encriptando {ruta}: {e}")


@eel.expose
def toggleRightClicker():
    global runningRight
    if runningRight:
        runningRight = False
        print('Right clicker toggled to %s' % runningRight)
    else:
        runningRight = True
        rightClicker_thread = threading.Thread(target=rightClicker, daemon=True)
        rightClicker_thread.start()
        print('Right clicker toggled to %s' % runningRight)
    
@eel.expose
def set_cpsRight(cps):
    global delay_cps_right
    print('CPS set to %s' % cps)
    delay_cps_right = int(cps)

@eel.expose
def workInMenusToggle():
    global workInMenus
    if workInMenus:
        workInMenus = False
    else:
        workInMenus = True
    print('Work in menus toggled to %s' % workInMenus)


@eel.expose
def destruct():
    global runningLeft, runningRight, destruct_activated

    # Bandera de autodestrucción
    destruct_activated = True
    runningLeft = False
    runningRight = False 

    if not es_admin():
        # Relanzar como admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    # Encriptar logs del programa
    logs = [os.path.join(os.getcwd(), "debug.log")]  # Agrega tus archivos aquí
    for archivo in logs:
        if os.path.exists(archivo):
            encriptar_y_eliminar_archivo(archivo)

    # Eliminar registros del sistema
    eliminar_registros()

    # Crear script de limpieza
    with open(temp_bat, "w") as f:
        f.write(f"""
        @echo off
        timeout /t 3 /nobreak >nul
        del /F /Q "{sys.argv[0]}"
        del /F /Q "{temp_bat}"
        """)

    # Ejecutar limpieza como proceso independiente
    subprocess.Popen(f'start /min cmd /c "{temp_bat}"', shell=True)
    os._exit(0)

    # ========== REGISTRAR LIMPIEZA AL SALIR ==========
    atexit.register(lambda: os.remove(temp_bat) if os.path.exists(temp_bat) else None)

    # Autodestrucción del ejecutable
    ejecutable = sys.argv[0]
    os.system(f"timeout /t 3 & del /F /Q \"{ejecutable}\"")
    sys.exit()

@eel.expose
def toggleLeftClicker():
    global runningLeft
    if runningLeft:
        runningLeft = False
        print('Left clicker toggled to %s' % runningLeft)
    else:
        runningLeft = True
        leftClicker_thread = threading.Thread(target=leftClicker, daemon=True)
        leftClicker_thread.start()

@eel.expose
def leftClicker():
    global window, workInMenus
    try:
        while runningLeft and not destruct_activated:
            currentWindow = win32gui.GetForegroundWindow()
            if currentWindow != window:
                window = win32gui.FindWindow("LWJGL", None)

            if not workInMenus:
                cursorInfo = win32gui.GetCursorInfo()[1]
                if cursorInfo > 50000 and cursorInfo < 100000:
                                time.sleep(1 / delay_cps)

                                continue
            if win32api.GetAsyncKeyState(0x01):
                start_time = time.perf_counter()

                # Hold variable (5-15ms)
                hold_time = random.uniform(0.005, 0.015)
                win32api.SendMessage(window, win32con.WM_LBUTTONDOWN, 0, 0)
                time.sleep(hold_time)
                win32api.SendMessage(window, win32con.WM_LBUTTONUP, 0, 0)

                # Delay con variación humana
                base_delay = 1 / delay_cps
                variation = random.choice([
                    random.gauss(base_delay, 0.02),
                    random.uniform(base_delay*0.7, base_delay*1.3)
                ])
                adjusted_delay = max(0.001, variation - hold_time)
                time.sleep(adjusted_delay)
    except Exception as e:
        print(f"Error en leftClicker: {e}")


@eel.expose
def rightClicker():
    global window
    while runningRight:
        currentWindow = win32gui.GetForegroundWindow()
        if currentWindow != window:
            window = win32gui.FindWindow("LWJGL", None)

        if win32api.GetAsyncKeyState(0x02):


            delay = 1 / delay_cps_right


            win32api.SendMessage(window, win32con.WM_RBUTTONDOWN, 0, 0)
            time.sleep(delay)
            win32api.SendMessage(window, win32con.WM_RBUTTONUP, 0, 0)


eel.start('gui.html', mode='chrome', size=(700, 440), suppress_error=True)






