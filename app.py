from flask import Flask, request
import sqlite3 as sql
import json
import logging
import logging.config
logging.config.fileConfig('./logfile/logging.conf')
logger = logging.getLogger()

app = Flask(__name__)

database = "shopDatabase.db"

@app.route('/list', methods=['GET'])
def list():
    try:
        with sql.connect(database) as con:
            cur = con.cursor()
            cur.execute("select * from PRODUCT")
            rows = cur.fetchall()
            logger.debug(rows)
            arr = []
            for i in range(len(rows)):
                arr.append({
                    "id" : rows[i][0],
                    "item" : rows[i][1],
                    "price" : rows[i][2],
                    "quantity" : rows[i][3]
                    })
            statusCode = 200
            msg = "Record successfully added"
    except:
        con.rollback()
        statusCode = 500
        msg = "error in insert operation"
    finally:
        con.close()
        results = {
            "statusCode" : statusCode,
            "msg" : msg,
            "list" : arr
        }
        return json.dumps(results)


@app.route('/addItem', methods=['POST'])
def addItem():
    try:
        # form-data
        # item = request.form['item']
        # price = request.form['price']
        # quantity = request.form['quantity']

        item = request.json['item']
        price = request.json['price']
        quantity = request.json['quantity']

        with sql.connect(database) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM PRODUCT WHERE item = ? ;", (item,))
            row = cur.fetchall()
            logger.debug(row)
            if row == None:
                cur.execute("INSERT INTO PRODUCT(item,price,quantity) VALUES (?,?,?)", (item, price, quantity))
                con.commit()
                statusCode = 200
                msg = "Record successfully added"
            else:
                statusCode = 400
                msg = "Record repeated addition"
    except:
        con.rollback()
        statusCode = 500
        msg = "error in insert operation"

    finally:
        con.close()
        results = {
            "statusCode" : statusCode,
            "msg" : msg,
        }
        return json.dumps(results)


@app.route('/deleteItem', methods=['GET'])
def deleteItem():
    id = int(request.args['id'])
    try:
        with sql.connect(database) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM PRODUCT WHERE id=?", (id,))
            con.commit()
            statusCode = 200
            msg = "Record successfully deleted"
    except:
        con.rollback()
        statusCode = 500
        msg = "error in delete operation"
    finally:
        con.close()
        results = {
            "statusCode" : statusCode,
            "msg" : msg,
        }
        return json.dumps(results)


@app.route('/modifyPrice', methods=['GET'])
def modifyPrice():
    id = int(request.args['id'])
    price = int(request.args['price'])
    try:
        with sql.connect(database) as con:
            cur = con.cursor()
            cur.execute("UPDATE PRODUCT SET price=? WHERE id=?;", (price, id))
            con.commit()
            statusCode = 200
            msg = "Record change successfully"
    except:
        con.rollback()
        statusCode = 500
        msg = "error in change operation"
    finally:
        con.close()
        results = {
            "statusCode" : statusCode,
            "msg" : msg,
        }
        return json.dumps(results)


@app.route('/order', methods=['POST'])
def order():
    try:
        order = request.json["order"]
        logger.debug(order)

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
            statusCode = 200    
            msg = "Record successfully order"
    except:
        con.rollback()
        statusCode = 500
        msg = "error in order operation"

    finally:
        con.close()
        results = {
            "statusCode" : statusCode,
            "msg" : msg,
            "order":arr,
            "total":total
        }
        return json.dumps(results)


@app.route('/select', methods=['GET'])
def select():
    try:
        item = request.args['item']
        with sql.connect(database) as con:
            # item = "\'"+item+"\'"
            logger.debug(item)
            cur = con.cursor()
            cur.execute("SELECT * FROM PRODUCT WHERE item = ? ;", (item,))
            row = cur.fetchall()
            logger.debug(row)
            arr = []
            for i in range(len(row)):
                arr.append({
                    "id" : row[i][0],
                    "item" : row[i][1],
                    "price" : row[i][2],
                    "quantity" : row[i][3]
                    })
            statusCode = 200    
            msg = "Select successfully order"
    except:
        con.rollback()
        statusCode = 500
        msg = "error in select operation"
    finally:    
        con.close()
        results = {
            "statusCode" : statusCode,
            "msg" : msg,
            "select":arr
        }
        return json.dumps(results)