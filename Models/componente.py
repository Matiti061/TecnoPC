# models/componente.py

class Componente:
    """
    Clase que representa un componente de PC para venta en la tienda.
    """
    
    def __init__(self, id, nombre, tipo, marca, precio, stock, descripcion=""):
        """
        Constructor de la clase Componente.
        
        Args:
            id (int): Identificador único del componente
            nombre (str): Nombre del componente
            tipo (str): Tipo de componente (RAM, Procesador, etc.)
            marca (str): Marca del componente
            precio (float): Precio de venta
            stock (int): Cantidad disponible en inventario
            descripcion (str, optional): Descripción detallada del componente
        """
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.marca = marca
        self.precio = precio
        self.stock = stock
        self.descripcion = descripcion
    
    def __str__(self):
        """Representación en texto del componente."""
        return f"{self.nombre} - {self.marca} (${self.precio})"
    
    def actualizar_stock(self, cantidad):
        """
        Actualiza el stock del componente.
        
        Args:
            cantidad (int): Cantidad a añadir (positivo) o quitar (negativo) del stock
            
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        nuevo_stock = self.stock + cantidad
        if nuevo_stock >= 0:
            self.stock = nuevo_stock
            return True
        return False
    
    def obtener_info_completa(self):
        """
        Retorna la información completa del componente.
        
        Returns:
            dict: Diccionario con todos los atributos del componente
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "marca": self.marca,
            "precio": self.precio,
            "stock": self.stock,
            "descripcion": self.descripcion
        }


# Subclases específicas para cada tipo de componente

class RAM(Componente):
    def __init__(self, id, nombre, marca, precio, stock, capacidad, velocidad, descripcion=""):
        super().__init__(id, nombre, RAM, marca, precio, stock, descripcion)
        self.capacidad = capacidad  # GB
        self.velocidad = velocidad  # MHz
    
    def obtener_info_completa(self):
        info = super().obtener_info_completa()
        info.update({
            "capacidad": self.capacidad,
            "velocidad": self.velocidad
        })
        return info


class Procesador(Componente):
    def __init__(self, id, nombre, marca, precio, stock, nucleos, velocidad, socket, descripcion=""):
        super().__init__(id, nombre, "Procesador", marca, precio, stock, descripcion)
        self.nucleos = nucleos
        self.velocidad = velocidad  # GHz
        self.socket = socket
    
    def obtener_info_completa(self):
        info = super().obtener_info_completa()
        info.update({
            "nucleos": self.nucleos,
            "velocidad": self.velocidad,
            "socket": self.socket
        })
        return info


class TarjetaGrafica(Componente):
    def __init__(self, id, nombre, marca, precio, stock, vram, tipo_memoria, descripcion=""):
        super().__init__(id, nombre, "Tarjeta Gráfica", marca, precio, stock, descripcion)
        self.vram = vram  # GB
        self.tipo_memoria = tipo_memoria  # GDDR6, etc.
    
    def obtener_info_completa(self):
        info = super().obtener_info_completa()
        info.update({
            "vram": self.vram,
            "tipo_memoria": self.tipo_memoria
        })
        return info


class PlacaMadre(Componente):
    def __init__(self, id, nombre, marca, precio, stock, socket, formato, chipset, descripcion=""):
        super().__init__(id, nombre, "Placa Madre", marca, precio, stock, descripcion)
        self.socket = socket
        self.formato = formato  # ATX, Micro-ATX, etc.
        self.chipset = chipset
    
    def obtener_info_completa(self):
        info = super().obtener_info_completa()
        info.update({
            "socket": self.socket,
            "formato": self.formato,
            "chipset": self.chipset
        })
        return info


class SSD(Componente):
    def __init__(self, id, nombre, marca, precio, stock, capacidad, velocidad_lectura, velocidad_escritura, descripcion=""):
        super().__init__(id, nombre, "SSD", marca, precio, stock, descripcion)
        self.capacidad = capacidad  # GB
        self.velocidad_lectura = velocidad_lectura  # MB/s
        self.velocidad_escritura = velocidad_escritura  # MB/s
    
    def obtener_info_completa(self):
        info = super().obtener_info_completa()
        info.update({
            "capacidad": self.capacidad,
            "velocidad_lectura": self.velocidad_lectura,
            "velocidad_escritura": self.velocidad_escritura
        })
        return info


class Refrigeracion(Componente):
    def __init__(self, id, nombre, marca, precio, stock, tipo, tdp, descripcion=""):
        super().__init__(id, nombre, "Refrigeración", marca, precio, stock, descripcion)
        self.tipo = tipo  # Líquida, Aire, etc.
        self.tdp = tdp  # W (capacidad de disipación)
    
    def obtener_info_completa(self):
        info = super().obtener_info_completa()
        info.update({
            "tipo_refrigeracion": self.tipo,
            "tdp": self.tdp
        })
        return info


class DisipadorCalor(Componente):
    def __init__(self, id, nombre, marca, precio, stock, material, dimensiones, descripcion=""):
        super().__init__(id, nombre, "Disipador de Calor", marca, precio, stock, descripcion)
        self.material = material  # Cobre, Aluminio, etc.
        self.dimensiones = dimensiones  # mm
    
    def obtener_info_completa(self):
        info = super().obtener_info_completa()
        info.update({
            "material": self.material,
            "dimensiones": self.dimensiones
        })
        return info
