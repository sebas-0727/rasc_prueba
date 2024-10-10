from flask import Blueprint, jsonify, request, redirect, url_for, render_template



mapa_blueprint = Blueprint('mapa', __name__)

@mapa_blueprint.route("/mapa")
def inicio():
    return render_template("mapa.html")

def init_app(app):
    app.register_blueprint(mapa_blueprint)
