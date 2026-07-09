from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

notes = []


class Note(BaseModel):
    title: str
    content: str
    completed: bool


@app.get("/")
def home():
    return {"message": "Welcome to the Notes API"}


@app.get("/notes")
def get_notes():
    return notes


@app.post("/notes")
def create_note(note: Note):
    notes.append(note)

    return {
        "message": "Note created successfully",
        "note": note,
        "completed": False
    }


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    if note_id >= len(notes):
        return {"error": "Note not found"}

    return notes[note_id]

@app.put("notes/{note_id}")
def update_note(note_id: int, note: Note):
    if note_id >= len(notes):
        return {"error": "Note not found"}
    
    notes[note_id] = note

    return {
        "message": "Note updated successfully",
        "note": note
    }


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    if note_id >= len(notes):
        return {"error": "Note not found"}

    deleted_note = notes.pop(note_id)

    return {
        "message": "Note deleted",
        "note": deleted_note
    }