from app import create_app, db
from flask import current_app

app = create_app() 

# Create database tables if they don't exist
with app.app_context():
    db.create_all()  

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=3000, debug=True)