from flask import Flask, render_template, request, redirect, url_for
from models import db, Product, Location, ProductMovement
from sqlalchemy import func, case
from sqlalchemy.orm import aliased

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# ---------- HOME ----------
@app.route('/')
def home():
    return redirect(url_for('products'))

# ---------- PRODUCTS ----------
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/product/add', methods=['POST'])
def add_product():
    product_id = request.form['product_id']
    name = request.form['name']
    db.session.add(Product(product_id=product_id, name=name))
    db.session.commit()
    return redirect(url_for('products'))

@app.route('/product/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('edit_product.html', product=product)

@app.route('/product/delete/<product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))

# ---------- LOCATIONS ----------
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/location/add', methods=['POST'])
def add_location():
    location_id = request.form['location_id']
    name = request.form['name']
    db.session.add(Location(location_id=location_id, name=name))
    db.session.commit()
    return redirect(url_for('locations'))

@app.route('/location/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    if request.method == 'POST':
        location.name = request.form['name']
        db.session.commit()
        return redirect(url_for('locations'))
    return render_template('edit_location.html', location=location)

@app.route('/location/delete/<location_id>')
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    return redirect(url_for('locations'))

# ---------- MOVEMENTS ----------
@app.route('/movements')
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('movements.html', movements=movements, products=products, locations=locations)

@app.route('/movement/add', methods=['POST'])
def add_movement():
    movement = ProductMovement(
        from_location=request.form.get('from_location') or None,
        to_location=request.form.get('to_location') or None,
        product_id=request.form['product_id'],
        qty=int(request.form['qty'])
    )
    db.session.add(movement)
    db.session.commit()
    return redirect(url_for('movements'))

@app.route('/movement/edit/<int:movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    products = Product.query.all()
    locations = Location.query.all()
    if request.method == 'POST':
        movement.product_id = request.form['product_id']
        movement.from_location = request.form.get('from_location') or None
        movement.to_location = request.form.get('to_location') or None
        movement.qty = int(request.form['qty'])
        db.session.commit()
        return redirect(url_for('movements'))
    return render_template('edit_movement.html', movement=movement, products=products, locations=locations)

@app.route('/movement/delete/<int:movement_id>')
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    return redirect(url_for('movements'))

# ---------- REPORT ----------
@app.route('/report')
def report():
    destination = aliased(Location)

    results = db.session.query(
        Product.name.label('product'),
        destination.name.label('location'),
        (
            func.coalesce(func.sum(
                case(
                    (ProductMovement.to_location == destination.location_id, ProductMovement.qty),
                    else_=0
                )
            ), 0) -
            func.coalesce(func.sum(
                case(
                    (ProductMovement.from_location == destination.location_id, ProductMovement.qty),
                    else_=0
                )
            ), 0)
        ).label('balance')
    ).join(ProductMovement, Product.product_id == ProductMovement.product_id)\
     .join(destination, ProductMovement.to_location == destination.location_id)\
     .group_by(Product.name, destination.name)\
     .all()

    return render_template('report.html', results=results)

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)
