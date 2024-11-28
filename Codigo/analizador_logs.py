# Importar las clases del módulo procesamiento_logs
from procesamiento_logs import Info, Warning, Debug, Error, ProcesadorLogs

class AnalizadorLogs:
    def __init__(self, logs_procesados):
        self.logs_procesados = logs_procesados
        self.contador_logs = self.contar_logs_por_tipo()  # Contar los logs por tipo
        self.total_logs = len(logs_procesados)  # Total de logs procesados
        self.detalle_errores = self.obtener_logs_de_error()  # Obtener los logs de error

    def contar_logs_por_tipo(self):
        """Contar los logs por tipo y devolver un diccionario."""
        contador = {"INFO": 0, "WARNING": 0, "DEBUG": 0, "ERROR": 0}
        for log in self.logs_procesados:
            if isinstance(log, Info):
                contador["INFO"] += 1
            elif isinstance(log, Warning):
                contador["WARNING"] += 1
            elif isinstance(log, Debug):
                contador["DEBUG"] += 1
            elif isinstance(log, Error):
                contador["ERROR"] += 1
        return contador

    def obtener_logs_de_error(self):
        """Obtener una lista de logs de tipo Error."""
        return [log for log in self.logs_procesados if isinstance(log, Error)]


