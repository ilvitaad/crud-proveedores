from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection
import psycopg2.extras

app = Flask(__name__)
app.secret_key =  "crud-proveedores-flask-2026"


# --- LEER (listado) ---
@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM proveedores ORDER BY id DESC")
    proveedores = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", proveedores=proveedores)


# --- CREAR ---
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():
    if request.method == "POST":
        datos = (
            request.form["nombre"],
            request.form["nit"],
            request.form["telefono"],
            request.form["correo"],
            request.form["direccion"],
            "activo" in request.form
        )

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO proveedores
            (nombre, nit, telefono, correo, direccion, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, datos)

        conn.commit()
        cur.close()
        conn.close()

        flash("Proveedor creado correctamente.")
        return redirect(url_for("index"))

    return render_template("form.html", proveedor=None)


# --- LEER UNO + ACTUALIZAR ---
@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
def editar_proveedor(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == "POST":
        datos = (
            request.form["nombre"],
            request.form["nit"],
            request.form["telefono"],
            request.form["correo"],
            request.form["direccion"],
            "activo" in request.form,
            id
        )

        cur.execute("""
            UPDATE proveedores SET
            nombre=%s,
            nit=%s,
            telefono=%s,
            correo=%s,
            direccion=%s,
            activo=%s
            WHERE id=%s
        """, datos)

        conn.commit()
        cur.close()
        conn.close()

        flash("Proveedor actualizado correctamente.")
        return redirect(url_for("index"))

    cur.execute("SELECT * FROM proveedores WHERE id=%s", (id,))
    proveedor = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("form.html", proveedor=proveedor)


# --- ELIMINAR ---
@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
def eliminar_proveedor(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM proveedores WHERE id=%s", (id,))

    conn.commit()
    cur.close()
    conn.close()

    flash("Proveedor eliminado.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)