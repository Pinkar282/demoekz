from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # only for demo

# In-memory storage (lists)
partners = []
managers = []
employees = []
hr = []  # кадровые записи
materials = []
suppliers = []
products = []
orders = []

# --- Utility functions ---
def find_by(field, value, collection):
    for i, item in enumerate(collection):
        if item.get(field) == value:
            return i, item
    return None, None

@app.context_processor
def inject_now():
    return {'datetime': datetime}

# ---------------- Routes ----------------
@app.route('/')
def index():
    return render_template('index.html', year=datetime.utcnow().year)

# Partners
@app.route('/partners')
def partners_page():
    return render_template('partners.html', partners=partners)

@app.route('/partners/add', methods=['POST'])
def add_partner():
    p = {
        'id': len(partners) + 1,
        'type': request.form.get('type',''),
        'name': request.form.get('name',''),
        'address': request.form.get('address',''),
        'inn': request.form.get('inn',''),
        'director': request.form.get('director',''),
        'phone': request.form.get('phone',''),
        'email': request.form.get('email',''),
        'logo': request.form.get('logo','logo.png'),
        'rating': float(request.form.get('rating') or 0),
        'sales_places': request.form.get('sales_places',''),
        'sales_history': request.form.get('sales_history',''),
        'rating_history': []
    }
    partners.append(p)
    flash('Партнер добавлен', 'success')
    return redirect(url_for('partners_page'))

# Managers: change partner rating
@app.route('/partners/<int:partner_id>/rating', methods=['POST'])
def change_partner_rating(partner_id):
    idx, p = find_by('id', partner_id, partners)
    if p:
        new_rating = float(request.form.get('rating') or p['rating'])
        reason = request.form.get('reason','')
        p['rating_history'].append({
            'old': p['rating'],
            'new': new_rating,
            'when': datetime.utcnow().isoformat(),
            'reason': reason
        })
        p['rating'] = new_rating
        flash('Рейтинг обновлён', 'success')
    return redirect(url_for('partners_page'))

# Materials
@app.route('/materials')
def materials_page():
    return render_template('materials.html', materials=materials)

@app.route('/materials/add', methods=['POST'])
def add_material():
    m = {
        'id': len(materials) + 1,
        'type': request.form.get('type',''),
        'name': request.form.get('name',''),
        'suppliers': request.form.get('suppliers',''),
        'qty_in_pack': request.form.get('qty_in_pack',''),
        'unit': request.form.get('unit','КГ'),
        'description': request.form.get('description',''),
        'image': request.form.get('image','placeholder.png'),
        'price': float(request.form.get('price') or 0),
        'stock_qty': float(request.form.get('stock_qty') or 0),
        'min_qty': 0,
        'history': []
    }
    materials.append(m)
    flash('Материал добавлен', 'success')
    return redirect(url_for('materials_page'))

# Suppliers
@app.route('/suppliers')
def suppliers_page():
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/suppliers/add', methods=['POST'])
def add_supplier():
    s = {
        'id': len(suppliers) + 1,
        'type': request.form.get('type',''),
        'name': request.form.get('name',''),
        'inn': request.form.get('inn',''),
        'supply_history': request.form.get('supply_history','')
    }
    suppliers.append(s)
    flash('Поставщик добавлен', 'success')
    return redirect(url_for('suppliers_page'))

# Products
@app.route('/products')
def products_page():
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['POST'])
def add_product():
    p = {
        'id': len(products) + 1,
        'article': request.form.get('article',''),
        'type': request.form.get('type',''),
        'name': request.form.get('name',''),
        'description': request.form.get('description',''),
        'image': request.form.get('image','placeholder.png'),
        'min_price': float(request.form.get('min_price') or 0),
        'size': request.form.get('size',''),
        'weight_net': request.form.get('weight_net',''),
        'weight_gross': request.form.get('weight_gross',''),
        'certificate': request.form.get('certificate',''),
        'standard_no': request.form.get('standard_no',''),
        'price_history': [],
        'time_to_make': request.form.get('time_to_make',''),
        'cost_price': request.form.get('cost_price',''),
        'workshop_no': request.form.get('workshop_no',''),
        'team_count': request.form.get('team_count',''),
        'materials': request.form.get('materials','')
    }
    products.append(p)
    flash('Продукция добавлена', 'success')
    return redirect(url_for('products_page'))

# Orders (Заявки)
@app.route('/orders')
def orders_page():
    return render_template('orders.html', orders=orders)

@app.route('/orders/add', methods=['POST'])
def add_order():
    o = {
        'id': len(orders) + 1,
        'partner': request.form.get('partner',''),
        'items': request.form.get('items',''),
        'status': 'Требуется предоплата',
        'created': datetime.utcnow().isoformat(),
        'prepay_due': (datetime.utcnow() + timedelta(days=3)).isoformat()
    }
    orders.append(o)
    flash('Заявка создана', 'success')
    return redirect(url_for('orders_page'))

@app.route('/orders/<int:order_id>/pay', methods=['POST'])
def pay_order(order_id):
    idx, o = find_by('id', order_id, orders)
    if o:
        o['status'] = 'Товар оплачен'
        flash('Заявка оплачена', 'success')
    return redirect(url_for('orders_page'))

@app.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    idx, o = find_by('id', order_id, orders)
    if o:
        o['status'] = 'Заказ отменен'
        flash('Заявка отменена', 'warning')
    return redirect(url_for('orders_page'))

# Employees
@app.route('/employees')
def employees_page():
    return render_template('employees.html', employees=employees)

@app.route('/employees/add', methods=['POST'])
def add_employee():
    e = {
        'id': len(employees)+1,
        'fio': request.form.get('fio',''),
        'birthdate': request.form.get('birthdate',''),
        'passport': request.form.get('passport',''),
        'bank': request.form.get('bank',''),
        'has_family': request.form.get('has_family','false'),
        'health': request.form.get('health','Здоров')
    }
    employees.append(e)
    flash('Сотрудник добавлен', 'success')
    return redirect(url_for('employees_page'))

# HR access (кадры)
@app.route('/hr')
def hr_page():
    return render_template('hr.html', hr=hr)

@app.route('/hr/add', methods=['POST'])
def add_hr():
    r = {
        'id': len(hr)+1,
        'fio': request.form.get('fio',''),
        'access': request.form.get('access','false') == 'true'
    }
    hr.append(r)
    flash('Кадровая запись добавлена', 'success')
    return redirect(url_for('hr_page'))

if __name__ == '__main__':
    app.run(debug=True)