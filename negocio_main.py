"""
negocio_main.py
Interfaz gráfica mínima y funcional (Tkinter) que usa negocio.py como backend.

Características:
 - Muestra productos en un Treeview.
 - Permite agregar / actualizar / eliminar productos (validando entradas).
 - Permite registrar una venta simple (selección de producto + cantidad) y guarda en ventas.csv,
   actualizando stock.
 - Genera un reporte simple de ventas (total).
 - Maneja errores con mensajes (no crashea).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import negocio  # el backend (asegúrate que negocio.py esté en el mismo directorio)
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema - Inventario y Ventas")
        self.root.geometry("900x620")
        self.build_ui()
        self.refresh_productos()

    def build_ui(self):
        # Tab control
        nb = ttk.Notebook(self.root)
        nb.pack(fill='both', expand=True, padx=8, pady=8)

        # -- Inventario tab
        f_inv = ttk.Frame(nb)
        nb.add(f_inv, text="Inventario")
        # form
        frm = ttk.LabelFrame(f_inv, text="Producto")
        frm.pack(fill='x', padx=8, pady=6)

        labels = ['ID (solo lectura)', 'Nombre', 'Categoría', 'Precio', 'Stock', 'Unidad']
        self.ent_vars = {}
        for i, label in enumerate(labels):
            ttk.Label(frm, text=label+':').grid(row=i, column=0, sticky='e', padx=6, pady=4)
            var = ttk.Entry(frm)
            var.grid(row=i, column=1, sticky='w', padx=6, pady=4)
            if i == 0:
                var.config(state='readonly')
            self.ent_vars[label] = var

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=0, column=2, rowspan=6, padx=12)
        ttk.Button(btn_frame, text="Agregar", command=self.ui_agregar_producto).pack(fill='x', pady=6)
        ttk.Button(btn_frame, text="Actualizar", command=self.ui_actualizar_producto).pack(fill='x', pady=6)
        ttk.Button(btn_frame, text="Eliminar", command=self.ui_eliminar_producto).pack(fill='x', pady=6)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos).pack(fill='x', pady=6)
        ttk.Button(btn_frame, text="Refrescar lista", command=self.refresh_productos).pack(fill='x', pady=6)

        # productos list
        cols = ("id", "nombre", "categoria", "precio_unitario", "stock", "unidad")
        self.tree = ttk.Treeview(f_inv, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=8, pady=6)
        self.tree.bind('<<TreeviewSelect>>', self.on_select_producto)

        # -- Ventas tab
        f_v = ttk.Frame(nb)
        nb.add(f_v, text="Ventas")
        fv = ttk.LabelFrame(f_v, text="Registrar Venta")
        fv.pack(fill='x', padx=8, pady=6)

        ttk.Label(fv, text="Producto:").grid(row=0, column=0, padx=6, pady=4, sticky='e')
        self.combo_producto = ttk.Combobox(fv, values=[], state='readonly', width=40)
        self.combo_producto.grid(row=0, column=1, padx=6, pady=4, sticky='w')
        ttk.Label(fv, text="Cantidad:").grid(row=1, column=0, padx=6, pady=4, sticky='e')
        self.entry_cantidad = ttk.Entry(fv, width=10)
        self.entry_cantidad.grid(row=1, column=1, padx=6, pady=4, sticky='w')
        ttk.Button(fv, text="Registrar Venta", command=self.ui_registrar_venta).grid(row=2, column=0, columnspan=2, pady=8)

        # ventas list
        fv2 = ttk.LabelFrame(f_v, text="Ventas registradas (recientes)")
        fv2.pack(fill='both', expand=True, padx=8, pady=6)
        self.tree_ventas = ttk.Treeview(fv2, columns=("id_venta", "fecha", "producto", "cantidad", "precio", "forma_pago"), show='headings', height=8)
        for h in ("id_venta", "fecha", "producto", "cantidad", "precio", "forma_pago"):
            self.tree_ventas.heading(h, text=h.capitalize())
            self.tree_ventas.column(h, anchor='center')
        self.tree_ventas.pack(fill='both', expand=True)

        ttk.Button(f_v, text="Refrescar ventas", command=self.refresh_ventas).pack(pady=6)

        # -- Reportes tab
        f_r = ttk.Frame(nb)
        nb.add(f_r, text="Reportes")
        ttk.Button(f_r, text="Total ventas y productos más vendidos", command=self.ui_reporte).pack(pady=10)
        self.txt_reporte = tk.Text(f_r, height=20)
        self.txt_reporte.pack(fill='both', expand=True, padx=8, pady=6)

    # ---------- UI handlers ----------
    def limpiar_campos(self):
        for k, ent in self.ent_vars.items():
            state = ent.cget('state')
            ent.config(state='normal')
            ent.delete(0, tk.END)
            if state == 'readonly':
                ent.config(state='readonly')

    def refresh_productos(self):
        try:
            productos = negocio.listar_productos()
            # actualizar tree
            for row in self.tree.get_children():
                self.tree.delete(row)
            for p in productos:
                vals = (p['id'], p['nombre'], p['categoria'], f"{p['precio_unitario']:.2f}", p['stock'], p['unidad'])
                self.tree.insert('', tk.END, values=vals)
            # actualizar combobox
            combo_vals = [f"{p['id']} - {p['nombre']}" for p in productos]
            self.combo_producto['values'] = combo_vals
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar productos: {e}")

    def on_select_producto(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        try:
            vals = self.tree.item(sel[0])['values']
            # llenar campos
            self.ent_vars['ID (solo lectura)'].config(state='normal')
            self.ent_vars['ID (solo lectura)'].delete(0, tk.END)
            self.ent_vars['ID (solo lectura)'].insert(0, str(vals[0]))
            self.ent_vars['ID (solo lectura)'].config(state='readonly')
            self.ent_vars['Nombre'].delete(0, tk.END); self.ent_vars['Nombre'].insert(0, vals[1])
            self.ent_vars['Categoría'].delete(0, tk.END); self.ent_vars['Categoría'].insert(0, vals[2])
            self.ent_vars['Precio'].delete(0, tk.END); self.ent_vars['Precio'].insert(0, vals[3])
            self.ent_vars['Stock'].delete(0, tk.END); self.ent_vars['Stock'].insert(0, vals[4])
            self.ent_vars['Unidad'].delete(0, tk.END); self.ent_vars['Unidad'].insert(0, vals[5])
        except Exception as e:
            print("on_select_producto:", e)

    def ui_agregar_producto(self):
        try:
            nombre = self.ent_vars['Nombre'].get().strip()
            if not nombre:
                messagebox.showwarning("Validación", "Nombre requerido.")
                return
            precio = float(self.ent_vars['Precio'].get() or 0)
            stock = int(self.ent_vars['Stock'].get() or 0)
            cat = self.ent_vars['Categoría'].get().strip()
            unidad = self.ent_vars['Unidad'].get().strip()
            ok = negocio.agregar_producto({
                'nombre': nombre,
                'categoria': cat,
                'precio_unitario': precio,
                'stock': stock,
                'unidad': unidad
            })
            if ok:
                messagebox.showinfo("OK", "Producto agregado.")
                self.limpiar_campos()
                self.refresh_productos()
            else:
                messagebox.showerror("Error", "No se pudo agregar producto.")
        except ValueError:
            messagebox.showwarning("Validación", "Precio o stock en formato inválido.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def ui_actualizar_producto(self):
        try:
            idv = self.ent_vars['ID (solo lectura)'].get()
            if not idv:
                messagebox.showwarning("Validación", "Selecciona un producto primero.")
                return
            nombre = self.ent_vars['Nombre'].get().strip()
            precio = float(self.ent_vars['Precio'].get() or 0)
            stock = int(self.ent_vars['Stock'].get() or 0)
            cat = self.ent_vars['Categoría'].get().strip()
            unidad = self.ent_vars['Unidad'].get().strip()
            ok = negocio.actualizar_producto(int(idv), {
                'nombre': nombre, 'categoria': cat, 'precio_unitario': precio, 'stock': stock, 'unidad': unidad
            })
            if ok:
                messagebox.showinfo("OK", "Producto actualizado.")
                self.refresh_productos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar producto.")
        except ValueError:
            messagebox.showwarning("Validación", "Precio o stock en formato inválido.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def ui_eliminar_producto(self):
        try:
            idv = self.ent_vars['ID (solo lectura)'].get()
            if not idv:
                messagebox.showwarning("Validación", "Selecciona un producto primero.")
                return
            if not messagebox.askyesno("Confirmar", "¿Eliminar producto?"):
                return
            ok = negocio.eliminar_producto(int(idv))
            if ok:
                messagebox.showinfo("OK", "Producto eliminado.")
                self.limpiar_campos()
                self.refresh_productos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar (quizá no existe).")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def ui_registrar_venta(self):
        try:
            sel = self.combo_producto.get()
            if not sel:
                messagebox.showwarning("Validación", "Selecciona un producto.")
                return
            prod_id = int(sel.split('-')[0].strip())
            cantidad = int(self.entry_cantidad.get() or 0)
            if cantidad <= 0:
                messagebox.showwarning("Validación", "Cantidad debe ser mayor que 0.")
                return
            # buscar precio actual
            productos = negocio.listar_productos()
            prod = next((p for p in productos if p['id'] == prod_id), None)
            if prod is None:
                messagebox.showerror("Error", "Producto no encontrado.")
                return
            venta = {
                'id_producto': prod_id,
                'cantidad': cantidad,
                'precio_unitario_venta': prod['precio_unitario'],
                'forma_pago': 'Efectivo'
            }
            res = negocio.registrar_venta(venta)
            if res.get('ok'):
                messagebox.showinfo("OK", res.get('mensaje'))
                self.entry_cantidad.delete(0, tk.END)
                self.refresh_productos()
                self.refresh_ventas()
            else:
                messagebox.showerror("Error", res.get('mensaje'))
        except ValueError:
            messagebox.showwarning("Validación", "Cantidad inválida.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def refresh_ventas(self):
        try:
            ventas = negocio.listar_ventas()
            # join nombre producto
            productos = {p['id']: p['nombre'] for p in negocio.listar_productos()}
            # limpiar
            for r in self.tree_ventas.get_children():
                self.tree_ventas.delete(r)
            # insertar últimas 200 ventas
            for v in sorted(ventas, key=lambda x: x['id_venta'], reverse=True)[:200]:
                nombre = productos.get(v['id_producto'], f"ID {v['id_producto']}")
                vals = (v['id_venta'], v['fecha'], nombre, v['cantidad'], f"{v['precio_unitario_venta']:.2f}", v.get('forma_pago',''))
                self.tree_ventas.insert('', tk.END, values=vals)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar ventas: {e}")

    def ui_reporte(self):
        try:
            rep = negocio.generar_reporte_ventas()
            pm = negocio.productos_mas_vendidos(10)
            texto = f"Total ventas: {rep.get('total_ventas', 0):.2f}\n\nProductos vendidos (top):\n"
            productos = {p['id']: p['nombre'] for p in negocio.listar_productos()}
            for pid, cant in pm:
                texto += f" - {productos.get(pid, f'ID {pid}')}: {cant}\n"
            self.txt_reporte.delete('1.0', tk.END)
            self.txt_reporte.insert('1.0', texto)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")

def main():
    root = tk.Tk()
    app = App(root)
    # cargar ventas inicial y productos
    try:
        app.refresh_ventas()
    except Exception:
        pass
    root.mainloop()

if __name__ == '__main__':
    main()
