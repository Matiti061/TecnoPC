# utils/database.py

import sqlite3
import json
import os
from datetime import datetime

class Database:
    """
    Clase para gestionar la conexión y operaciones con la base de datos.
    """
    
    def __init__(self, db_file="tienda_electronica.db"):
        """
        Constructor de la clase Database.
        
        Args:
            db_file (str, optional): Ruta al archivo de base de datos
        """
        self.db_file = db_file
        self.connection = None
        self.initialize_db()
    
    def get_connection(self):
        """
        Obtiene una conexión a la base de datos.
        
        Returns:
            sqlite3.Connection: Conexión a la base de datos
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close_connection(self):
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_db(self):
        """Inicializa la estructura de la base de datos si no existe."""
        if not os.path.exists(self.db_file):
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Crear tablas
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS tiendas (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                ciudad TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL,
                horario_apertura TEXT DEFAULT '09:00',
                horario_cierre TEXT DEFAULT '18:00'
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendedores (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT NOT NULL,
                tienda_id INTEGER NOT NULL,
                fecha_contratacion TEXT,
                FOREIGN KEY (tienda_id) REFERENCES tiendas(id)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS componentes (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                marca TEXT NOT NULL,
                precio REAL NOT NULL,
                descripcion TEXT,
                propiedades TEXT
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventario (
                id INTEGER PRIMARY KEY,
                tienda_id INTEGER NOT NULL,
                componente_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (tienda_id) REFERENCES tiendas(id),
                FOREIGN KEY (componente_id) REFERENCES componentes(id),
                UNIQUE(tienda_id, componente_id)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY,
                vendedor_id INTEGER NOT NULL,
                tienda_id INTEGER NOT NULL,
                cliente TEXT,
                fecha TEXT NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (vendedor_id) REFERENCES vendedores(id),
                FOREIGN KEY (tienda_id) REFERENCES tiendas(id)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS items_venta (
                id INTEGER PRIMARY KEY,
                venta_id INTEGER NOT NULL,
                componente_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas(id),
                FOREIGN KEY (componente_id) REFERENCES componentes(id)
            )
            ''')
            
            conn.commit()
    
    # Métodos para tiendas
    
    def guardar_tienda(self, tienda):
        """
        Guarda una tienda en la base de datos.
        
        Args:
            tienda (Tienda): Objeto tienda a guardar
            
        Returns:
            int: ID de la tienda guardada
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO tiendas (id, nombre, direccion, ciudad, telefono, email, horario_apertura, horario_cierre)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tienda.id,
            tienda.nombre,
            tienda.direccion,
            tienda.ciudad,
            tienda.telefono,
            tienda.email,
            tienda.horario_apertura,
            tienda.horario_cierre
        ))
        
        conn.commit()
        return cursor.lastrowid if tienda.id is None else tienda.id
    
    def obtener_tiendas(self):
        """
        Obtiene todas las tiendas de la base de datos.
        
        Returns:
            list: Lista de diccionarios con la información de las tiendas
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tiendas')
        return [dict(row) for row in cursor.fetchall()]
    
    def obtener_tienda(self, tienda_id):
        """
        Obtiene una tienda por su ID.
        
        Args:
            tienda_id (int): ID de la tienda a buscar
            
        Returns:
            dict: Información de la tienda, None si no existe
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tiendas WHERE id = ?', (tienda_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # Métodos para vendedores
    
    def guardar_vendedor(self, vendedor):
        """
        Guarda un vendedor en la base de datos.
        
        Args:
            vendedor (Vendedor): Objeto vendedor a guardar
            
        Returns:
            int: ID del vendedor guardado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO vendedores (id, nombre, apellido, email, telefono, tienda_id, fecha_contratacion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            vendedor.id,
            vendedor.nombre,
            vendedor.apellido,
            vendedor.email,
            vendedor.telefono,
            vendedor.tienda.id if vendedor.tienda else None,
            vendedor.fecha_contratacion
        ))
        
        conn.commit()
        return cursor.lastrowid if vendedor.id is None else vendedor.id
    
    def obtener_vendedores(self, tienda_id=None):
        """
        Obtiene vendedores de la base de datos, opcionalmente filtrados por tienda.
        
        Args:
            tienda_id (int, optional): ID de la tienda para filtrar
            
        Returns:
            list: Lista de diccionarios con la información de los vendedores
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if tienda_id:
            cursor.execute('SELECT * FROM vendedores WHERE tienda_id = ?', (tienda_id,))
        else:
            cursor.execute('SELECT * FROM vendedores')
        
        return [dict(row) for row in cursor.fetchall()]
    
    def obtener_vendedor(self, vendedor_id):
        """
        Obtiene un vendedor por su ID.
        
        Args:
            vendedor_id (int): ID del vendedor a buscar
            
        Returns:
            dict: Información del vendedor, None si no existe
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM vendedores WHERE id = ?', (vendedor_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # Métodos para componentes e inventario
    
    def guardar_componente(self, componente):
        """
        Guarda un componente en la base de datos.
        
        Args:
            componente (Componente): Objeto componente a guardar
            
        Returns:
            int: ID del componente guardado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Convertir propiedades específicas a JSON
        info = componente.obtener_info_completa()
        propiedades = {k: v for k, v in info.items() 
                      if k not in ['id', 'nombre', 'tipo', 'marca', 'precio', 'stock', 'descripcion']}
        
        cursor.execute('''
        INSERT OR REPLACE INTO componentes (id, nombre, tipo, marca, precio, descripcion, propiedades)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            componente.id,
            componente.nombre,
            componente.tipo,
            componente.marca,
            componente.precio,
            componente.descripcion,
            json.dumps(propiedades)
        ))
        
        conn.commit()
        return cursor.lastrowid if componente.id is None else componente.id
    
    def actualizar_inventario(self, tienda_id, componente_id, cantidad):
        """
        Actualiza la cantidad de un componente en el inventario de una tienda.
        
        Args:
            tienda_id (int): ID de la tienda
            componente_id (int): ID del componente
            cantidad (int): Nueva cantidad
            
        Returns:
            bool: True si se actualizó correctamente
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO inventario (tienda_id, componente_id, cantidad)
        VALUES (?, ?, ?)
        ''', (tienda_id, componente_id, cantidad))
        
        conn.commit()
        return True
    
    def obtener_inventario_tienda(self, tienda_id):
        """
        Obtiene el inventario completo de una tienda.
        
        Args:
            tienda_id (int): ID de la tienda
            
        Returns:
            list: Lista de diccionarios con la información del inventario
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT i.id, i.tienda_id, i.componente_id, i.cantidad, 
               c.nombre, c.tipo, c.marca, c.precio, c.descripcion, c.propiedades
        FROM inventario i
        JOIN componentes c ON i.componente_id = c.id
        WHERE i.tienda_id = ?
        ''', (tienda_id,))
        
        resultados = []
        for row in cursor.fetchall():
            item = dict(row)
            if item['propiedades']:
                try:
                    item['propiedades'] = json.loads(item['propiedades'])
                except:
                    item['propiedades'] = {}
            resultados.append(item)
            
        return resultados
    
    def obtener_stock_componente(self, tienda_id, componente_id):
        """
        Obtiene la cantidad disponible de un componente en una tienda.
        
        Args:
            tienda_id (int): ID de la tienda
            componente_id (int): ID del componente
            
        Returns:
            int: Cantidad disponible, 0 si no hay stock
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT cantidad FROM inventario 
        WHERE tienda_id = ? AND componente_id = ?
        ''', (tienda_id, componente_id))
        
        row = cursor.fetchone()
        return row['cantidad'] if row else 0
    
    def obtener_componentes(self, tipo=None):
        """
        Obtiene todos los componentes, opcionalmente filtrados por tipo.
        
        Args:
            tipo (str, optional): Tipo de componente a filtrar
            
        Returns:
            list: Lista de diccionarios con la información de los componentes
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if tipo:
            cursor.execute('SELECT * FROM componentes WHERE tipo = ?', (tipo,))
        else:
            cursor.execute('SELECT * FROM componentes')
        
        resultados = []
        for row in cursor.fetchall():
            item = dict(row)
            if item['propiedades']:
                try:
                    item['propiedades'] = json.loads(item['propiedades'])
                except:
                    item['propiedades'] = {}
            resultados.append(item)
            
        return resultados
    
    def obtener_componente(self, componente_id):
        """
        Obtiene un componente por su ID.
        
        Args:
            componente_id (int): ID del componente a buscar
            
        Returns:
            dict: Información del componente, None si no existe
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM componentes WHERE id = ?', (componente_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
            
        item = dict(row)
        if item['propiedades']:
            try:
                item['propiedades'] = json.loads(item['propiedades'])
            except:
                item['propiedades'] = {}
                
        return item
    
    # Métodos para ventas
    
    def registrar_venta(self, venta, items_venta):
        """
        Registra una venta y sus ítems asociados.
        
        Args:
            venta (dict): Información de la venta (vendedor_id, tienda_id, cliente, fecha, total)
            items_venta (list): Lista de ítems de la venta (componente_id, cantidad, precio_unitario, subtotal)
            
        Returns:
            int: ID de la venta registrada
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Insertar venta
        cursor.execute('''
        INSERT INTO ventas (vendedor_id, tienda_id, cliente, fecha, total)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            venta['vendedor_id'],
            venta['tienda_id'],
            venta['cliente'],
            venta.get('fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            venta['total']
        ))
        
        venta_id = cursor.lastrowid
        
        # Insertar items de venta
        for item in items_venta:
            cursor.execute('''
            INSERT INTO items_venta (venta_id, componente_id, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                venta_id,
                item['componente_id'],
                item['cantidad'],
                item['precio_unitario'],
                item['subtotal']
            ))
            
            # Actualizar inventario (restar la cantidad vendida)
            self.actualizar_stock_tras_venta(venta['tienda_id'], item['componente_id'], item['cantidad'])
        
        conn.commit()
        return venta_id
    
    def actualizar_stock_tras_venta(self, tienda_id, componente_id, cantidad_vendida):
        """
        Actualiza el stock después de una venta.
        
        Args:
            tienda_id (int): ID de la tienda
            componente_id (int): ID del componente
            cantidad_vendida (int): Cantidad vendida
            
        Returns:
            bool: True si se actualizó correctamente
        """
        stock_actual = self.obtener_stock_componente(tienda_id, componente_id)
        nuevo_stock = max(0, stock_actual - cantidad_vendida)
        return self.actualizar_inventario(tienda_id, componente_id, nuevo_stock)
    
    def obtener_ventas(self, tienda_id=None, fecha_inicio=None, fecha_fin=None):
        """
        Obtiene las ventas realizadas, con posibilidad de filtrar por tienda y fechas.
        
        Args:
            tienda_id (int, optional): ID de la tienda
            fecha_inicio (str, optional): Fecha de inicio en formato 'YYYY-MM-DD'
            fecha_fin (str, optional): Fecha de fin en formato 'YYYY-MM-DD'
            
        Returns:
            list: Lista de diccionarios con la información de las ventas
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM ventas WHERE 1=1'
        params = []
        
        if tienda_id:
            query += ' AND tienda_id = ?'
            params.append(tienda_id)
            
        if fecha_inicio:
            query += ' AND fecha >= ?'
            params.append(fecha_inicio)
            
        if fecha_fin:
            query += ' AND fecha <= ?'
            params.append(fecha_fin)
            
        query += ' ORDER BY fecha DESC'
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def obtener_detalles_venta(self, venta_id):
        """
        Obtiene los detalles de una venta específica.
        
        Args:
            venta_id (int): ID de la venta
            
        Returns:
            dict: Diccionario con la información de la venta y sus ítems
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Obtener información de la venta
        cursor.execute('''
        SELECT v.*, vd.nombre || ' ' || vd.apellido as vendedor_nombre,
               t.nombre as tienda_nombre
        FROM ventas v
        JOIN vendedores vd ON v.vendedor_id = vd.id
        JOIN tiendas t ON v.tienda_id = t.id
        WHERE v.id = ?
        ''', (venta_id,))
        
        venta = cursor.fetchone()
        if not venta:
            return None
            
        resultado = dict(venta)
        
        # Obtener ítems de la venta
        cursor.execute('''
        SELECT iv.*, c.nombre, c.marca, c.tipo
        FROM items_venta iv
        JOIN componentes c ON iv.componente_id = c.id
        WHERE iv.venta_id = ?
        ''', (venta_id,))
        
        resultado['items'] = [dict(row) for row in cursor.fetchall()]
        
        return resultado
    
    def obtener_ventas_por_vendedor(self, vendedor_id, fecha_inicio=None, fecha_fin=None):
        """
        Obtiene las ventas realizadas por un vendedor específico.
        
        Args:
            vendedor_id (int): ID del vendedor
            fecha_inicio (str, optional): Fecha de inicio en formato 'YYYY-MM-DD'
            fecha_fin (str, optional): Fecha de fin en formato 'YYYY-MM-DD'
            
        Returns:
            list: Lista de diccionarios con la información de las ventas
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM ventas WHERE vendedor_id = ?'
        params = [vendedor_id]
        
        if fecha_inicio:
            query += ' AND fecha >= ?'
            params.append(fecha_inicio)
            
        if fecha_fin:
            query += ' AND fecha <= ?'
            params.append(fecha_fin)
            
        query += ' ORDER BY fecha DESC'
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def obtener_estadisticas_ventas(self, tienda_id=None, fecha_inicio=None, fecha_fin=None):
        """
        Obtiene estadísticas de ventas, opcionalmente filtradas por tienda y fechas.
        
        Args:
            tienda_id (int, optional): ID de la tienda
            fecha_inicio (str, optional): Fecha de inicio en formato 'YYYY-MM-DD'
            fecha_fin (str, optional): Fecha de fin en formato 'YYYY-MM-DD'
            
        Returns:
            dict: Diccionario con estadísticas de ventas
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
        SELECT COUNT(*) as total_ventas, 
               SUM(total) as monto_total,
               AVG(total) as promedio_venta,
               MAX(total) as venta_maxima,
               MIN(total) as venta_minima
        FROM ventas
        WHERE 1=1
        '''
        params = []
        
        if tienda_id:
            query += ' AND tienda_id = ?'
            params.append(tienda_id)
            
        if fecha_inicio:
            query += ' AND fecha >= ?'
            params.append(fecha_inicio)
            
        if fecha_fin:
            query += ' AND fecha <= ?'
            params.append(fecha_fin)
        
        cursor.execute(query, params)
        estadisticas = dict(cursor.fetchone())
        
        # Componentes más vendidos
        query_componentes = '''
        SELECT c.id, c.nombre, c.tipo, c.marca, SUM(iv.cantidad) as total_vendido
        FROM items_venta iv
        JOIN componentes c ON iv.componente_id = c.id
        JOIN ventas v ON iv.venta_id = v.id
        WHERE 1=1
        '''
        
        if tienda_id:
            query_componentes += ' AND v.tienda_id = ?'
        
        if fecha_inicio:
            query_componentes += ' AND v.fecha >= ?'
            
        if fecha_fin:
            query_componentes += ' AND v.fecha <= ?'
            
        query_componentes += ' GROUP BY c.id ORDER BY total_vendido DESC LIMIT 5'
        
        cursor.execute(query_componentes, params)
        estadisticas['componentes_populares'] = [dict(row) for row in cursor.fetchall()]
        
        # Vendedores con más ventas
        query_vendedores = '''
        SELECT v.vendedor_id, vd.nombre, vd.apellido, 
               COUNT(*) as total_ventas, SUM(v.total) as monto_total
        FROM ventas v
        JOIN vendedores vd ON v.vendedor_id = vd.id
        WHERE 1=1
        '''
        
        if tienda_id:
            query_vendedores += ' AND v.tienda_id = ?'
        
        if fecha_inicio:
            query_vendedores += ' AND v.fecha >= ?'
            
        if fecha_fin:
            query_vendedores += ' AND v.fecha <= ?'
            
        query_vendedores += ' GROUP BY v.vendedor_id ORDER BY monto_total DESC LIMIT 5'
        
        cursor.execute(query_vendedores, params)
        estadisticas['vendedores_destacados'] = [dict(row) for row in cursor.fetchall()]
        
        return estadisticas
    
    # Métodos de búsqueda y utilidades
    
    def buscar_componentes(self, termino_busqueda):
        """
        Busca componentes que coincidan con un término de búsqueda.
        
        Args:
            termino_busqueda (str): Término a buscar
            
        Returns:
            list: Lista de componentes que coinciden con la búsqueda
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        termino = f"%{termino_busqueda}%"
        
        cursor.execute('''
        SELECT * FROM componentes 
        WHERE nombre LIKE ? OR tipo LIKE ? OR marca LIKE ? OR descripcion LIKE ?
        ''', (termino, termino, termino, termino))
        
        resultados = []
        for row in cursor.fetchall():
            item = dict(row)
            if item['propiedades']:
                try:
                    item['propiedades'] = json.loads(item['propiedades'])
                except:
                    item['propiedades'] = {}
            resultados.append(item)
            
        return resultados
    
    def eliminar_componente(self, componente_id):
        """
        Elimina un componente de la base de datos.
        
        Args:
            componente_id (int): ID del componente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar si hay ventas relacionadas
        cursor.execute('SELECT COUNT(*) as total FROM items_venta WHERE componente_id = ?', (componente_id,))
        if cursor.fetchone()['total'] > 0:
            # No se puede eliminar porque hay ventas asociadas
            return False
            
        # Eliminar del inventario
        cursor.execute('DELETE FROM inventario WHERE componente_id = ?', (componente_id,))
        
        # Eliminar el componente
        cursor.execute('DELETE FROM componentes WHERE id = ?', (componente_id,))
        
        conn.commit()
        return True
    
    def eliminar_vendedor(self, vendedor_id):
        """
        Elimina un vendedor de la base de datos.
        
        Args:
            vendedor_id (int): ID del vendedor a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar si hay ventas relacionadas
        cursor.execute('SELECT COUNT(*) as total FROM ventas WHERE vendedor_id = ?', (vendedor_id,))
        if cursor.fetchone()['total'] > 0:
            # No se puede eliminar porque hay ventas asociadas
            return False
        
        # Eliminar el vendedor
        cursor.execute('DELETE FROM vendedores WHERE id = ?', (vendedor_id,))
        
        conn.commit()
        return True
    
    def backup_database(self, backup_file=None):
        """
        Crea una copia de seguridad de la base de datos.
        
        Args:
            backup_file (str, optional): Ruta del archivo de respaldo
            
        Returns:
            str: Ruta del archivo de respaldo creado
        """
        if not backup_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f"backup_{timestamp}_{os.path.basename(self.db_file)}"
            
        self.close_connection()
        
        if os.path.exists(self.db_file):
            import shutil
            shutil.copy2(self.db_file, backup_file)
            
        return backup_file