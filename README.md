# TecnoPC

**Los mejores componentes para tu PC**

Este programa es funcional (de momento) en Python 3.13.2  **No probado en otras versiones**

## Ejecutacion del programa

Solo con que ejecutes el archivo main esta bien, por ejemplo:

> $ python main.py

## Estructura de los archivos momentanea

### Controllers

Todos los archivos controladores tales como el inventario y la venta de productos

### Models

Carpeta que da cada modelo de venta, de inventario, componente, etc.

### Views

En este archivo es la interfaz, esta todo hecho con PyQt6 listo para ejecutar

#### De manera suelta se encuentra el archivo main, no esta dentro de una carpeta especifica

## Software necesario

### Desarrollo

* [Git](https://git-scm.com/)

### Uso

* [Python](https://www.python.org/)

## Software recomendado

* [PyCharm](https://www.jetbrains.com/pycharm/): IDE para programar en Python
(Gracias Esteban por tanto)

## Licencia

* El repositorio esta licenciado bajo la licencia MIT, la puedes ver por [aquí](https://github.com/Matiti061/TecnoPC/blob/main/LICENSE)

## PARA HACER

Solo para uso interno de programadores en este repositorio

### Necesario

* [ ] Pendiente: Agregar funciones de Busqueda de productos, Agregar item,
Finalizar Venta, agregar estadisticas (Archivo: interfaz_tienda.py)
* [X] OK: Agregar la funcion de poder cancelar una venta de manera rapida
* [X] OK: Agregar tabla de ID de productos, Nombre, tipo, etc.
* [X] OK: Colocar un filtro de busqueda de los productos
* [X] OK: Poder cambiar entre tiendas al igual que entre vendedores en el
apartado de Ventas
* [X] OK: Agregar algun tipo de limite al lugar de agregar items en la pestaña
de Ventas
* [X] OK: Poder calcular las comisiones de cada vendedor (Plus para que el profe
nos quiera mucho, aunque falta mejorarlo)

### No tan necesario pero bonito

* [ ] Pendiente: Mejorar el diseño de la pagina con Qt Designer o algun otro editor
* [ ] Pendiente: Cambiar las ciudades de las tiendas (Hay ciudades aleatorias
las cuales tienen nombres de PM pero se ubican en las ciudades que mas venden de
cada sector de Chile) (Si quieren poner alguna tienda, adelante)
* [X] OK: Poner limite al lugar de "Precio Max" en el apartado de Inventario
* [ ] Pendiente: Agregar algo de gerente como en AeroChinquihue (No lo dijo el
profe pero si alguien lo quiere hacer adelante, no me quiero calentar la cabeza
en eso los quiero mucho)
