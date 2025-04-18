import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk
import io
import os

class AgregarProducto:
    def __init__(self, root, db_path, callback=None):
        """
        Inicializa la ventana para agregar un nuevo producto
        
        Args:
            root: Ventana principal
            db_path: Ruta a la base de datos SQLite
            callback: Función a llamar después de agregar un producto para actualizar la vista
        """
        self.root = root
        self.db_path = db_path
        self.callback = callback
        
        # Crear la ventana
        self.window = tk.Toplevel(root)
        self.window.title("Agregar Nuevo Producto")
        self.window.geometry("800x700")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.window.configure(bg="#ffffff")
        
        # Variables
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar(value="RAM")
        self.stock_var = tk.IntVar(value=1)
        self.precio_var = tk.DoubleVar(value=0.0)
        self.descripcion_text = None  # Se creará como Text widget
        self.imagen_path = None
        self.imagen_data = None
        self.imagen_label = None
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea todos los widgets de la ventana"""
        # Frame principal con scroll
        main_canvas = tk.Canvas(self.window, bg="#ffffff")
        main_scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=main_canvas.yview)
        main_scrollable_frame = tk.Frame(main_canvas, bg="#ffffff")
        
        main_scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=main_scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")
        
        # Contenedor para los campos del formulario
        form_frame = tk.Frame(main_scrollable_frame, bg="#ffffff", padx=40, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo_label = tk.Label(form_frame, text="AGREGAR NUEVO PRODUCTO", bg="#ffffff", fg="#333333", 
                              font=("Arial", 16, "bold"))
        titulo_label.pack(pady=(0, 20))
        
        # Campos del formulario
        # Campo Nombre
        self._crear_campo_formulario(form_frame, "Nombre del producto:", self.nombre_var)
        
        # Campo Categoría
        categoria_frame = tk.Frame(form_frame, bg="#ffffff")
        categoria_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(categoria_frame, text="Categoría:", bg="#ffffff", font=("Arial", 12)).pack(anchor=tk.W)
        
        categorias = ["RAM", "CPU", "GPU", "Motherboard", "Storage", "Case", "PSU", "Cooling"]
        categoria_combo = ttk.Combobox(categoria_frame, textvariable=self.categoria_var, values=categorias, state="readonly", 
                                    font=("Arial", 12), width=15)
        categoria_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Campo Stock
        stock_frame = tk.Frame(form_frame, bg="#ffffff")
        stock_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(stock_frame, text="Stock:", bg="#ffffff", font=("Arial", 12)).pack(anchor=tk.W)
        
        stock_spin = tk.Spinbox(stock_frame, from_=0, to=1000, textvariable=self.stock_var, font=("Arial", 12), width=10)
        stock_spin.pack(anchor=tk.W, pady=(5, 0))
        
        # Campo Precio
        precio_frame = tk.Frame(form_frame, bg="#ffffff")
        precio_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(precio_frame, text="Precio ($):", bg="#ffffff", font=("Arial", 12)).pack(anchor=tk.W)
        
        precio_entry = tk.Entry(precio_frame, textvariable=self.precio_var, font=("Arial", 12), width=15)
        precio_entry.pack(anchor=tk.W, pady=(5, 0))
        
        # Campo Descripción
        desc_frame = tk.Frame(form_frame, bg="#ffffff")
        desc_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(desc_frame, text="Descripción:", bg="#ffffff", font=("Arial", 12)).pack(anchor=tk.W)
        
        self.descripcion_text = tk.Text(desc_frame, height=5, width=50, font=("Arial", 12), wrap=tk.WORD)
        self.descripcion_text.pack(fill=tk.X, pady=(5, 0))
        
        # Campo Imagen
        imagen_frame = tk.Frame(form_frame, bg="#ffffff")
        imagen_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(imagen_frame, text="Imagen del producto:", bg="#ffffff", font=("Arial", 12)).pack(anchor=tk.W)
        
        imagen_botones_frame = tk.Frame(imagen_frame, bg="#ffffff")
        imagen_botones_frame.pack(fill=tk.X, pady=(5, 0))
        
        btn_seleccionar_imagen = tk.Button(imagen_botones_frame, text="Seleccionar imagen", command=self._seleccionar_imagen,
                                        bg="#2196F3", fg="white", font=("Arial", 11), padx=10, pady=5)
        btn_seleccionar_imagen.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_eliminar_imagen = tk.Button(imagen_botones_frame, text="Eliminar imagen", command=self._eliminar_imagen,
                                     bg="#f44336", fg="white", font=("Arial", 11), padx=10, pady=5)
        btn_eliminar_imagen.pack(side=tk.LEFT)
        
        # Preview de la imagen
        self.imagen_frame = tk.Frame(form_frame, bg="#ffffff", height=200, width=200, bd=1, relief=tk.SOLID)
        self.imagen_frame.pack(pady=10)
        self.imagen_frame.pack_propagate(False)  # Mantener el tamaño del frame
        
        self.imagen_label = tk.Label(self.imagen_frame, bg="#f9f9f9", text="Sin imagen seleccionada")
        self.imagen_label.pack(fill=tk.BOTH, expand=True)
        
        # Botones finales
        botones_frame = tk.Frame(form_frame, bg="#ffffff")
        botones_frame.pack(fill=tk.X, pady=(20, 0))
        
        btn_guardar = tk.Button(botones_frame, text="Guardar Producto", command=self._guardar_producto,
                             bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        btn_guardar.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_cancelar = tk.Button(botones_frame, text="Cancelar", command=self.cerrar,
                              bg="#f44336", fg="white", font=("Arial", 12), padx=20, pady=10)
        btn_cancelar.pack(side=tk.LEFT)
    
    def _crear_campo_formulario(self, parent, label_text, variable):
        """Crea un campo de formulario estándar con label y entry"""
        frame = tk.Frame(parent, bg="#ffffff")
        frame.pack(fill=tk.X, pady=10)
        
        tk.Label(frame, text=label_text, bg="#ffffff", font=("Arial", 12)).pack(anchor=tk.W)
        
        entry = tk.Entry(frame, textvariable=variable, font=("Arial", 12), width=50)
        entry.pack(fill=tk.X, pady=(5, 0))
    
    def _seleccionar_imagen(self):
        """Abre un diálogo para seleccionar una imagen"""
        try:
            filetypes = [
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Todos los archivos", "*.*")
            ]
            imagen_path = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=filetypes)
            
            if imagen_path:
                self.imagen_path = imagen_path
                # Cargar y mostrar la imagen
                imagen = Image.open(imagen_path)
                
                # Redimensionar manteniendo la relación de aspecto
                imagen.thumbnail((200, 200))
                
                # Convertir a formato Tkinter
                imagen_tk = ImageTk.PhotoImage(imagen)
                
                # Guardar la imagen en formato binario para la base de datos
                with open(imagen_path, "rb") as f:
                    self.imagen_data = f.read()
                
                # Actualizar la etiqueta con la imagen
                if self.imagen_label:
                    self.imagen_label.config(image=imagen_tk, text="")
                    self.imagen_label.image = imagen_tk  # Mantener referencia
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {e}")
    
    def _eliminar_imagen(self):
        """Elimina la imagen seleccionada"""
        self.imagen_path = None
        self.imagen_data = None
        
        # Restablecer la etiqueta
        if self.imagen_label:
            self.imagen_label.config(image="", text="Sin imagen seleccionada")
            if hasattr(self.imagen_label, 'image'):
                del self.imagen_label.image
    
    def _guardar_producto(self):
        """Guarda el nuevo producto en la base de datos"""
        # Validar campos obligatorios
        nombre = self.nombre_var.get().strip()
        categoria = self.categoria_var.get()
        stock = self.stock_var.get()
        precio = self.precio_var.get()
        descripcion = self.descripcion_text.get("1.0", tk.END).strip()
        
        if not nombre:
            messagebox.showwarning("Aviso", "El nombre del producto es obligatorio")
            return
        
        if precio <= 0:
            messagebox.showwarning("Aviso", "El precio debe ser mayor que cero")
            return
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insertar el nuevo producto
            cursor.execute("""
                INSERT INTO productos (nombre, categoria, stock, precio, descripcion, imagen)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, categoria, stock, precio, descripcion, self.imagen_data))
            
            # Guardar cambios
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            
            # Llamar al callback si existe
            if self.callback:
                self.callback()
            
            # Cerrar la ventana
            self.cerrar()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al guardar el producto: {e}")
    
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
    
    app = AgregarProducto(root, db_path)
    root.mainloop()