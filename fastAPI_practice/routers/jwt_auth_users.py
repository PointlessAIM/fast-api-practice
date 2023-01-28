#RECORDAR IMPLEMENTAR REFRESH TOKEN MÁS ADELANTE

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(tags=["JWT authentication"], responses={404:{"Alert":"not found"}})
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
SECRET = "BnQq74yG1zzd16X1arON/99MoPY422xkg80sXlpFrWg"
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")
#OAuth2PasswordBearer: nos permite definir un esquema de autenticación basado en tokens

crypt = CryptContext(schemes=["bcrypt"])
#CryptContext: nos permite definir un contexto de encriptación para la contraseña
#schemes: algoritmo de encriptación que vamos a utilizar


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password:str

users_db = {
    "pointless": {
        "username": "pointless",
        "full_name": "Mayber Illidge",
        "email": "mail@mail.com",
        "disabled": False,
        "password": "$2a$12$OA5rxji54ayuDhVQPO8/P.Yy4L.SMI8eMBfv5y5T1OlQcRuSK4sFS"
        #12123345
    },
    "mayb": {
        "username": "mayb",
        "full_name": "Mayber Illidge",
        "email": "mail@mail.com",
        "disabled": True,
        "password": "$2a$12$OA5rxji54ayuDhVQPO8/P.Yy4L.SMI8eMBfv5y5T1OlQcRuSK4sFS"
    }
}

#Búsqueda del usuario dentro de la DB, validamos usuario y contraseña
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

#Búsqueda del usuario como objeto User, no necesitamos la contraseña
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])

async def authenticate_user(token:str=Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Auth":"bearer"}
        )
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    return search_user(username)

async def current_user(user:User = Depends(authenticate_user)):
 
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return user


@router.post("/login")
async def login (form: OAuth2PasswordRequestForm = Depends()):

    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="revisa tus datos de acceso, seguro que los escribiste bien?"
        )
    
    user = search_user_db(form.username)

    #verify: verifica si la contraseña introducida por el usuario coincide con la contraseña encriptada en la DB
    #form.password: contraseña introducida por el usuario
    #user.password: contraseña encriptada en la DB
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="revisa tus datos de acceso, seguro que los escribiste bien?"
        )

     
    access_token = {
        "sub": user.username, 
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),

    }
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM) , "token_type": "bearer"}

@router.get("/users/me")
#muestra los datos del usuario actual
async def me(user:User = Depends(current_user)):
    return user

# me: muestra los datos del usuario actual
#para que sea posible, user: depende de current_user, que depende de authenticate_user, que depende de oauth2
#oauth2: depende de la ruta /login
