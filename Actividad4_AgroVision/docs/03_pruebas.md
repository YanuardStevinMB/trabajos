# Plan de pruebas
| Caso | Entrada | Resultado |
|---|---|---|
| CP-01 | GET /health | 200 y status ok |
| CP-02 | GET /api/crops | cinco cultivos |
| CP-03 | imagen válida | 201 y registro |
| CP-04 | tipo inválido | 415 |
| CP-05 | cultivo inválido | 422 |
| CP-06 | imagen menor 40x40 | 422 |
| CP-07 | GET /api/analyses | historial |
| CP-08 | POST análisis | persistencia |
## Automatización
```bash
pytest -q
```
Resultado validado antes de la entrega: **4 pruebas aprobadas de 4**.
