from flask import Flask, render_template,request,jsonify
import requests
import mysql.connector
mydb=mysql.connector.connect(host="127.0.0.1",user="root",passwd="1111",database="grocery_billing")
mycursor=mydb.cursor()
app = Flask(__name__)

@app.route('/checkout', methods=['POST'])
def checkout():
    cart_items = request.json['cartItems']
    bill=[]
    total=0
    for i in cart_items:
        itemname=i['name']
        price=i['price']
        quantity=i['quantity']
        query = f"INSERT INTO `grocery_billing`.`bills` (`item`, `quantity`, `price_per_unit`, `total_price`, `created_at`) VALUES ('{itemname}', {quantity}, {price}, {quantity * price}, NOW());"
        mycursor.execute(query)
        mydb.commit()
        bill.append(itemname)
        total+=price*quantity
    items_str = ', '.join(bill)
    query = "INSERT INTO customers_bill (items, total_price) VALUES (%s, %s)"
    values = (items_str, total)
    mycursor.execute(query,values)
    mydb.commit()
    return jsonify({'message': 'Cart items received successfully'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
