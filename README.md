# UEFA Nations League Predictor

Simulador de la UEFA Nations League basado en el método Monte Carlo: ejecuta miles de repeticiones del torneo completo (fase de grupos, playoffs cruzados, cuartos de final y Final Four) para estimar la probabilidad real de cada selección de ascender, descender o levantar el trofeo.

## 🚀 Demo / Screenshot

> Añade aquí un enlace a la demo en vivo o una captura de pantalla de la pantalla principal y del detalle de una simulación.

## 📋 Tabla de contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Tests](#tests)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Autor](#autor)

## ✨ Características

- **Simulación Monte Carlo del torneo completo**: fase de grupos, playoffs de ascenso/descenso entre ligas (A/B, B/C, C/D), cuartos de final a ida y vuelta, y Final Four a partido único.
- **Modelo de goles esperados calibrado con datos reales**: ratings de ataque y defensa por selección, ajustados mediante una regresión de Poisson (estilo Dixon-Coles/Maher) sobre ~4.500 partidos internacionales de los últimos 4 años, en vez de un único rating genérico.
- **Estadísticas globales por liga**: probabilidad de alcanzar cuartos, semifinal, final y título (Liga A), o de ascender/descender (Ligas B, C y D).
- **Probabilidad por posición de grupo**: desglosada por cada grupo real de la competición (A1–A4, B1–B4, C1–C4, D1–D2).
- **Simulaciones individuales guardadas**: selección y consulta de partidas concretas, con clasificación por grupo, resultados jornada a jornada y cuadro eliminatorio completo, marcando el equipo ganador de cada eliminatoria.
- **Interfaz con identidad visual propia**: banderas por selección, paginación de simulaciones y diseño responsive.

## 🛠️ Tecnologías

**Backend**
- Python 3
- FastAPI + Uvicorn
- tqdm

**Frontend**
- React + Vite
- Tailwind CSS v4
- flag-icons

**Preparación de datos** (`data_prep/`)
- pandas, NumPy, SciPy — ajuste de la regresión de Poisson para los ratings de ataque/defensa

## 📦 Instalación

```bash
git clone https://github.com/usuario/nations-league-ia.git
cd nations-league-ia
```

**Backend:**

```bash
pip install fastapi uvicorn tqdm
```

**Frontend** (en otra terminal):

```bash
cd frontend
npm install
```

## ⚙️ Configuración

Este proyecto no requiere variables de entorno ni claves de API. Los ajustes relevantes están directamente en el código:

- `main.py` → `N_SIMULATIONS` y `N_SAVED_SIMULATIONS`: número total de simulaciones a ejecutar y cuántas se guardan con detalle de partidos.
- `main.py` → configuración de `CORSMiddleware`: origen permitido para el frontend en desarrollo (`http://localhost:5173` por defecto).

## 💻 Uso

**1. Arranca el backend** desde la raíz del proyecto:

```bash
python -m uvicorn main:app --reload
```

Disponible en `http://127.0.0.1:8000` (documentación interactiva en `/docs`).

**2. Arranca el frontend** desde `frontend/`:

```bash
npm run dev
```

Disponible en `http://localhost:5173`.

**3. Desde el navegador**, pulsa **Simular torneo**. Al terminar, verás las estadísticas globales por liga, la probabilidad por posición de grupo, y una selección de simulaciones guardadas que puedes abrir para ver su detalle completo (grupos, resultados y eliminatorias).

### Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/simulate` | Ejecuta una nueva tanda de simulaciones |
| `GET` | `/api/results` | Estadísticas globales y resumen de simulaciones guardadas |
| `GET` | `/api/simulations/{id}` | Clasificación y partidos completos de una simulación concreta |
| `GET` | `/api/teams` | Listado de selecciones (código, nombre, liga, grupo) |

## 📁 Estructura del proyecto

```
nations-league-ia/
├── main.py                  # Punto de entrada FastAPI y orquestación de la simulación
├── api/                     # Endpoints REST
├── data/                    # elo.csv, config.json, fixtures.json y resultados generados
├── data_prep/                # Ajuste de ratings de ataque/defensa a partir de datos históricos
│   ├── build_attack_defense.py
│   ├── team_mapping.py
│   └── output/
├── engine/                  # Motor de simulación
│   ├── builders/             # Construcción de grupos, ligas y competición
│   ├── knockout/             # Cuartos, playoffs y Final Four
│   ├── loaders/               # Carga de equipos, calendario y configuración
│   ├── models/                 # Modelo de goles esperados
│   ├── probability/           # Muestreo Poisson
│   ├── rankings/               # Clasificaciones cruzadas entre grupos
│   ├── simulators/             # Simulación de partidos, grupos, eliminatorias
│   └── standings/              # Cálculo de clasificaciones
├── models/                  # Entidades del dominio (Team, Match, Tie, FinalFour...)
├── output/                  # Persistencia de resultados en JSON
├── utils/
└── frontend/                # Aplicación React
    └── src/
        ├── api/
        ├── components/
        └── App.jsx
```

## 🧪 Tests

Actualmente el proyecto no cuenta con tests automatizados. Contribuciones añadiendo cobertura (especialmente sobre el motor de simulación y el cálculo de clasificaciones/desempates) son bienvenidas.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea tu rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Distribuido bajo licencia [MIT/otra]. Ver `LICENSE` para más información.

## 👤 Autor

Tu nombre - [@tu_usuario](https://github.com/tu_usuario)