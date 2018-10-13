from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


from app import routes # Este import al final es intencinal para evitar los probles de dependencias circulares.