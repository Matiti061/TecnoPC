#GG
import pathlib
import random
from package.model import Model
from package.dataclasses.store import Store
from package.dataclasses.person import Person
from package.dataclasses.product import Product
from package.dataclasses.provider import Provider

if pathlib.Path("data.json").exists():
    raise FileExistsError("Data file already exists")

model = Model()

# Managers
model.manager.create_manager(
    "12345678",
    Person("Matías", "Barrientos", "+56912345678", "matias.barrientos@administracion.tecnopc.cl", "contraseña123")
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

model.provider.create_provider(Provider("TecnoProductos", "+56912121212", "tecnoproductos@tecnopc.cl", "1212"))
model.provider.create_provider(Provider("Atlas PC", "+56912121212", "atlaspc@tecnopc.cl", "1212"))

del model
model = Model()
# Employees
employees = [
    # 22.000.000-1
    ["22000000", Person("Juan", "Pérez", "+56987654321", "juan.perez@tecnopc.cl", "juanperez123")],
    # 23.000.000-K
    ["23000000", Person("María", "Gomez", "+56987654322", "maria.gomez@tecnopc.cl", "mariagomez123")],
    # 24.000.000-8
    ["24000000", Person("Carlos", "López", "+56987654323", "carlos.lopez@tecnopc.cl", "carloslopez123")],
    # 25.000.000-6
    ["25000000", Person("Esteban", "Martínez", "+56987654324", "esteban.martinez@tecnopc.cl", "estebanmartinez123")],
    # 27.000.000-2
    ["27000000", Person("Jesús", "Minnitti", "+56945612783", "jesus.minnitti@tecnopc.cl", "jesusminnitti123")]
]
employee_uuids = []
for employee in employees:
    employee_uuids.append(
        model.employee.create_employee(store_uuids[random.randint(0, len(store_uuids) - 1)], employee[0], employee[1])
    )

# Products
products = [
    Product("AMD", "Ryzen 5 5600X", "Procesador", "6 núcleos, 12 hilos", 159990, "TecnoProductos"),
    Product("Asus", "ROG Strix B550-F", "Placa madre", "ATX, AM4", 129990, "TecnoProductos"),
    Product("Corsair", "RM750x", "Fuente de poder", "750W, 80 Plus Gold", 89990, "TecnoProductos"),
    Product("Corsair", "Vengeance LPX 32GB", "RAM", "DDR4 3200MHz", 129990, "TecnoProductos"),
    Product("Gigabyte", "AORUS GeForce RTX 3060", "Tarjeta gráfica", "12GB GDDR6", 499990, "TecnoProductos"),
    Product("Gigastone", "Game Turbo 1TB", "SSD", "SATA III", 39990, "TecnoProductos"),
    Product("Gigastone", "Game Turbo 2x16GB", "RAM", "DDR4 3200MHz", 64990, "TecnoProductos"),
    Product("Intel", "Core i5-12400F", "Procesador", "6 núcleos, 12 hilos", 199990, "TecnoProductos"),
    Product("Intel", "Core i7-12700K", "Procesador", "12 núcleos, 20 hilos", 299990, "TecnoProductos"),
    Product("Kingston", "A2000 500GB", "SSD", "NVMe M.2", 49990, "TecnoProductos"),
    Product("Kingston", "Fury 16GB", "RAM", "DDR4 3200MHz", 75990, "TecnoProductos"),
    Product("MSI", "MAG B550M Mortar", "Placa madre", "Micro-ATX, AM4", 89990, "TecnoProductos"),
    Product("Samsung", "970 EVO Plus 1TB", "SSD", "NVMe M.2", 129990, "TecnoProductos"),
    Product("Seagate", "Barracuda 2TB", "HDD", "7200RPM, SATA III", 49990, "TecnoProductos"),
    Product("Western Digital", "Blue 1TB", "HDD", "7200RPM, SATA III", 39990, "TecnoProductos"),
]
product_uuids = []
for product in products:
    product_uuids.append(model.product.create_product(store_uuids[random.randint(0, len(store_uuids) - 1)], product))