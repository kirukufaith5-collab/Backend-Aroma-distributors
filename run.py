# run.py
from app import create_app  # or 'from app import app' depending on your setup

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)