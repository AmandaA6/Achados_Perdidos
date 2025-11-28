from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import SessionLocal
from models.item import Item
import os, datetime

UPLOAD_FOLDER = "static/uploads"

item_bp = Blueprint("item", __name__, url_prefix="/itens")

# Listar itens
@item_bp.route("/")
def listar():
    db = SessionLocal()
    itens = db.query(Item).all()
    db.close()
    return render_template("item/listar.html", itens=itens)

# Cadastrar novo item
@item_bp.route("/novo", methods=["GET", "POST"])
def novo():
    db = SessionLocal()

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        local = request.form.get("local")
        data_str = request.form.get("data")
        status = request.form.get("status")

        data_obj = datetime.datetime.strptime(data_str, "%Y-%m-%d").date()

        arquivo = request.files["foto"]
        filename = None
        if arquivo and arquivo.filename != "":
            filename = arquivo.filename
            caminho = os.path.join(UPLOAD_FOLDER, filename)
            arquivo.save(caminho)

        novo_item = Item(
            nome=nome,
            descricao=descricao,
            local=local,
            data=data_obj,
            status=status,
            foto=filename
        )

        db.add(novo_item)
        db.commit()
        db.close()
        flash("Item cadastrado com sucesso!")
        return redirect(url_for("item.listar"))

    db.close()
    return render_template("item/novo.html")

# Excluir item
@item_bp.route("/excluir/<int:id>")
def excluir(id):
    db = SessionLocal()
    item = db.query(Item).filter_by(id=id).first()

    if item:
        db.delete(item)
        db.commit()

    db.close()
    flash("Item removido!")
    return redirect(url_for("item.listar"))
