"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route('/api/cupcakes')
def list_cupcakes():
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes', methods = ["POST"])
def create_cupcake():
    new_cupcake = Cupcake(flavor=request.json["flavor"], rating=request.json["rating"],
    size=request.json["size"], image=request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.to_dict()), 201)

@app.route('/api/cupcakes/<int:id>', methods = ["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:id>', methods = ["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")

@app.route('/')
def show_cupcakes():
    return render_template('index.html')