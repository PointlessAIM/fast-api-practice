from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
#exponer recursos estáticos (this method seems deprecated)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def url():
    return {"url_message": "Mayber, this is the main page?"}



