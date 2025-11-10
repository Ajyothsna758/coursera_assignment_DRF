# What are u going to do in this project
- You will create a fully functioning API project for the Little Lemon restaurant so that the client application developers can use the APIs to develop web and mobile applications.

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