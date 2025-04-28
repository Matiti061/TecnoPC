"""
Generates an initial data.json containing sample data.
"""

import pathlib
from package.model import Model, Manager, Store, Employee, Product

if pathlib.Path("data.json").exists():
    raise FileExistsError("Data file already exists")

model = Model()

# Managers
model.manager.create_manager(
    "12345678",
    Manager("Matías", "Barrientos", "+56912345678", "matias.barrientos@administracion.tecnopc.cl", "contraseña123")
)

# Stores
stores = [
    Store("Tienda Bosquemar", "Avenida Bosquemar 123", "Viña del Mar", "+56322123456", "bosquemar@tecnopc.cl"),
    Store("Tienda Mirasol", "Calle Mirasol 456", "Santiago", "+56222987654", "mirasol@tecnopc.cl"),
    Store("Tienda Valle Volcanes", "Avenida Valle Volcanes 789", "Temuco", "+56452654321", "vallevolcanes@tecnopc.cl"),
    Store("Tienda La Serena", "Calle La Serena 321", "La Serena", "+56512345678", "laserena@tecnopc.cl"),
    Store("Tienda Antofagasta", "Avenida Antofagasta 654", "Antofagasta", "+56552345678", "antofagasta@tecnopc.cl")
]
store_uuids = []
for store in stores:
    store_uuids.append(model.store.create_store(store))

# Employees
employees = [
    Employee("Juan", "Pérez", "987654321", "juan.perez@tecnopc.cl"),
    Employee("María", "Gomez", "987654322", "maria.gomez@tecnopc.cl"),
    Employee("Carlos", "López", "987654323", "carlos.lopez@tecnopc.cl"),
    Employee("Esteban", "Martínez", "987654324", "esteban.martinez@tecnopc.cl"),
    Employee("Jesús", "Minnitti", "945612783", "jesus.minnitti@tecnopc.cl")
]
employee_uuids = []
for employee in employees:
    employee_uuids.append(model.employee.create_employee(employee))

# Products
products = [
    Product("AMD", "Ryzen 5 5600X", "Procesador", "6 núcleos, 12 hilos", 159990),
    Product("Asus", "ROG Strix B550-F", "Placa madre", "ATX, AM4", 129990),
    Product("Corsair", "RM750x", "Fuente de poder", "750W, 80 Plus Gold", 89990),
    Product("Corsair", "Vengeance LPX 32GB", "RAM", "DDR4 3200MHz", 129990),
    Product("Gigabyte", "AORUS GeForce RTX 3060", "Tarjeta gráfica", "12GB GDDR6", 499990),
    Product("Gigastone", "Game Turbo 1TB", "SSD", "SATA III", 39990),
    Product("Gigastone", "Game Turbo 2x16GB", "RAM", "DDR4 3200MHz", 64990),
    Product("Intel", "Core i5-12400F", "Procesador", "6 núcleos, 12 hilos", 199990),
    Product("Intel", "Core i7-12700K", "Procesador", "12 núcleos, 20 hilos", 299990),
    Product("Kingston", "A2000 500GB", "SSD", "NVMe M.2", 49990),
    Product("Kingston", "Fury 16GB", "RAM", "DDR4 3200MHz", 75990),
    Product("MSI", "MAG B550M Mortar", "Placa madre", "Micro-ATX, AM4", 89990),
    Product("Samsung", "970 EVO Plus 1TB", "SSD", "NVMe M.2", 129990),
    Product("Seagate", "Barracuda 2TB", "HDD", "7200RPM, SATA III", 49990),
    Product("Western Digital", "Blue 1TB", "HDD", "7200RPM, SATA III", 39990)
]
product_uuids = []
for product in products:
    product_uuids.append(model.product.create_product(product))

# Store operations
model.product.create_product_in_store(store_uuids[0], product_uuids[2])
model.employee.create_employee_in_store(store_uuids[0], employee_uuids[1])
