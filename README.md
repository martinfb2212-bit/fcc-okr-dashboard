# FCC IT Modernization — OKR Executive Dashboard

Dashboard gerencial construido en **Streamlit** para monitorear los OKRs críticos del caso de estudio *FCC – IT Modernization*, mapeados a dos pivotes del marco de Evolución Digital (Barahona, INCAE 2026).

---

## Objetivo del Dashboard

Proveer al CIO y alta gerencia señales claras y accionables sobre el avance de la modernización TI de la FCC, específicamente en dos dimensiones estratégicas:

1. **Alineamiento Dinámico** — capacidad de ajustar estrategia y portafolio de forma continua basada en datos.
2. **Liderazgo Digital y Cultural** — evolución del habitus organizacional desde mando/control hacia orquestación, change agents y seguridad psicológica.

---

## Cómo correrlo localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/fcc-okr-dashboard.git
cd fcc-okr-dashboard

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
streamlit run app.py
```

La app abre automáticamente en `http://localhost:8501`

---

## Estructura del Repositorio

```
fcc-okr-dashboard/
│
├── app.py                  # Aplicación principal Streamlit
├── requirements.txt        # Dependencias Python
├── README.md               # Este archivo
│
└── data/
    ├── okr_timeseries.csv  # Serie de tiempo por KR (12 semanas / 6 meses)
    └── okr_snapshot.csv    # Estado actual de cada KR (para semáforo y tarjetas)
```

---

## Supuestos de Datos Simulados

Los datos son **completamente sintéticos**, generados para reflejar una trayectoria plausible y coherente con los hechos reportados en el caso:

| Supuesto | Valor inicial simulado | Valor final simulado | Fuente del caso |
|----------|----------------------|---------------------|-----------------|
| % presupuesto O&M | 78% (2024-Q1) | 52% (2024-Q3) | Caso: de >85% a <50% |
| Lead time prototipo (horas) | 210h | 44h | Caso: ~7 meses → <48h |
| % staff actitud positiva | 33% | 76% | Caso: 1/3 → >80% (sep 2015) |
| Change agents activos | 4 | 14 | Caso: intrapreneurs en 18 bureaus |
| Check-ins realizados (%) | 55% | 88% | Diseño del CIO (scrums semanales) |
| Seguridad psicológica (1-10) | 4.2 | 7.1 | Estimado a partir del caso |

**Cadencia de los datos:** Los CSVs contienen observaciones semanales (52 puntos) y mensuales (12 puntos) según la cadencia de cada KR. Los valores siguen una tendencia de mejora con variación aleatoria controlada (ruido gaussiano ±5%) para simular realismo.

---

## Pivotes y OKRs Incluidos

### Pivote 1: Alineamiento Dinámico
- **AD-1** Transformar la gestión del portafolio TI de presupuesto fijo a asignación continua basada en datos
- **AD-2** Institucionalizar check-ins de estrategia digital con alta gerencia
- **AD-3** Reducir el tiempo de prototipado como señal de capacidad de respuesta adaptativa

### Pivote 2: Liderazgo Digital y Cultural
- **LC-1** Construir y activar una red de change agents en todos los bureaus
- **LC-2** Elevar la adopción de nuevas prácticas digitales y reducir comportamientos de "pedir permiso"
- **LC-3** Transformar la percepción del cambio en el personal TI de amenaza a oportunidad

---

## Alineación con Tablas Excel (GPT)

Para la coordinación con el trabajo paralelo en GPT, los nombres exactos de pivotes, objetivos e indicadores en este dashboard corresponden a:

- **Tabla 1 (Ambiente del problema):** Tomador de decisiones = CIO (Dr. David Bray); Tarea = IT Modernization; Entorno = Agencia federal regulatoria, 207 sistemas legacy, presupuesto plano.
- **Tabla 2 (Pivote–Objetivo–KR):** Ver sección "Pivotes y OKRs Incluidos" arriba.

---

*Caso de estudio: Desouza, Denford & Krishnamurthy (2019). Marco teórico: Barahona, J.C. (2026), Evolución Digital, INCAE Business School.*
