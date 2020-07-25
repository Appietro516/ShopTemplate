# Online shop template

Andrew Raftovich

This project is an active working shop with the ability to modify items & view product analytics on an admin panel located on the frontend

## Shop routes

| Page      | Route  |
| ------    | ------ |
| Home      | /      |
| Analytics | /dashboard |
| Edit     | /dashboard/products  |
| Login    | /dashboard/login     |
| Logout   | /dashboard/logout    |
| Checkout | /order/<int: id> |

## RESTful API routes

| Function | Route |
| ------ | ------ |
| `GET` all products | /products |
| `GET` a single product | /products/<int: id> |
| `POST` new product | /products/new |
| `PUT` `DELETE` update products | /products/<int: id>/update  |
| `POST` make payment | /charge |
| `GET` check payment | /charge/<charge_id> |
| `POST` login | /login |

## Build for development

1. Run the server-side Flask app in one terminal window:

    ```sh
    $ cd server
    $ python3.7 -m venv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ python app.py
    ```

    Navigate to [http://localhost:5000](http://localhost:5000)

2. Run the client-side Vue app in a different terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run serve
    ```

    Navigate to [http://localhost:8080](http://localhost:8080)

## Build with

Flask, Vue.js, Postgresql

## Payment manager

[Stripe](https://stripe.com/)

### Code foundation

Server setup is from [this tutorial](https://testdriven.io/blog/accepting-payments-with-stripe-vuejs-and-flask/) for setting up shop payments, & a working flask and vue.js servers.