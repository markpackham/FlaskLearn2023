from market import db
# database stored in "\instance\market.db"
from market import bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    # grab all items in one go so set "lazy" to True
    # this won't be stored as a column but as a relationship
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        # overide what is stored as password_hash so it actually becomes a hash
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            # show commas for large numbers, 3rd digit starting from right
            # so £1000 becomes £1,000
            return f'£{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'£{self.budget}'

    def check_password_correct(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_object):
        # returns true if user can afford item
        return self.budget >= item_object.price

    def can_sell(self, item_object):
        return item_object in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    # needed in order to have a relationship with User
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        # do exact opposite to "buy()"
        self.owner = None
        user.budget += self.price
        db.session.commit()