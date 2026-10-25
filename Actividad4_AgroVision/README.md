# AgroVision - Prototipo funcional

Prototipo de la **Actividad 4 - Diseño del prototipo** de la asignatura Proyecto de Software, como continuidad de la formulación del proyecto **“Desarrollo de un software para la detección temprana de enfermedades en cultivos agrícolas mediante análisis de imágenes”**.

## Funcionalidades
- Selección de cultivo: café, yuca, banano, plátano o aguacate.
- Carga y vista previa de JPG, PNG y WEBP.
- Análisis visual preventivo basado en métricas de color, brillo y contraste.
- Clasificación orientativa: saludable, en observación o posible afectación.
- Puntaje visual, confianza, patrones y recomendación.
- Persistencia con SQLite e historial de resultados.
- API REST con Swagger (`/docs`).
- Pruebas automatizadas y GitHub Actions.
- Ejecución local o con Docker.

> **Importante:** el algoritmo incluido es una aproximación heurística para un prototipo académico. No reemplaza un diagnóstico agronómico ni debe usarse para indicar tratamientos.

## Instalación rápida con Python

Requisitos: Python 3.12+.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abrir: `http://localhost:8000`

API: `http://localhost:8000/docs`

## Instalación con Docker

```bash
docker compose up --build
```

Abrir: `http://localhost:8000`

## Pruebas

```bash
pytest -q
```

## Imágenes de demostración

```bash
python scripts/create_demo_images.py
```

Se crearán `demo_images/hoja_saludable.png` y `demo_images/hoja_afectada.png`.

## Estructura

```text
app/
  main.py          API y endpoints
  analyzer.py      procesamiento de imagen
  database.py      persistencia SQLite
  static/          interfaz web
scripts/           utilidades de demostración
tests/             pruebas automatizadas
docs/              requisitos, ciclo, pruebas y evidencias
.github/workflows/ integración continua
```

## Ciclo de prototipado aplicado
1. Concepto.
2. Recolección de requisitos.
3. Diseño rápido.
4. Construcción funcional.
5. Evaluación.
6. Refinamiento.
7. Entrega.

Ver `docs/02_ciclo_prototipo.md` para el detalle.

## Integrantes
- Jesús Santiago Castillo Moyano
- Yanuard Stevin Montialegre Bonilla
- Luis Enrique Lemus Duque

Corporación Universitaria Iberoamericana - Ingeniería de Software - 2026.
