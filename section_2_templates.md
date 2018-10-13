# Section 2 - Templates

[Volver al README.md](README.md)

El objetivo de esta sección es explicar que son los templates en flask y el uso de Jinja2.


## Contenido

* [Que son los Templates](#que-son-los-templates)
* [Conditional Statement](#conditional-statement)
* [Loops](#loops)
* [Herencia de Templates](#herencia-de-templates)
* [Macros](#macros)
* [Filters](#filters)
* [Desarrollar nuestros propios Filters](#desarrollar-nuestros-propios-filters)
* [Referencias](#referencias)

## Que son los Templates

Flas por default lee los templates desde una carpeta llamada ``templates``. Dentro de esta carpeta se deben guardar los archivos html que van a ser renderizados.  
Para poder mostrar el tempalte se debe llamar la funcion ``render_template`` que viene con flask. Esta función tiene que ser importada ``from flask import render_template``.  
Dentro del llamo a esta funcion se puenden pasar parametros que van a ser utilizados por el template que esta siendo renderizado.

### Ejemplo

* **/app/templates/index.html**

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }} - Microblog</title>
    </head>
    <body>
        <h1> Hi, {{ user.username }}</h1>
    </body>
    </html>
    ```

* **/app/routes.py**

    ```python
    from flask import render_template
    from app import app
    
    
    @app.route('/')
    @app.route('/index')
    def index():    
        user = {'username': 'gabriel'} # Faked user
        return render_template('index.html', user=user, title='Home')
    ```

## Conditional Statement

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {% if title %}
    <title>{{ title }} - Microblog</title>
    {% else %}
    <title>Welcome to Microblog</title>
    {% endif %}
</head>
<body>
    <h1> Hi, {{ user.username }}</h1>
</body>
</html>
```

## Loops

* ``/app/routes.py``

    ```python
    from flask import render_template
    from app import app
    
    
    @app.route('/')
    @app.route('/index')
    def index():
        user = {'username': 'gabriel'} # Faked user
    
        # Faked Posts
        posts = [
            {
                'author': {'username': 'John'},
                'body': 'Beautiful day in Vienna'
            },
            {
                'author': {'username': 'Gsbriel'},
                'body': 'Beautiful day in Buenos Aires'
            },
            {
                'author': {'username': 'Sandrita'},
                'body': 'Beautiful day in China'
            }
        ]
    
        return render_template('index.html', user=user, title='Home', posts=posts)
    
    ```

* ``/app/templates/index.html``
    
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        {% if title %}
        <title>{{ title }} - Microblog</title>
        {% else %}
        <title>Welcome to Microblog</title>
        {% endif %}
    </head>
    <body>
        <h1> Hi, {{ user.username }}</h1>
        {% for post in posts %}
        <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
        {% endfor %}
    </body>
    </html>
    ```

## Herencia de Templates

Se utiliza para rederizar secciones que son comunes a varios templates, como puede ser un Navbar, footer, etc.


* ``/app/templates/base.html``
    
    ```html
    <!DOCTYPE html>
    <html lang="en">
      <head>
          <meta charset="UTF-8">
          {% if title %}
              <title>{{ title }} - Microblog</title>
          {% else %}
              <title>Welcome to Microblog</title>
          {% endif %}
      </head>
      <body>
          <div>
              Microblog: <a href="/index">Home</a>
          </div>
          {% block content %} {% endblock %}
      </body>
    </html>
    ```

* ``/app/templates/index.html``
    
    ```html
    {% extends "base.html" %}

    {% block content %}
      <h1> Hi, {{ user.username }}</h1>
      {% for post in posts %}
        <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
      {% endfor %}
    {% endblock %}
    ```


## Macros

Los macros son como funciones pero para templates, 

* ``macros.py``

    ```python
    from flask import Flask, render_template
    
    app = Flask(__name__)
    
    
    @app.route('/')
    def index():
        myList = [123, 345, 4343, 545]
        myOtherList = [122, 3234, 34534, 65464]
        return render_template('index.html', name='Gsbriel', my_list=myList, my_other_list=myOtherList)
    
    
    if __name__ == '__main__':
        app.run(debug=True)
    
    ```

* ``/templates/index.html``

    ```html
    {% from "_macros.html" import hello %}
    {% from "_macros.html" import displayNumbers %}
    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        {{ hello(name) }}
        <hr>
        {{ displayNumbers(my_list) }}
        <hr>
        {{ displayNumbers(my_other_list) }}
    </body>
    </html>
    ```

* ``/templates/_macros.html``

    ```html
    {% macro hello(name) %}
        <h1>Hello, {{ name }}</h1>
    {% endmacro %}
    
    {% macro displayNumbers(numbers) %}
        <ul>
          {% for num in numbers %}
            <li>{{ num }}</li>
            {% endfor %}
        </ul>
    {% endmacro %}
    ```

## Filters

Esta sección se va implementar mas adelante

## Desarrollar nuestros propios Filters

Esta sección se va implementar mas adelante

## Referencias 
[The Flask Mega-Tutorial Part II: Templates](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates)  
[Jinja webSite](http://jinja.pocoo.org/)  
[Jinja 2.10 Documentation](http://jinja.pocoo.org/docs/2.10/)  
[Flask Templates Documentation](http://flask.pocoo.org/docs/1.0/templating/)