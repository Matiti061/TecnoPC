class InventarioController:
    """
    Controlador para gestionar el inventario de las tiendas.
    """
    
    def __init__(self, tiendas):
        """
        Constructor del controlador de inventario.
        
        Args:
            tiendas (list): Lista de tiendas a gestionar
        """
        self.tiendas = tiendas
    
    def buscar_componente_global(self, id_componente):
        """
        Busca un componente en todas las tiendas.
        
        Args:
            id_componente (int): ID del componente a buscar
            
        Returns:
            dict: Información del componente y las tiendas donde está disponible
        """
        resultado = {"componente": None, "disponibilidad": []}
        
        for tienda in self.tiendas:
            componente_en_tienda = tienda.buscar_componente(id_componente)
            if componente_en_tienda:
                resultado["componente"] = componente_en_tienda["componente"]
                resultado["disponibilidad"].append({
                    "tienda": tienda,
                    "cantidad": componente_en_tienda["cantidad"]
                })
        
        return resultado if resultado["componente"] else None
    
    def buscar_por_tipo_y_caracteristicas(self, tipo, **kwargs):
        """
        Busca componentes por tipo y características específicas.
        
        Args:
            tipo (str): Tipo de componente a buscar
            **kwargs: Características específicas para filtrar
            
        Returns:
            list: Lista de componentes que cumplen con los criterios
        """
        resultados = []
        
        for tienda in self.tiendas:
            componentes = tienda.listar_componentes_por_tipo(tipo)
            
            for item in componentes:
                componente = item["componente"]
                info_completa = componente.obtener_info_completa()
                
                # Verificar si cumple con todos los criterios
                cumple_criterios = True
                for key, value in kwargs.items():
                    if key not in info_completa or info_completa[key] != value:
                        cumple_criterios = False
                        break
                
                if cumple_criterios:
                    resultados.append({
                        "componente": componente,
                        "tienda": tienda,
                        "cantidad": item["cantidad"]
                    })
        
        return resultados
    
    def transferir_entre_tiendas(self, id_componente, tienda_origen, tienda_destino, cantidad):
        """
        Transfiere componentes entre tiendas.
        
        Args:
            id_componente (int): ID del componente a transferir
            tienda_origen (Tienda): Tienda de origen
            tienda_destino (Tienda): Tienda de destino
            cantidad (int): Cantidad a transferir
            
        Returns:
            bool: True si la transferencia fue exitosa, False en caso contrario
        """
        # Verificar disponibilidad en tienda de origen
        componente_origen = tienda_origen.buscar_componente(id_componente)
        if not componente_origen or componente_origen["cantidad"] < cantidad:
            return False
        
        # Actualizar inventario en tienda de origen
        componente_origen["cantidad"] -= cantidad
        
        # Actualizar inventario en tienda de destino
        tienda_destino.agregar_componente(componente_origen["componente"], cantidad)
        
        return True