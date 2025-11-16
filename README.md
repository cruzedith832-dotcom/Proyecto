READ ME:

Para ejecutar este proyecto, solo necesitas tener instalado Python 3.x.

1. Descargar el repositorio.
2. Preparar la carpeta data/: Asegúrate de que la carpeta data/ contenga los archivos CSV. El módulo negocio.py intentará crear estos archivos con sus encabezados si no existen.

productos.csv (contiene el inventario inicial).

ventas.csv (vacío al inicio o con registros de prueba).

3. Busca el sig. archivo: negocio_main.py y ábrelo

F L U J O   F E L I Z

El sistema soporta las siguientes operaciones básicas:

Inventario:

Ver Productos: Se listan todos los productos cargados.

Agregar Producto: Llenar los campos y hacer clic en "Agregar" (asigna ID automáticamente).

Editar/Eliminar: Seleccionar una fila del Treeview, modificar los campos y hacer clic en "Actualizar" o "Eliminar".

Ventas:

Registrar Venta: Seleccionar un producto del Combobox, ingresar la cantidad.

Reducción de Stock: Al hacer clic en "Registrar Venta", el sistema verifica el stock y, si es suficiente, guarda la venta en ventas.csv y reduce el stock en productos.csv.


Reportes (Pestaña "Reportes"):

Consultar: Al hacer clic en el botón, el sistema calcula el total de ventas y el ranking de los productos más vendidos a partir de ventas.csv.