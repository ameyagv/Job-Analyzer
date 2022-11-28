from flask import jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from src.app import db
import uuid


class User:

    def startSession(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return (jsonify(user), 200)

    def signup(self):
        print(request.form)
        user = {
            '_id': uuid.uuid4().hex,
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            }
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        if db.users.find_one({'email': user['email']}):
            return (jsonify({'error': 'Email address already in use'}),
                    400)

        if db.users.insert_one(user):
            return self.startSession(user)

        return (jsonify({'error': 'Signup failed'}), 400)

    def logout(self):
        session.clear()
        return redirect('/')

    def login(self):

        user = db.users.find_one({'email': request.form.get('email')})

        if user and pbkdf2_sha256.verify(request.form.get('password'),user['password']):
            return self.startSession(user)

        return (jsonify({'error': 'Invalid login credentials'}), 401)
