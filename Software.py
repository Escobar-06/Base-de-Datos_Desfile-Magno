import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Creacion de la base de datos
def conectar_db():
    conn = sqlite3.connect("desfile_magno.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT,
            edad TEXT,
            puesto TEXT,
            tipo TEXT
        )
    """)
    conn.commit()
    conn.close()

# Funciones
def agregar_participante():
    if not nombre_var.get():
        messagebox.showwarning("Campo requerido", "El nombre es obligatorio.")
        return

    conn = sqlite3.connect("desfile_magno.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO participantes (nombre, telefono, edad, puesto, tipo)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nombre_var.get(),
        telefono_var.get(),
        edad_var.get(),
        puesto_var.get(),
        tipo_var.get()
    ))
    conn.commit()
    conn.close()
    limpiar_campos()
    mostrar_participantes()

def mostrar_participantes():
    for row in tabla.get_children():
        tabla.delete(row)

    conn = sqlite3.connect("desfile_magno.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM participantes")
    for row in cursor.fetchall():
        tabla.insert("", tk.END, values=row)
    conn.close()

def limpiar_campos():
    nombre_var.set("")
    telefono_var.set("")
    edad_var.set("")
    puesto_var.set("")
    tipo_var.set("Vendedor")

# Interfaz gráfica
conectar_db()
ventana = tk.Tk()
ventana.title("Gestión de Participantes - Desfile Magno")
ventana.geometry("980x720")

# Variables
nombre_var = tk.StringVar()
telefono_var = tk.StringVar()
edad_var = tk.StringVar()
puesto_var = tk.StringVar()
tipo_var = tk.StringVar(value="Vendedor")

# Formulario tipo de campo de texto
tk.Label(ventana, text="Nombre:").grid(row=0, column=0, sticky="w")
tk.Entry(ventana, textvariable=nombre_var).grid(row=0, column=1)

tk.Label(ventana, text="Teléfono:").grid(row=1, column=0, sticky="w")
tk.Entry(ventana, textvariable=telefono_var).grid(row=1, column=1)

tk.Label(ventana, text="Edad:").grid(row=2, column=0, sticky="w")
tk.Entry(ventana, textvariable=edad_var).grid(row=2, column=1)

tk.Label(ventana, text="Puesto:").grid(row=3, column=0, sticky="w")
tk.Entry(ventana, textvariable=puesto_var).grid(row=3, column=1)

tk.Label(ventana, text="Tipo:").grid(row=4, column=0, sticky="w")
opciones_tipo = ttk.Combobox(ventana, textvariable=tipo_var, values=["Vendedor", "Trabajador", "Publicidad"])
opciones_tipo.grid(row=4, column=1)

tk.Button(ventana, text="Agregar", command=agregar_participante).grid(row=6, column=1, pady=10)
tk.Button(ventana, text="Limpiar", command=limpiar_campos).grid(row=7, column=1)

# Tabla y opciones 
tabla = ttk.Treeview(ventana, columns=("id", "nombre", "telefono", "edad", "puesto", "tipo"), show="headings")
tabla.heading("id", text="ID")
tabla.heading("nombre", text="Nombre")
tabla.heading("telefono", text="Teléfono")
tabla.heading("edad", text="Edad")
tabla.heading("puesto", text="Puesto")
tabla.heading("tipo", text="Tipo")
tabla.grid(row=8, column=0, columnspan=5, sticky="nsew")

# Vista del registro de los participantes
scroll = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll.set)
scroll.grid(row=8, column=4, sticky="ns")

# Ejecutar y manetener la ventana activa
mostrar_participantes()
ventana.mainloop()
