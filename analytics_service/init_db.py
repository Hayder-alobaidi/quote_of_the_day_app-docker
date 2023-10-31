from app import db, app, QuoteCount

with app.app_context():
    # Create the tables
    db.create_all()

    # (Optional) Initialize some data or perform initial checks
    if not QuoteCount.query.first():
        print("Database initialized. No initial records created.")
    else:
        print("Database already initialized.")
