# Project scope
- Developed fully functioning API project for the Little Lemon restaurant so that the client application developers can use the APIs to develop web and mobile applications. People with different roles will be able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders. 
- Created one single Django app called LittleLemonAPI and implement all API endpoints in it. Use pipenv to manage the dependencies in the virtual environment.
1. need to deal with 3 types of persons (Managers, Customers and Delivery crew)
   - user registration and authentication
      - `http://127.0.0.1:8000/api/users/`
   - assign users to groups or remove users from groups
      - `http://127.0.0.1:8000/api/users/{userId}/groups`
2. assign work to users
3. If manager:
   -  add, edit, and remove menu items
   -  Managers should also be able to update any user to a delivery person.
4. If customer (if a user doesn't belong to any specific group you should consider them a customer):
   - able to browse menu items, filter them by categories, and price ranges, and search menu items. 
5. You need to create APIs that will allow customers to add menu items to their cart and place an order. But here's the catch, the cart must be emptied when the order is successfully created
6. You can also add an API endpoints to flush the cart at any point. One customer should only be able to have one cart at a time, and one cart should be able to contain multiple menu items.
- The Delivery process:
1. First, you need API endpoints for the managers to browse the orders and assign them to a delivery person. 
2.  Managers should also be able to filter orders by their status, like delivered and not delivered.
3.  If Delivery person:
    -  After successful authentication, delivery people should be able to browse orders assigned to them by using your API endpoints and mark them as delivered. 
4.  Customers can always come to the orders endpoint to see their orders, including the status of that order and the total price.
5.  Throttling Process:
    - Finally, you will need to implement some throttling for the APIs you built, limit it to five API calls per minute. 
6.  While working on this project, please ensure that your API endpoints support only the required HTTP methods, and always return the appropriate status code with the response. 

## Tools:
- You should use VS Code for writing the code, 
- you will need to use Django with Django REST framework or DRF, 
- and everything should work in a virtual environment. For testing and debugging you can use insomnia,
-  use only the packages and libraries you learned about earlier in this course. 
-  Just one last thing, if you use a session authentication class during the development, make sure to comment that out before submission. The finished project should only support token-based authentication.

## User Groups:
- In this project you will deal with three types of users, __managers, customers, and the delivery crew__.
- You'll start with the user registration and authentication process that each user will use, then you will create API endpoints that can be used to assign users to a group like manager or a delivery person.
## use djsoer (User registration and token generation endpoints)
1. API end point: http://127.0.0.1:8000/api/users/ 
- method: GET, as a admin access all users list
- method: POST, Creates a new user with name, email and password
1. API end point: http://127.0.0.1:8000/api/token/login/
- method: POST, Anyone with a valid username and password Generates access tokens that can be used in other API calls in this project (need to pass username and password in body)
1. API end point: http://127.0.0.1:8000/api/users/me
- method: GET, Anyone with a valid user token Generates access tokens that can be used in other API calls in this project
## Admin endpoints
1. API end point: http://127.0.0.1:8000/api/admin/users-list/
- method: GET, as a admin able to return all list of users
2. API end point: http://127.0.0.1:8000/api/admin/groups/
- method: GET, as a admin able to return all list of groups
3. API end point: http://127.0.0.1:8000/api/admin/users/
- method: POST, as a admin able to add user to manager's group (need to pass Body tab-> Form data -> `username: manager1`)
- method: DELETE, as a admin able to delete user from manager's group (need to pass Body tab-> Form data -> `username: manager1`)
## User group management endpoints (Manager)
1. API end point: http://127.0.0.1:8000/api/groups/manager/users/
- method: GET
   - as a manager able to Returns all managers
   - as a customer, delivery crew or admin Denies access and returns 401 – Unauthorized
- method: POST
   - as a manager able to Assigns the user in the payload to the manager group and returns 201-Created (need to pass Body tab-> Form data -> `username: manager1`)
   - as a customer, delivery crew or admin Denies access and returns 401 – Unauthorized 
1. API end point: http://127.0.0.1:8000/api/groups/manager/users/{userid}
   - as a manager able to Removes this particular user from the manager group and returns 200 – Success if everything is okay. If the user is not found, returns 404 – Not found
   - as a customer, delivery crew or admin Denies access and returns 401 – Unauthorized 
## User group management endpoints (Delivery Crew)
1. API end point: http://127.0.0.1:8000//api/groups/delivery-crew/users
- method: GET
   - as a manager able to Returns all delivery-crew members
   - as a customer, delivery crew or admin Denies access and returns 401 – Unauthorized
- method: POST
   - as a manager able to Assigns the user in the payload to the delivery-crew group and returns 201-Created (need to pass Body tab-> Form data -> `username: dc1`)
   - as a customer, delivery crew or admin Denies access and returns 401 – Unauthorized 
1. API end point: http://127.0.0.1:8000//api/groups/delivery-crew/users/{userid}
   - as a manager able to Removes this particular user from the delivery-crew group and returns 200 – Success if everything is okay. If the user is not found, returns 404 – Not found
   - as a customer, delivery crew or admin Denies access and returns 401 – Unauthorized 

## Category End points:
1. API end point: http://127.0.0.1:8000/api/category/
- method: GET
   - as a customer, delivery crew and manager able to access Lists all category items. Return a 200 – Ok HTTP status code
- method: POST
   - as a manager able to Creates a new category item and returns 201 - Created
   - as a customer or delivery crew or admin Denies access and returns 401 – Unauthorized HTTP status code (not create)
1. API end point: http://127.0.0.1:8000/api/category/1/ {categoryid=1}
- method: GET
   - as a manager, customer or delivery crew member able to access single category item
- method: PUT
   - as a manager able to Updates single category item
   - as a customer or delivery crew member or admin Denies access and returns 401 – Unauthorized HTTP status code
- method: PATCH
   - as a manager able to partial updates single category item
   - as a customer or delivery crew member or admin Denies access and returns 401 – Unauthorized HTTP status code
- method: DELETE
   - as a manager able to delete single category item
   - as a customer or delivery crew member or admin Denies access and returns 401 – Unauthorized HTTP status code
## Menu-items End points:
1. API end point: http://127.0.0.1:8000/api/menu-items/
- method: GET
   - as a customer, delivery crew and manager able to access Lists all menu items. Return a 200 – Ok HTTP status code
- method: POST
   - as a manager able to Creates a new menu item and returns 201 - Created
   - as a customer or delivery crew or admin Denies access and returns 403 – Unauthorized HTTP status code (not create)
1. API end point: http://127.0.0.1:8000/api/menu-items/1/ {menuitemid=1}
- method: GET
   - as a manager, customer or delivery crew member able to access single menu item
- method: PUT
   - as a manager able to Updates single menu item
   - as a customer or delivery crew member or admin Denies access and returns 401 – Unauthorized HTTP status code
- method: PATCH
   - as a manager able to partial updates single menu item
   - as a customer or delivery crew member or admin Denies access and returns 401 – Unauthorized HTTP status code
- method: DELETE
   - as a manager able to delete single menu item
   - as a customer or delivery crew member or admin Denies access and returns 401 – Unauthorized HTTP status code
## Cart management endpoints (customer)
1. API end point: http://127.0.0.1:8000/api/cart/menu-items/
- method: GET
   - as a customer to Returns current items in the cart for the current user token
   - as a manager, dc or admin Denies access and returns 401 – Unauthorized HTTP status code
- method: POST
   - as a customer to Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items
   - as a manager, dc or admin Denies access and returns 401 – Unauthorized HTTP status code
- method: DELETE
   - as a customer Deletes all menu items created by the current user token
   - as a manager, dc or admin Denies access and returns 401 – Unauthorized HTTP status code
## Order management endpoints
1. API end point: http://127.0.0.1:8000/api/orders/
- method: GET
   - as a manager to Returns all orders with order items by all users
   - as a delivery crew member to Returns all orders with order items assigned to the delivery crew
   - as a customer to Returns all orders with order items created by this user
- method: POST
   - as a customer to Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user.
   - as a manager, dc or admin Denies access and returns 401 – Unauthorized HTTP status code
2. API end point: http://127.0.0.1:8000/api/orders/1/ {orderId=1}
- method: GET
   - as a customer able to Returns all items for this order id. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code.
   - as delivery crew member or admin or manager Denies access and returns 401 – Unauthorized HTTP status code
- method: PUT
   - as a manager able to updates order item and also update the order status to 0 or 1.
          - If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery.
          - If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered.
   - as a dc, admin or customer Denies access and returns 401 – Unauthorized HTTP status code
- method: PATCH
   - as a manager able to Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1.
          - If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery.
          - If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered.
   - as a delivery crew member to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order.
   - as a unassigned dc or customer Denies access and returns 401 – Unauthorized HTTP status code
- method: DELETE
   - as a manager able to Deletes this order
   - as a dc, admin or customer Denies access and returns 401 – Unauthorized HTTP status code


