from flask import Flask, request
import sqlite3 as sql
import json

app = Flask(__name__)

database = "shopDatabase.db"


def getData():
    with sql.connect(database) as con:
        cur = con.cursor()
        cur.execute("select * from PRODUCT")
        rows = cur.fetchall()
        return rows


@app.route('/list', methods=['GET'])
def list():
    db = getData()
    print(db)
    arr = []
    for i in range(len(db)):
        arr.append({
            "id" : db[i][0],
            "item" : db[i][1],
            "price" : db[i][2],
            "quantity" : db[i][3]
            })

    return json.dumps(arr)


@app.route('/addItem', methods=['POST'])
def addItem():
    try:
        item = request.form['item']
        price = request.form['price']
        quantity = request.form['quantity']

        with sql.connect(database) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO PRODUCT(item,price,quantity) VALUES (?,?,?)", (item, price, quantity))
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"

    finally:
        con.close()
        return msg


@app.route('/deleteItem/<int:id>', methods=['GET'])
def deleteItem(id):
    id = int(id)
    try:
        with sql.connect(database) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM PRODUCT WHERE id=?", (id))
            con.commit()
            msg = "Record successfully deleted"
    except:
        con.rollback()
        msg = "error in delete operation"
    finally:
        con.close()
        return msg


@app.route('/modifyPrice/<int:id>/<int:pic>', methods=['GET'])
def modifyPrice(id, pic):
    id = int(id)
    price = int(pic)
    try:
        with sql.connect(database) as con:
            cur = con.cursor()
            cur.execute("UPDATE PRODUCT SET price=? WHERE id=?;", (pic, id))
            con.commit()
            msg = "Record change successfully"
    except:
        con.rollback()
        msg = "error in change operation"
    finally:
        con.close()
        return msg


@app.route('/order', methods=['POST'])
def order():
    try:
        order = request.json["order"]
        print(order)

        total = 0
        arr = []
        
        with sql.connect(database) as con:
            for i in range(len(order)):
                tmp =order[i]
                item = tmp['item']
                orderQuantity = tmp['orderQuantity']
                cur = con.cursor()
                cur.execute("SELECT * FROM PRODUCT WHERE item = ? ;", (item,))
                row = cur.fetchall()
                arr.append({
                    "id" : row[0][0],
                    "item" : row[0][1],
                    "price" : row[0][2],
                    "orderQuantity" : orderQuantity
                    })
                total = total + (arr[i]['price']*orderQuantity)
                remaingQuantity = row[0][3] - orderQuantity
                cur.execute("UPDATE PRODUCT SET quantity = ? WHERE id = ?;",(remaingQuantity,arr[i]['id'],))
                con.commit()
            msg = "Record successfully order"
        return {"msg": msg ,"order":arr,"total":total}
    except:
        con.rollback()
        return "error in order operation"

    finally:
        con.close()


@app.route('/select/<string:item>', methods=['GET'])
def select(item):
    with sql.connect(database) as con:
        # item = "\'"+item+"\'"
        print(item)
        cur = con.cursor()
        cur.execute("SELECT * FROM PRODUCT WHERE item = ? ;", (item,))
        row = cur.fetchall()
        print(row)
        arr = []
        for i in range(len(row)):
            arr.append({
                "id" : row[i][0],
                "item" : row[i][1],
                "price" : row[i][2],
                "quantity" : row[i][3]
                })

        return json.dumps(arr)