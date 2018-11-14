# Section 4 - Database

[Volver al README.md](README.md)

Para utilizar base de datos relacionales es recomendable utilizar un **Object Relational Mapper**, o **ORM**, ``Flask-SQLAlchemy`` es un **ORM** que nos permite trabajar con las bases de Datos a un alto nivel utilizando clases, objetos y metodos en lugar de tablas y SQL. 
El paquete de ``SQL-Alchemy`` soporta una larga lista de motores de Bases de Datos, incluyendo los mas populares como ser *MySQL*, *PostgresSQL* y *SQlite*.

Para instalar ``Flask-SQLAlchemy``:

```console
(venv) $ pip install flask-SQLAlchemy
```

## Contenido

* [Database Migration](#database-migrations)
* [Configuración](#configuracion)
* [Database Models](#database-models)
* [Creating The Migration Repository](#creating-the-migration-repository)
* [Referencias](#referencias)


## Database Migrations

``Flask-Migrate``, nos permite trabajar con las modificaciones de las bases de Datos sin perder información. Esta extensión de **Flask** es un wrapper para ``Alembic``, un framework de migración de base de datos para *SQL-Alchemy*.  

Para instalar ``Flask-Migrate``:
```console
(venv) $ pip install flask-migrate
```

## Configuracion

* ``config.py``

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'My_secret key'
    
    # Configure the Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Una vez agregada la cofiguración de la base de datos dentro del ``config.py``, se deben crear las instancias de la base de datos y la migración.

* ``app/__init__.py``

```python
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models
```

## Database Models


Los datos que van a ser guradados en la base de datos son representados como una collección de clases, usualmente llamada *database models*. La capa **ORM** dentro del **SQLAlchemy** se encarga de mapear los objetos de estas clases dentro registro en las tablas de la base de datos. 

* ``app/models.py``

```python
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username) 
```

## Creating The Migration Repository

Para crear o inicializar el repositorio se debe ejecutar el siguiente comando:

```console
(venv) $ flask db init

  Creating directory /mnt/c/Users/Gabriel/OneDrive/Projects/curso-flask/migrations ... done
  Creating directory /mnt/c/Users/Gabriel/OneDrive/Projects/curso-flask/migrations/versions ... done
  Generating /mnt/c/Users/Gabriel/OneDrive/Projects/curso-flask/migrations/alembic.ini ... done
  Generating /mnt/c/Users/Gabriel/OneDrive/Projects/curso-flask/migrations/env.py ... done
  Generating /mnt/c/Users/Gabriel/OneDrive/Projects/curso-flask/migrations/README ... done
  Generating /mnt/c/Users/Gabriel/OneDrive/Projects/curso-flask/migrations/script.py.mako ... done
  Please edit configuration/connection/logging settings in '/mnt/c/Users/Gabriel/OneDrive/Projects/curso-flask/migrations/alembic.ini' before proceeding.
```

> **NOTA:** el comando ``flask`` confia en la variable de entorno ``FLASK_APP`` para saber doende esta la aplicación Flask:  
>  ``FLASK_APP=microblog.py``

Luego de ejecutar este comando, aparece una nuevo directorio llamado *migrations*, que contine algunos archivos y un subdirectorio llamado *versions*. Todos los archivos que poseee la carpeta *migrations*, incluyendo los subdirectorios tienen que ser tratados como parte del proyecto, por lo que tienen que ser agregados al control de cambios (GIT).  


## The First Database Migration


## Referencias 
[The Flask Mega-Tutorial Part IV: Databases](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database)  
[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org)  
[SQL-Alchemy](https://www.sqlalchemy.org/) 
[Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate)  
[Alembic](https://bitbucket.org/zzzeek/alembic)