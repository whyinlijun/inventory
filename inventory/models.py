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

    def __repr__(self):
        return '<Cloth %r>' % self.color_name

class Customer(db.Model):
    #客户信息表
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return '<Customer %r>' % self.name

class Goods(db.Model):
    #商品信息表
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    price = db.Column(db.Float)

    def __init__(self, name, price):
        self.name = name
        self.price = price


    def __repr__(self):
        return '<Goods %r>' % self.name

class Orders(db.Model):
    #订单表
    ID = db.Column(db.String(30), primary_key=True)
    customer = db.Column(db.String(20))
    date = db.Column(db.String(15), index=True)
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Float)

    def __repr__(self):
        return '<Orders %r>' % self.order_ID

class OrderDetail(db.Model):
    #订单详情
    id = db.Column(db.Integer, primary_key=True)
    order_ID = db.Column(db.String(30), index=True)
    goods_name = db.Column(db.String(30))
    goods_quantity = db.Column(db.Integer)
    goods_amount = db.Column(db.Float)






