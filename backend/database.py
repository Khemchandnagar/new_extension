from flask import Flask, jsonify, render_template, request, session, redirect
from flask_mysqldb import MySQL
from datetime import timedelta


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'khem'
app.config['MYSQL_DB'] = 'face_extension'

mysql = MySQL(app)

class User:
    def __init__(self, id, email,image):
        self.id = id
        self.email = email
        self.image = image

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'image':self.image
        }



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    print(data)
    # Create a cursor to interact with the database
    cur = mysql.connection.cursor()

    # Execute the login query
    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cur.fetchone()

    # Close the cursor
    cur.close()

    # Check if the user exists in the database
    print(type(user))

    if user:
        # Successful login
        user = User(id=user[2], email=user[0], image=user[1])
        print(user.serialize())
        return jsonify({'message': 'Login successful', 'user': user.serialize()})
    else:
        # Failed login
        return jsonify({'message': 'Login failed'})






if __name__ == '__main__':
    app.run()
