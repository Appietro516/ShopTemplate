# Online shop template

Andrew Raftovich

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
    $ npm run serve
    ```

    Navigate to [http://localhost:8080](http://localhost:8080)

## Build with

Flask, Vue.js, Postgresql