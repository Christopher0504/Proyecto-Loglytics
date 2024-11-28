import re

# Definición de las clases de log (Padre y Subclases)
class Log:
    def __init__(self, timestamp, ip, nivel):
        self.timestamp = timestamp
        self.ip = ip
        self.nivel = nivel
    
    def __str__(self):
        return f"{self.timestamp} - {self.ip} - {self.nivel}"

class Info(Log):
    def __init__(self, timestamp, ip, nivel, mensaje):
        super().__init__(timestamp, ip, nivel)
        self.mensaje = mensaje
    
    def __str__(self):
        return f"{super().__str__()} - {self.mensaje}"

class Warning(Log):
    def __init__(self, timestamp, ip, nivel, mensaje):
        super().__init__(timestamp, ip, nivel)
        self.mensaje = mensaje
    
    def __str__(self):
        return f"{super().__str__()} - {self.mensaje}"

class Debug(Log):
    def __init__(self, timestamp, ip, nivel, mensaje, codigo_http):
        super().__init__(timestamp, ip, nivel)
        self.mensaje = mensaje
        self.codigo_http = codigo_http
    
    def __str__(self):
        return f"{super().__str__()} - {self.mensaje} - {self.codigo_http}"

class Error(Log):
    def __init__(self, timestamp, ip, nivel, mensaje, codigo_http):
        super().__init__(timestamp, ip, nivel)
        self.mensaje = mensaje
        self.codigo_http = codigo_http
    
    def __str__(self):
        return f"{super().__str__()} - {self.mensaje} - {self.codigo_http}"

# Clase ProcesadorLogs
class ProcesadorLogs:
    def __init__(self, archivo):
        self.archivo = archivo  # Ruta del archivo de logs
        self.logs_procesados = []  # Lista para almacenar los logs procesados

    def procesar_log(self, log_line):
        """Procesa una línea de log y devuelve una instancia de log correspondiente."""
    
        # Obtener los valores básicos del log (timestamp, ip y nivel)
        timestamp = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', log_line).group(0)
        ip = re.search(r'- ([\d\.]+) -', log_line).group(1)
        nivel = re.search(r'- (\w+) -', log_line).group(1)
    
        # Procesar según el tipo de log
        if nivel == "INFO":
            mensaje = re.search(r'INFO - (.+)', log_line).group(1)
            return Info(timestamp, ip, nivel, mensaje)

        elif nivel == "WARNING":
            mensaje = re.search(r'WARNING - (.+)', log_line).group(1)
            return Warning(timestamp, ip, nivel, mensaje)

        elif nivel == "DEBUG":
            mensaje = re.search(r'"(.+?)"', log_line).group(1)  # Extraer el mensaje del método HTTP
            codigo_http = re.search(r'\d{3}$', log_line).group(0)  # Extraer el código HTTP
            return Debug(timestamp, ip, nivel, mensaje, codigo_http)

        elif nivel == "ERROR":
            # Asegurarnos de que se capturen correctamente el mensaje y el código HTTP en los logs de error
            mensaje_match = re.search(r'"(.+?)"', log_line)  # Capturar el mensaje entre comillas
            if mensaje_match:
                mensaje = mensaje_match.group(1)
                codigo_http_match = re.search(r'\d{3}$', log_line)  # Extraer el código HTTP al final de la línea
                if codigo_http_match:
                    codigo_http = codigo_http_match.group(0)
                    return Error(timestamp, ip, nivel, mensaje, codigo_http)

        return None

    def procesar_logs(self):
        # Leer el archivo de logs y procesar línea por línea
        with open(self.archivo, "r") as archivo:
            for linea in archivo:
                log = self.procesar_log(linea.strip())  # Eliminar saltos de línea y procesar cada log
                if log:
                    self.logs_procesados.append(log)
                    #print(log)  # Imprimir cada log procesado
        return self.logs_procesados

    def obtener_logs(self):
        # Devuelve la lista de logs procesados
        return self.logs_procesados


