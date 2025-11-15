import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------
# Funciones simuladas
# ---------------------------

def agregar_producto():
    messagebox.showinfo("Inventario", "Producto agregado correctamente.")

def actualizar_producto():
    messagebox.showinfo("Inventario", "Producto actualizado.")

def eliminar_producto():
    messagebox.showwarning("Inventario", "Producto eliminado.")

def buscar_producto():
    messagebox.showinfo("Inventario", "Búsqueda completada.")

def agregar_venta():
    messagebox.showinfo("Ventas", "Producto agregado a la venta.")

def calcular_total():
    messagebox.showinfo("Ventas", "Total de la venta calculado.")

def limpiar_campos():
    messagebox.showinfo("Ventas", "Campos limpiados.")

def generar_reporte_ventas():
    messagebox.showinfo("Reportes", "Reporte de ventas generado correctamente.")

def reporte_inventario():
    messagebox.showinfo("Reportes", "Reporte de inventario generado.")

def productos_mas_vendidos():
    messagebox.showinfo("Reportes", "Mostrando productos más vendidos.")

# ---------------------------
# Ventana principal
# ---------------------------
root = tk.Tk()
root.title("Sistema de Gestión - Inventario, Ventas y Reportes")
root.geometry("850x600")
root.config(bg="#f2f2f2")

# ---------------------------
# Estilo general
# ---------------------------
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 9))
style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"))

# ---------------------------
# Cuaderno de pestañas
# ---------------------------
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ===========================
#        PESTAÑA INVENTARIO
# ===========================
frame_inventario = ttk.Frame(notebook)
notebook.add(frame_inventario, text="Inventario")

titulo_inv = ttk.Label(frame_inventario, text="GESTIÓN DE INVENTARIO", font=("Segoe UI", 12, "bold"))
titulo_inv.pack(pady=10)

frame_datos_inv = ttk.LabelFrame(frame_inventario, text="Datos del Producto")
frame_datos_inv.pack(fill="x", padx=10, pady=5)

labels_inv = ["ID Producto:", "Nombre:", "Categoría:", "Precio:", "Stock:", "Unidad:"]
entradas_inv = {}
for i, texto in enumerate(labels_inv):
    ttk.Label(frame_datos_inv, text=texto).grid(row=i, column=0, padx=5, pady=5, sticky="e")
    entrada = ttk.Entry(frame_datos_inv, width=30)
    entrada.grid(row=i, column=1, padx=5, pady=5)
    entradas_inv[texto] = entrada

frame_botones_inv = ttk.Frame(frame_inventario)
frame_botones_inv.pack(pady=10)

ttk.Button(frame_botones_inv, text="Agregar Producto", command=agregar_producto).pack(side="left", padx=5)
ttk.Button(frame_botones_inv, text="Actualizar Producto", command=actualizar_producto).pack(side="left", padx=5)
ttk.Button(frame_botones_inv, text="Eliminar Producto", command=eliminar_producto).pack(side="left", padx=5)
ttk.Button(frame_botones_inv, text="Buscar Producto", command=buscar_producto).pack(side="left", padx=5)

frame_lista_inv = ttk.LabelFrame(frame_inventario, text="Listado de Productos")
frame_lista_inv.pack(fill="both", expand=True, padx=10, pady=10)

columnas_inv = ("ID", "Nombre", "Categoría", "Precio", "Stock", "Unidad")
tabla_inv = ttk.Treeview(frame_lista_inv, columns=columnas_inv, show="headings")
for col in columnas_inv:
    tabla_inv.heading(col, text=col)
    tabla_inv.column(col, anchor="center", width=120)
tabla_inv.pack(fill="both", expand=True)

# ===========================
#        PESTAÑA VENTAS
# ===========================
frame_ventas = ttk.Frame(notebook)
notebook.add(frame_ventas, text="Ventas")

titulo_ventas = ttk.Label(frame_ventas, text="REGISTRO DE VENTAS", font=("Segoe UI", 12, "bold"))
titulo_ventas.pack(pady=10)

frame_datos_ventas = ttk.LabelFrame(frame_ventas, text="Datos de Venta")
frame_datos_ventas.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_datos_ventas, text="Producto:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
combo_producto = ttk.Combobox(frame_datos_ventas, values=["Martillo", "Clavos", "Taladro", "Pintura"])
combo_producto.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_datos_ventas, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_cantidad = ttk.Entry(frame_datos_ventas, width=30)
entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

frame_botones_ventas = ttk.Frame(frame_ventas)
frame_botones_ventas.pack(pady=10)
ttk.Button(frame_botones_ventas, text="Agregar a venta", command=agregar_venta).pack(side="left", padx=5)
ttk.Button(frame_botones_ventas, text="Calcular Total", command=calcular_total).pack(side="left", padx=5)
ttk.Button(frame_botones_ventas, text="Limpiar Campos", command=limpiar_campos).pack(side="left", padx=5)

frame_total = ttk.Frame(frame_ventas)
frame_total.pack(pady=5)
ttk.Label(frame_total, text="Total de la Venta:").pack(side="left", padx=5)
entry_total = ttk.Entry(frame_total, width=15)
entry_total.pack(side="left", padx=5)

frame_lista_ventas = ttk.LabelFrame(frame_ventas, text="Listado de la Venta")
frame_lista_ventas.pack(fill="both", expand=True, padx=10, pady=10)

columnas_ventas = ("Producto", "Cantidad", "Precio Unitario", "Subtotal")
tabla_ventas = ttk.Treeview(frame_lista_ventas, columns=columnas_ventas, show="headings")
for col in columnas_ventas:
    tabla_ventas.heading(col, text=col)
    tabla_ventas.column(col, anchor="center", width=150)
tabla_ventas.pack(fill="both", expand=True)

# ===========================
#        PESTAÑA REPORTES
# ===========================
frame_reportes = ttk.Frame(notebook)
notebook.add(frame_reportes, text="Reportes")

titulo_reportes = ttk.Label(frame_reportes, text="REPORTES Y ESTADÍSTICAS", font=("Segoe UI", 12, "bold"))
titulo_reportes.pack(pady=10)

frame_datos_reportes = ttk.LabelFrame(frame_reportes, text="Datos del Reporte")
frame_datos_reportes.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_datos_reportes, text="Fecha:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_fecha = ttk.Entry(frame_datos_reportes, width=25)
entry_fecha.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_datos_reportes, text="Total de Ventas:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_total_ventas = ttk.Entry(frame_datos_reportes, width=25)
entry_total_ventas.grid(row=1, column=1, padx=5, pady=5)

frame_botones_reportes = ttk.Frame(frame_reportes)
frame_botones_reportes.pack(pady=10)
ttk.Button(frame_botones_reportes, text="Generar Reporte de Ventas", command=generar_reporte_ventas).pack(side="left", padx=5)
ttk.Button(frame_botones_reportes, text="Reporte de Inventario", command=reporte_inventario).pack(side="left", padx=5)
ttk.Button(frame_botones_reportes, text="Productos Más Vendidos", command=productos_mas_vendidos).pack(side="left", padx=5)

frame_resultado_reportes = ttk.LabelFrame(frame_reportes, text="Lista de Productos Más Vendidos")
frame_resultado_reportes.pack(fill="both", expand=True, padx=10, pady=10)

txt_reportes = tk.Text(frame_resultado_reportes, wrap="word")
txt_reportes.insert("1.0", "Seleccione una opción para generar reportes...")
txt_reportes.pack(fill="both", expand=True, padx=5, pady=5)

# ---------------------------
root.mainloop()
