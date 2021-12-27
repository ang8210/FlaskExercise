# API

## 簡介

| 功能                   | API                 | Input                                                        | Output |      |
| :--------------------- | ------------------- | ------------------------------------------------------------ | ------ | ---- |
| 新增品項(POST)         | {{url}}/addItem     | {<br /> "item" : "aaa" (*string*),<br /> "price" : 60 (*int*),<br /> "quantity" : 100 (*int*)<br />} |        |      |
| 刪除品項(GET)          | {{url}}/deleteItem  | id = 5 (*int*)                                               |        |      |
| 更改特定品項價格(POST) | {{url}}/modifyPrice | id = 5 (*int*)<br />price =65 (*int*)                        |        |      |
| 列出所有列表(GET)      | {{url}}/list        |                                                              |        |      |
| 搜尋特定品項(GET)      | {{url}}/select        | item = "bbb" (*string*)                                      |        |      |



 ## curl API

### addItem

$ curl -X POST "http://127.0.0.1:5000/addItem" -H 'Content-Type: application/json' -d '{"item":"eee","price":60,"quantity":100}'

### deleteItem

$ curl -X GET "http://127.0.0.1:5000/deleteItem?id=6"

### modifyPrice

$ curl -X GET "http://127.0.0.1:5000/modifyPrice?id=2&price=30"

### order

$ curl -X POST "http://127.0.0.1:5000/order" -H 'Content-Type: application/json' -d '{"order": [{"item":"ccc","orderQuantity": 30},{"item":"eee","orderQuantity": 50}]}'

### list

$ curl -X GET "http://127.0.0.1:5000/list" 

### select

$ curl -X GET "http://127.0.0.1:5000/select?item=aaa"