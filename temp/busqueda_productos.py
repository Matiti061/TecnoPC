import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
import io
import os

class BusquedaProductos:
    def __init__(self, root, db_path, callback=None):
        """
        Inicializa la ventana de búsqueda de productos
        
        Args:
            root: Ventana principal
            db_path: Ruta a la base de datos SQLite
            callback: Función a llamar cuando se selecciona un producto (para agregar a venta)
        """
        self.root = root
        self.db_path = db_path
        self.callback = callback
        
        # Crear la ventana
        self.window = tk.Toplevel(root)
        self.window.title("Búsqueda de Productos")
        self.window.geometry("900x600")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.window.configure(bg="#ffffff")
        
        # Variables
        self.busqueda_var = tk.StringVar()
        self.filtro_var = tk.StringVar(value="Todos")
        
        self._crear_widgets()
        self._cargar_productos()
    
    def _crear_widgets(self):
        """Crea todos los widgets de la ventana"""
        # Frame principal
        main_frame = tk.Frame(self.window, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame superior (búsqueda y filtros)
        top_frame = tk.Frame(main_frame, bg="#ffffff")
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Etiqueta de búsqueda
        lbl_busqueda = tk.Label(top_frame, text="Buscar:", bg="#ffffff", font=("Arial", 12))
        lbl_busqueda.pack(side=tk.LEFT, padx=(0, 10))
        
        # Entrada de búsqueda
        entry_busqueda = tk.Entry(top_frame, textvariable=self.busqueda_var, font=("Arial", 12), width=30)
        entry_busqueda.pack(side=tk.LEFT, padx=(0, 10))
        entry_busqueda.bind("<KeyRelease>", lambda event: self._filtrar_productos())
        
        # Etiqueta de filtro
        lbl_filtro = tk.Label(top_frame, text="Filtrar por categoría:", bg="#ffffff", font=("Arial", 12))
        lbl_filtro.pack(side=tk.LEFT, padx=(20, 10))
        
        # Combobox de filtro
        self.combo_filtro = ttk.Combobox(top_frame, textvariable=self.filtro_var, state="readonly", width=15, font=("Arial", 12))
        self.combo_filtro['values'] = ["Todos", "RAM", "CPU", "GPU", "Motherboard", "Storage", "Case", "PSU", "Cooling"]
        self.combo_filtro.pack(side=tk.LEFT)
        self.combo_filtro.bind("<<ComboboxSelected>>", lambda event: self._filtrar_productos())
        
        # Frame para el Treeview (lista de productos)
        tree_frame = tk.Frame(main_frame, bg="#ffffff")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Crear el Treeview (tabla)
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, selectmode="browse")
        self.tree['columns'] = ('ID', 'Nombre', 'Categoría', 'Stock', 'Precio', 'Descripción')
        
        # Configurar columnas
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Nombre', width=200, anchor=tk.W)
        self.tree.column('Categoría', width=100, anchor=tk.CENTER)
        self.tree.column('Stock', width=80, anchor=tk.CENTER)
        self.tree.column('Precio', width=100, anchor=tk.CENTER)
        self.tree.column('Descripción', width=350, anchor=tk.W)
        
        # Configurar encabezados
        self.tree.heading('#0', text='')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Categoría', text='Categoría')
        self.tree.heading('Stock', text='Stock')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Descripción', text='Descripción')
        
        # Empacar el Treeview
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Doble clic en un producto
        self.tree.bind("<Double-1>", self._seleccionar_producto)
        
        # Frame inferior (botones)
        bottom_frame = tk.Frame(main_frame, bg="#ffffff")
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botón de seleccionar
        btn_seleccionar = tk.Button(bottom_frame, text="Seleccionar Producto", command=self._seleccionar_producto_boton,
                                  bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
        btn_seleccionar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de detalles
        btn_detalles = tk.Button(bottom_frame, text="Ver Detalles", command=self._ver_detalles,
                              bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
        btn_detalles.pack(side=tk.LEFT)
        
        # Botón de cerrar
        btn_cerrar = tk.Button(bottom_frame, text="Cerrar", command=self.cerrar,
                             bg="#f44336", fg="white", font=("Arial", 12), padx=10, pady=5)
        btn_cerrar.pack(side=tk.RIGHT)
    
    def _cargar_productos(self):
        """Carga todos los productos de la base de datos en el Treeview"""
        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtener los productos
            cursor.execute("SELECT id, nombre, categoria, stock, precio, descripcion FROM productos")
            productos = cursor.fetchall()
            
            # Agregar productos al Treeview
            for producto in productos:
                self.tree.insert('', tk.END, values=producto)
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
    
    def _filtrar_productos(self):
        """Filtra los productos según el texto de búsqueda y la categoría seleccionada"""
        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Construir la consulta SQL según los filtros
            texto_busqueda = self.busqueda_var.get().lower()
            categoria = self.filtro_var.get()
            
            if categoria == "Todos":
                if texto_busqueda:
                    cursor.execute("""
                        SELECT id, nombre, categoria, stock, precio, descripcion 
                        FROM productos 
                        WHERE LOWER(nombre) LIKE ? OR LOWER(descripcion) LIKE ?
                    """, (f'%{texto_busqueda}%', f'%{texto_busqueda}%'))
                else:
                    cursor.execute("SELECT id, nombre, categoria, stock, precio, descripcion FROM productos")
            else:
                if texto_busqueda:
                    cursor.execute("""
                        SELECT id, nombre, categoria, stock, precio, descripcion 
                        FROM productos 
                        WHERE categoria = ? AND (LOWER(nombre) LIKE ? OR LOWER(descripcion) LIKE ?)
                    """, (categoria, f'%{texto_busqueda}%', f'%{texto_busqueda}%'))
                else:
                    cursor.execute("""
                        SELECT id, nombre, categoria, stock, precio, descripcion 
                        FROM productos 
                        WHERE categoria = ?
                    """, (categoria,))
            
            productos = cursor.fetchall()
            
            # Agregar productos filtrados al Treeview
            for producto in productos:
                self.tree.insert('', tk.END, values=producto)
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al filtrar productos: {e}")
    
    def _seleccionar_producto_boton(self, event=None):
        """Maneja el evento de seleccionar un producto con el botón"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor selecciona un producto")
            return
        
        # Obtener datos del producto seleccionado
        valores = self.tree.item(selected[0], 'values')
        
        # Si hay una función de callback, enviar el producto seleccionado
        if self.callback:
            producto_id = valores[0]
            self.callback(producto_id)
            self.cerrar()
    
    def _seleccionar_producto(self, event=None):
        """Maneja el evento de doble clic en un producto"""
        self._seleccionar_producto_boton()
    
    def _ver_detalles(self):
        """Muestra los detalles completos de un producto, incluyendo su imagen"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor selecciona un producto")
            return
        
        # Obtener ID del producto seleccionado
        valores = self.tree.item(selected[0], 'values')
        producto_id = valores[0]
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtener todos los datos del producto, incluyendo la imagen
            cursor.execute("""
                SELECT nombre, categoria, stock, precio, descripcion, imagen 
                FROM productos 
                WHERE id = ?
            """, (producto_id,))
            
            producto = cursor.fetchone()
            conn.close()
            
            if producto:
                # Crear ventana de detalles
                detalle_window = tk.Toplevel(self.window)
                detalle_window.title(f"Detalles de {producto[0]}")
                detalle_window.geometry("600x500")
                detalle_window.resizable(False, False)
                detalle_window.configure(bg="#ffffff")
                
                # Frame principal
                main_frame = tk.Frame(detalle_window, bg="#ffffff")
                main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                
                # Lado izquierdo (imagen)
                left_frame = tk.Frame(main_frame, bg="#ffffff", width=200)
                left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
                
                # Mostrar imagen del producto si existe
                if producto[5]:
                    try:
                        imagen_data = producto[5]
                        imagen = Image.open(io.BytesIO(imagen_data))
                        imagen = imagen.resize((200, 200), Image.LANCZOS)
                        imagen_tk = ImageTk.PhotoImage(imagen)
                        
                        lbl_imagen = tk.Label(left_frame, image=imagen_tk, bg="#ffffff")
                        lbl_imagen.image = imagen_tk  # Mantener referencia
                        lbl_imagen.pack(padx=10, pady=10)
                    except Exception as e:
                        lbl_no_imagen = tk.Label(left_frame, text="No se pudo cargar la imagen", bg="#ffffff", fg="red")
                        lbl_no_imagen.pack(padx=10, pady=10)
                else:
                    lbl_no_imagen = tk.Label(left_frame, text="Sin imagen\ndisponible", bg="#ffffff", fg="#999999", 
                                           font=("Arial", 12), height=10, width=20)
                    lbl_no_imagen.pack(padx=10, pady=10)
                
                # Lado derecho (información)
                right_frame = tk.Frame(main_frame, bg="#ffffff")
                right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
                
                # Información del producto
                tk.Label(right_frame, text="Nombre:", bg="#ffffff", font=("Arial", 12, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 5))
                tk.Label(right_frame, text=producto[0], bg="#ffffff", font=("Arial", 12), anchor="w").pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(right_frame, text="Categoría:", bg="#ffffff", font=("Arial", 12, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 5))
                tk.Label(right_frame, text=producto[1], bg="#ffffff", font=("Arial", 12), anchor="w").pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(right_frame, text="Stock:", bg="#ffffff", font=("Arial", 12, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 5))
                tk.Label(right_frame, text=str(producto[2]), bg="#ffffff", font=("Arial", 12), anchor="w").pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(right_frame, text="Precio:", bg="#ffffff", font=("Arial", 12, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 5))
                tk.Label(right_frame, text=f"${producto[3]:,.2f}", bg="#ffffff", font=("Arial", 12), anchor="w").pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(right_frame, text="Descripción:", bg="#ffffff", font=("Arial", 12, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 5))
                
                # Text widget para descripción con scroll
                desc_frame = tk.Frame(right_frame, bg="#ffffff")
                desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
                
                desc_scrollbar = tk.Scrollbar(desc_frame)
                desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                desc_text = tk.Text(desc_frame, wrap=tk.WORD, height=5, font=("Arial", 12), 
                                   yscrollcommand=desc_scrollbar.set, bg="#f9f9f9", bd=1)
                desc_text.insert(tk.END, producto[4])
                desc_text.config(state=tk.DISABLED)
                desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                desc_scrollbar.config(command=desc_text.yview)
                
                # Botón de cerrar
                tk.Button(right_frame, text="Cerrar", command=detalle_window.destroy,
                        bg="#f44336", fg="white", font=("Arial", 12), padx=20, pady=5).pack(pady=(10, 0))
                
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar los detalles del producto: {e}")
    
    def cerrar(self):
        """Cierra la ventana"""
        self.window.destroy()

# Función para probar la clase (solo si se ejecuta este archivo directamente)
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    
    # Ruta a la base de datos (ajustar según sea necesario)
    db_path = "db/tiendapc.db"
    
    # Verificar si la base de datos existe
    if not os.path.exists(db_path):
        messagebox.showerror("Error", f"Base de datos no encontrada en {db_path}")
        root.destroy()
        exit()
    
    app = BusquedaProductos(root, db_path)
    root.mainloop()