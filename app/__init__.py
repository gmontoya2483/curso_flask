from flask import Flask

app = Flask(__name__)

from app import routes # Este import al final es intencinal para evitar los probles de dependencias circulares.