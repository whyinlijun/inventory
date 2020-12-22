from flask import render_template, redirect, url_for, request
from inventory import app, db
from inventory.forms import ClothForm
from inventory.models import Cloth


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