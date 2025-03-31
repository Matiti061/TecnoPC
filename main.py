import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Models.componente import Componente
from Models.vendedor import Vendedor
from Models.tienda import Tienda
from Controllers.inventario_controller import InventarioController
from Controllers.venta_controller import VentaController
from Views.interfaz_tienda import InterfazTienda

from PyQt6.QtWidgets import QApplication

def crear_datos_ejemplo():
    """
    Crea datos de ejemplo para la aplicación.
    """
    # Crear tiendas
    tienda_bosquemar = Tienda(1, "Tienda Bosquemar", "Av. Bosquemar 123", "Viña del Mar", "32-2123456", "bosquemar@tecnopc.cl")
    tienda_mirasol = Tienda(2, "Tienda Mirasol", "Calle Mirasol 456", "Santiago", "2-2987654", "mirasol@tecnopc.cl")
    tienda_vallevolcanes = Tienda(3, "Tienda ValleVolcanes", "Av. ValleVolcanes 789", "Temuco", "45-2654321", "vallevolcanes@tecnopc.cl")
    
    # Crear componentes
    ram = Componente(1, "Kingston Fury 16GB", "RAM", "Kingston", "DDR4 3200MHz", 75.99)
    procesador = Componente(2, "Intel Core i5-12400F", "Procesador", "Intel", "6 núcleos, 12 hilos", 199.99)
    ssd = Componente(3, "Samsung 970 EVO Plus 1TB", "SSD", "Samsung", "NVMe M.2", 129.99)
    
    # Agregar componentes al inventario de las tiendas
    tienda_bosquemar.agregar_componente(ram, 10)
    tienda_bosquemar.agregar_componente(procesador, 5)
    tienda_mirasol.agregar_componente(ssd, 8)
    tienda_vallevolcanes.agregar_componente(ram, 15)
    tienda_vallevolcanes.agregar_componente(ssd, 10)
    
    # Crear vendedores
    vendedor1 = Vendedor(1, "Juan", "Pérez", "juan.perez@tecnopc.cl", "987654321", tienda_bosquemar, "2023-01-15")
    vendedor2 = Vendedor(2, "María", "Gómez", "maria.gomez@tecnopc.cl", "987654322", tienda_mirasol, "2023-02-20")
    vendedor3 = Vendedor(3, "Carlos", "López", "carlos.lopez@tecnopc.cl", "987654323", tienda_vallevolcanes, "2023-03-10")
    
    # Lista de tiendas y vendedores
    tiendas = [tienda_bosquemar, tienda_mirasol, tienda_vallevolcanes]
    vendedores = [vendedor1, vendedor2, vendedor3]
    
    return tiendas, vendedores


def main():
    """
    Función principal que inicia la aplicación.
    """
    app = QApplication(sys.argv)
    
    # Crear datos de ejemplo
    tiendas, vendedores = crear_datos_ejemplo()
    
    # Crear controladores
    controlador_inventario = InventarioController(tiendas)
    controlador_ventas = VentaController()
    
    # Crear y mostrar la interfaz
    ventana = InterfazTienda(controlador_inventario, controlador_ventas, tiendas, vendedores)
    ventana.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
