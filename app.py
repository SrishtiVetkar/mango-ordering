from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'mango_order_123'  


# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mango_orders'
app.config['MYSQL_PORT'] = 3307


mysql = MySQL(app)
@app.route('/login', methods=['GET', 'POST'])  
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'farmer' and password == '1234':
            return redirect(url_for('dashboard'))  
        else:
            return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        mobile = request.form['mobile']
        mango_type = request.form['mango_type']
        quantity = request.form['quantity']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orders (name, address, mobile, mango_type, quantity, status) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (name, address, mobile, mango_type, quantity, 'Pending'))
        mysql.connection.commit()
        cur.close()

        return render_template('success.html', name=name)
    return render_template('order.html')


@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()

    # Summary Counts
    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders WHERE status='Pending'")
    pending_orders = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders WHERE status='Approved'")
    approved_orders = cur.fetchone()[0]

    cur.close()

    return render_template('dashboard.html', orders=orders, total_orders=total_orders, pending_orders=pending_orders, approved_orders=approved_orders)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/update_status/<int:order_id>/<string:new_status>')
def update_status(order_id, new_status):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET status=%s WHERE id=%s", (new_status, order_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('dashboard'))

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE id=%s", (order_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)
