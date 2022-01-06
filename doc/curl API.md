# curl API
## addItem
### Successfully
```powershell
$ curl -X POST "http://127.0.0.1:5000/addItem" -H 'Content-Type: application/json' -d '{"item":"Puff ","price":45,"quantity":100}'
```
```powershell
#Response
{
  "statusCode": 200,
  "msg": "Successfully added"
}
```
### Failed
* Repeated addition
```powershell
$ curl -X POST "http://127.0.0.1:5000/addItem" -H 'Content-Type: application/json' -d '{"item":"Scone","price":55,"quantity":100}'
```
```powershell
#Response
{
  "statusCode": 400,
  "msg": "Repeated addition"
}
```
* Parameter format error
```powershell
$ curl -X POST "http://127.0.0.1:5000/addItem" -H 'Content-Type: application/json' -d '{"item":"                 ","price":-10,"quantity":-10}'
```
```powershell
#Response
{
  "statusCode": 400,
  "msg": "Parameter format error"
}
```
## deleteItem
### Successfully
```powershell
$ curl -X GET "http://127.0.0.1:5000/deleteItem?id=5"
```
```powershell
#Response
{
  "statusCode": 200,
  "msg": "Successfully deleted"
}
```
### Failed
* No such id
```powershell
  $ curl -X GET "http://127.0.0.1:5000/deleteItem?id=20"
```
```powershell
#Response
{
  "statusCode": 400,
  "msg": "No such id"
}
```
## modifyPrice
### Successfully
```powershell
$ curl -X GET "http://127.0.0.1:5000/modifyPrice?id=3&price=30"
```
```powershell
#Response
{
  "statusCode": 200,
  "msg": "Successfully change"
}
```
### Failed
* No such id
```powershell
$ curl -X GET "http://127.0.0.1:5000/modifyPrice?id=20&price=30"
```
```powershell
#Response
{
  "statusCode": 400,
  "msg": "No such id"
}
```
## order
### Successfully
```powershell
$ curl -X POST "http://127.0.0.1:5000/order" -H 'Content-Type: application/json' -d '{"order": [{"item":"Brownie","orderQuantity": 2},{"item":"Tiramisu","orderQuantity": 3}]}'
```
```powershell
#Response
{
  "statusCode": 200,
  "msg": "Successfully order", 
  "order": [
    {
      "id": 1,
      "item": "Brownie",       
      "price": 50,
      "orderQuantity": 2       
    },
    {
      "id": 2,
      "item": "Tiramisu",
      "price": 55,
      "orderQuantity": 3
    }
  ],
  "total": 265
}
```
### Failed
* No such item
```powershell
$ curl -X POST "http://127.0.0.1:5000/order" -H 'Content-Type: application/json' -d '{"order": [{"item":"Coke","orderQuantity": 2},{"item":"Tiramisu","orderQuantity": 1}]}'
```
```powershell
#Response
{
  "statusCode": 400,
  "msg": "order - No such item",
  "order": [],
  "total": 0
}
```
* Parameter format error
```powershell
$ curl -X POST "http://127.0.0.1:5000/order" -H 'Content-Type: application/json' -d '{"order": [{"item":"Brownie","orderQuantity": 0},{"item":"Tiramisu","orderQuantity": 1}]}'
```
```powershell
#Response
{
  "statusCode": 400,
  "msg": "order - Parameter format error",
  "order": [],
  "total": 0
}
```
* Quantity not enough
```powershell
$ curl -X POST "http://127.0.0.1:5000/order" -H 'Content-Type: application/json' -d '{"order": [{"item":"Macaron","orderQuantity": 1000},{"item":"Tiramisu","orderQuantity": 1}]}'
```
```powershell
#Response
{
  "statusCode": 400,
  "msg": "order - Understock",
  "order": [],
  "total": 0
}
```

## list
### Successfully
```powershell
$ curl -X GET "http://127.0.0.1:5000/list"
```
```powershell
#Response
{
  "statusCode": 200,
  "msg": "Successfully",
  "list": [
    {
      "id": 1,
      "item": "Brownie",
      "price": 50,
      "quantity": 98
    },
    {
      "id": 2,
      "item": "Tiramisu",
      "price": 55,
      "quantity": 98
    },
    {
      "id": 3,
      "item": "Macaron",
      "price": 30,
      "quantity": 100
    },
    {
      "id": 4,
      "item": "Scone",
      "price": 35,
      "quantity": 100
    },
    {
      "id": 7,
      "item": "Puff ",
      "price": 45,
      "quantity": 100
    }
  ]
}
```
## select
### Successfully
```powershell
$ curl -X GET "http://127.0.0.1:5000/select?item=Scone"
```
```powershell
#Response
{
  "statusCode": 200,
  "msg": "Successfully select",
  "select": [
    {
      "id": 4,
      "item": "Scone",
      "price": 35,
      "quantity": 100
    }
  ]
}
```
### Failed
* No such item
```powershell
$ curl -X GET "http://127.0.0.1:5000/select?item=Coke"
```
```powershell
#Response
{
  "statusCode": 400,
  "msg": "No such item",
  "select": []
}
```

