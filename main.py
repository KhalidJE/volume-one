from fastapi import FastAPI as fast, HTTPException
from pydantic import BaseModel as bm

app = fast(title="Manga Tracker API")

class Manga(bm):
    id: int
    title: str
    status: str
    chapters_read: int

class addManga(bm):
    title: str
    status: str
    chapters_read: int

manga_db: list[Manga] = [
    Manga(id=1, title="One Piece", status="reading", chapters_read=1191),
    Manga(id=2, title="Ichi the Witch", status="completed", chapters_read=94),
    Manga(id=3, title="Goodnight Punpun", status="plan_to_read", chapters_read=0)
]

def find_manga(manga_id: int) -> Manga:
    for manga in manga_db:
        if manga.id == manga_id:
            return manga
    raise HTTPException(status_code=404, detail=f"No manga with ID {manga_id}")

@app.get("/api/manga")
def list_manga() -> list[Manga]:
    return manga_db

@app.post("/api/manga", status_code=201)
def add_manga(payload: addManga) -> Manga:
    new_id = max((m.id for m in manga_db), default=0) + 1
    manga = Manga(id=new_id, **payload.model_dump())
    manga_db.append(manga)
    return manga

@app.get("/api/manga/{manga_id}")
def get_manga(manga_id: int) -> Manga:
    return find_manga(manga_id)

@app.post("/api/manga/{manga_id}", status_code=204)
def delete_manga(manga_id: int) -> None:
    manga = find_manga(manga_id)
    manga_db.remove(manga)