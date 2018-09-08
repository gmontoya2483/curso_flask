# Section 1 - Hello World!

El objetivo de esta sección es explicar como estructurar un proyecto flask en forma correcta.


## Contenido

* [Instalar Python](#instalar-python)
    * [Ubuntu](#ubuntu)
    * [Diferencias entre virtualenv y venv](#diferencias-entre-virtualenv-y-venv)
* [Instalar Flask](#instalar-flask)
* [Aplicación Flask Hello World](#aplicacion-flask-hello-world)
* [Ejecutar la aplicación](#ejecutar-la-aplicacion)
    * [En linux](#en-linux)
    * [En Windows](#en-windows)
    * [En PowerShell](#en-powershell)
    * [Modo Debug](#modo-debug)
* [Referencias](#referencias)

    
## Instalar Python

### Ubuntu

```console
$ sudo apt-get update
$ sudo apt-get upgrade

$ sudo apt-get install python3
$ sudo apt-get install python3-pip
```

```console
$ sudo apt-get install python3-venv
user@host:~/OneDrive/Projects/curso-flask$ python3 -m venv venv-ubuntu
```

ó

```console
$ sudo pip3 install virtualenv
user@host:~/OneDrive/Projects/curso-flask$$ virtualenv venv-ubuntu --python=python3
```

```console
user@host:~/OneDrive/Projects/curso-flask$ source venv-ubuntu/bin/activate
(venv-ubuntu) user@host:~/OneDrive/Projects/curso-flask$

(venv-ubuntu) user@host:~/OneDrive/Projects/curso-flask$ deactivate
user@host:~/OneDrive/Projects/curso-flask$
```

### Diferencias entre ``virtualenv`` y ``venv``

* **[virtualenv](https://pypi.org/project/virtualenv/)** es una herramienta muy popular que crea entornos aislados de Python para las bibliotecas de Python. Si no está familiarizado con esta herramienta, le recomiendo que la aprenda, ya que es una herramienta muy útil, y haré comparaciones con ella durante el resto de esta respuesta.

    Funciona mediante la instalación de un montón de archivos en un directorio (por ejemplo: env/), y luego modificar la variable de entorno para PATH prefijo una bin directorio personalizado (por ejemplo: env/bin/). Se coloca una copia exacta del binario python o python3 en este directorio, pero Python está programado para buscar bibliotecas relativas a su ruta primero, en el directorio de entorno. No forma parte de la biblioteca estándar de Python, pero está oficialmente bendecida por PyPA (Python Packaging Authority). Una vez activado, puede instalar paquetes en el entorno virtual usando pip.

* **[venv](https://docs.python.org/3/library/venv.html)** es un paquete enviado con Python 3, que se puede ejecutar utilizando python3 -m venv (aunque por alguna razón algunas distribuciones se separan hacia fuera en un paquete de distribución independiente, como python3-venv en Ubuntu/Debian). Tiene un propósito similar al virtualenv, y funciona de una manera muy similar, pero no necesita copiar los binarios de Python (excepto en Windows). Úselo si no necesita admitir Python 2. Al momento de escribir, la comunidad de Python parece estar contenta con virtualenv y no he escuchado hablar mucho de venv.


## Instalar Flask

Para instalar los requerimientos del proyecto es necesario conectarse al entorno virtual. De esta forma las librerias solo se instalan en el en ese entorno y las aplicaciones quedan encapsuladas.

```console
user@host:~/OneDrive/Projects/curso-flask$ source venv-ubuntu/bin/activate
(venv-ubuntu) user@host:~/OneDrive/Projects/curso-flask$ pip install flask
```

> **NOTA**: Al estar conectado a un entorno virtual, ya no es mas necesarion especificar la version de Python en el comando. Esto se debe que dentro del entorno virtual existe una única version de Python corriendo. 


## Aplicacion Flask Hello World

Flask es un framework que nos permite escribir una aplicación entera en un uúnico archivo. Esto no es practico y no se utiliza dado que en aplicaciones de tamanio medio o grande, el código seria inmanejable.  

Lo recomendable es:  

* Crear dentro del proyecto un packete para la aplicación, llamado en este caso **app**.
* Dentro del archivo ``__init__.py``, del modulo **app**, se importa ``Flask``, se instancia la clase ``Flask`` y se importa el arhivo donde se definen las rutas, ``routes.py``  

  * ``/app/__init__.py``
  
      ```python
      from flask import Flask
        
      app = Flask(__name__)
        
      from app import routes # Este import al final es intencinal para evitar los probles de dependencias circulares.
      ```

* Dentro del paquete **app** crear el archivo ``routes.py``, el cuál contiene los mapeos de la aplicación.
    
    * ``/app/routes.py``
  
      ```python
      from app import app


      @app.route('/')
      @app.route('/index')
      def index():
          return f'Hello, World!!'
      ```

* En el root del proyecto se encuentra el script que ejecuta la aplicacion, en este caso ``microblog.py``. Este script lo único que contiene es la importacion de **app**.

    * ``/app/routes.py``
    
       ```python
      from app import app
      ```


## Ejecutar la aplicacion

La estructura que se genero, facilita las cosas al deployar la aplicación:

### En linux

```console
(venv-ubuntu) gabriel@LAPTOP-E28IELG7:~/OneDrive/Projects/curso-flask$ export FLASK_APP=microblog.py
(venv-ubuntu) gabriel@LAPTOP-E28IELG7:~/OneDrive/Projects/curso-flask$ flask run
```


## En Windows
```console
(venv) C:\Users\Gabriel\OneDrive\Projects\curso-flask> set FLASK_APP=microblog.py
(venv) C:\Users\Gabriel\OneDrive\Projects\curso-flask> flask run
```

## En PowerShell
```console
(venv) PS C:\Users\Gabriel\OneDrive\Projects\curso-flask> $env:FLASK_APP = "microblog.py"
(venv) PS C:\Users\Gabriel\OneDrive\Projects\curso-flask>  flask run
```

> **Nota:** utilizando ``flask run --host=0.0.0.0``, hace que se pueda acceder a la aplicacion desde otros ordenadores.  
>  Por otro lado en lugar de ``flask run`` tambien se puede utilizar ``python -m flask``. 


## Modo Debug

```console
(venv-ubuntu) $ export FLASK_ENV=development
(venv-ubuntu) $ flask run
```

Esto hace lo siguiente:

Activa el debugger  
Activa la recarga automatica
habilita el modo debug en la aplicacion Flask.

> **NOTA:** Para facilitar las cosas y poder correr la aplocacion directamente desde ``PyCharm``, se puede realizar la siguiente modificacion en el archivo ``microblog.py``.  
> ```python
>   from app import app
>   
>   if __name__ == '__main__':
>    app.run(port=5000, debug=True)
>
>``` 
> De esta forma tambien se puede ejecutar la applicación como cualquier otro programa **python**:  
> ```console
> (venv-ubuntu) $ python microblog.py
> ```

## Referencias 
[The Flask Mega-Tutorial Part I: Hello, World!](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)  
[Installing python](https://www.udemy.com/flask-mega-tutorial/learn/v4/t/lecture/10403940?start=0)  
[Flask Quickstart](http://flask.pocoo.org/docs/1.0/quickstart/)