import tkinter as tk
from tkinter import messagebox
import mysql.connector

class FlightReservationSystem:
    def __init__(self, total_seats=40):
        self.total_seats = total_seats
        self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="m2308hp123",
            database="reservaavion"
        )
        self.db_cursor = self.db_connection.cursor()

    def realizar_reserva(self, nombre, numero_identificacion):
        sql_check = "SELECT COUNT(*) FROM reservas WHERE numero_identificacion = %s"
        self.db_cursor.execute(sql_check, (numero_identificacion,))
        if self.db_cursor.fetchone()[0] > 0:
            return f"Ya existe una reserva para {nombre}."
        
        sql_count = "SELECT COUNT(*) FROM reservas"
        self.db_cursor.execute(sql_count)
        if self.db_cursor.fetchone()[0] >= self.total_seats:
            return "Lo siento, el vuelo está completamente lleno."
        
        sql_insert = "INSERT INTO reservas (nombre, numero_identificacion, numero_asiento) VALUES (%s, %s, %s)"
        numero_asiento = self.db_cursor.lastrowid + 1
        self.db_cursor.execute(sql_insert, (nombre, numero_identificacion, numero_asiento))
        self.db_connection.commit()
        return f"Reserva exitosa para {nombre}. Número de asiento: {numero_asiento}"

    def cancelar_reserva(self, numero_identificacion):
        sql_check = "SELECT nombre FROM reservas WHERE numero_identificacion = %s"
        self.db_cursor.execute(sql_check, (numero_identificacion,))
        result = self.db_cursor.fetchone()
        if not result:
            return "No se encontró ninguna reserva con este número de identificación."
        
        nombre = result[0]
        sql_delete = "DELETE FROM reservas WHERE numero_identificacion = %s"
        self.db_cursor.execute(sql_delete, (numero_identificacion,))
        self.db_connection.commit()
        return f"Reserva de {nombre} ha sido cancelada exitosamente."

    def ver_reservas(self):
        sql = "SELECT nombre, numero_identificacion, numero_asiento FROM reservas"
        self.db_cursor.execute(sql)
        reservas = self.db_cursor.fetchall()
        if not reservas:
            return "No hay reservas actualmente."
        
        lista_reservas = []
        for nombre, identificacion, asiento in reservas:
            lista_reservas.append(f"Identificación: {identificacion}, Nombre: {nombre}, Asiento: {asiento}")
        
        return lista_reservas

    def asientos_disponibles(self):
        sql = "SELECT COUNT(*) FROM reservas"
        self.db_cursor.execute(sql)
        reservas_actuales = self.db_cursor.fetchone()[0]
        return self.total_seats - reservas_actuales

class FlightReservationGUI:
    def __init__(self, root):
        self.sistema = FlightReservationSystem()
        self.root = root
        self.root.title("Sistema de Reservas de Vuelo")
        self.create_widgets()

    def create_widgets(self):
        self.label_nombre = tk.Label(self.root, text="Nombre completo:")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=5)
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        self.label_identificacion = tk.Label(self.root, text="Número de identificación:")
        self.label_identificacion.grid(row=1, column=0, padx=10, pady=5)
        self.entry_identificacion = tk.Entry(self.root)
        self.entry_identificacion.grid(row=1, column=1, padx=10, pady=5)

        self.button_reservar = tk.Button(self.root, text="Realizar Reserva", command=self.realizar_reserva)
        self.button_reservar.grid(row=2, column=0, padx=10, pady=5)

        self.button_cancelar = tk.Button(self.root, text="Cancelar Reserva", command=self.cancelar_reserva)
        self.button_cancelar.grid(row=2, column=1, padx=10, pady=5)

        self.button_ver_reservas = tk.Button(self.root, text="Ver Reservas", command=self.ver_reservas)
        self.button_ver_reservas.grid(row=3, column=0, padx=10, pady=5)

        self.button_asientos_disponibles = tk.Button(self.root, text="Asientos Disponibles", command=self.asientos_disponibles)
        self.button_asientos_disponibles.grid(row=3, column=1, padx=10, pady=5)

    def realizar_reserva(self):
        nombre = self.entry_nombre.get()
        identificacion = self.entry_identificacion.get()
        resultado = self.sistema.realizar_reserva(nombre, identificacion)
        messagebox.showinfo("Reserva", resultado)

    def cancelar_reserva(self):
        identificacion = self.entry_identificacion.get()
        resultado = self.sistema.cancelar_reserva(identificacion)
        messagebox.showinfo("Cancelar Reserva", resultado)

    def ver_reservas(self):
        reservas = self.sistema.ver_reservas()
        mensaje = "\n".join(reservas)
        messagebox.showinfo("Reservas", mensaje)    

    def asientos_disponibles(self):
        disponibles = self.sistema.asientos_disponibles()
        messagebox.showinfo("Asientos Disponibles", f"Hay {disponibles} asientos disponibles.")

root = tk.Tk()
app = FlightReservationGUI(root)
root.mainloop()
