from __future__ import annotations
import json, sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "agrovision.db"

def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn=sqlite3.connect(DB_PATH); conn.row_factory=sqlite3.Row
    return conn

def init_db() -> None:
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            crop TEXT NOT NULL, filename TEXT NOT NULL, status TEXT NOT NULL,
            label TEXT NOT NULL, confidence REAL NOT NULL, health_score REAL NOT NULL,
            green_ratio REAL NOT NULL, yellow_ratio REAL NOT NULL, brown_ratio REAL NOT NULL,
            dark_ratio REAL NOT NULL, brightness REAL NOT NULL, symptoms TEXT NOT NULL,
            recommendation TEXT NOT NULL
        )""")
        conn.commit()

def save_analysis(crop:str, filename:str, result)->int:
    with connect() as conn:
        cur=conn.execute("""INSERT INTO analyses (
            crop,filename,status,label,confidence,health_score,green_ratio,yellow_ratio,
            brown_ratio,dark_ratio,brightness,symptoms,recommendation
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
            crop,filename,result.status,result.label,result.confidence,result.health_score,
            result.green_ratio,result.yellow_ratio,result.brown_ratio,result.dark_ratio,
            result.brightness,json.dumps(result.symptoms,ensure_ascii=False),result.recommendation
        ))
        conn.commit(); return int(cur.lastrowid)

def list_analyses(limit:int=20)->list[dict]:
    with connect() as conn:
        rows=conn.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
    return [_row_to_dict(r) for r in rows]

def get_analysis(analysis_id:int)->dict|None:
    with connect() as conn:
        row=conn.execute("SELECT * FROM analyses WHERE id = ?",(analysis_id,)).fetchone()
    return _row_to_dict(row) if row else None

def stats()->dict:
    with connect() as conn:
        total=conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
        affected=conn.execute("SELECT COUNT(*) FROM analyses WHERE status='POSIBLE_AFECTACION'").fetchone()[0]
        observation=conn.execute("SELECT COUNT(*) FROM analyses WHERE status='OBSERVACION'").fetchone()[0]
        healthy=conn.execute("SELECT COUNT(*) FROM analyses WHERE status='SALUDABLE'").fetchone()[0]
    return {"total":total,"healthy":healthy,"observation":observation,"affected":affected}

def _row_to_dict(row:sqlite3.Row)->dict:
    result=dict(row); result["symptoms"]=json.loads(result["symptoms"]); return result
