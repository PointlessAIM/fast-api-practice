from fastapi import APIRouter, HTTPException, status
from db.models.user_models import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId


#se especifica la ruta que se va a compartir en la aplicación principal y sus funciones

router = APIRouter(prefix="/users_db", tags=["usersdb"], 
                    responses={404:{"Alert":"not found"}})


    
users_list = []

#obtener un usuario específico por ID
@router.get("/{id}")
async def user_id(id: str):
   
    return search_user("_id",ObjectId(id))

@router.get("/", response_model=list[User])
async def get_all_users():
    return users_schema(db_client.local.usersdb.find())

def search_user(field:str, key): 
    
    try:
        user=db_client.local.usersdb.find_one({field: key})
              
        return User(**user_schema(user))
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "No se ha encontrado el usuario"}) 
    

@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def insert_user(user:User):
    if type(search_user("email",user.email)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

    user_dict = dict(user)    
    del user_dict["id"]

    id = db_client.local.usersdb.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.usersdb.find_one({"_id": id}))

    return User(**new_user)

@router.put("/", response_model=User)
async def update_user(user:User):
    user_dict = dict(user)    
    del user_dict["id"]

    try:
        db_client.local.usersdb.find_one_and_replace(
            {"_id":ObjectId(user.id)}, user_dict
            )
    except:
        raise HTTPException(status_code=406, detail={"Error":"No se ha actualizado el usuario"})      
    
    return search_user("_id",ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:str):
    found = db_client.local.usersdb.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=406, detail={"Error":"Mo se ha eliminado el ususario porque no existe"}) 
     


    