# Section 3 - Web Forms

[Volver al README.md](README.md)

El objetivo de esta sección es explicar como utilizar la extensión ``Flask-WTF``.  
Las extensiones de **Flask** son paquetes de **Python** que son instalados utilizando ``pip``

```console
(venv) $ pip install flask-wtf
```

## Contenido

* [Configuration](#configuration)
* [User Login Form](#user-login-form)
* [Form Templates](#form-templates)
* [Form Views](#form-views)
* [Receiving Form Data](#receiving-form-data)
* [Improving Field Validation](#improving-field-validation)
* [Generating Links](#generating-links)
* [Referencias](#referencias)

## Configuration

Para poder utilizar la extension de Flask-WTF, la instancia de la aplicación Flask tiene que ser configurada con una *secret-key*. Esta clave es utilizada por Flask-WTF para proteger los **WebForms** contra ataques del tipo *Cross site request forgery*.  
Las variables pueden ser definidas de varias formas, la forma mas sencilla (no la mejor) es definirlas en ``app.config``, justo luego de crear la instancia de la aplicacioón.

* ``/app/__init__.py``

```python
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'My_secret key'

from app import routes # Este import al final es intencinal para evitar los probles de dependencias circulares.
```

Este aproach puede ser utilizado en aplicaciones pequeñas, pero a medida que el proyecto crece el utilizar ``app.config``, se vuelve complicado de manejar. La forma ideal de manejar la configuración de la aplicacion es creando un archivo de configuracion el cual va a tener una clase que maneje la configuración.

* ``config.py``
```python
class Config(object):
    SECRET_KEY = 'My_secret key'
```

Una mejor forma de definir el archivo de configuracion es no tener las variables hardcodedas y obtener sus valores de variables de entorno o de urchivo de configuración. En este caso utilizaremos variables de entorno.

* ``config.py``

```python
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'My_secret key'

```

* ``/app/__init__.py``

```python
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes # Este import al final es intencinal para evitar los probles de dependencias circulares.
```

Al momento de tener que agregar un nuevo parametro de configuracion lo único que habria que hacer es agregarlo a la clase ``Config``.

## User Login Form

La extension de **Flask-WTF** utiliza clases de **Python** para representar WebForms. Los campos del Formulario son definidos como variables de clase. Cada campo es una instacia de un tipo de campo (``StringField()``, ``PasswordField()``, etc).
A los campos se le puede agregar una lista de ``validators``, como puede ser en este ejemplo ``DataRequired()``

* ``/app/forms.py``

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
```

## Form Templates

Los campos que son definidos en el Formulario, son renderizados en el template en forma automática. 

El argumento ``form.hidden_tag()`` genera un campo oculto que incluye un campo oculto token que es utilizado para proteger el formulario contro ataques **CSRF**.  

El ``<form>`` tiene 2 argumentos ``action`` y ``method``.  
``action`` indica a que *url* se tiene  que ir alenviar el formulario. Al dejar el valor en blanco redirecciona la ejecución al mismo url que hizo el llamdo.

* ``app/templates/login.html``

```html
{% extends "base.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}
        </p>
        <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

## Form Views

Para poder visualizar el formulario se necesita una nueva route que renderice ``login.html``. Vamos a enviar dentro del request una instancia del ``LoginForm()`` como parametro.

* **app/routes.py**

```python
from flask import render_template
from app import app
from app.forms import LoginForm

...
...

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

```

Para poder acceder a la ruta ``/login`` vamos a modificar ``base.html`` para agregarle un navigation bar.

* **app/templates/base.html**

```html
<div>
    Microblog:
    <a href="/index">Home</a>
    <a href="/login">Login</a>
</div>

```

## Receiving Form Data

* **app/routes.py**

```python
from flask import render_template, flash, redirect

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
```

Para poder permitir que la ruta reciba el Formulario se debe agregar el método ``POST`` al decorator.  
Por otro lado el método ``form.validate_on_submit()`` realiza todo el trabajo de procesamiento del Formulario. Este método devuelve ``False`` si el browser envia un ``GET`` request. En este caso salta el if y va directamente a hacer el render del Template.  

Cuando el browser envia un ``POST`` request, ``form.validate_on_submit()`` obtiene toda la data, ejecuta todas las validaciones y si todo esta bien, devuelve ``True``, lo que indica que los datos recibidos son validos y pueden ser procesados por la aplicación.  
Si alguna de las validaciones fallan, ``form.validate_on_submit()`` va a devolver ``False`` y va a realizar el render del template.

Cuando ``form.validate_on_submit()`` devuelve ``True``, se llama a la función ``flash()`` que sirve para mostrar mensajes al usuario (En este caso de confirmación). Luego de mostrar el mensaje, se llama la función ``redirect()`` para navegar automaticamente a otra pagina, en este caso ``index.html``


* **app/templates/base.html**

```html
<html>
    <head>
        {% if title %}
        <title>{{ title }} - microblog</title>
        {% else %}
        <title>microblog</title>
        {% endif %}
    </head>
    <body>
        <div>
            Microblog:
            <a href="/index">Home</a>
            <a href="/login">Login</a>
        </div>
        <hr>
        {% with messages = get_flashed_messages() %}
        {% if messages %}
        <ul>
            {% for message in messages %}
            <li>{{ message }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </body>
</html>
```

Cuando se llama a la función ``flash()``, Flask guarda los mensajes, pero no son mostrados a no ser que se especifique en el template donde se deben renderizar.
En Jinja2, ``with`` es utilizado para para asignar a la variable ``messages`` el resultado de llamar a la función ``get_flashed_messages()``.


## Improving Field Validation

Las validaciones que se agragan a los campos del formulario previenen que datos invalidos sean aceptados. La forma que la aplicacion maneja las entradas inválidas es mostrando nuevamente el formulario para permitirle al usuario hacer las correcciones que sean necesarias.  

El único cambio que haz que realizar es agregar ``for`` loops luego de cada campo para renderizar los mensajes de error.

* ``app/templates/login.html``

```html
{% extends "base.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}<br>
            {% for error in form.username.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}<br>
            {% for error in form.password.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```


## Generating Links

No es recomendable escribir los links directamente ni en los templates ni en los archivos de código fuente. Si en algún momento se decide reorganizar los links es complicado buscar todos los links para re escribirlos en forma correcta.  

Para tener un mejor control, Flask provee una función llamda ``url_for()``, que genera las URLs utilizando el mapeo interno. Por ejemplo: ``url_for('index'')`` devuelve ``/index``. El argumento de la función es el ``endpoint``, que en este caso es el nombre de la función.

* ``app/routes.py``: Use url\_for() function for links

```python
from flask import render_template, redirect, flash, url_for
from app import app
from app.forms import LoginForm

...

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

```

``url_for()`` también esta accesible en el los templates de ``Jinja2``

* ``app/templates/base.html``: Use url\_for() function for links

```html
    <div>
        Microblog:
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('login') }}">Login</a>
    </div>
```


## Referencias 
[The Flask Mega-Tutorial Part III: Web Forms](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms)  
[Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)  
[WTForms](https://wtforms.readthedocs.io/en/stable/)  