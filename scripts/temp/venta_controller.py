from datetime import datetime

class Venta:
    """
    Clase que representa una venta realizada.
    """
    
    def __init__(self, id, vendedor, tienda, fecha=None):
        """
        Constructor de la clase Venta.
        
        Args:
            id (int): Identificador único de la venta
            vendedor (Vendedor): Vendedor que realizó la venta
            tienda (Tienda): Tienda donde se realizó la venta
            fecha (datetime, optional): Fecha de la venta
        """
        self.id = id
        self.vendedor = vendedor
        self.tienda = tienda
        self.fecha = fecha if fecha else datetime.now()
        self.mes = self.fecha.month
        self.anio = self.fecha.year
        self.items = []  # Lista de componentes vendidos
        self.total = 0
    
    def agregar_item(self, componente, cantidad=1):
        """
        Agrega un componente a la venta.
        
        Args:
            componente (Componente): Componente vendido
            cantidad (int, optional): Cantidad vendida
            
        Returns:
            bool: True si se agregó correctamente
        """
        # Verificar disponibilidad en el inventario
        comp_tienda = self.tienda.buscar_componente(componente.id)
        if not comp_tienda or comp_tienda["cantidad"] < cantidad:
            return False
        
        # Actualizar inventario
        comp_tienda["cantidad"] -= cantidad
        
        # Agregar a la venta
        self.items.append({
            "componente": componente,
            "cantidad": cantidad,
            "precio_unitario": componente.precio,
            "subtotal": componente.precio * cantidad
        })
        
        # Actualizar total
        self.total += componente.precio * cantidad
        
        return True
    
    def finalizar_venta(self):
        """
        Finaliza la venta y registra en el vendedor.
        
        Returns:
            dict: Resumen de la venta
        """
        self.vendedor.registrar_venta(self)
        
        return {
            "id": self.id,
            "fecha": self.fecha,
            "vendedor": str(self.vendedor),
            "tienda": str(self.tienda),
            "items": len(self.items),
            "total": self.total
        }


class VentaController:
    """
    Controlador para gestionar las ventas.
    """
    
    def __init__(self):
        """
        Constructor del controlador de ventas.
        """
        self.ventas = []
        self._ultimo_id = 0
    
    def crear_venta(self, vendedor, tienda):
        """
        Crea una nueva venta.
        
        Args:
            vendedor (Vendedor): Vendedor que realiza la venta
            tienda (Tienda): Tienda donde se realiza la venta
            
        Returns:
            Venta: Objeto venta creado
        """
        self._ultimo_id += 1
        venta = Venta(self._ultimo_id, vendedor, tienda)
        self.ventas.append(venta)
        return venta
    
    def buscar_venta(self, id_venta):
        """
        Busca una venta por su ID.
        
        Args:
            id_venta (int): ID de la venta a buscar
            
        Returns:
            Venta: Venta encontrada, None si no existe
        """
        for venta in self.ventas:
            if venta.id == id_venta:
                return venta
        return None
    
    def ventas_por_vendedor(self, vendedor, mes=None, anio=None):
        """
        Obtiene las ventas realizadas por un vendedor.
        
        Args:
            vendedor (Vendedor): Vendedor a consultar
            mes (int, optional): Mes para filtrar
            anio (int, optional): Año para filtrar
            
        Returns:
            list: Lista de ventas del vendedor
        """
        ventas_vendedor = []
        
        for venta in self.ventas:
            if venta.vendedor.id == vendedor.id:
                if (mes is None or venta.mes == mes) and (anio is None or venta.anio == anio):
                    ventas_vendedor.append(venta)
        
        return ventas_vendedor
    
    def ventas_por_tienda(self, tienda, mes=None, anio=None):
        """
        Obtiene las ventas realizadas en una tienda.
        
        Args:
            tienda (Tienda): Tienda a consultar
            mes (int, optional): Mes para filtrar
            anio (int, optional): Año para filtrar
            
        Returns:
            list: Lista de ventas de la tienda
        """
        ventas_tienda = []
        
        for venta in self.ventas:
            if venta.tienda.id == tienda.id:
                if (mes is None or venta.mes == mes) and (anio is None or venta.anio == anio):
                    ventas_tienda.append(venta)
        
        return ventas_tienda