install:
    pip install -r requirements.txt

run:
    python -m app.main

test_2:
    curl -i http://localhost:4221/

test_8:
    curl -vvv -d "hello world" localhost:4221/files/readme.txt