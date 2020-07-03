# bitbucket_sync2codecommit

## Install

    $ virtualenv -p python3 venv && source venv/bin/activate
    $ pip install -r requirements.txt

## Run

    Run Development
    $ FLASK_APP=app.py FLASK_ENV=development flask run

    # Run production (do not forget to setup proper webserver - nginx/apache/...)
    $ cp wsgi.ini.sample wsgi.ini
    $ uwsgi uwsgi.ini

## Test

    # Send testing request
    ./tests/test_request.sh localhost:5000/hooks/webhook-test-project
