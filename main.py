from fastapi import FastAPI as fast, HTTPException
from pydantic import BaseModel as bm

app = fast(title="Manga Tracker API")

class Manga(bm):
    id: int
    title: str
    status: str
    chapters_read: int

class AddManga(bm):
    title: str
    status: str
    chapters_read: int

class UpdateManga(bm):
    title: str | None = None
    status: str | None = None
    chapters_read: int | None = None

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
def add_manga(payload: AddManga) -> Manga:
    new_id = max((m.id for m in manga_db), default=0) + 1
    manga = Manga(id=new_id, **payload.model_dump())
    manga_db.append(manga)
    return manga

@app.get("/api/manga/{manga_id}")
def get_manga(manga_id: int) -> Manga:
    return find_manga(manga_id)

@app.patch("/api/manga/{manga_id}")
def update_manga(manga_id: int, payload: UpdateManga) -> Manga:
    manga = find_manga(manga_id)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(manga, field, value)
    return manga

@app.delete("/api/manga/{manga_id}", status_code=204)
def delete_manga(manga_id: int) -> None:
    manga = find_manga(manga_id)
    manga_db.remove(manga)