from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from math import sqrt
from typing import Iterable

from PIL import Image, ImageStat

SUPPORTED_CROPS = {
    "cafe": "Café",
    "yuca": "Yuca",
    "banano": "Banano",
    "platano": "Plátano",
    "aguacate": "Aguacate",
}

@dataclass(frozen=True)
class AnalysisResult:
    label: str
    status: str
    confidence: float
    health_score: float
    green_ratio: float
    yellow_ratio: float
    brown_ratio: float
    dark_ratio: float
    brightness: float
    symptoms: list[str]
    recommendation: str

def _ratio(pixels: Iterable[tuple[int, int, int]], predicate) -> float:
    pixels = list(pixels)
    if not pixels:
        return 0.0
    return sum(1 for p in pixels if predicate(*p)) / len(pixels)

def analyze_image(raw: bytes, crop: str) -> AnalysisResult:
    if crop not in SUPPORTED_CROPS:
        raise ValueError("Cultivo no soportado")
    try:
        image = Image.open(BytesIO(raw)).convert("RGB")
    except Exception as exc:
        raise ValueError("El archivo no es una imagen válida") from exc
    if image.width < 40 or image.height < 40:
        raise ValueError("La imagen debe tener al menos 40x40 píxeles")

    sample = image.copy()
    sample.thumbnail((240, 240))
    pixels = list(sample.get_flattened_data())

    green_ratio = _ratio(pixels, lambda r,g,b: g > r*1.10 and g > b*1.10 and g > 65)
    yellow_ratio = _ratio(pixels, lambda r,g,b: r > 120 and g > 105 and b < 105 and abs(r-g) < 85)
    brown_ratio = _ratio(pixels, lambda r,g,b: r > 65 and 0.35 < (g/max(r,1)) < 0.85 and b < g*0.85)
    dark_ratio = _ratio(pixels, lambda r,g,b: (r+g+b)/3 < 55)

    stat = ImageStat.Stat(sample)
    brightness = sum(stat.mean)/3
    variability = sum(sqrt(v) for v in stat.var)/3

    stress = (
        yellow_ratio*0.34 + brown_ratio*0.42 + dark_ratio*0.18
        + max(0.0,(65-brightness)/255)*0.18
        + max(0.0,(18-variability)/100)*0.08
    )
    benefit = green_ratio*0.48
    health_score = max(0.0, min(100.0, 72 + benefit*42 - stress*120))

    symptoms=[]
    if yellow_ratio >= 0.12: symptoms.append("amarillamiento visible")
    if brown_ratio >= 0.08: symptoms.append("zonas marrones o necróticas")
    if dark_ratio >= 0.12: symptoms.append("manchas oscuras relevantes")
    if green_ratio < 0.22: symptoms.append("baja predominancia de tejido verde")
    if brightness < 62: symptoms.append("imagen muy oscura; se recomienda repetir la captura")
    if not symptoms: symptoms.append("no se detectaron patrones visuales fuertes de estrés")

    if health_score >= 72:
        status="SALUDABLE"; label="Apariencia saludable"
        recommendation="Mantener el monitoreo preventivo. Si existen síntomas no visibles en la fotografía, consultar a un profesional agronómico."
    elif health_score >= 48:
        status="OBSERVACION"; label="Requiere observación"
        recommendation="Tomar una nueva fotografía con buena iluminación y revisar el cultivo en campo. Si los síntomas persisten, solicitar concepto técnico."
    else:
        status="POSIBLE_AFECTACION"; label="Posible afectación visual"
        recommendation="Aislar visualmente la zona afectada, registrar nuevas fotografías y solicitar revisión de un técnico o ingeniero agrónomo antes de aplicar tratamientos."

    confidence=min(0.94,max(0.55,0.60+abs(health_score-60)/180+min(0.12,variability/600)))
    return AnalysisResult(
        label=label,status=status,confidence=round(confidence*100,1),
        health_score=round(health_score,1),green_ratio=round(green_ratio*100,1),
        yellow_ratio=round(yellow_ratio*100,1),brown_ratio=round(brown_ratio*100,1),
        dark_ratio=round(dark_ratio*100,1),brightness=round(brightness,1),
        symptoms=symptoms,recommendation=recommendation
    )
