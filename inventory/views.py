from flask import render_template, redirect, url_for, request
from inventory import app, db
from inventory.forms import ClothForm
from inventory.models import Cloth, Customer, Goods


@app.route('/addcloth', methods=['GET', 'POST'])
def add_cloth():
    form = ClothForm()
    if form.validate_on_submit():
        cloth = Cloth(
                        color_name=form.color_name.data,
                        supplier=form.supplier.data,
                        width=form.width.data,
                        fibre=form.fibre.data
                        )
        db.session.add(cloth)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_cloth.html', form=form)

#顾客增加，GET方法，name名称
@app.route('/addcustomer')
def add_customer():
    if 'name' in request.values:
        customer = Customer(
                        name = request.values.get('name'),
                    )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('add_customer'))
    customers=Customer.query.all()
    cus_dict={}
    for item in customers:
        cus_dict[item.id]=item.name
    return cus_dict

@app.route('/getprice')
def get_price():
    if 'id' in request.values:
        price = Goods.query.get(int(request.values.get('id')))
        print(price.price)
    return str(price.price)

@app.route('/')
def index():
    datas = Cloth.query.all()
    for item in datas:
        print(item.color_name)
    return render_template('index.html', datas=datas)

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method=="POST":
        formData = request.form
        c_data = request.form.getlist('color')
        b_data = request.form.getlist('length')
        d_data = request.form.getlist('price')
        
        return ';'.join(c_data)+ ';'.join(b_data)+';'.join(d_data)
    return render_template("add_cloth_order.html")

@app.route('/test')
def test():
    custom=Customer.query.all()
    goods = Goods.query.all()
    return render_template("addorder.html", data={'custom':custom, 'goods':goods})