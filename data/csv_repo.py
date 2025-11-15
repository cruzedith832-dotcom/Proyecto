import csv
import os
from datetime import datetime

# --- Configuración de Rutas y Encabezados ---
# Las rutas asumen que el archivo 'csv_repo.py' está en 'src/' y los datos en 'data/'.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')
PRODUCTOS_FILE = os.path.join(DATA_DIR, 'productos.csv')
VENTAS_FILE = os.path.join(DATA_DIR, 'ventas.csv')

# Campos esperados para cada archivo
PRODUCTOS_FIELDS = ['id', 'nombre', 'categoria', 'precio_unitario', 'stock', 'unidad']
VENTAS_FIELDS = ['id_venta', 'fecha', 'id_producto', 'cantidad', 'precio_unitario_venta', 'forma_pago']

# --------------------------------------------------------------------------------
# FUNCIONES DE UTILIDAD INTERNAS
# --------------------------------------------------------------------------------

def _asegurar_archivo(filepath, fieldnames):
    """Verifica si el archivo CSV existe y, si no, lo crea con su cabecera."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if not os.path.exists(filepath):
        try:
            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
            return True
        except Exception as e:
            print(f"ERROR: No se pudo crear el archivo {filepath}: {e}")
            return False
    return True

def _escribir_todos_los_productos(productos):
    """Reescribe todo el archivo productos.csv. Se usa para actualizar y eliminar."""
    if not _asegurar_archivo(PRODUCTOS_FILE, PRODUCTOS_FIELDS):
        return False

    try:
        with open(PRODUCTOS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=PRODUCTOS_FIELDS)
            writer.writeheader()
            # Convertir todos los valores a string antes de escribir en CSV
            productos_str = [{k: str(v) for k, v in p.items()} for p in productos]
            writer.writerows(productos_str)
        return True
    except Exception as e:
        print(f"ERROR: Fallo al reescribir productos.csv: {e}")
        return False

# --------------------------------------------------------------------------------
# FUNCIONES PRINCIPALES: INVENTARIO (CRUD)
# --------------------------------------------------------------------------------

def leer_productos():
    """Lee productos.csv y devuelve una lista de diccionarios, con tipos convertidos."""
    
    if not _asegurar_archivo(PRODUCTOS_FILE, PRODUCTOS_FIELDS):
        return []

    productos = []
    try:
        with open(PRODUCTOS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convertir tipos de datos para su uso numérico en la aplicación
                try:
                    row['id'] = int(row['id'])
                    row['precio_unitario'] = float(row['precio_unitario'])
                    row['stock'] = int(row['stock'])
                except (ValueError, TypeError):
                    print(f"ADVERTENCIA: Fila ignorada por datos inválidos o faltantes: {row}")
                    continue
                productos.append(row)
    except Exception as e:
        print(f"ERROR al leer productos.csv: {e}")
        
    return productos


def agregar_producto(producto):
    """Agrega un nuevo producto al final de productos.csv. (Inventario: Registrar)"""
    
    if not _asegurar_archivo(PRODUCTOS_FILE, PRODUCTOS_FIELDS):
        return False
        
    try:
        with open(PRODUCTOS_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=PRODUCTOS_FIELDS)
            # Convertir a string antes de escribir
            producto_str = {k: str(v) for k, v in producto.items()}
            writer.writerow(producto_str)
        return True
    except Exception as e:
        print(f"ERROR al guardar producto en productos.csv: {e}")
        return False


def actualizar_producto(id_producto, nuevos_datos):
    """Busca un producto por ID y actualiza sus campos. (Inventario: editar)"""
    productos = leer_productos()
    actualizado = False
    
    for producto in productos:
        if producto['id'] == id_producto:
            # Actualiza solo los campos proporcionados
            for key, value in nuevos_datos.items():
                if key in PRODUCTOS_FIELDS:
                    producto[key] = value
            actualizado = True
            break
            
    if actualizado:
        return _escribir_todos_los_productos(productos) # Reescribe el archivo completo
        
    return False

def eliminar_producto(id_producto):
    """Elimina un producto por ID. (Inventario: eliminar)"""
    productos = leer_productos()
    
    # Crea una nueva lista excluyendo el producto a eliminar
    productos_filtrados = [p for p in productos if p['id'] != id_producto]
    
    if len(productos_filtrados) < len(productos):
        # Reescribe solo si se eliminó un producto
        return _escribir_todos_los_productos(productos_filtrados)
        
    return False

# --------------------------------------------------------------------------------
# FUNCIONES AUXILIARES DE VENTAS
# --------------------------------------------------------------------------------

def leer_ventas():
    """Lee ventas.csv y devuelve una lista de diccionarios, con tipos convertidos."""
    
    if not _asegurar_archivo(VENTAS_FILE, VENTAS_FIELDS):
        return []
        
    ventas = []
    try:
        with open(VENTAS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Conversión de tipos
                try:
                    row['id_venta'] = int(row['id_venta'])
                    row['id_producto'] = int(row['id_producto'])
                    row['cantidad'] = int(row['cantidad'])
                    row['precio_unitario_venta'] = float(row['precio_unitario_venta'])
                except (ValueError, TypeError):
                    continue
                ventas.append(row)
    except Exception as e:
        print(f"ERROR al leer ventas.csv: {e}")
        
    return ventas

def guardar_venta(registro_venta):
    """Agrega un registro de venta a ventas.csv. (Ventas: Registrar venta)"""
    
    if not _asegurar_archivo(VENTAS_FILE, VENTAS_FIELDS):
        return False
        
    try:
        with open(VENTAS_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=VENTAS_FIELDS)
            # Convertir a string antes de escribir
            registro_venta_str = {k: str(v) for k, v in registro_venta.items()}
            writer.writerow(registro_venta_str)
        return True
    except Exception as e:
        print(f"ERROR al guardar venta en ventas.csv: {e}")
        return False