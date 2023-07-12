from fastapi import FastAPI, Depends
import models, database, schemas
from sqlalchemy.orm import Session
from database import SessionLocal

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def getdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blog")
def list(limit:int | None=None, db:Session=Depends(getdb)):
    if limit:
        blogs = db.query(models.Blog).limit(limit=limit).all()
    else:
        blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}")
def detail(id:int, db:Session=Depends(getdb)):
    blog = db.query(models.Blog).filter(models.Blog.id ==id).first()
    return blog
@app.post("/blog")
def create(req: schemas.Blog, db : Session = Depends(getdb)):
    new_blog = models.Blog(title=req.title, body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
@app.put("/blog/{id}")
def update(id:int, req:schemas.Blog, db:Session=Depends(getdb)):
    db.query(models.Blog).filter(models.Blog.id == id).update(req.dict())
    db.commit()
    return "update"

@app.delete("/blog/{id}")
def destroy(id:int, db:Session=Depends(getdb)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return "done"