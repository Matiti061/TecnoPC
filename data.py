import dataclasses
import pathlib
from package.model import Model
from package.dataclasses.client import Client
from package.dataclasses.manager import Manager
from package.dataclasses.product import Product
from package.dataclasses.employee import Employee
from package.dataclasses.provider import Provider
from package.dataclasses.store import Store

if pathlib.Path("data.json").exists():
    raise FileExistsError("Data file already exists")
model = Model()
employee_uuids = []
product_uuids = []

# Clients
clients = [
    Client("10000000", "Roberto", "Carlos", "+56940000000"),
    Client("11000000", "Axel", "Subiabre", "+56945000000"),
    Client("12000000", "Vicente", "Espinoza", "+56960000000")
]
for client in clients:
    model.clients.create(dataclasses.asdict(client))

# Discounts todo

# Employees
employees = [
    # 22.000.000-1
    Employee("22000000", "Juan", "Pérez", "+56987654321", "juan.perez@tecnopc.cl", "juanperez123"),
    # 23.000.000-K
    Employee("23000000", "María", "Gomez", "+56987654322", "maria.gomez@tecnopc.cl", "mariagomez123"),
    # 24.000.000-8
    Employee("24000000", "Carlos", "López", "+56987654323", "carlos.lopez@tecnopc.cl", "carloslopez123"),
    # 25.000.000-6
    Employee("25000000", "Esteban", "Martínez", "+56987654324", "esteban.martinez@tecnopc.cl", "estebanmartinez123"),
    # 27.000.000-2
    Employee("27000000", "Jesús", "Minnitti", "+56945612783", "jesus.minnitti@tecnopc.cl", "jesusminnitti123")
]
for employee in employees:
    employee_uuids.append(model.employees.create(dataclasses.asdict(employee)))

# Managers
managers = [
    Manager("12345678", "Matías", "Barrientos", "+56912345678", "matias.barrientos@tecnopc.cl", "contraseña123")
]
for manager in managers:
    model.managers.create(dataclasses.asdict(manager))

# Products
products = [
    Product("AMD", "Ryzen 5 5600X", "Procesador", "6 núcleos, 12 hilos", 159990, "Proveedor 1"),
    Product("Asus", "ROG Strix B550-F", "Placa madre", "ATX, AM4", 129990, "Proveedor 1"),
    Product("Corsair", "RM750x", "Fuente de poder", "750W, 80 Plus Gold", 89990, "Proveedor 1"),
    Product("Corsair", "Vengeance LPX 32GB", "RAM", "DDR4 3200MHz", 129990, "Proveedor 1"),
    Product("Gigabyte", "AORUS GeForce RTX 3060", "Tarjeta gráfica", "12GB GDDR6", 499990, "Proveedor 1"),
    Product("Gigastone", "Game Turbo 1TB", "SSD", "SATA III", 39990, "Proveedor 1"),
    Product("Gigastone", "Game Turbo 2x16GB", "RAM", "DDR4 3200MHz", 64990, "Proveedor 1"),
    Product("Intel", "Core i5-12400F", "Procesador", "6 núcleos, 12 hilos", 199990, "Proveedor 1"),
    Product("Intel", "Core i7-12700K", "Procesador", "12 núcleos, 20 hilos", 299990, "Proveedor 1"),
    Product("Kingston", "A2000 500GB", "SSD", "NVMe M.2", 49990, "Proveedor 1"),
    Product("Kingston", "Fury 16GB", "RAM", "DDR4 3200MHz", 75990, "Proveedor 1"),
    Product("MSI", "MAG B550M Mortar", "Placa madre", "Micro-ATX, AM4", 89990, "Proveedor 1"),
    Product("Samsung", "970 EVO Plus 1TB", "SSD", "NVMe M.2", 129990, "Proveedor 1"),
    Product("Seagate", "Barracuda 2TB", "HDD", "7200RPM, SATA III", 49990, "Proveedor 1"),
    Product("Western Digital", "Blue 1TB", "HDD", "7200RPM, SATA III", 39990, "Proveedor 1"),
]
for product in products:
    product_uuids.append(model.products.create(dataclasses.asdict(product)))

# Providers
providers = [
    Provider("Proveedor 1", "12121212", "Puerto Montt", "a@a.com", "1212"),
    Provider("Proveedor 2", "12121212", "Puerto Montt", "a@a.com", "1212")
]
for provider in providers:
    model.providers.create(dataclasses.asdict(provider))

# Sales todo

# Stores
stores = [
    Store("Tienda Bosquemar", "Avenida Bosquemar 123", "Viña del Mar", "+56322123456", "bosquemar@tecnopc.cl", [], []),
    Store("Tienda Mirasol", "Calle Mirasol 456", "Santiago", "+56222987654", "mirasol@tecnopc.cl", [], []),
    Store("Tienda Valle Volcanes", "Avenida Valle Volcanes 789", "Temuco", "+56452654321", "vallevolcanes@tecnopc.cl", [], []),
    Store("Tienda La Serena", "Calle La Serena 321", "La Serena", "+56512345678", "laserena@tecnopc.cl", [], []),
    Store("Tienda Antofagasta", "Avenida Antofagasta 654", "Antofagasta", "+56552345678", "antofagasta@tecnopc.cl", [], [])
]
for index, store in enumerate(stores):
    store.employee_uuids = [employee_uuids[index]]
    store.product_uuids = [product_uuids[index*3:index*3+3]]
    model.stores.create(dataclasses.asdict(store))
