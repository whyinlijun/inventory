from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class ClothForm(FlaskForm):
    color_name = StringField("颜色名称", validators=[DataRequired(),])
    supplier = StringField("供应商", validators=[DataRequired()])
    width = FloatField('门幅宽度', validators=[DataRequired(),])
    firbe = SelectField('材质', choices=('全棉', '棉绸', '雪纺'))
    submit = SubmitField('添加')
