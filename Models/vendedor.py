
class Vendedor:
    """
    Clase que representa a un vendedor de la tienda.
    """
    
    def __init__(self, id, nombre, apellido, email, telefono, tienda, fecha_contratacion=None):
        """
        Constructor de la clase Vendedor.
        
        Args:
            id (int): Identificador único del vendedor
            nombre (str): Nombre del vendedor
            apellido (str): Apellido del vendedor
            email (str): Email del vendedor
            telefono (str): Teléfono de contacto
            tienda (Tienda): Tienda a la que pertenece el vendedor
            fecha_contratacion (str, optional): Fecha de contratación
        """
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.tienda = tienda
        self.fecha_contratacion = fecha_contratacion
        self.ventas = []
    
    def __str__(self):
        """Representación en texto del vendedor."""
        return f"{self.nombre} {self.apellido} - Tienda: {self.tienda.nombre}"
    
    def registrar_venta(self, venta):
        """
        Registra una nueva venta realizada por el vendedor.
        
        Args:
            venta (Venta): Objeto venta a registrar
            
        Returns:
            bool: True si se registró correctamente
        """
        self.ventas.append(venta)
        return True
    
    def calcular_comisiones(self, mes, anio):
        """
        Calcula las comisiones del vendedor en un período específico.
        
        Args:
            mes (int): Mes para calcular comisiones
            anio (int): Año para calcular comisiones
            
        Returns:
            float: Total de comisiones del período
        """
        total_ventas = 0
        for venta in self.ventas:
            if venta.mes == mes and venta.anio == anio:
                total_ventas += venta.total
        
        # Comisión del 5% sobre el total de ventas
        return total_ventas * 0.05
    
    def obtener_info(self):
        """
        Retorna la información del vendedor.
        
        Returns:
            dict: Diccionario con los datos del vendedor
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "tienda": self.tienda.nombre if self.tienda else None,
            "fecha_contratacion": self.fecha_contratacion
        }