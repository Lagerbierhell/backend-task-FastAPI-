Backend Task-FastAPI

Technologien: Python 3.11 / Poetry / FastAPI / PostgreSQL / Docker


Gehe auf die offizielle Python-Seite und installiere Python 3.11:
https://www.python.org/downloads/

PostgreSQL

Installiere PostgreSQL:
https://www.postgresql.org/download/

Poetry

Installiere Poetry für die Abhängigkeitsverwaltung:
https://python-poetry.org/docs/basic-usage/

Docker

Installiere Docker:
https://www.docker.com/



ERSTER WEG

1 Docker 
    Bevor du startest, stelle sicher, dass du folgendes installierth hast:

    Docker Desktop

    Ein Terminal (Windows: PowerShell / CMD, macOS/Linux: Terminal)

2 Docker-Compose starten
    Öffne ein Terminal im Projektordner.

    Führe folgenden Befehl aus:
    "docker-compose up"

    Docker lädt die benötigten Images herunter und startet die Container.
    Die App und die Datenbank laufen dann automatisch.

3 FastAPI Backend: http://localhost:4200

    Swagger-Dokumentation (API-Tester): http://localhost:4200/docs
    Hier kannst du Tasks erstellen, löschen, bearbeiten und erledigte Tasks auflisten.

4 App stoppen

    Im Terminal:
    docker-compose down
    Damit werden die Container gestoppt, die Datenbankdaten bleiben aber erhalten (im Docker-Volume).


ZWEITER WEG

5 Projekt vorbereiten

    Lade das Projekt herunter oder klone es via Git:

    git clone <projekt-url>
    cd <projekt-ordner>


    Erstelle eine virtuelle Umgebung über Poetry:

    poetry install
    poetry shell


    Damit werden alle Python-Abhängigkeiten installiert und die virtuelle Umgebung aktiviert.


6 Datenbank-Konfiguration (Umständlicher weg)
    Die App benötigt eine PostgreSQL-Datenbank. FastAPI kann die Datenbank nicht automatisch erstellen – sie muss vorab existieren.

    Empfohlene Test-Datenbank (Standardwerte):
    DATABASE_URL=postgresql+asyncpg://root:root@localhost:5432/mydatabase 


    Lege eine .env-Datei im Projektverzeichnis an und füge dort diese Zugangsdaten ein.
    SQLAlchemy erstellt automatisch die Tabellen, sobald die Datenbank existiert.
    
7 FASTAPI Starten

    Stelle sicher, dass die virtuelle Umgebung aktiv ist (poetry shell).

    Starte die App:

    uvicorn src.app.main:app

    --reload sorgt dafür, dass die App bei Änderungen am Code automatisch neu startet.

    Die App ist jetzt erreichbar unter:
    http://127.0.0.1:8000

    Swagger-Dokumentation für die API:
    http://127.0.0.1:8000/docs

8 Die Endpunkte

    Die API-Endpunkte funktionieren wie folgt:

    POST /create_task → neue Task erstellen

    GET /list_tasks → alle Tasks auflisten

    DELETE /delete_task/{task_id} → Task löschen

    PUT /update_task_description/{task_id} → Task-Beschreibung ändern

    GET /list_done_tasks → erledigte Tasks auflisten

    PUT /mark_task_done/{task_id} → Task als erledigt markieren

    9 Hinweise!!

    Die .env-Datei darf niemals in ein Repository hochgeladen werden, das in Produktion verwendet wird.

    Für Produktionsbetrieb Passwörter, Host und Port anpassen.

    Migrationen: Für Änderungen an Tabellenstruktur in Produktion sollten Tools wie Alembic genutzt werden.

