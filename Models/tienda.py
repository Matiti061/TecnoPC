# models/tienda.py

class Tienda:
    """
    Clase que representa una tienda física de la cadena.
    """
    
    def __init__(self, id, nombre, direccion, ciudad, telefono, email, horario_apertura="09:00", horario_cierre="18:00"):
        """
        Constructor de la clase Tienda.
        
        Args:
            id (int): Identificador único de la tienda
            nombre (str): Nombre de la tienda
            direccion (str): Dirección física
            ciudad (str): Ciudad donde se ubica
            telefono (str): Teléfono de contacto
            email (str): Email de contacto
            horario_apertura (str, optional): Hora de apertura (formato 24h)
            horario_cierre (str, optional): Hora de cierre (formato 24h)
        """
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.ciudad = ciudad
        self.telefono = telefono
        self.email = email
        self.horario_apertura = horario_apertura
        self.horario_cierre = horario_cierre
        self.inventario = {}  # Dict con componentes disponibles en la tienda
        self.vendedores = []  # Lista de vendedores de la tienda
    
    def __str__(self):
        """Representación en texto de la tienda."""
        return f"{self.nombre} - {self.ciudad}"
    
    def agregar_vendedor(self, vendedor):
        """
        Agrega un vendedor a la tienda.
        
        Args:
            vendedor (Vendedor): Vendedor a agregar
            
        Returns:
            bool: True si se agregó correctamente
        """
        if vendedor not in self.vendedores:
            self.vendedores.append(vendedor)
            vendedor.tienda = self
            return True
        return False
    
    def agregar_componente(self, componente, cantidad=1):
        """
        Agrega un componente al inventario de la tienda.
        
        Args:
            componente (Componente): Componente a agregar
            cantidad (int, optional): Cantidad a agregar. Default es 1.
            
        Returns:
            bool: True si se agregó correctamente
        """
        if componente.id in self.inventario:
            self.inventario[componente.id]["cantidad"] += cantidad
        else:
            self.inventario[componente.id] = {
                "componente": componente,
                "cantidad": cantidad
            }
        return True
    
    def buscar_componente(self, id_componente):
        """
        Busca un componente en el inventario de la tienda.
        
        Args:
            id_componente (int): ID del componente a buscar
            
        Returns:
            dict: Información del componente si existe, None en caso contrario
        """
        if id_componente in self.inventario:
            return self.inventario[id_componente]
        return None
    
    def listar_componentes_por_tipo(self, tipo):
        """
        Lista todos los componentes de un tipo específico.
        
        Args:
            tipo (str): Tipo de componente a buscar (RAM, Procesador, etc.)
            
        Returns:
            list: Lista de componentes del tipo especificado
        """
        componentes = []
        for item in self.inventario.values():
            if item["componente"].tipo == tipo:
                componentes.append({
                    "componente": item["componente"],
                    "cantidad": item["cantidad"]
                })
        return componentes
    
    def obtener_info(self):
        """
        Retorna la información de la tienda.
        
        Returns:
            dict: Diccionario con los datos de la tienda
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "telefono": self.telefono,
            "email": self.email,
            "horario": f"{self.horario_apertura} - {self.horario_cierre}",
            "vendedores": len(self.vendedores),
            "componentes_distintos": len(self.inventario)
        }