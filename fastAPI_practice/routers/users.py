from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    weight: str
    height: str
    
users_list = [User(id=1, name="Mayber", surname="Illidge", age=25, weight="75kg", height="184cm"),
              User(id=2, name="Antonio", surname="Illidge", age=24, weight="75kg", height="184cm"),
              User(id=3, name="Mayber", surname="Mafla", age=25, weight="73kg", height="184cm")]

@router.get("/usersjson/")
async def user_json():
    return [{"name": "Mayber", "surname": "Illidge", "age":25, "weight":"75kg", "height":"184cm"},
            {"name": "Antonio", "surname": "Illidge", "age":24, "weight":"75kg", "height":"184cm"},
            {"name": "Mayber", "surname": "Mafla", "age":25, "weight":"73kg", "height":"184cm"}]

@router.get("/users/")
async def users():
    return users_list

@router.get("/user/{id}")
async def user_id(id: int):
    return search_user(id)

@router.get("/user/")
async def user_id(id: int):
    return search_user(id)
    
def search_user(id:int):
    user= filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        return {"Error": "No se ha encontrado el usuario"}
    
@router.post("/user/", status_code=201)
async def insert_user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
        
    else:
        users_list.append(user)
        return {"Message": "Success"}

@router.put("/user/")
async def update_user(user:User):
    found = False
    
    for index, is_user in enumerate(users_list):
        if is_user.id == user.id:
            users_list[index] = user
            found = True
        
    if not found:
        return {"Error":"No se ha actualizado el usuario"}
    
    return user

@router.delete("/user/{id}")
async def delete_user(id:int):
    found = False
    for index, is_user in enumerate(users_list):
        if is_user.id == id:
            del users_list[index] 
            found = True
    if not found:
        return {"Error":"Mo se ha eliminado el ususario"}
    return {"Message": "Success"}
    


    
