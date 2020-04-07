from pathlib import Path

from sqlalchemy.orm import Session


def execute(bind, filename: str):
    session = Session(bind=bind)
    file_path = Path(f"migrations/versions/{filename}").absolute()
    with open(file_path) as f:
        sql_to_execute = f.read()
        session.execute(sql_to_execute)
        session.commit()
