from . import db
from flask_login import UserMixin
from datetime import datetime
USER_ROLE = "user"
STAFF_ROLE = "staff"
class Users(db.Model, UserMixin):
    def get_id(self):
        return self.phonenumber
    phonenumber = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(20))
    date_joined = db.Column(db.Date, default = datetime.utcnow)
    expenses = db.relationship('Expenses', backref='users')

class Expenses(db.Model):
    expense_id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    date_purchase = db.Column(db.String(10), nullable = False)
    amount = db.Column(db.Float, nullable=False)
    user = db.Column(db.String(100), db.ForeignKey('users.phonenumber'), nullable=False)


class staffs(db.Model, UserMixin):
    def get_id(self):
        return self.staffid
    staffid = db.Column(db.String(10), primary_key=True, unique=True,nullable=False)
    password = db.Column(db.String(200), nullable=False)




