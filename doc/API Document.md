# API Document

## Functions

1. Add item

2. Delete item

3. Update the price of item

4. Order

5. Show all lists

6. Search item



### 1. Add item

#### Instructions

| **Method** | **path**        | Request  (json body)                                         |
| ---------- | --------------- | ------------------------------------------------------------ |
| POST       | {{url}}/addItem | {   <br />     "item" : "aaa" (*string*),   <br />     "price" : 60 (*int*),   <br />     "quantity" : 100 (*int*)<br />} |

#### Response

* Successfully

  ```powershell
  {
    "statusCode": 200,
    "msg": "Successfully added"
  }
  ```

* Failed

  * Repeated addition

    ```powershell
    {
      "statusCode": 400,
      "msg": "Repeated addition"
    }
    ```

  * Parameter format error

    ```powershell
    {
      "statusCode": 400,
      "msg": "Parameter format error"
    }
    ```

### 2. Delete item

| **Method** | **path**           | Request        |
| ---------- | :----------------- | -------------- |
| GET        | {{url}}/deleteItem | id = 5 (*int*) |

#### Response

* Successfully

  ```powershell
  {
    "statusCode": 200,
    "msg": "Successfully deleted"
  }
  ```

* Failed

  * No such id

    ```powershell
    {
      "statusCode": 400,
      "msg": "No such id"
    }
    ```

### 3. Update the price of item

| **Method** | **path**            | Request                               |
| ---------- | ------------------- | ------------------------------------- |
| GET        | {{url}}/modifyPrice | id = 3 (*int*)<br />price =30 (*int*) |

#### Response

* Successfully

  ```powershell
  {
    "statusCode": 200,
    "msg": "Successfully change"
  }
  ```

* Failed

  * No such id

    ```powershell
    {
      "statusCode": 400,
      "msg": "No such id"
    }
    ```

### 4. Order

| **Method** | **path**      | Request  (json body)                                         |
| ---------- | ------------- | ------------------------------------------------------------ |
| post       | {{url}}/order | {<br />  "order": [<br />    {<br />      "item":"Brownie"(*string*),<br />      "orderQuantity": 1(*int*)<br />    },<br />    {<br />      "item":"Tiramisu"(*string*),<br />      "orderQuantity": 1(*int*)<br />    }<br />  ]<br />} |

#### Response

* Successfully

  ```powershell
  {
    "statusCode": 200,
    "msg": "Successfully change"
  }
  ```

* Failed

  * No such item

    ```powershell
    {
      "statusCode": 400,
      "msg": "order - No such item",
      "order": [],
      "total": 0
    }
    ```

  * Parameter format error

    ```powershell
    {
      "statusCode": 400,
      "msg": "order - Parameter format error",
      "order": [],
      "total": 0
    }
    ```

  * Understock

    ```powershell
    {
      "statusCode": 400,
      "msg": "order - Understock",
      "order": [],
      "total": 0
    }
    ```

    

### 5. Show all lists

| **Method** | **path**     | Request |
| ---------- | ------------ | ------- |
| GET        | {{url}}/list |         |

#### Response

* Successfully

  ```powershell
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

### 6. Search item

| **Method** | **path**       | Request                   |
| ---------- | -------------- | ------------------------- |
| GET        | {{url}}/select | item = "Scone" (*string*) |

#### Response

* Successfully

  ```powershell
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

* Failed

  * No such item

    ```powershell
    {
      "statusCode": 400,
      "msg": "No such item",
      "select": []
    }
    ```

### 







































































