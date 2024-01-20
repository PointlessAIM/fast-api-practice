from fastapi import APIRouter

#se especifica la ruta que se va a compartir en la aplicación principal y sus funciones
#prefix: ruta que se va a compartir
#tags: etiquetas que se van a mostrar en la documentación
#responses: respuestas que se van a mostrar en la documentación
router = APIRouter(prefix="/products", tags= ["products"],
                    responses={404:{"Alert":"not found"}})

products_list = ["producto 1" , "producto 2", "producto 3", "producto 4", "producto 5"]

@router.get("/")
async def get_products():
    return products_list
    
@router.get("/{id}")
async def get_products(id:int):
    return products_list[id]