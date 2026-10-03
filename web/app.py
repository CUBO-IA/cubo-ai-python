import os

from flask import Flask, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-cambia-esta-clave")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(300), nullable=False)


def crear_productos():
    if Producto.query.count() == 0:
        db.session.add_all(
            [
                Producto(
                    nombre="Laptop Lenovo",
                    descripcion="Laptop ideal para trabajo, estudio y entretenimiento.",
                    precio=699.99,
                    imagen="https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
                ),
                Producto(
                    nombre="Audífonos inalámbricos",
                    descripcion="Audífonos Bluetooth con excelente calidad de sonido.",
                    precio=49.99,
                    imagen="https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
                ),
                Producto(
                    nombre="Smartphone",
                    descripcion="Smartphone moderno con pantalla de alta resolución.",
                    precio=399.99,
                    imagen="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9",
                ),
                Producto(
                    nombre="Teclado mecánico",
                    descripcion="Teclado mecánico RGB para trabajar y jugar.",
                    precio=79.99,
                    imagen="https://images.unsplash.com/photo-1587829741301-dc798b83add3",
                ),
            ]
        )
        db.session.commit()


def cantidad_en_carrito():
    return sum(session.get("carrito", {}).values())


@app.route("/")
def index():
    return render_template(
        "index.html",
        productos=Producto.query.all(),
        cantidad_carrito=cantidad_en_carrito(),
    )


@app.route("/producto/<int:id>")
def producto(id):
    return render_template(
        "producto.html",
        producto=Producto.query.get_or_404(id),
        cantidad_carrito=cantidad_en_carrito(),
    )


@app.route("/carrito/agregar/<int:id>")
def agregar_carrito(id):
    Producto.query.get_or_404(id)
    carrito = session.get("carrito", {})
    id = str(id)
    carrito[id] = carrito.get(id, 0) + 1
    session["carrito"] = carrito
    return redirect(url_for("carrito"))


@app.route("/carrito/eliminar/<int:id>")
def eliminar_carrito(id):
    carrito = session.get("carrito", {})
    carrito.pop(str(id), None)
    session["carrito"] = carrito
    return redirect(url_for("carrito"))


@app.route("/carrito")
def carrito():
    items = []
    total = 0
    for id, cantidad in session.get("carrito", {}).items():
        producto = db.session.get(Producto, int(id))
        if producto:
            subtotal = producto.precio * cantidad
            items.append({"producto": producto, "cantidad": cantidad, "subtotal": subtotal})
            total += subtotal

    return render_template(
        "carrito.html",
        productos=items,
        total=total,
        cantidad_carrito=cantidad_en_carrito(),
    )


with app.app_context():
    db.create_all()
    crear_productos()


if __name__ == "__main__":
    app.run(debug=True)
