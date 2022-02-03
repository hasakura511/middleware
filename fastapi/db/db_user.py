from sqlalchemy.orm.session import Session
from db.hash import Hash
from schemas import UserBase
from db.models import DBUser
from fastapi import HTTPException, status


def _check(db_object, id_=None):
    if not db_object:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{DBUser.__tablename__} id {id_} not found')


# post


def db_create_user(db: Session, request: UserBase):
    new_user = DBUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )

    db.add(new_user)
    db.commit()
    # need to refresh to add the id to new_user
    db.refresh(new_user)
    return new_user


# post
def db_update_user(db: Session, user_id: int, request: UserBase):
    # user is query object
    user = db.query(DBUser).filter(DBUser.id == user_id)
    # user.first() is a DBUser object, if nonexistant = None
    _check(user.first(), user_id)
    # update exists in the query object, not the DBUser object
    user.update({
        DBUser.username: request.username,
        DBUser.email: request.email,
        DBUser.password: Hash.bcrypt(request.password),
    })
    db.commit()
    # fast api router.post does not know how to handle querty objects, will error out, can only pass Base model objects
    return user.first()


# get
def db_get_all_users(db: Session):
    users = db.query(DBUser).all()
    print(users)
    # [<db.models.DBUser at 0x7fd60d901670>]
    return users


# get
def db_get_user(db: Session, user_id: int):
    # returns an iterable if there is no first()
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    _check(user, user_id)

    return user


# get
def db_get_username(db: Session, username: str):
    # returns an iterable if there is no first()
    user = db.query(DBUser).filter(DBUser.username == username).first()
    _check(user, username)

    return user


# get
def db_delete_user(db: Session, user_id: int):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    _check(user.first(), user_id)
    db.delete(user)
    db.commit()
    return user
