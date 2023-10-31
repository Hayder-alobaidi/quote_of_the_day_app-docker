from app import app, db, Quote

# Push an application context manually
with app.app_context():
    db.create_all()

    # Add quotes
    quote1 = Quote(text="Life is what happens when you're busy making other plans. – John Lennon")
    quote2 = Quote(text="The purpose of our lives is to be happy. — Dalai Lama")

    # Commit changes to the database
    db.session.add(quote1)
    db.session.add(quote2)
    db.session.commit()

print("Database initialized!")
