from flask import Flask, request, g, current_app
import sqlite3 as sql
import json
import logging
import logging.config
logging.config.fileConfig('./logfile/logging.conf')
logger = logging.getLogger()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

database = "./sql/shopDatabase.db"


# Database link(資料庫連結)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(database)
    # logger.debug("get_db")
    return db  

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # logger.debug("close_connection")
        db.close()

# from werkzeug.local import LocalProxy
# db = LocalProxy(get_db)

# Database search data(資料庫搜尋資料)
def search(some: str, value):  # Use value search some
    con = get_db()
    cur = con.cursor()
    grammar = "SELECT * FROM PRODUCT WHERE " + some + " =?;"
    cur.execute(grammar, (value,))
    row = cur.fetchall()
    logger.debug("search - "+json.dumps(row))
    return row


# Show all list (顯示所有列表API)
@app.route('/list', methods=['GET'])
def list():
    with app.app_context():
        try:
            arr = []
            con = get_db()
            cur = con.cursor()
            cur.execute("select * from PRODUCT")
            rows = cur.fetchall()
            logger.debug(rows)
            for i in range(len(rows)):
                if rows[i][4] == 1:
                    arr.append({
                        "id": rows[i][0],
                        "item": rows[i][1],
                        "price": rows[i][2],
                        "quantity": rows[i][3]
                    })
            statusCode = 200
            msg = "Successfully"
            logger.info("list - Successfully")
        except:
            con.rollback()
            statusCode = 500
            msg = "Failed"
            logger.info("list - Error")
        finally:
            con.close()
            results = {
                "statusCode": statusCode,
                "msg": msg,
                "list": arr
            }
            logger.debug("list - "+json.dumps(results))
            return results


# Add item (新增資料API)
@app.route('/addItem', methods=['POST'])
def addItem():
    with app.app_context():
        try:
            con = get_db()
            logger.debug("addItem - "+json.dumps(request.json))
            item = request.json['item']
            price = request.json['price']
            quantity = request.json['quantity']
            if item == "" or str(item).isspace(): # item is None
                statusCode = 400
                msg = "Parameter format error"
                logger.info("addItem - Parameter format error")
            elif type(price) != int or type(quantity) != int: # price or quantity are not int
                statusCode = 400
                msg = "Parameter format error"
                logger.info("addItem - Parameter format error")
            elif price < 0 or quantity < 0: # price or quantity are < 0
                statusCode = 400
                msg = "Parameter format error"
                logger.info("addItem - Parameter format error")
            else:
                row = search("item", item)
                if row: 
                    if row[0][4] == 0: # data isDelete staus change false
                        cur = con.cursor()
                        cur.execute("UPDATE PRODUCT SET isDelete = ? WHERE id = ?;",(1, row[0][0],))
                        cur.execute("UPDATE PRODUCT SET price = ? WHERE id = ?;",(price, row[0][0],))
                        cur.execute("UPDATE PRODUCT SET quantity = ? WHERE id = ?;",(quantity, row[0][0],))
                        con.commit()
                        statusCode = 200
                        msg = "Successfully added"
                        logger.info("addItem - Record successfully change isDelete staus")
                    else: # data already exists
                        statusCode = 400
                        msg = "Repeated addition"
                        logger.info("addItem -  Record repeated addition")
                else:
                    cur = con.cursor()
                    cur.execute(
                        "INSERT INTO PRODUCT(item,price,quantity) VALUES (?,?,?)", (item, price, quantity))
                    con.commit()
                    statusCode = 200
                    msg = "Successfully added"
                    logger.info("addItem - Record successfully added")
        except:
            con.rollback()
            statusCode = 500
            msg = "Add failed"
            logger.info("addItem - Error in insert operation")

        finally:
            con.close()
            results = {
                "statusCode": statusCode,
                "msg": msg,
            }
            logger.debug("addItem - "+json.dumps(results))
            return results


# Delete item (刪除資料API)
@app.route('/deleteItem', methods=['GET'])
def deleteItem():
    with app.app_context():
        try:
            con = get_db()
            id = request.args['id']
            if id.isdigit():
                id = int(id)
                row = search("id", id)
                if row and row[0][4] == 1:# data already exists and isn't delete staus
                    cur = con.cursor()
                    # cur.execute("DELETE FROM PRODUCT WHERE id=?", (id,))
                    cur.execute("UPDATE PRODUCT SET isDelete = ? WHERE id = ?;",(0, id,))
                    con.commit()
                    statusCode = 200
                    msg = "Successfully deleted"
                    logger.info("deleteItem - Record successfully deleted")
                else:
                    statusCode = 400
                    msg = "No such id"
                    logger.info("deleteItem - No such id")
            else:
                statusCode = 400
                msg = "Parameter format error"
                logger.info("deleteItem - Parameter format error")
        except:
            con.rollback()
            statusCode = 500
            msg = "Delete failed"
            logger.info("deleteItem - Error in delete operation")
        finally:
            con.close()
            results = {
                "statusCode": statusCode,
                "msg": msg,
            }
            logger.debug("deleteItem - "+json.dumps(results))
            return results


# Update the price of item(更改特定品項價錢API)
@app.route('/modifyPrice', methods=['GET'])
def modifyPrice():
    with app.app_context():
        try:
            con = get_db()
            id = int(request.args['id'])
            price = int(request.args['price'])
            row = search("id", id)
            if row and row[0][4] == 1:# data already exists and isn't delete staus
                cur = con.cursor()
                cur.execute("UPDATE PRODUCT SET price=? WHERE id=?;", (price, id,))
                con.commit()
                statusCode = 200
                msg = "Successfully change"
                logger.info("modifyPrice - Record change successfully")
            else:
                statusCode = 400
                msg = "No such id"
                logger.info("modifyPrice - No such id")
        except:
            con.rollback()
            statusCode = 500
            msg = "Change failed"
            logger.info("modifyPrice - Error in change operation")
        finally:
            con.close()
            results = {
                "statusCode": statusCode,
                "msg": msg,
            }
            logger.debug("modifyPrice - "+json.dumps(results))
            return results


# Order (下單API)
@app.route('/order', methods=['POST'])
def order():
    with app.app_context():
        try:
            con = get_db()
            arr = []
            total = 0
            order = request.json["order"]
            logger.debug("order - "+json.dumps(order))
            for i in range(len(order)):
                tmp = order[i]
                item = tmp['item']
                orderQuantity = tmp['orderQuantity']
                if orderQuantity == 0: # order quantity is 0
                    arr = []
                    tmpStr = json.dumps(orderQuantity)
                    logger.debug("order - "+ item +" orderQuantity:" + tmpStr)
                    statusCode = 400
                    msg = "order - Parameter format error"
                    logger.info("order - Order quantity is 0")
                    break
                row = search("item",item)
                if row and row[0][4] == 1:
                    sum = row[0][3] - orderQuantity
                    if  sum < 0:# quantity not enough
                        arr = []
                        logger.debug("order - "+ item +" inventoryQuantity: " + str(sum))
                        statusCode = 400
                        msg = "order - Understock"
                        logger.info("order - Inventory quantity not enough")
                        break
                    else : # data already exists and isn't delete staus
                        arr.append({
                            "id": row[0][0],
                            "item": row[0][1],
                            "price": row[0][2],
                            "orderQuantity": orderQuantity
                        })
                        logger.info("order - OrderArr add item "+row[0][1])
                else:
                    arr = []
                    statusCode = 400
                    msg = "order - No such item"
                    logger.info("order -  No such item")
                    break
            logger.debug("order - len(order):"+ str(len(order)) +" len(arr):"+str(len(arr)))
            if arr:
                for i in range(len(arr)): 
                    tmpItem = arr[i]
                    total = total + (tmpItem["price"]*tmpItem["orderQuantity"])
                    row = search("item",tmpItem["item"])
                    remaingQuantity = row[0][3] - tmpItem["orderQuantity"]
                    cur = con.cursor()
                    cur.execute("UPDATE PRODUCT SET quantity = ? WHERE id = ?;",(remaingQuantity, tmpItem["id"],))
                    con.commit()
                statusCode = 200
                msg = "Successfully order"
                logger.info("order - Record successfully order")
        except:
            con.rollback()
            statusCode = 500
            arr = []
            msg = "Order failed"
            logger.info("order - Error in order operation")
        finally:
            con.close()
            results = {
                "statusCode": statusCode,
                "msg": msg,
                "order": arr,
                "total": total
            }
            logger.debug("order -"+ json.dumps(results))
            return results


# Search item (搜尋特定品項API)
@app.route('/select', methods=['GET'])
def select():
    with app.app_context():
        try:
            con = get_db()
            arr = []
            item = request.args['item']
            logger.debug("select - item :" + item)
            row = search("item", item)
            logger.debug("select - " + json.dumps(row))
            if row and row[0][4]==1:
                # for i in range(len(row)):
                arr.append({
                    "id": row[0][0],
                    "item": row[0][1],
                    "price": row[0][2],
                    "quantity": row[0][3]
                })
                statusCode = 200
                msg = "Successfully select"
                logger.info("select - Record select successfully")
            else:
                statusCode = 400
                msg = "No such item"
                logger.info("select - No such item")
        except:
            con.rollback()
            statusCode = 500
            msg = "Selection failed"
            logger.info("select - Error in select operation")
        finally:
            con.close()
            results = {
                "statusCode": statusCode,
                "msg": msg,
                "select": arr
            }
            logger.debug("select - "+json.dumps(results))
            return results
