from io import BytesIO
from pathlib import Path
from fastapi.testclient import TestClient
from PIL import Image
import app.database as database
from app.main import app
def png_bytes(color=(65,145,70)):
    image=Image.new("RGB",(120,120),color); stream=BytesIO(); image.save(stream,format="PNG"); return stream.getvalue()
def test_health_and_analysis_flow(tmp_path:Path,monkeypatch):
    monkeypatch.setattr(database,"DB_PATH",tmp_path/"test.db"); database.init_db(); client=TestClient(app)
    assert client.get("/health").json()["status"]=="ok"
    assert any(c["code"]=="cafe" for c in client.get("/api/crops").json())
    response=client.post("/api/analyses",data={"crop":"cafe"},files={"image":("hoja.png",png_bytes(),"image/png")})
    assert response.status_code==201
    payload=response.json(); assert payload["crop"]=="cafe" and payload["filename"]=="hoja.png"
    history=client.get("/api/analyses").json(); assert len(history)==1 and history[0]["id"]==payload["id"]
