"""
negocio.py
Backend para gestión de inventario y ventas con CSV.

Funciones principales:
 - listar_productos() -> list[dict]
 - agregar_producto(producto: dict) -> bool
 - actualizar_producto(id_producto: int, nuevos_datos: dict) -> bool
 - eliminar_producto(id_producto: int) -> bool
 - listar_ventas() -> list[dict]
 - registrar_venta(venta: dict) -> bool
 - calcular_total_venta(items: list[dict]) -> float
 - productos_mas_vendidos(top_n=10) -> list[tuple(producto_id, cantidad_total)]

Robusto: maneja archivos faltantes creando cabeceras, valida tipos y captura errores para evitar crasheos.
"""

import csv
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Campos esperados
PRODUCTOS_FIELDS = ['id', 'nombre', 'categoria', 'precio_unitario', 'stock', 'unidad']
VENTAS_FIELDS = ['id_venta', 'fecha', 'id_producto', 'cantidad', 'precio_unitario_venta', 'forma_pago']

def _find_csv(filename):
    """
    Busca el archivo en rutas comunes:
    - carpeta actual
    - ./data/
    - ../data/
    - /mnt/data (entorno dev)
    - CWD absoluta
    Retorna Path (no str).
    """
    candidates = [
        Path.cwd() / filename,
        Path.cwd() / 'data' / filename,
        Path.cwd().parent / 'data' / filename,
        Path('/mnt/data') / filename,
    ]
    for p in candidates:
        if p.exists():
            return p
    # Si no existe, preferir crear en ./data/
    target = Path.cwd() / 'data' / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        # crear archivo con cabecera
        try:
            with target.open('w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=PRODUCTOS_FIELDS if 'producto' in filename else VENTAS_FIELDS)
                writer.writeheader()
        except Exception:
            pass
    return target

# Rutas resueltas
PRODUCTOS_FILE = _find_csv('productos.csv')
VENTAS_FILE = _find_csv('ventas.csv')

# -------------------------
# Utilidades internas
# -------------------------
def _asegurar_archivo(filepath: Path, fieldnames):
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if not filepath.exists():
            with filepath.open('w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
        return True
    except Exception as e:
        print(f"[negocio] ERROR al asegurar archivo {filepath}: {e}")
        return False

def _leer_csv(filepath: Path, fieldnames):
    if not _asegurar_archivo(filepath, fieldnames):
        return []
    rows = []
    try:
        with filepath.open('r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"[negocio] ERROR al leer {filepath}: {e}")
    return rows

def _escribir_csv(filepath: Path, fieldnames, rows):
    if not _asegurar_archivo(filepath, fieldnames):
        return False
    try:
        with filepath.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                # asegurar cadenas
                safe = {k: ('' if r.get(k) is None else str(r.get(k))) for k in fieldnames}
                writer.writerow(safe)
        return True
    except Exception as e:
        print(f"[negocio] ERROR al escribir {filepath}: {e}")
        return False

# -------------------------
# Productos (CRUD)
# -------------------------
def listar_productos():
    raw = _leer_csv(PRODUCTOS_FILE, PRODUCTOS_FIELDS)
    productos = []
    for r in raw:
        try:
            prod = {
                'id': int(r.get('id', 0)),
                'nombre': r.get('nombre', '') or '',
                'categoria': r.get('categoria', '') or '',
                'precio_unitario': float(r.get('precio_unitario', 0) or 0),
                'stock': int(r.get('stock', 0) or 0),
                'unidad': r.get('unidad', '') or ''
            }
            productos.append(prod)
        except Exception:
            # Ignorar fila corrupta pero no crashear
            continue
    return productos

def _siguiente_id_productos(productos):
    ids = [p['id'] for p in productos if isinstance(p.get('id'), int)]
    return (max(ids) + 1) if ids else 1

def agregar_producto(producto):
    """
    producto: dict con keys: nombre, categoria, precio_unitario, stock, unidad
    Retorna True/False.
    """
    try:
        productos = listar_productos()
        nuevo_id = _siguiente_id_productos(productos)
        p = {
            'id': int(nuevo_id),
            'nombre': str(producto.get('nombre', '')).strip(),
            'categoria': str(producto.get('categoria', '')).strip(),
            'precio_unitario': float(producto.get('precio_unitario', 0) or 0),
            'stock': int(producto.get('stock', 0) or 0),
            'unidad': str(producto.get('unidad', '')).strip()
        }
        productos.append(p)
        # convertir a dicts string para escribir
        rows = [{k: str(v) for k, v in prod.items()} for prod in productos]
        return _escribir_csv(PRODUCTOS_FILE, PRODUCTOS_FIELDS, rows)
    except Exception as e:
        print(f"[negocio] ERROR agregar_producto: {e}")
        return False

def actualizar_producto(id_producto, nuevos_datos):
    try:
        productos = listar_productos()
        found = False
        for prod in productos:
            if prod['id'] == int(id_producto):
                # actualizar sólo campos presentes
                for k in ('nombre', 'categoria', 'precio_unitario', 'stock', 'unidad'):
                    if k in nuevos_datos:
                        if k == 'precio_unitario':
                            prod[k] = float(nuevos_datos[k] or 0)
                        elif k == 'stock':
                            prod[k] = int(nuevos_datos[k] or 0)
                        else:
                            prod[k] = str(nuevos_datos[k])
                found = True
                break
        if not found:
            return False
        rows = [{k: str(v) for k, v in p.items()} for p in productos]
        return _escribir_csv(PRODUCTOS_FILE, PRODUCTOS_FIELDS, rows)
    except Exception as e:
        print(f"[negocio] ERROR actualizar_producto: {e}")
        return False

def eliminar_producto(id_producto):
    try:
        productos = listar_productos()
        productos_filtrados = [p for p in productos if p['id'] != int(id_producto)]
        if len(productos_filtrados) == len(productos):
            return False  # no existía
        rows = [{k: str(v) for k, v in p.items()} for p in productos_filtrados]
        return _escribir_csv(PRODUCTOS_FILE, PRODUCTOS_FIELDS, rows)
    except Exception as e:
        print(f"[negocio] ERROR eliminar_producto: {e}")
        return False

# -------------------------
# Ventas
# -------------------------
def listar_ventas():
    raw = _leer_csv(VENTAS_FILE, VENTAS_FIELDS)
    ventas = []
    for r in raw:
        try:
            v = {
                'id_venta': int(r.get('id_venta', 0)),
                'fecha': r.get('fecha', ''),
                'id_producto': int(r.get('id_producto', 0)),
                'cantidad': int(r.get('cantidad', 0)),
                'precio_unitario_venta': float(r.get('precio_unitario_venta', 0) or 0),
                'forma_pago': r.get('forma_pago', '')
            }
            ventas.append(v)
        except Exception:
            continue
    return ventas

def _siguiente_id_venta(ventas):
    ids = [v['id_venta'] for v in ventas if isinstance(v.get('id_venta'), int)]
    return (max(ids) + 1) if ids else 1

def registrar_venta(venta):
    """
    venta: dict con keys: id_producto(int), cantidad(int), precio_unitario_venta(float), forma_pago(str)
    - agrega registro a ventas.csv y decrementa stock si hay suficiente stock.
    Retorna dict {'ok': bool, 'mensaje': str}
    """
    try:
        productos = listar_productos()
        prod = next((p for p in productos if p['id'] == int(venta.get('id_producto'))), None)
        if prod is None:
            return {'ok': False, 'mensaje': 'Producto no encontrado.'}
        cantidad = int(venta.get('cantidad', 0) or 0)
        if cantidad <= 0:
            return {'ok': False, 'mensaje': 'Cantidad inválida.'}
        if prod['stock'] < cantidad:
            return {'ok': False, 'mensaje': f'Stock insuficiente. Disponible: {prod["stock"]}'}
        ventas = listar_ventas()
        idv = _siguiente_id_venta(ventas)
        fecha = venta.get('fecha') or datetime.now().isoformat(timespec='seconds')
        precio_unitario_venta = float(venta.get('precio_unitario_venta', prod['precio_unitario']))
        nuevo = {
            'id_venta': int(idv),
            'fecha': fecha,
            'id_producto': int(prod['id']),
            'cantidad': int(cantidad),
            'precio_unitario_venta': float(precio_unitario_venta),
            'forma_pago': str(venta.get('forma_pago', ''))
        }
        # escribir venta
        ventas_rows = [{k: str(v) for k, v in vrow.items()} for vrow in ventas] + [{k: str(v) for k, v in nuevo.items()}]
        if not _escribir_csv(VENTAS_FILE, VENTAS_FIELDS, ventas_rows):
            return {'ok': False, 'mensaje': 'Fallo al guardar la venta.'}
        # decrementar stock y guardar productos
        prod['stock'] = prod['stock'] - cantidad
        prod_rows = [{k: str(p[k]) for k in PRODUCTOS_FIELDS} for p in productos]
        _escribir_csv(PRODUCTOS_FILE, PRODUCTOS_FIELDS, prod_rows)
        return {'ok': True, 'mensaje': f'Venta registrada (id {idv}).'}
    except Exception as e:
        print(f"[negocio] ERROR registrar_venta: {e}")
        return {'ok': False, 'mensaje': 'Error interno al registrar venta.'}

def calcular_total_venta(items):
    """
    items: lista de dicts {'id_producto': int, 'cantidad': int, 'precio_unitario': float}
    Retorna float total.
    """
    total = 0.0
    try:
        for it in items:
            c = int(it.get('cantidad', 0) or 0)
            pu = float(it.get('precio_unitario', 0) or 0)
            total += c * pu
    except Exception:
        return 0.0
    return round(total, 2)

def productos_mas_vendidos(top_n=10):
    ventas = listar_ventas()
    conteo = defaultdict(int)
    for v in ventas:
        try:
            conteo[int(v['id_producto'])] += int(v['cantidad'])
        except Exception:
            continue
    orden = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    return orden[:top_n]

def generar_reporte_ventas(fecha_inicio=None, fecha_fin=None):
    """
    Genera resumen simple: ventas totales y cantidad por producto entre fechas (ISO strings or None).
    Retorna dict con resumen.
    """
    ventas = listar_ventas()
    total = 0.0
    conteo = defaultdict(int)
    for v in ventas:
        try:
            fecha = v.get('fecha')
            if fecha_inicio or fecha_fin:
                # comparar como strings ISO si vienen; intentar parseo
                if fecha:
                    try:
                        fdt = datetime.fromisoformat(fecha)
                    except Exception:
                        continue
                    if fecha_inicio:
                        fi = datetime.fromisoformat(fecha_inicio)
                        if fdt < fi:
                            continue
                    if fecha_fin:
                        ff = datetime.fromisoformat(fecha_fin)
                        if fdt > ff:
                            continue
            # acumular
            total += float(v.get('precio_unitario_venta', 0)) * int(v.get('cantidad', 0))
            conteo[int(v.get('id_producto', 0))] += int(v.get('cantidad', 0))
        except Exception:
            continue
    return {'total_ventas': round(total, 2), 'por_producto': dict(conteo)}

# Si el archivo se ejecuta directamente, muestra un pequeño demo en consola sin crash.
if __name__ == '__main__':
    print("Demo rápido de negocio.py")
    print("productos file:", PRODUCTOS_FILE)
    print("ventas file:", VENTAS_FILE)
    # listar
    prods = listar_productos()
    print(f"{len(prods)} productos cargados.")
