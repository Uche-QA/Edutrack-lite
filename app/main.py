from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.Routers import enrollment, user, course


app = FastAPI(  
    title= "Edutrack Lite API",
    description= "This is a simple API",
    version= "1.0.0",
    docs_url= "/docs",
    redoc_url= "/redoc"
    )

# Register routers
app.include_router(user.router)
app.include_router(course.router)
app.include_router(enrollment.router)

@app.get("/")
def root():
    return {"message": "Welcome to EduTrack Lite API"}
