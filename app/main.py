from fastapi import FastAPI
from app.routes import auth_routes, masterdata_routes
from app.models import user as user_model, master_data as md_model
from app.database.session import engine
from app.exceptions.handlers import duplicate_name_exception_handler, not_found_exception_handler, global_exception_handler
from app.exceptions.custom_exceptions import DuplicateNameException, NotFoundException

# Create DB tables only for quick local dev (when not using Alembic).
# For production with Alembic, you can remove or keep for first-run convenience.

# user_model.Base.metadata.create_all(bind=engine)
# md_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce FastAPI (advanced template)")

# Simple root route so browser GET requests work
@app.get("/", tags=["health"])
def root():
    return {"message": "E-commerce FastAPI is running!"}

app.include_router(auth_routes.router)
app.include_router(masterdata_routes.router)

# Register exception handlers
app.add_exception_handler(DuplicateNameException, duplicate_name_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
