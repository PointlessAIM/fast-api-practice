from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app=FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

#define los datos que representan a un usuario en el sistema
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

#hereda de User, añadiendo el campo de contraseña para regular el acceso
class UserDB(User):
    password:str

#Información de los usuarios en la base de datos
users_db = {
    "pointless": {
        "username": "pointless",
        "full_name": "Mayber Illidge",
        "email": "mail@mail.com",
        "disabled": False,
        "password": "12123345"
    },
    "mayb": {
        "username": "mayb",
        "full_name": "Mayber Illidge",
        "email": "mail@mail.com",
        "disabled": True,
        "password": "12123345"
    }
}

#Búsqueda del usuario dentro de la DB
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

#Búsqueda del usuario como objeto de clase
def search_user(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

#Recibe como parámetro un token de autenticación para validar la interacción del usuario con el sistema
#así como reconocer quién es el usuario actual
async def current_user(token:str=Depends(oauth2)):
    user = search_user(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Auth":"bearer"}
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return user

#login: usamos un objeto tipo OAuth2 = Depends() para obtener los datos de inicio de sesión del usuario
# a través del parámetro form
@app.post("/login")
async def login (form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="revisa tus datos de acceso, seguro que los escribiste bien?"
        )
    
    user = search_user(form.username)

    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="revisa tus datos de acceso, seguro que los escribiste bien?"
        )
    
    return {"access_token": user.username , "token_type": "bearer"}


@app.get("/users/me")
#muestra los datos del usuario actual
async def me(user:User = Depends(current_user)):
    return user

