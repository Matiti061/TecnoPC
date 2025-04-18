# Warning: Running this script will delete the JSON file stored in the root directory.

import os
from package.model import *
os.remove("data.json")
model = Model()

store_uuids = [
    model.add_store(Store("Tienda Bosquemar", "Av. Bosquemar 123", "Viña del Mar", "322123456", "bosquemar@tecnopc.cl")),
    model.add_store(Store("Tienda Mirasol", "Calle Mirasol 456", "Santiago", "22987654", "mirasol@tecnopc.cl")),
    model.add_store(Store("Tienda ValleVolcanes", "Av. ValleVolcanes 789", "Temuco", "452654321", "vallevolcanes@tecnopc.cl"))

]
worker_uuids = [
    model.add_worker(Worker("Juan", "Pérez", "987654321", "juan.perez@tecnopc.cl")),
    model.add_worker(Worker("Maria", "Gomez", "987654322", "maria.gomez@tecnopc.cl")),
    model.add_worker(Worker("Carlos", "López", "987654323", "carlos.lopez@tecnopc.cl"))
]
product_uuids = [
    model.add_product(Product("Kingston", "Fury 16GB", "RAM", "DDR4 3200MHz", 75990)),
    model.add_product(Product("Intel", "Core i5-12400F", "Procesador", "6 núcleos, 12 hilos", 199990)),
    model.add_product(Product("Samsung", "970 EVO Plus 1TB", "SSD", "NVMe M.2", 129990))
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
