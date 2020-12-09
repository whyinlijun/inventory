from inventory import db

class ClothInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #ID,唯一默认
    date = db.Column(db.Date, index=True) #日期
    color_id = db.Column(db.Integer, db.ForeignKey('cloth.id')) #颜色代码
    length = db.Column(db.Float) #长度
    price = db.Column(db.Float)  #价格
    use_length = db.Column(db.Float, default=0.00) #已用长度
    use_finish = db.Column(db.Boolean, default=False) #用完标志
    memo = db.Column(db.Text) 

class Cloth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String(50), index=True)
    supplier = db.Column(db.String(50))
    width = db.Column(db.Float)
    fibre = db.Column(db.String(50))
    photo = db.Column(db.LargeBinary)
