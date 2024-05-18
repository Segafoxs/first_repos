import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from models import Base,Person
import psycopg2
from fastapi import FastAPI, Depends, status, HTTPException, security
from pydantic import BaseModel
from models import User
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import jwt


#postgresql://user:password@localhost/database
postgres_database = "postgresql://postgres:Admin1@localhost/metanit"

engine = create_engine(postgres_database)
Session = sessionmaker(autoflush=False, bind=engine)


app = FastAPI()
security = HTTPBasic()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
token = None




def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(tok: str):
    try:
        payload = jwt.decode(tok, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass

def get_user(username: str):
    with Session(autoflush=False, bind=engine) as db:
        people = db.query(Person).filter(Person.login == username).first()
        if people is None:
            return None
        else:
            return people.id



def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username, credentials.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

def get_user_from_db(username: str, password: str):
    with Session(autoflush=False, bind=engine) as db:
        people = db.query(Person).filter(Person.login == username, Person.password == password).first()
        if people is not None:
            global token
            token = create_jwt_token({"sub": username})
            username = get_user_from_token(token)
            return {"id": people.id, "token": token, "username": username}

        else:
            return None



@app.get("/protected_resource")
def get_protected_resourse(user: User = Depends(authenticate_user)):
    return {"message": "You have access to the protected resource!", "user_info": user}


@app.get("/salary")
def get_salary():
    if token is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not token")
    else:
        return {"message": "salary"}



if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8066, reload=True, workers=3)