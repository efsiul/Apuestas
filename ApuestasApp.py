import tkinter as tk
from tkinter import messagebox
import random
import time
from math import pi, sin, cos

class ApuestasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Programa de Apuestas")
        
        self.participantes = []
        self.marcadores = []
        self.resultados = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        self.clear_window()
        
        self.num_participantes_label = tk.Label(self.root, text="Número de Participantes:", font=("Helvetica", 14))
        self.num_participantes_label.pack(padx=10, pady=5)
        
        self.num_participantes_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.num_participantes_entry.pack(padx=10, pady=5)
        
        self.add_num_participantes_button = tk.Button(self.root, text="Aceptar", command=self.agregar_num_participantes, font=("Helvetica", 14), bg="blue", fg="white")
        self.add_num_participantes_button.pack(padx=10, pady=20)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def agregar_num_participantes(self):
        try:
            self.num_participantes = int(self.num_participantes_entry.get())
            if self.num_participantes <= 0:
                raise ValueError
            self.solicitar_nombres()
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingrese un número válido de participantes.")
    
    def solicitar_nombres(self):
        self.clear_window()
        
        self.participantes_entries = []
        for i in range(self.num_participantes):
            frame = tk.Frame(self.root)
            frame.pack(fill="x", padx=10, pady=5)
            label = tk.Label(frame, text=f"Nombre del Participante {i+1}:", font=("Helvetica", 14))
            label.pack(side="left")
            entry = tk.Entry(frame, font=("Helvetica", 14))
            entry.pack(side="right")
            self.participantes_entries.append(entry)
        
        self.finalizar_nombres_button = tk.Button(self.root, text="Finalizar", command=self.finalizar_nombres, font=("Helvetica", 14), bg="blue", fg="white")
        self.finalizar_nombres_button.pack(padx=10, pady=20)
    
    def finalizar_nombres(self):
        self.participantes = []
        for entry in self.participantes_entries:
            nombre = entry.get().strip()
            if not nombre:
                messagebox.showwarning("Advertencia", "Todos los nombres deben ser ingresados.")
                return
            self.participantes.append(nombre)
        
        self.solicitar_marcadores()
    
    def solicitar_marcadores(self):
        self.clear_window()
        
        self.marcadores_entries = []
        for i in range(self.num_participantes):
            frame = tk.Frame(self.root)
            frame.pack(fill="x", padx=10, pady=5)
            label = tk.Label(frame, text=f"Marcador {i+1}:", font=("Helvetica", 14))
            label.pack(side="left")
            entry = tk.Entry(frame, font=("Helvetica", 14))
            entry.pack(side="right", fill="x", expand=True)
            self.marcadores_entries.append(entry)
        
        self.finalizar_marcadores_button = tk.Button(self.root, text="Finalizar", command=self.finalizar_marcadores, font=("Helvetica", 14), bg="blue", fg="white")
        self.finalizar_marcadores_button.pack(padx=10, pady=20)
    
    def finalizar_marcadores(self):
        self.marcadores = []
        for entry in self.marcadores_entries:
            marcador_text = entry.get().strip()
            if not marcador_text:
                messagebox.showwarning("Advertencia", "Todos los marcadores deben ser ingresados.")
                return
            try:
                equipo1, equipo2 = map(int, marcador_text.split(','))
                self.marcadores.append((equipo1, equipo2))
            except ValueError:
                messagebox.showwarning("Advertencia", "Los marcadores deben tener el formato 'equipo1,equipo2'.")
                return
        
        self.solicitar_nombres_equipos()
    
    def solicitar_nombres_equipos(self):
        self.clear_window()
        
        self.equipo1_label = tk.Label(self.root, text="Nombre del Equipo 1:", font=("Helvetica", 14))
        self.equipo1_label.pack(padx=10, pady=5)
        self.equipo1_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.equipo1_entry.pack(padx=10, pady=5)
        
        self.equipo2_label = tk.Label(self.root, text="Nombre del Equipo 2:", font=("Helvetica", 14))
        self.equipo2_label.pack(padx=10, pady=5)
        self.equipo2_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.equipo2_entry.pack(padx=10, pady=5)
        
        self.iniciar_button = tk.Button(self.root, text="Iniciar Ruleta", command=self.iniciar_ruleta, font=("Helvetica", 14), bg="blue", fg="white")
        self.iniciar_button.pack(padx=10, pady=20)
    
    def iniciar_ruleta(self):
        
        equipo1 = self.equipo1_entry.get().strip()
        equipo2 = self.equipo2_entry.get().strip()
        
        if not equipo1 or not equipo2:
            messagebox.showwarning("Advertencia", "Debe ingresar los nombres de ambos equipos.")
            return
        
        self.resultado = tk.Toplevel(self.root)
        self.resultado.title("Ruleta de Marcadores")
        
        self.main_frame = tk.Frame(self.resultado)
        self.main_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.main_frame, width=500, height=500)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        
        self.canvas.create_text(400, 50, text=f"Equipo 1: {equipo1}", fill="blue", font=("Helvetica", 16))
        self.canvas.create_text(400, 80, text=f"Equipo 2: {equipo2}", fill="red", font=("Helvetica", 16))
        
        self.draw_ruleta()
        
        self.girar_button = tk.Button(self.main_frame, text="Girar Ruleta", command=self.girar_ruleta, font=("Helvetica", 14), bg="green", fg="white")
        self.girar_button.pack(side="bottom", fill="x", expand=True, padx=10, pady=10)
        
        self.tabla_frame = tk.Frame(self.main_frame)
        self.tabla_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.resultados_label = tk.Label(self.tabla_frame, text="Resultados:", font=("Helvetica", 16, "bold"))
        self.resultados_label.pack(side="top", anchor="w")
        
        self.header_frame = tk.Frame(self.tabla_frame)
        self.header_frame.pack(fill="x")
        
        self.participantes_label = tk.Label(self.header_frame, text="Participante", borderwidth=2, relief="solid", width=15, font=("Helvetica", 14, "bold"))
        self.participantes_label.pack(side="left", fill="x", expand=True)
        
        self.equipo1_label = tk.Label(self.header_frame, text=self.equipo1, borderwidth=2, relief="solid", fg="blue", width=15, font=("Helvetica", 14, "bold"))
        self.equipo1_label.pack(side="left", fill="x", expand=True)
        
        self.equipo2_label = tk.Label(self.header_frame, text=self.equipo2, borderwidth=2, relief="solid", fg="red", width=15, font=("Helvetica", 14, "bold"))
        self.equipo2_label.pack(side="left", fill="x", expand=True)
        
        self.row_frames = []
    
    def draw_ruleta(self):
        self.canvas.delete("all")
        num_participantes = len(self.participantes)
        angle_step = 2 * pi / num_participantes
        
        colors = ["#FF177D","#31A2AC","#AFF001", "#AA11AB", "#FFC3A0",  "#FDD125", "#392F5A", "#61C0BF", "#6B4226", "#D9BF77"]
        self.segmentos = []
        self.name_tags = []
        
        for i in range(num_participantes):
            angle = i * angle_step
            x0 = 250 + 150 * cos(angle)
            y0 = 250 + 150 * sin(angle)
            x1 = 250 + 150 * cos(angle + angle_step)
            y1 = 250 + 150 * sin(angle + angle_step)
            arc = self.canvas.create_arc(100, 100, 400, 400, start=angle*180/pi, extent=angle_step*180/pi, fill=colors[i % len(colors)], outline="black", tags="segmento")
            line = self.canvas.create_line(250, 250, x0, y0, fill="black", tags="linea_segmento")
            
            name_x = 250 + 200 * cos(angle + angle_step / 2)
            name_y = 250 + 200 * sin(angle + angle_step / 2)
            name = self.canvas.create_text(name_x, name_y, text=self.participantes[i], font=("Helvetica", 12, "bold"), tags="nombre", anchor="center")
            self.adjust_text_position(name, name_x, name_y, angle_step, angle)
            
            segmento = {
                'angle': angle,
                'arc': arc,
                'line': line,
                'participante': self.participantes[i],
                'marcador': None
            }
            self.segmentos.append(segmento)
            self.name_tags.append(name)
        
        self.canvas.create_line(250, 250, 250, 100, fill="black", tags="linea_segmento")  # Línea inicial
    
    def adjust_text_position(self, text, x, y, angle_step, angle):
        bbox = self.canvas.bbox(text)
        width = bbox[2] - bbox[0]
        if width > 100:  # Ajustar si el texto es muy largo
            self.canvas.itemconfig(text, width=100)
    
    def girar_ruleta(self):
        random.shuffle(self.marcadores)
        num_participantes = len(self.participantes)
        angle_step = 2 * pi / num_participantes
        
        for i in range(36):  # Simulación de giro de la ruleta
            angle_offset = (i * pi / 18) % (2 * pi)
            self.canvas.delete("marcadores")
            self.canvas.delete("linea_segmento")
            
            for segmento in self.segmentos:
                angle = segmento['angle'] - angle_offset  # Ajuste para que ambos giren en el mismo sentido
                start_angle = angle * 180 / pi
                self.canvas.itemconfig(segmento['arc'], start=start_angle, extent=angle_step*180/pi)
                x0 = 250 + 150 * cos(angle)
                y0 = 250 + 150 * sin(angle)
                self.canvas.coords(segmento['line'], 250, 250, x0, y0)
                
                marcador_x = 250 + 75 * cos(angle + angle_step / 2)
                marcador_y = 250 + 75 * sin(angle + angle_step / 2)
                marcador_text = f"{self.marcadores[self.segmentos.index(segmento) % len(self.marcadores)][0]}, {self.marcadores[self.segmentos.index(segmento) % len(self.marcadores)][1]}"
                self.canvas.create_text(marcador_x, marcador_y, text=marcador_text, tags="marcadores")
            
            self.root.update()
            time.sleep(0.1)
        
        # Asignar los marcadores finales
        self.canvas.delete("marcadores")
        angle_offset = (36 * pi / 18) % (2 * pi)
        for segmento in self.segmentos:
            angle = segmento['angle'] - angle_offset  # Ajuste para que ambos giren en el mismo sentido
            start_angle = angle * 180 / pi
            self.canvas.itemconfig(segmento['arc'], start=start_angle, extent=angle_step*180/pi)
            x0 = 250 + 150 * cos(angle)
            y0 = 250 + 150 * sin(angle)
            self.canvas.coords(segmento['line'], 250, 250, x0, y0)
            
            marcador_x = 250 + 75 * cos(angle + angle_step / 2)
            marcador_y = 250 + 75 * sin(angle + angle_step / 2)
            marcador_text = f"{self.marcadores[self.segmentos.index(segmento) % len(self.marcadores)][0]}, {self.marcadores[self.segmentos.index(segmento) % len(self.marcadores)][1]}"
            self.canvas.create_text(marcador_x, marcador_y, text=marcador_text, tags="marcadores")
            segmento['marcador'] = self.marcadores[self.segmentos.index(segmento) % len(self.marcadores)]
        
        self.actualizar_tabla()
    
    def actualizar_tabla(self):
        for frame in self.row_frames:
            frame.destroy()
        
        self.row_frames = []
        
        for segmento in self.segmentos:
            row_frame = tk.Frame(self.tabla_frame)
            row_frame.pack(fill="x")
            
            tk.Label(row_frame, text=segmento['participante'], borderwidth=2, relief="solid", width=15, height=2).pack(side="left", fill="x", expand=True)
            tk.Label(row_frame, text=segmento['marcador'][0], borderwidth=2, relief="solid", fg="blue", width=15, height=2).pack(side="left", fill="x", expand=True)
            tk.Label(row_frame, text=segmento['marcador'][1], borderwidth=2, relief="solid", fg="red", width=15, height=2).pack(side="left", fill="x", expand=True)
            
            self.row_frames.append(row_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = ApuestasApp(root)
    root.mainloop()
