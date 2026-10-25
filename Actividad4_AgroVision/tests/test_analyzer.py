from io import BytesIO
from PIL import Image
from app.analyzer import analyze_image
def image_bytes(color,size=(120,120)):
    image=Image.new("RGB",size,color); stream=BytesIO(); image.save(stream,format="PNG"); return stream.getvalue()
def test_green_image_is_not_flagged_as_severe():
    r=analyze_image(image_bytes((55,150,70)),"cafe"); assert r.status in {"SALUDABLE","OBSERVACION"}; assert r.green_ratio>70
def test_brown_image_is_flagged_for_attention():
    r=analyze_image(image_bytes((125,75,35)),"aguacate"); assert r.status in {"OBSERVACION","POSIBLE_AFECTACION"}; assert r.brown_ratio>70
def test_rejects_tiny_image():
    try: analyze_image(image_bytes((20,100,20),(10,10)),"cafe"); assert False
    except ValueError as exc: assert "40x40" in str(exc)
