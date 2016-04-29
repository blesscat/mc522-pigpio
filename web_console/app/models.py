import socket, threading, __builtin__

# from app import db
from werkzeug.security import generate_password_hash


# class User(db.Model):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     permission = db.Column(db.Integer)
#
#     def __init__(self, username=None, password=None, permission=15):
#         self.username = username
#         self.password = password
#         self.permission = permission
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return self.id
#
#     def get_username(self):
#         return self.username
#
#     def get_password(self):
#         return self.password
#
#     def update_password(self, newPassword):
#         self.password = generate_password_hash(newPassword)
#         db.session.commit()
#         return self.password


class data_pipe(threading.Thread):
    def __init__(self):
        super(data_pipe, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.sock.bind(('127.0.0.1', 9999))
        while True:
            data, __builtin__.addr = self.sock.recvfrom(1024)
            data = data.split(':')
            __builtin__.data[data[0]] = data[1]
