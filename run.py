from app import create_app, db
# Ensure models are imported so SQLAlchemy registers them
from app import models  

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables for all imported models
    app.run(debug=True)