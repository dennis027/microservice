from app import app, db, DBCredentials

with app.app_context():
    db.create_all()

    # Create three instances of DBCredentials
    db1 = DBCredentials(
        db_type='postgresql',
        db_name='mydb1',
        db_user='user1',
        db_password='password1',
        db_host='localhost',
        db_port=5432
    )

    db2 = DBCredentials(
        db_type='mysql',
        db_name='mydb2',
        db_user='user2',
        db_password='password2',
        db_host='localhost',
        db_port=3306
    )

    db3 = DBCredentials(
        db_type='sqlite',
        db_name='mydb3.db',  # For SQLite, use the filename
        db_user='',
        db_password='',
        db_host='',
        db_port=0
    )

    # Add instances to the session and commit
    db.session.add(db1)
    db.session.add(db2)
    db.session.add(db3)
    db.session.commit()

    print("Database seeded successfully.")
