import shutil
import os
import re
import unicodedata

class LogProcessor:
    def __init__(self, nombre_archivo, carpeta_origen, carpeta_destino):
        self.nombre_archivo = nombre_archivo
        self.carpeta_origen = carpeta_origen
        self.carpeta_destino = carpeta_destino
        self.ruta_origen = os.path.join(carpeta_origen, nombre_archivo)
        self.ruta_destino = os.path.join(carpeta_destino, nombre_archivo)

    # Método para eliminar secuencias de escape ANSI
    @staticmethod
    def eliminar_escapes_ansi(texto):
        patron_ansi = r'\x1b\[[0-9;]*[mG]'
        return re.sub(patron_ansi, '', texto)

    # Método para eliminar tildes
    @staticmethod
    def eliminar_tildes(texto):
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sin_tildes = ''.join([caracter for caracter in texto_normalizado if unicodedata.category(caracter) != 'Mn'])
        return texto_sin_tildes

    # Método para procesar cada línea del log
    def procesar_linea(self, linea):
        linea = self.eliminar_escapes_ansi(linea)

        # Buscar y procesar el patrón ` - - ` con el código HTTP
        match = re.search(r' - - .*"[^"]*" (\d{3}) ', linea)
        if match:
            codigo_http = int(match.group(1))
            if codigo_http < 400:
                linea = linea.replace(' - - ', ' - DEBUG - ')
            else:
                linea = linea.replace(' - - ', ' - ERROR - ')

        # Agregar un guion entre la comilla de cierre de la ruta HTTP y el código HTTP
        linea = re.sub(r'" (\d{3}) ', r'" - \1 ', linea)

        # Eliminar el último guion si está presente
        linea = re.sub(r' -$', '', linea)

        # Eliminar timestamps repetidos entre corchetes
        linea = re.sub(r'\[\d{2}/\w{3}/\d{4} \d{2}:\d{2}:\d{2}\]', '', linea).strip()

        # Eliminar tildes
        linea = self.eliminar_tildes(linea)

        return linea

    # Método principal para procesar el archivo
    def procesar_archivo(self):
        try:
            if os.path.exists(self.ruta_origen):
                # Copiar el archivo
                shutil.copy(self.ruta_origen, self.ruta_destino)
                print(f"Archivo '{self.nombre_archivo}' copiado exitosamente a '{self.carpeta_destino}'.")

                # Leer el archivo y procesar las líneas
                with open(self.ruta_destino, 'r', encoding='utf-8') as archivo:
                    lineas = archivo.readlines()

                # Eliminar las primeras 5 líneas y procesar el resto
                lineas = [self.procesar_linea(linea) for linea in lineas[5:]]

                # Guardar los cambios en el archivo con codificación utf-8
                with open(self.ruta_destino, 'w', encoding='utf-8') as archivo:
                    archivo.writelines(linea + '\n' for linea in lineas)

                print(f"Se procesaron las líneas del archivo '{self.nombre_archivo}' correctamente.")
            else:
                print(f"El archivo '{self.nombre_archivo}' no existe en la carpeta '{self.carpeta_origen}'.")
        except Exception as e:
            print(f"Error al copiar o modificar el archivo: {e}")


# Instanciamos la clase y ejecutamos el procesamiento

def importar():
    nombre_archivo = 'logs.txt'
    carpeta_origen = '../servidor_py'
    carpeta_destino = '.'
    log_processor = LogProcessor(nombre_archivo, carpeta_origen, carpeta_destino)
    log_processor.procesar_archivo()