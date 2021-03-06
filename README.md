# py-monitaur

A simple monitoring application reversing probes from server to client.

Look at the examples directory for an idea on how to use it.

## Running on linux

```
$ git clone https://github.com/TwistTheNeil/py-monitaur.git
$ cd py-monitaur
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ flask init-db
$ FLASK_APP=app FLASK_ENV=production flask run
```

Substitute `FLASK_ENV=production` for `FLASK_ENV=dev` for development purposes.

Follow [Flask's documentation](http://flask.pocoo.org/docs/1.0/installation/#installation) for platform specific instructions.

## Reverse proxying example

Using nginx

```
server {
    # Other config

    server_name monitaur.domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_buffering off;
    }

    # This issue will be fixed in a later update
    location /register {
	allow 127.0.0.1;
        deny all;
    }
}
```

## Screenshots

![alt text](docs/servers.view.png "Servers View")
![alt text](docs/services.view.png "Services View")
