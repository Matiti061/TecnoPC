# Warning: Running this script will delete the JSON file stored in the root directory.

import os
from package.model import *
try:
    os.remove("data.json")
except FileNotFoundError:
    pass
model = Model()

store_uuids = [
    model.add_store(Store("Tienda Bosquemar", "Av. Bosquemar 123", "Viña del Mar", "322123456", "bosquemar@tecnopc.cl")),
    model.add_store(Store("Tienda Mirasol", "Calle Mirasol 456", "Santiago", "22987654", "mirasol@tecnopc.cl")),
    model.add_store(Store("Tienda ValleVolcanes", "Av. ValleVolcanes 789", "Temuco", "452654321", "vallevolcanes@tecnopc.cl")),
    model.add_store(Store("Tienda La Serena", "Calle La Serena 321", "La Serena", "512345678", "laserena@tecnopc.cl")),
    model.add_store(Store("Tienda Antofagasta", "Av. Antofagasta 654", "Antofagasta", "412345678", "antofagasta@tecnopc.cl"))
    

]
worker_uuids = [
    model.add_worker(Worker("Juan", "Pérez", "987654321", "juan.perez@tecnopc.cl")),
    model.add_worker(Worker("Maria", "Gomez", "987654322", "maria.gomez@tecnopc.cl")),
    model.add_worker(Worker("Carlos", "López", "987654323", "carlos.lopez@tecnopc.cl")),
    model.add_worker(Worker("Esteban", "Martinez", "987654324", "esteban.martinez@tecnopc.cl")),
    model.add_worker(Worker("Jesus", "Minitti", "945612783", "jesus.minitti@tecnopc.cl"))

]
product_uuids = [
    model.add_product(Product("Kingston", "Fury 16GB", "RAM", "DDR4 3200MHz", 75990)),
    model.add_product(Product("Intel", "Core i5-12400F", "Procesador", "6 núcleos, 12 hilos", 199990)),
    model.add_product(Product("Samsung", "970 EVO Plus 1TB", "SSD", "NVMe M.2", 129990)),
    model.add_product(Product("Asus", "ROG Strix B550-F", "Placa madre", "ATX, AM4", 129990)),
    model.add_product(Product("Corsair", "RM750x", "Fuente de poder", "750W, 80 Plus Gold", 89990)),
    model.add_product(Product("Ryzen", "5 5600X", "Procesador", "6 núcleos, 12 hilos", 159990)),
    model.add_product(Product("Gigabyte", "AORUS GeForce RTX 3060", "Tarjeta gráfica", "12GB GDDR6", 499990)),
    model.add_product(Product("Kingston", "A2000 500GB", "SSD", "NVMe M.2", 49990)),
    model.add_product(Product("Gigastone", "Game Turbo 1TB", "SSD", "SATA III", 39990)),
    model.add_product(Product("Gigastone", "Game Turbo 2X16 GB", "RAM", "DDR4 3200MHZ", 649990)),
    model.add_product(Product("Asus", "ROG Strix B550-F", "Placa madre", "ATX, AM4", 129990)),
    model.add_product(Product("Intel", "Core i7-12700K", "Procesador", "12 núcleos, 20 hilos", 299990)),
    model.add_product(Product("Corsair", "Vengeance LPX 32GB", "RAM", "DDR4 3200MHz", 129990)),
    model.add_product(Product("Seagate", "Barracuda 2TB", "HDD", "7200 RPM, SATA III", 49990)),
    model.add_product(Product("Western Digital", "Blue 1TB", "HDD", "7200 RPM, SATA III", 39990)),
    model.add_product(Product("AMD", "ROG STRIX B550-F", "Placa madre", "ATX, AM4", 129990)),
    model.add_product(Product("MSI", "MAG B550M Mortar", "Placa madre", "Micro-ATX, AM4", 89990)),

]

model.add_product_to_store(store_uuids[0], product_uuids[2])
model.add_worker_to_store(store_uuids[0], worker_uuids[1])
# La identificación debería ser el RUT
model.add_manager("12345678", Manager(
    "Matias",
    "Barrientos",
    "912345678",
    "matias.barrientos@it.tecnopc.cl",
    "contraseña123"
))
