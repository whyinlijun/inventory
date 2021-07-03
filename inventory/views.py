#_*_ coding:utf-8 _*_
from flask import render_template, redirect, url_for, request
from inventory import app, db
from inventory.forms import ClothForm
from inventory.models import Cloth, Customer, Goods, Orders, OrderDetail


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

@app.route('/addgoods/<goodsname>/<goodsprice>')
def add_goods(goodsname, goodsprice):
    gs = Goods(name=goodsname, price=float(goodsprice))
    db.session.add(gs)
    db.session.commit()
    return goodsname+goodsprice

@app.route('/getprice')
def get_price():
    if 'id' in request.values:
        price = Goods.query.get(int(request.values.get('id')))
    return str(price.price)

@app.route('/')
def index():
    od = Orders.query.all()
    odt = OrderDetail.query.all()
    return render_template('index.html', data={'od':od, 'odt':odt})

@app.route('/addorder', methods=['POST', 'GET'])
def addOrder():
    custom=Customer.query.all()
    goods = Goods.query.all()
    if request.method=="POST":
        add_order()
        return redirect(url_for('ordersList'))
    return render_template("addorder.html", data={'custom':custom, 'goods':goods})

@app.route('/orderslist')
def ordersList():
    od = Orders.query.order_by(db.desc(Orders.id)).all()
    ods = OrderDetail.query.order_by(db.desc(OrderDetail.order_id)).all()
    return render_template('listorders.html', data={'od':od, 'ods':ods})

@app.route('/orderview/<orderid>')
def orderView(orderid):
    od = Orders.query.filter(Orders.id==orderid).first()
    ods = OrderDetail.query.filter(OrderDetail.order_id==orderid).all()
    return render_template('orderview.html', data = {'od':od, 'ods':ods})

@app.route('/orderdel/<orderid>')
def orderDel(orderid):
    od = Orders.query.filter(Orders.id==orderid).first()
    ods = OrderDetail.query.filter(OrderDetail.order_id==orderid).all()
    db.session.delete(od)
    for item in ods:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('ordersList'))

@app.route('/orderupdate/<orderid>', methods=['POST', 'GET'])
def orderUpdate(orderid):
    od = Orders.query.filter(Orders.id==orderid).first()
    ods = OrderDetail.query.filter(OrderDetail.order_id==orderid).all()
    custom=Customer.query.all()
    goods = Goods.query.all()

    if request.method=='POST':
        db.session.delete(od)
        for item in ods:
            db.session.delete(item)

        add_order()
        return redirect(url_for('ordersList'))


    return render_template("orderupdate.html", data={'custom':custom, 'goods':goods, 'od':od, 'ods':ods,'xuhao':1})

def add_order():
    order = Orders()
    order.id = request.form.get('order_id')
    order.customer = request.form.get('customer')
    order.date = request.form.get('order_date')
    order.amount = int(request.form.get('order_amount'))
    order.quantity = float(request.form.get('order_quantity'))
    db.session.add(order)

    for x, y, z in zip(
        request.form.getlist('goods_id'), [int(x) for x in request.form.getlist('quantity')], request.form.getlist('amount')):
        od = OrderDetail()
        od.order_id = request.form.get('order_id')
        od.goods_id=x
        od.goods_quantity=y
        od.goods_amount=z
        db.session.add(od)
    db.session.commit()


