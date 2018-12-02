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
* [The First Database Migration](#the-first-database-migration)
* [Database Relationship - One to Many](#database-relationship---one-to-many)
* [Shell Context](#shell-context)
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

Una vez que tenemos el repositorio de la migración luego de inicializar la base de datos. ``Alabemic`` compara el schema de la base de datos definido en el modelo contra el schema actual utilizado en la base de datos. Luego genera el script de migración con los cambios necesarionpara hacer que que la base de datos y el modelo matcheen.  

El subcomendo ``flask db migrate`` crea esta migracion en forma automatica.

```console
(venv) $ flask db migrate -m "Users table"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_username' on '['username']'
Generating C:\Users\Gabriel\OneDrive\Projects\curso-flask\migrations\versions\dee040b454d0_users_table.py ... done
```

El script generado es ahora parte del proyecto y tiene que ser incorporado al control de código (GIT). Dentro de este script hay 2 fuciones ``upgrade()`` y ``downgrade()``. La función ``upgrade()`` aplica la migración, mientras que ``downgrade()`` remueve los cambios. Esto permite a **Albemic** migrar la base de datos a cualquier punto en la historia.  


* ``migrations/versions/dee040b454d0_users_table.py``

```python
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dee040b454d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
```



El comando ``flask db migrate`` no realiza cambios en la base de datos, solo genera el script de migración. Para aplicar los cambios en la base de datos, es necesario utilizar el comando ``flask db upgrade``.  

```comamnd
(venv) $ flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> dee040b454d0, Users table
``` 



Al utilizar **SQLite**, si la base de datos no existe, la migración crea la el archivo de la base de datos. Al trabajar con servidores de base de datos como **PostgreSQL** o **MySQL**, es necesario crear la base de datos en el servidor antes de ejecutar el comando ``flask db upgrade``

> **NOTA:** **Flask-SQLAlchemy** utiliza *snake case* como convención de nombres por default para las tablas. Por ejemplo para el modelo **User**, el nombre de tabla correspondiente va a ser **user**, para un modelo **AddressAndPhone** el nombre de la tabla sería **address_and_phone**. Si se prefiere utilizar otros nombres, se debe agregar el atributo ``__tablename__`` al modelo con el nombre que se quiera poner.


## Database Relationship - One to Many

* ``app/models.py``

```python
from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

```

Para definir una relación **one to many**, en la parte del **many** se debe colocar una clave foranea hacia **one**. En este caso *Un User escribe muchos Post*, La clave foranea esta en la tabla **Post** y hace refencia a la clave primaria de **User**:

```python

class Post(db.Model):
    
    ...
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    ...

``` 

Por otro lado en la parte uno se debe colocar una relación hacia la tabla muchos:

```python
class User(db.Model):
    ...
    
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    ...
```

``db.relationship`` no define un campo dentro la base de datos, es una funcionalidad de **SQL-Alchemy** que nos permite manejar en forma mas simplificada las reciones.  
De esta manera si tenenos un usuario y queremos saber los posts que escribio solo tenemos que escribir ``u.posts``.

El primer atributo de ``db.relationship('Post', backref='author', lazy='dynamic')`` es el nombre del Model class que representa a la parte ``many`` de la relación, en este ejemplo *Post*. El ``backref`` indica el nembre de campo que va a ser agregado a los objetos de ``many``, de esta forma podemos averiguar el autor de un post ``post.author``.  

 El argumento ``Lazy`` indica como el query de la relación va ser manejado (``select``, ``inmediate``, ``joined``, ``subquery``, ``noload``,``dynamic``)
 
 > NOTA: al agregar la tabla Post, es necesario correr nuevamente el script migrate y upgrade para actulizar la base de datos.
 
 
```command
(venv) $ flask db migrate -m "Post table and Relationship with User"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'post'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_post_timestamp' on '['timestamp']'
  Generating /mnt/c/Users/Gabriel/OneDrive/Projects/curso-
  flask/migrations/versions/ccf929af2f68_post_table_and_relationship_with_user.py ... done


(venv) $ flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade dee040b454d0 -> ccf929af2f68, Post table and Relationship with User

```
 
 
## Shell Context

Otro modulo principal de flask es ``flask shell``, que nos permite ejecutar instrucciones python en linea de comando, similar a ``Python`` pero con la diferencia que ya tenenos dentro del shell el contexto de nuestra applicacion:

```command
(venv) $ python
>>> app
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'app' is not defined
>>>

(venv) $ flask shell
>>> app
<Flask 'app'>

```

como se puede ver no hace falta importor **app** como cuando se utiliza ``Python``.  No obstante esto, podemos definir nuestro propio shell context utilizando el decorator ``@app.shell_context_processor``

* ``microblog.py``

```python
from app import app, db
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
```

Con este contecto vamos a poder utilizar la db, User and Post en el shell sin necesidad de importarlos.

>**NOTA:** Si el shell no reconoce los nombres lugo de crear la funcion ``make_shell_context()`` es debibo a que no esta registrada, por los que es necesario setear uevamente la varible ``FLASK_APP=microblog.py``   
> Linux: ``export FLASK_APP=microblog.py``  
> Windows: ``set FLASK_APP=microblog.py``




## Referencias 
[The Flask Mega-Tutorial Part IV: Databases](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database)  
[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org)  
[SQL-Alchemy](https://www.sqlalchemy.org/) 
[Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate)  
[Alembic](https://bitbucket.org/zzzeek/alembic)