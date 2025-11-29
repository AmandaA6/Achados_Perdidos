from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import SessionLocal
from models.item import Item
import os, datetime

UPLOAD_FOLDER = "static/uploads"

item_bp = Blueprint("item", __name__, url_prefix="/itens")

# LISTAR TODOS OS ITENS
@item_bp.route("/")
def listar():
    db = SessionLocal()
    itens = db.query(Item).all()
    db.close()
    return render_template("item/listar.html", itens=itens)

# LISTAR PENDENTES
@item_bp.route("/pendentes")
def pendentes():
    db = SessionLocal()
    itens = db.query(Item).filter_by(status="pendente").all()
    db.close()
    return render_template("item/listar.html", itens=itens)

# LISTAR ENCONTRADOS
@item_bp.route("/encontrados")
def encontrados():
    db = SessionLocal()
    itens = db.query(Item).filter_by(status="encontrado").all()
    db.close()
    return render_template("item/listar.html", itens=itens)

# CADASTRAR ITEM
@item_bp.route("/novo", methods=["GET", "POST"])
def novo():
    db = SessionLocal()

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        local = request.form.get("local")
        data_str = request.form.get("data")

        status = "pendente"

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

# MARCAR COMO ENCONTRADO
@item_bp.route("/marcar_encontrado/<int:id>", methods=["GET", "POST"])
def marcar_encontrado(id):
    db = SessionLocal()
    item = db.query(Item).filter_by(id=id).first()

    if not item:
        db.close()
        flash("Item não encontrado!")
        return redirect(url_for("item.listar"))

    if request.method == "POST":
        item.status = "encontrado"
        item.nome_encontrou = request.form.get("nome_encontrou")
        item.contato_encontrou = request.form.get("contato_encontrou")
        item.data_encontrado = datetime.datetime.now().date()

        db.commit()
        db.close()
        flash("Item marcado como encontrado!")
        return redirect(url_for("item.listar"))

    db.close()
    return render_template("item/marcar_encontrado.html", item=item)

# EDITAR ITEM
@item_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    db = SessionLocal()
    item = db.query(Item).filter_by(id=id).first()

    if not item:
        db.close()
        flash("Item não encontrado!")
        return redirect(url_for("item.listar"))

    if request.method == "POST":
        item.nome = request.form.get("nome")
        item.descricao = request.form.get("descricao")
        item.local = request.form.get("local")

        data_str = request.form.get("data")
        item.data = datetime.datetime.strptime(data_str, "%Y-%m-%d").date()

        arquivo = request.files["foto"]
        if arquivo and arquivo.filename != "":
            if item.foto and os.path.exists(os.path.join(UPLOAD_FOLDER, item.foto)):
                os.remove(os.path.join(UPLOAD_FOLDER, item.foto))
            
            filename = arquivo.filename
            caminho = os.path.join(UPLOAD_FOLDER, filename)
            arquivo.save(caminho)
            item.foto = filename

        db.commit()
        db.close()
        flash("Item atualizado com sucesso!")
        return redirect(url_for("item.listar"))

    db.close()
    return render_template("item/editar.html", item=item)

# EXCLUIR ITEM
@item_bp.route("/excluir/<int:id>")
def excluir(id):
    db = SessionLocal()
    item = db.query(Item).filter_by(id=id).first()

    if item:
        if item.foto and os.path.exists(os.path.join(UPLOAD_FOLDER, item.foto)):
            os.remove(os.path.join(UPLOAD_FOLDER, item.foto))
        
        db.delete(item)
        db.commit()

    db.close()
    flash("Item removido!")
    return redirect(url_for("item.listar"))
