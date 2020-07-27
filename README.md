# Online shop template

Andrew Raftovich

This shop template was built to be used to help set up a working shop with little to no work on the backend and a focus on frontend design for a quick deployment. This site uses a database designed to fit most potential products and a full admin panel to modify products, view & update orders, and analytical data about sales.

## Shop routes

| Page      | Route  |
| ------    | ------ |
| Home      | /      |
| Analytics | /Dashboard |
| Edit     | /Dashboard/Products  |
| Orders   | /Dashboard/Orders    |
| Login    | /Dashboard/Login     |
| Logout   | /Dashboard/Logout    |
| Checkout | /Order/<int: id>     |
| Complete | /Complete/<int: id>  |

## RESTful API routes
   
| Function | Route |
| ------ | ------  |
| `GET` all products | /products |
| `GET` a single product | /products/<int: id> |
| `POST` new product | /products/new |
| `PUT` `DELETE` update products | /products/<int: id>/update  |
| `GET` customer orders | /products/orders |
| `POST` admin login | /login  |
| `POST` customer login | /customer |
| `POST` purchase   | /purchase  |
| `POST` make payment | /charge  |
| `GET` check payment | /charge/<charge_id> |

## TODO

- [ ] Remove ability to delete products and set a product toggle
  - Purchase products that contain enabled property
  - set to disabled when stock hits 0
  - ability to toggle product on admin panel
  - setup product quantity to api
- [ ] combine API purchase and charge routes
- [ ] Develop scripts to access analytics, cost & orders per day/month/year
- [ ] Ability to hold multiple images in database w/ primary image
- [ ] Build analtyics panel
- [ ] Build storefront
- [ ] Develop cart component
- [ ] Build order page
  - Customer checkout form
  - returning customer form w/ login
- [ ] Improve admin login page
- [ ] customer order status script by id
- [ ] Order info page
- [ ] Fix api purchase route to save product name in table instead of id
- [ ] Test and Fix database first time setup to include admin user credentials
- [ ] Set up database foreign key between orders and customers

Future tasks:
- [ ] Deploy to Heroku
- [ ] Email server
  - Flask email templates w/ order updates

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

## First time setup

Recommended development software:
- [pgAdmin 4](https://www.postgresql.org/)
- [Postman](https://www.postman.com/)

1. setup a PostgreSQL database
2. Setup a stripe account and get a stripe payment secret_key
3. Set environment variables in a .env file according to server/settings.py

## Built with

- [Flask](https://flask.palletsprojects.com/en/1.1.x/),
- [Vue.js](https://vuejs.org/)
- [Postgresql](https://www.postgresql.org/)
- [Stripe](https://stripe.com/)