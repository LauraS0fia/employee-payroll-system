from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routes.employee_routes import router as employee_router

app = FastAPI()

# Servir archivos estáticos (HTML, CSS, JS)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Página principal

@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")

# Conectar rutas del CRUD de empleados

app.include_router(employee_router)
