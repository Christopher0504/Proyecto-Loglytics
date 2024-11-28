import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
from analizador_logs import AnalizadorLogs, ProcesadorLogs

class DashboardLogs:
    def __init__(self, analizador_logs):
        self.analizador = analizador_logs
        # Obtener los datos de los logs procesados y los resultados del análisis
        self.data_por_tipo = self.analizador.contador_logs  # Diccionario con cantidad de logs por tipo
        self.total_logs = self.analizador.total_logs  # Total de logs procesados
        self.errores = self.analizador.detalle_errores  # Lista de logs de tipo ERROR

    def mostrar_dashboard(self):
        # Crear la figura y especificar el tamaño
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_facecolor('#f2f2f2')  
        fig.suptitle("Dashboard de Análisis de Logs", fontsize=16)

        # Configuración de la cuadrícula con GridSpec sin constrained_layout
        gs = gridspec.GridSpec(2, 2, height_ratios=[3, 2], width_ratios=[2, 1], wspace=0.3, hspace=0.4)

        # Gráfico de Barras - Superior Izquierda
        ax1 = fig.add_subplot(gs[0, 0])
        etiquetas = list(self.data_por_tipo.keys())
        valores = list(self.data_por_tipo.values())
        colores = ['#4a90e2', '#50e3c2', '#e94e77', '#f39c12']  # Colores para cada tipo de log
        ax1.bar(etiquetas, valores, color=colores, edgecolor="black", linewidth=0.7)
        ax1.set_xlabel("Tipos de Log")
        ax1.set_ylabel("Cantidad")
        ax1.set_title("Cantidad de Logs por Tipo")

        # Tabla de Reportes - Inferior Izquierda
        ax2 = fig.add_subplot(gs[1, 0])
        if self.errores:
            data = {
                "Timestamp": [error.timestamp for error in self.errores],
                "IP": [error.ip for error in self.errores],
                "Nivel": [error.nivel for error in self.errores],
                "Mensaje": [error.mensaje for error in self.errores],
                "Código HTTP": [error.codigo_http for error in self.errores],
            }
            df_errores = pd.DataFrame(data)
            ax2.axis("tight")
            ax2.axis("off")
            table = ax2.table(cellText=df_errores.values, colLabels=df_errores.columns, cellLoc='center', loc='center', 
                              colColours=["#4a90e2"] * len(df_errores.columns))
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1.2, 1.2)
            table.auto_set_column_width(col=list(range(len(df_errores.columns))))
            for k, cell in table._cells.items():
                cell.set_edgecolor('#dddddd')
                if k[0] == 0:  
                    cell.set_text_props(weight='bold', color='white')
                    cell.set_facecolor('#4a90e2')
                else:
                    cell.set_facecolor('#f9f9f9')
            ax2.set_title("Tabla de Reportes de Errores", fontsize=12, weight='bold')
        else:
            ax2.text(0.5, 0.5, "No se encontraron logs de error.", ha="center", va="center", fontsize=12)

        # Gráfico Circular - Inferior Derecha
        ax3 = fig.add_subplot(gs[1, 1])
        porcentajes = [valor / self.total_logs * 100 for valor in valores]
        etiquetas_con_porcentaje = [f"{etiqueta} - {porcentaje:.1f}%" for etiqueta, porcentaje in zip(etiquetas, porcentajes)]
        wedges, texts, autotexts = ax3.pie(porcentajes, labels=etiquetas_con_porcentaje, autopct='%1.1f%%', startangle=140,
                                           colors=colores, textprops={'color':"black"}, wedgeprops={"edgecolor": "black"})
        for text in autotexts:
            text.set_color("black")
        ax3.set_title("Porcentaje de Tipos de Logs", fontsize=12, weight='bold')

        # Mostrar el gráfico
        plt.show()
        
def implementar():
        # Procesar los logs antes de crear el analizador
        procesador = ProcesadorLogs("logs.txt")
        logs_procesados = procesador.procesar_logs()
        # Crear la instancia del AnalizadorLogs con los logs procesados
        analizador = AnalizadorLogs(logs_procesados)
        # Crear la instancia del DashboardLogs
        dashboard = DashboardLogs(analizador)
        # Mostrar el dashboard con los gráficos y la tabla
        dashboard.mostrar_dashboard()