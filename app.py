from flask import Flask, render_template
from models.database import Base, engine
from controllers.usuario_controller import usuario_bp
from controllers.item_controller import item_bp

from models.item import Item
from models.usuario import Usuario

app = Flask(__name__)
app.secret_key = "chave-secreta"

Base.metadata.create_all(engine)

app.register_blueprint(usuario_bp)
app.register_blueprint(item_bp)  

@app.route("/")
def index():
    return render_template("index.html")

