from pathlib import Path
from PIL import Image, ImageDraw
OUT=Path(__file__).resolve().parent.parent/"demo_images"; OUT.mkdir(exist_ok=True)
healthy=Image.new("RGB",(900,600),(226,236,219)); d=ImageDraw.Draw(healthy); d.ellipse((160,70,740,540),fill=(48,137,68),outline=(24,90,45),width=10); d.line((450,90,450,520),fill=(223,234,190),width=16); healthy.save(OUT/"hoja_saludable.png")
affected=Image.new("RGB",(900,600),(230,224,199)); d=ImageDraw.Draw(affected); d.ellipse((160,70,740,540),fill=(130,133,55),outline=(88,82,40),width=10)
for box in [(290,180,400,290),(470,145,585,260),(375,330,520,455),(525,350,625,450)]: d.ellipse(box,fill=(100,55,26),outline=(65,35,20),width=5)
d.line((450,90,450,520),fill=(188,175,95),width=16); affected.save(OUT/"hoja_afectada.png")
print(f"Imágenes creadas en: {OUT}")
