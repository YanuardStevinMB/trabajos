# Recolección de requisitos del prototipo
## Necesidad
El proyecto busca apoyar la detección temprana de posibles afectaciones visibles en cultivos mediante fotografías.
## Actores
- Agricultor o pequeño productor.
- Equipo del proyecto.
- Profesional agronómico como referencia externa.
## Requisitos funcionales
- RF-01: seleccionar café, yuca, banano, plátano o aguacate.
- RF-02: cargar JPG, PNG o WEBP de máximo 8 MB.
- RF-03: validar formato, tamaño y resolución.
- RF-04: analizar color, brillo y contraste.
- RF-05: clasificar como saludable, observación o posible afectación.
- RF-06: mostrar puntaje, confianza, patrones y recomendación.
- RF-07: almacenar el resultado.
- RF-08: consultar historial y estadísticas.
- RF-09: exponer API REST.
## No funcionales
- Interfaz responsive.
- Persistencia SQLite.
- Ejecución local o Docker.
- Pruebas automatizadas.
- Advertencia de no diagnóstico.
