from flask import render_template
from inventory import app
from inventory.forms import ClothForm

@app.route('/')
def index():
    form = ClothForm()
    return render_template('add_cloth.html', form=form)