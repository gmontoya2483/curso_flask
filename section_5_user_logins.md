# Section 5 - User Logins

[Volver al README.md](README.md)

En esta sección se muestra como crear un subsistema de login de usuario.

## Contenido

* [Password Hashing](#password-hashing)
* [Introducción a Flask-Login](#introduccin-a-flask-login)
* [Preparando el modelo de usuario para Flask-Login](#preparando-el-modelo-de-usuario-para-flask-login)
* [User Loader Function](#user-loader-function)
* [Logging Users in](#logging-users-in)
* [Logging Users Out](#logging-users-out)
* [Requiring Users To Login](#requiring-users-to-login)
* [Showing The Logged In User in Templates](#showing-the-logged-in-user-in-templates)
* [User Registration](#user-registration)
* [Referencias](#referencias)




## Password Hashing

Para poder guardar los passwords de los usuarios en la base de datos, es preferible no guardarlas en forma plana. Flask 
hace uso del paquete ``Werkzeug`` que implementa la funcionalidad de *password  hashing*

Ejemplo:

```console
(venv) $ flask shell
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:06:47) [MSC v.1914 32 bit (Intel)] on win32
App: app [production]
Instance: C:\Users\Gabriel\OneDrive\Projects\curso-flask\instance

>>> from werkzeug.security import check_password_hash
>>> from werkzeug.security import generate_password_hash
>>> hash = generate_password_hash('foobar')
>>> hash
'pbkdf2:sha256:50000$8Bqq9AS0$0cc56d388d85c78e92b0c60dd9ebe8ef4d720814dd98eb9e58d510d06e17c4ba'
>>>
>>> check_password_hash(hash, 'foobar')
True
>>> check_password_hash(hash, 'barfoo')
False
>>>
>>> hash = generate_password_hash('foobar')
>>> hash
'pbkdf2:sha256:50000$f2TgFn6q$6a86134a3461c0fdbff81a02b4712f3b99a6861b96ae1ebf181dc69a89759155'
>>> check_password_hash(hash, 'foobar')
True
>>>
>>> exit()

(venv) $
```

*Werkzeug* en su modulo security tiene 2 funciones que sirven para el manejo de passwords, ``generate_password_hash()``
y ``check_password_hash()``.


La lógica completa del password hashing se puede implementar como 2 nuevos metodos in modelo de ``User``.

* app/models.py

```python
from werkzeug.security import generate_password_hash, check_password_hash

# ...

class User(db.Model):
    # ...

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

Teniendo estos 2 metodos, un objeto de usuario puede realizar en forma segura la verificación del password sin la necesidad de almacenar el password original en la base de datos.

```console
(venv) $ flask shell
Python 3.7.0b3 (default, Mar 30 2018, 04:35:22)
[GCC 7.3.0] on linux
App: app [production]
Instance: /mnt/c/Users/Gabriel/OneDrive/Projects/curso-flask/instance
>>> u = User(username='susan', email='susan@example.com')
>>> u.set_password('mypassword')
>>> u.check_password('anotherpassword')
False
>>> u.check_password('mypassword')
True
>>> u.password_hash
'pbkdf2:sha256:50000$Y57Dfvn5$2bd08debcd11b1e0a39302ef51b32e8c15fd0d4bf0a7b34af1cad60c390b0716'
>>> exit()
(venv) $

```

## Introducción a Flask-Login

La extensión *Flask-Login* los estados de login del usuario. Esto es que los usuarionse logean a la aplicación
y navegan por disitintas páginas mientras la aplicacion recuerda que el usuario esta logueado.  
También provee la funcionalidad de *Recordarme* que permite a los usuarios permanecer logueados icluso luego de 
cerrar el Navegador.

Para instalar *Flask-Login*:  

```console
(venv) $ pip install flask-login
```

Como cualquier otra extensión de Flask, *Flask-Login* necesita ser creada al momento que la aplicación es 
instanciada.

* app/__init__.py

```python
# ...
from flask_login import LoginManager

app = Flask(__name__)
# ...
login = LoginManager(app)

# ...
```

## Preparando el modelo de usuario para Flask-Login

La extensión *Flask-Login* trabaja con el modelo de usuario de la applicación y espera ciertas propiedades y metodos que 
sean implementados.

Los cuatro items requeridos son los siguientes:

* ``is_authenticated``: una propiedad que devuelve ``True`` si el usuario tiene credenciales válidas o 
de lo contrario, ``False``.

* ``is_active``: una propiedad que devuelve ``True`` si la cuenta de usuario esta activa, o de lo contrario 
devuelve ``False``

* ``is_anonymous``: una propiedad que devuelve ``False`` para usuarios regulares, y devuelve ``True`` para un usario anónimo.  

* ``get_id()``: Es un método que devuelve un el identificador único como un string para un usuario.

Estas propiedades y métodos pueden falcilmente ser creados pero dado que su implementación es generica,  
*Flask-Login* provee una clase *mixin* llamada ``UserMixin`` que incluye una implementación genericas de estos items. 
Esta implemetantion es apropiada para la mayoria de los modelos de Usuario que se utilicen. 

Para agregar la clase *mixin* al modelos, basta con hacer que la clase ``User`` herede  también de la clase ``UserMixin``:  

* app/models.py

```python
# ...
from flask_login import UserMixin

class User(UserMixin, db.Model):
    # ...

``` 

## User Loader Function

*Flask-Login* mantiene el seguimiento del usuario logeado guardando su identificador único el *user session* de Flask, 
un espacio de alamacenamiento asignado a cada usuario que se conecta a la aplicación. Cada vez que el usuario 
que esta logeado navega a una nueva pagina, *Flask-Logein* trae el el ID del usuario desde la *session* y carga el 
usuario en la memoria.

Debido a que *Flask-Login* conoce nada de la base de datos, es necesario que a la aplicación la ayude a cargar el usuario. 
Por esta razón, *Flask-Login* espera que la aplicacion configure una funcion *user loader*, que pueda ser llamada para cargar usuario 
pasandole un ID. Esta funcón puede ser agregada en el modulo *app/models.py*

* app/models.py

```python

from app import login
# ...

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

```

El *user loader* es registrado con el decorador ``@login.user_loader``. El ``id`` que *Flask-Login* pasa a la función 
como un argumento va ser un *string*, por lo que dado que la base de datos utiliza los ids numéricos, es necesario
 convertirlos a ``integer``
 
 
 
## Logging Users in
 
* app/routes.py
 
 ```python

# ...
from flask_login import current_user, login_user
from app.models import User

# ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

```

Las dos primeras lineas de la función ``login()`` son para no permitir que un usuario que ya este logeado puede acceder al 
``/login``. En este caso es redirigido a ``/index``.  
La variable ``current_user`` viene con ``Flask-Login`` y puede ser utilizada en cualquier momento durante el manejo para 
para obtener el usuario que hizo el request. El valor de esta variable puede ser un objeto de User desde la base de datos, 
o un anonimo si el usuario todavia no se logueo.

El siguiente paso es cargar el usuario de la base de datos y también se hace el checkeo del password. En caso que el usuario 
no exista o que el password sea invalido, se muestra un mensage de usario o password invalido y se redirige al usuario
 nuevamnte a la pagina de ``/login``.  
 
 En caso que el usuario y el password sean correctos, se llama a la función ``login_user()``, que viene con *Flask-Login*.
 Esta función registra el usuario como logeado, lo que significa que cada vez que el usuario navegue por la applicacion la 
 variable ``current_user`` va a estar seteada con este usuario.
 
 Finalmente el ususario es redirigido a la página ``/index``
 
 
## Logging Users Out

* app/routes.py

```python
# ...
from flask_login import logout_user

# ...

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
```

* app/templates/base.html

```html
    <div>
        Microblog:
        <a href="{{ url_for('index') }}">Home</a>
        {% if current_user.is_anonymous %}
        <a href="{{ url_for('login') }}">Login</a>
        {% else %}
        <a href="{{ url_for('logout') }}">Logout</a>
        {% endif %}
    </div>
```

La propiedad ``is_anonymous`` es uno uno de los atributos que ``Flask-Login`` agrega a los objetos de ``User`` a través 
de la clase ``UserMixin``. La expresion ``current_user.is_anonymous`` va ser ``True`` solo cuando el usuario no este logueado.


## Requiring Users To Login

*Flask-Login* provee una funcionalidad muy útil que fuerza a los usuarios a a estar logueados antes que estos puedan ver 
ciertas páginas de la applicación. Si un usuario que no esta logueado intenta ver una página protegida, *Flask-logi* lo 
redirecciona al formulario de login y sólo lo redirecciona a la página que queria ver una vez que el usuario esta loguedo.  

Para poder implementar el redireccionamiento a la página de login, *Flask-Login* necesita saber cual es la función que 
maneja el login. Esto pude ser agregado dentro del *app/__init__.py*.  

```python
# ...

login = LoginManager(app)
login.login_view = 'login'

```

El valor *'login'* es el nombre de la función (o el endpoint) para la vista de login (la pagina login). Es decir el 
nombre que se usa en las llamadas a ``url_for()``.  

La forma en que *Flask-Login* protege una vista de usuarios anonimos es mediente el decorador ``@login_required``. 
Cuando este decorador es agregado **debajo**del decorador ``@app.route``, la función pasa a estar protegida y no va a 
permitir el acceso a usuarios no autenticados.

* app/routes.py

```python
from flask_login import login_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    # ...
```

Lo que habria que hacer es implementar el redireccionamiento a la pagina solicitada luego que el login fue exitoso. 
Cuando un usuario intenta ingrasar auna pagina protegida sin estar logeado, este va a ser redirigido a a la pagina de login, 
este redireccionamiento va a incluir cierta información extra de modo que la aplicacion puede volver a la pagina que fue
originalmente solicitada.
 
Por ejemplo, si un usuario que no esta logueado intenta ingresar a */index*, el decorador ``@login_required`` va a 
interceptar el requerimiento y va a redireccionar al usuario a la página de */login*, asimismo va a agregar el 
argumento *next* a la URL, el cual posee la url original del llamado (*/login?next=/index*).
 
Este argumento puede ser capturado y asi una vez que el usario se loguea a la aplicacion en lugar de ser redirigido a 
una página determinada, se lo puede redirigir a la pagina que estuvo intentando ingresar. 
 
* app/routes.py
 
```python
from flask import request
from werkzeug.urls import url_parse

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ...
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # ... 
 
 ```
 
 Una vez que el usuario es logueaod utilizando la función ``login_user()``, el valor del argumento ``next`` es obtenido 
 desde la variable ``request``. Esta variable posee toda la informacion que el cliente envia con el request. 
 El atributo ``request.args`` expone el contenido del query string en un diccionario.

Existen 3 casos posibles:

* Que no exista el argumento ``next``, entonces el usuario es redireccionado a la página index.
* Que la url tenga el argumento ``next`` que hace referencia a un path relativo (es decir sin el dominio). En este caso 
el usuario es redireccionado a la pagina indicada en ele argumento next.
* Que la url tenga el argumento ``next``, pero este hace referencia a un full path es decir con dominio. En este caso la 
el usuario es redirigido a la página index.

Este último caso, se debe a hacer la aplicacion mas segura . Puede ser posible que un atacante inserte una a URL a un sitio 
malisioso en el argumento ``next``. Esto podemos evistarlo haciendo que nuestra applicaion solo redirecciones URL relativas, 
lo que asegura que siempre vamos a estar dentro de nuestra aplicacion. para poder determinar si la URL es relativa o 
absoluta, se la parsea con la la función ``url_parse()`` de ``Werkzeug`` y luego se chequea si existe el componente ``netloc``.


## Showing The Logged In User in Templates

Para mostrar el usuario actual en el template, se puede usar el el ``current_user`` de ``Flask-Login``.

* app/templates/index.html

```html
{% extends "base.html" %}

{% block content %}
    <h1>Hi, {{ current_user.username }}!</h1>
    {% for post in posts %}
    <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
    {% endfor %}
{% endblock %}
```

Tabien debemos sacar el argumento ``user`` del redenr de ``/index``

* app/routes.py

```python

@app.route('/')
@app.route('/index')
@login_required
def index():
    
    # ...

    return render_template('index.html', title='Home Page', posts=posts)

```


## User Registration

* app/forms.py

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

# ...

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
            
```

Además de las validaciones estádares ``DataRequired``, ``Email`` y ``EqualTo``, se agregaron 2 metodoas ``validate_username()`` 
y ``validate_email()``. Cuando se agregan metodos a un Formulario que cumplan con el patrón ``vaidate_<field_name>``, 
*WTForms* los considera como *custom validators* y los invoca junto con los validadores estádares. En este caso se esta validando 
que tanto el username como el email sean únicos. En caso que ya existan en la base de datos se dispara la excepcioón ``ValidationError``.  


Para mostrar el la pagina para registrar un usuario:

* app/templates/register.html

```html

{% extends "base.html" %}

{% block content %}
    <h1>Register</h1>
    <form action="" method="post">
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}<br>
            {% for error in form.username.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.email.label }}<br>
            {{ form.email(size=64) }}<br>
            {% for error in form.email.errors %}
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
        <p>
            {{ form.password2.label }}<br>
            {{ form.password2(size=32) }}<br>
            {% for error in form.password2.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}

```

También se debe agregar un link en la pagina de login que permita abrir la página de registro:

* app/templates/login.html

```html
<p>New User? <a href="{{ url_for('register') }}">Click to Register!</a></p>
```


Finalmente se debe agregar la ruta que maneje el registro de nuevos usarios.

* app/routes.py

```python
from app import db
from app.forms import RegistrationForm

# ...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
```


## Referencias 
[The Flask Mega-Tutorial Part V: User Logins](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins)  
[Werkzeug](http://werkzeug.pocoo.org/)  
[Flask-Login](https://flask-login.readthedocs.io/en/latest/)  
