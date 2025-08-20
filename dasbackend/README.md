# backend-task-FastAPI-
-----------------------------------------------------
Python 3.11 / Poetry / FastAPI / Postgres SQL 
-----------------------------------------------------
Gehe auf die offizielle Python-Seite:
https://www.python.org/downloads/
-----------------------------------------------------
https://www.postgresql.org/download/
-----------------------------------------------------
https://python-poetry.org/docs/basic-usage/
-----------------------------------------------------
1.create_task(task: TaskCreate)
Methode: POST
Beschreibung: Erstellt eine neue Task in der Datenbank.
Input: JSON mit Task-Daten (description, optional due_at)
Output: JSON mit allen Task-Daten inklusive generierter ID, created_at und done=False

Beispiel:
{
  "description": "Einkaufen",
  "due_at": "2025-08-25T12:00:00Z"
}
Return:
{
  "id": 1,
  "description": "Einkaufen",
  "created_at": "2025-08-20T22:00:00Z",
  "due_at": "2025-08-25T12:00:00Z",
  "done": false
}

2️. list_tasks()
Methode: GET
Beschreibung: Gibt eine Liste aller Tasks zurück, sowohl erledigte als auch offene.
Output: Array von Task-Objekten

3️. delete_task(task_id: int)
Methode: DELETE
Beschreibung: Löscht eine Task anhand ihrer ID.
Input: task_id (int)
Output: Boolean → True, wenn die Task existierte und gelöscht wurde, sonst False

4️. update_task_description(task_id: int, new_description: str)
Methode: PUT / PATCH
Beschreibung: Aktualisiert die Beschreibung einer Task anhand ihrer ID.
Input: Task-ID und neue Beschreibung
Output: Aktualisierte Task-Daten als JSON oder None, wenn die Task nicht existiert

5️. list_done_tasks()
Methode: GET
Beschreibung: Gibt eine Liste aller erledigten Tasks zurück (done=True).
Output: Array von Task-Objekten, die erledigt sind

6️. mark_task_done_bool(task_id: int)
Methode: PUT / PATCH
Beschreibung: Markiert eine Task als erledigt (done=True) anhand ihrer ID.
Input: Task-ID
Output: JSON der aktualisierten Task mit done=True

uvicorn src.app.main:app --reload
