from flask import Blueprint, render_template, request, redirect, url_for, session
from models.usuario import Usuario
from models.database import SessionLocal  # <-- AGORA FUNCIONA!

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        with SessionLocal() as db:
            usuario_existente = db.query(Usuario).filter_by(email=email).first()

            if usuario_existente:
                return render_template("usuario/cadastro.html", erro="Email já cadastrado")

            db.add(Usuario(nome=nome, email=email, senha=senha))
            db.commit()

        return redirect(url_for("usuario.login"))

    return render_template("usuario/cadastro.html")

@usuario_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        with SessionLocal() as db:
            usuario = db.query(Usuario).filter_by(email=email, senha=senha).first()

        if usuario:
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            return redirect(url_for("index"))

        return render_template("usuario/login.html", erro="Email ou senha incorretos")

    return render_template("usuario/login.html")

@usuario_bp.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('usuario.login'))
    with SessionLocal() as db:
        usuario = db.query(Usuario).get(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)

@usuario_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

