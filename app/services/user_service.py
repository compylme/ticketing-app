from app.models import User

def create_user(db, name, email):
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        raise ValueError("user with the same email already exists")
    user = User(
        name = name,
        email = email
    )
    db.add(user)
    db.commit()
    return user