import os
import json
import network
import urequests
import machine
from time import sleep, time


class OTAUpdater:
    def __init__(self, ssid, password, repo_url, filename):
        self.ssid = ssid
        self.password = password
        self.repo_url = repo_url
        self.filename = filename
        self.version_url = self.repo_url + 'version.json'
        
        # Obtener la versión actual
        self.current_version = 0
        if 'version.json' in os.listdir():
            try:
                with open('version.json') as f:
                    self.current_version = int(json.load(f)['version'])
                    print(self.current_version)
            except (ValueError, KeyError):
                print("Error leyendo la versión actual. Usando versión 0.")
        
    def connect_wifi(self, timeout=10):
        """Conectar a Wi-Fi con un tiempo máximo de espera."""
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.ssid, self.password)
        
        start_time = time()
        while not sta_if.isconnected():
            if time() - start_time > timeout:
                raise OSError("No se pudo conectar a WiFi dentro del tiempo límite.")
            print('.', end="")
            sleep(0.25)
        #print(f'\nConectado a WiFi, IP es: {sta_if.ifconfig()[0]}')


    def fetch_latest_code(self):
        """Descargar el nuevo firmware."""
        try:
            response = urequests.get(self.repo_url + self.filename)
            if response.status_code == 200:
                with open(self.filename, 'w') as f:
                    f.write(response.text)
                print(f"Firmware descargado: {self.filename}")
            else:
                print("Error: Firmware no encontrado en el servidor.")
        except Exception as e:
            print(f"Error al descargar el firmware: {e}")
        finally:
            response.close()


    def check_for_updates(self):
        """Comprobar si hay actualizaciones disponibles."""
        try:
            self.connect_wifi()
            response = urequests.get(self.version_url)
            if response.status_code == 200:
                data = json.loads(response.text)
                self.latest_version = int(data['version'])
                print(f'Última versión es: {self.latest_version}')
                response.close()


                if self.current_version < self.latest_version:
                    print("Nueva versión disponible.")
                    return True
            else:
                print("Error al verificar la versión del servidor.")
        except Exception as e:
            print(f"Error al comprobar actualizaciones: {e}")
        finally:
            try:
                response.close()
            except:
                pass
        return False


    def download_and_install_update_if_available(self):
        """Descargar e instalar actualizaciones si están disponibles."""
        try:
            if self.check_for_updates():
                self.fetch_latest_code()
                # Cambia a la nueva versión
                with open('version.json', 'w') as f:
                    json.dump({'version': self.latest_version}, f)
                print('Firmware actualizado exitosamente. Reiniciando...')
                machine.reset()
            else:
                print("No se encontraron actualizaciones.")
        except Exception as e:
            print(f"Error durante la actualización: {e}")

