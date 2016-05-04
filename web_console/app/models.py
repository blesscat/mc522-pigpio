from app import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    permission = db.Column(db.Integer)

    def __init__(self, username=None, password=None, permission=15):
        self.username = username
        self.password = password
        self.permission = permission

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def update_password(self, newPassword):
        self.password = generate_password_hash(newPassword)
        db.session.commit()
        return self.password


class monitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lcd = db.Column(db.String(100))
    addr = db.Column(db.String(100))
    dice = db.Column(db.String(100))
    attr = db.Column(db.String(100))

    def __init__(self, lcd='0', addr='None', dice='0 0 0 0 0 0', attr='None'):
        self.lcd = lcd
        self.addr = addr
        self.dice = dice
        self.attr = attr

    def update_db(self, data):
        if data[0] == 'lcd':
            self.lcd = data[1]
        if data[0] == 'addr':
            self.addr = data[1]
        if data[0] == 'dice':
            self.dice = data[1]
        if data[0] == 'attr':
            self.attr = data[1]
        db.session.commit()
