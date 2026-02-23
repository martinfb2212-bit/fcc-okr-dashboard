"""
FCC IT Modernization — OKR Executive Dashboard
Versión self-contained: datos embebidos, sin archivos CSV externos.
Solo requiere app.py + requirements.txt + README.md en GitHub.
Marco: Evolución Digital (Barahona, INCAE 2026)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ── Paleta ─────────────────────────────────────────────────────────────────────
C_BG     = "#0F1117"
C_CARD   = "#1C1F2E"
C_ACCENT = "#4F8EF7"
C_GREEN  = "#22C55E"
C_YELLOW = "#F59E0B"
C_RED    = "#EF4444"
C_TEXT   = "#E2E8F0"
C_MUTED  = "#94A3B8"

# ── Datos embebidos ────────────────────────────────────────────────────────────
KRS = [
    # (pivote, obj_id, obj_nombre, kr_id, kr_nombre, unidad, meta, v_ini, v_fin, cadencia, owner, direction)
    ("Alineamiento Dinámico","AD-1","Rebalancear portafolio TI hacia innovación",
     "AD-1-KR1","% presupuesto TI en O&M","%",50,78,52,"Mensual","CIO / CFO TI","down"),
    ("Alineamiento Dinámico","AD-1","Rebalancear portafolio TI hacia innovación",
     "AD-1-KR2","Decisiones portafolio ajustadas por datos","#",6,1,6,"Trimestral","Director PMO","up"),
    ("Alineamiento Dinámico","AD-1","Rebalancear portafolio TI hacia innovación",
     "AD-1-KR3","Lead time aprobación de cambio (días)","días",7,28,8,"Mensual","CIO","down"),
    ("Alineamiento Dinámico","AD-2","Institucionalizar check-ins de estrategia digital",
     "AD-2-KR1","% check-ins realizados vs planificados","%",90,55,88,"Mensual","CIO / Chief of Staff","up"),
    ("Alineamiento Dinámico","AD-2","Institucionalizar check-ins de estrategia digital",
     "AD-2-KR2","Ajustes estratégicos documentados por trimestre","#",4,0,4,"Trimestral","Chief of Staff TI","up"),
    ("Alineamiento Dinámico","AD-2","Institucionalizar check-ins de estrategia digital",
     "AD-2-KR3","% iniciativas con alineamiento estratégico explícito","%",85,40,83,"Trimestral","Director PMO","up"),
    ("Alineamiento Dinámico","AD-3","Reducir tiempo de prototipado",
     "AD-3-KR1","Lead time promedio prototipo (horas)","horas",48,210,44,"Semanal","Director Arquitectura TI","down"),
    ("Alineamiento Dinámico","AD-3","Reducir tiempo de prototipado",
     "AD-3-KR2","% solicitudes resueltas con reuso/cloud","%",70,22,68,"Trimestral","Director Arquitectura TI","up"),
    ("Liderazgo Digital y Cultural","LC-1","Activar red de change agents",
     "LC-1-KR1","Change agents activos","#",15,4,14,"Trimestral","CHRO / CIO","up"),
    ("Liderazgo Digital y Cultural","LC-1","Activar red de change agents",
     "LC-1-KR2","% bureaus con change agent operativo","%",100,22,89,"Mensual","CHRO","up"),
    ("Liderazgo Digital y Cultural","LC-1","Activar red de change agents",
     "LC-1-KR3","Ideas bottom-up implementadas por trimestre","#",8,1,7,"Trimestral","Director Innovación","up"),
    ("Liderazgo Digital y Cultural","LC-2","Elevar adopción digital y autonomía de equipo",
     "LC-2-KR1","% empleados usando herramientas colaborativas","%",85,31,82,"Mensual","Director TI / RRHH","up"),
    ("Liderazgo Digital y Cultural","LC-2","Elevar adopción digital y autonomía de equipo",
     "LC-2-KR2","Seguridad psicológica (escala 1-10)","score",7.5,4.2,7.1,"Trimestral","CHRO","up"),
    ("Liderazgo Digital y Cultural","LC-2","Elevar adopción digital y autonomía de equipo",
     "LC-2-KR3","% decisiones operativas sin escalar al CIO","%",60,18,58,"Mensual","CIO","up"),
    ("Liderazgo Digital y Cultural","LC-3","Transformar percepción del cambio en staff TI",
     "LC-3-KR1","% staff con actitud positiva al cambio","%",80,33,76,"Trimestral","CHRO","up"),
    ("Liderazgo Digital y Cultural","LC-3","Transformar percepción del cambio en staff TI",
     "LC-3-KR2","% participación en scrums semanales","%",75,28,73,"Semanal","Scrum Master / CIO","up"),
    ("Liderazgo Digital y Cultural","LC-3","Transformar percepción del cambio en staff TI",
     "LC-3-KR3","Rotación voluntaria equipo TI (% anual)","%",8,18,9,"Trimestral","CHRO","down"),
]

@st.cache_data
def build_data(n_weeks=52):
    rng = np.random.default_rng(42)
    rows_ts, rows_sn = [], []
    for (piv,oid,onom,kid,knom,uni,meta,vi,vf,cad,own,direc) in KRS:
        trend = np.linspace(vi, vf, n_weeks)
        noise = abs(vf - vi) * 0.06
        vals  = trend + rng.normal(0, noise, n_weeks)
        if uni == "%":   vals = np.clip(vals, 0, 100)
        elif uni=="score": vals = np.clip(vals, 1, 10)
        else:            vals = np.clip(vals, 0, None)
        for w in range(n_weeks):
            rows_ts.append(dict(
                semana_num=w+1, periodo=f"S{w+1:02d}",
                pivote=piv, objetivo_id=oid, objetivo_nombre=onom,
                kr_id=kid, kr_nombre=knom, unidad=uni,
                valor_actual=round(float(vals[w]),2),
                meta=meta, cadencia=cad, owner=own, direction=direc
            ))
        # snapshot = última semana
        v_last = round(float(vals[-1]), 2)
        pct = min(round(v_last/meta*100,1),100) if direc=="up" else min(round(meta/v_last*100,1),100)
        sem = "🟢 Verde" if pct>=90 else ("🟡 Amarillo" if pct>=70 else "🔴 Rojo")
        rows_sn.append(dict(
            pivote=piv, objetivo_id=oid, objetivo_nombre=onom,
            kr_id=kid, kr_nombre=knom, unidad=uni,
            valor_actual=v_last, meta=meta,
            pct_avance=pct, semaforo=sem,
            cadencia=cad, owner=own, direction=direc
        ))
    return pd.DataFrame(rows_ts), pd.DataFrame(rows_sn)

ts_full, snap_full = build_data()

# ── Página ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FCC IT Modernization — OKR Dashboard",
    page_icon="📡", layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
<style>
html,body,[class*="css"]{{background:{C_BG};color:{C_TEXT};font-family:'Inter','Segoe UI',sans-serif;}}
.stSidebar{{background:{C_CARD};}}
.mcard{{background:{C_CARD};border-radius:12px;padding:18px 20px;border-left:4px solid {C_ACCENT};margin-bottom:10px;}}
.sec{{font-size:1rem;font-weight:700;color:{C_MUTED};letter-spacing:.08em;text-transform:uppercase;margin:26px 0 10px 0;}}
.ibox{{background:{C_CARD};border-radius:10px;padding:16px 20px;border:1px solid #2D3748;margin-bottom:8px;}}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<h2 style='color:{C_ACCENT};margin-bottom:2px'>📡 FCC OKR Dashboard</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{C_MUTED};font-size:.78rem'>Evolución Digital · INCAE 2026</p>", unsafe_allow_html=True)
    st.divider()

    pivote_sel = st.selectbox("🔭 Pivote estratégico",
        ["Todos","Alineamiento Dinámico","Liderazgo Digital y Cultural"])

    per_map = {"Últimas 12 semanas":12,"Últimas 24 semanas":24,"Año completo (52 sem)":52}
    n_weeks = per_map[st.selectbox("📅 Período", list(per_map.keys()))]

    snap_f = snap_full if pivote_sel=="Todos" else snap_full[snap_full["pivote"]==pivote_sel]
    obj_map = {f"{r['objetivo_id']} — {r['objetivo_nombre']}": r['objetivo_id']
               for _, r in snap_f.drop_duplicates("objetivo_id").iterrows()}
    obj_lbl = st.selectbox("🎯 OKR específico", ["Todos"]+list(obj_map.keys()))
    obj_sel = None if obj_lbl=="Todos" else obj_map[obj_lbl]

    st.divider()
    st.markdown(f"<p style='color:{C_MUTED};font-size:.72rem'>Datos simulados · Caso FCC<br>Desouza et al. (2019)</p>",
                unsafe_allow_html=True)

# ── Filtros ────────────────────────────────────────────────────────────────────
snap = snap_full.copy()
ts   = ts_full[ts_full["semana_num"] > (52-n_weeks)].copy()
if pivote_sel != "Todos":
    snap = snap[snap["pivote"]==pivote_sel]
    ts   = ts[ts["pivote"]==pivote_sel]
if obj_sel:
    snap = snap[snap["objetivo_id"]==obj_sel]
    ts   = ts[ts["objetivo_id"]==obj_sel]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='padding:6px 0 18px 0'>
  <h1 style='color:{C_TEXT};font-size:1.75rem;margin:0'>
    FCC IT Modernization — OKR Executive Dashboard
  </h1>
  <p style='color:{C_MUTED};margin:5px 0 0 0'>
    Pivotes: <b>Alineamiento Dinámico</b> · <b>Liderazgo Digital y Cultural</b>
    &nbsp;|&nbsp; Filtro: <b>{pivote_sel}</b> &nbsp;|&nbsp; Período: <b>{n_weeks} semanas</b>
  </p>
</div>
""", unsafe_allow_html=True)

# ── Métricas resumen ───────────────────────────────────────────────────────────
n_v = (snap["semaforo"]=="🟢 Verde").sum()
n_a = (snap["semaforo"]=="🟡 Amarillo").sum()
n_r = (snap["semaforo"]=="🔴 Rojo").sum()
avg = snap["pct_avance"].mean() if not snap.empty else 0

def mcard(col, lbl, val, sub, color):
    col.markdown(f"""
    <div class="mcard" style="border-left-color:{color}">
      <div style="color:{C_MUTED};font-size:.72rem;font-weight:700;text-transform:uppercase">{lbl}</div>
      <div style="font-size:1.9rem;font-weight:800;color:{color};line-height:1.2">{val}</div>
      <div style="color:{C_MUTED};font-size:.73rem">{sub}</div>
    </div>""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
mcard(c1,"KRs en Verde",   f"{n_v}", "En meta o por encima",       C_GREEN)
mcard(c2,"KRs en Amarillo",f"{n_a}", "Entre 70–89% de la meta",    C_YELLOW)
mcard(c3,"KRs en Rojo",    f"{n_r}", "Por debajo del 70% de meta", C_RED)
mcard(c4,"Avance Promedio",f"{avg:.0f}%","Sobre KRs visibles",     C_ACCENT)

# ── Tarjetas por objetivo ──────────────────────────────────────────────────────
st.markdown('<div class="sec">Vista ejecutiva por objetivo</div>', unsafe_allow_html=True)

for obj_id, grp in snap.groupby("objetivo_id", sort=False):
    onom    = grp["objetivo_nombre"].iloc[0]
    piv_nm  = grp["pivote"].iloc[0]
    avg_obj = grp["pct_avance"].mean()
    with st.expander(f"**{obj_id}** — {onom}  |  {piv_nm}  |  Avance: {avg_obj:.0f}%", expanded=True):
        cols = st.columns(len(grp))
        for i,(_,row) in enumerate(grp.iterrows()):
            sc = C_GREEN if "Verde" in row["semaforo"] else (C_YELLOW if "Amarillo" in row["semaforo"] else C_RED)
            icon = "🟢" if "Verde" in row["semaforo"] else ("🟡" if "Amarillo" in row["semaforo"] else "🔴")
            cols[i].markdown(f"""
            <div class="mcard" style="border-left-color:{sc}">
              <div style="color:{C_MUTED};font-size:.68rem;font-weight:700;text-transform:uppercase">{row['kr_id']}</div>
              <div style="font-size:.82rem;color:{C_TEXT};margin:4px 0 8px 0">{row['kr_nombre']}</div>
              <div style="font-size:1.55rem;font-weight:800;color:{sc}">{row['valor_actual']}
                <span style="font-size:.85rem;color:{C_MUTED}"> {row['unidad']}</span></div>
              <div style="color:{C_MUTED};font-size:.72rem">Meta: <b>{row['meta']} {row['unidad']}</b></div>
              <div style="margin:8px 0 4px 0;background:#2D3748;border-radius:4px;height:5px">
                <div style="width:{min(row['pct_avance'],100)}%;background:{sc};height:5px;border-radius:4px"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:.68rem;color:{C_MUTED}">
                <span>{icon} {row['pct_avance']:.0f}%</span>
                <span>👤 {row['owner']}</span>
              </div>
              <div style="font-size:.68rem;color:{C_MUTED};margin-top:3px">🔄 {row['cadencia']}</div>
            </div>""", unsafe_allow_html=True)

# ── Gráficas de tendencia ──────────────────────────────────────────────────────
st.markdown('<div class="sec">Tendencia de KRs en el tiempo</div>', unsafe_allow_html=True)

kr_list = ts["kr_id"].unique().tolist()
n_cols  = min(2, len(kr_list)) if kr_list else 1
cols_ch = st.columns(n_cols)

for idx, kid in enumerate(kr_list):
    df_kr    = ts[ts["kr_id"]==kid].sort_values("semana_num")
    row_s    = snap_full[snap_full["kr_id"]==kid]
    if row_s.empty: continue
    row_s    = row_s.iloc[0]
    sc       = C_GREEN if "Verde" in row_s["semaforo"] else (C_YELLOW if "Amarillo" in row_s["semaforo"] else C_RED)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_kr["periodo"], y=df_kr["valor_actual"],
        fill="tozeroy", fillcolor="rgba(79,142,247,0.07)",
        line=dict(color=sc, width=2.5), mode="lines",
        hovertemplate="%{x}<br>%{y:.1f} "+row_s['unidad']+"<extra></extra>"
    ))
    fig.add_hline(y=row_s["meta"], line_dash="dot", line_color=C_MUTED, line_width=1.5,
                  annotation_text=f"Meta: {row_s['meta']}", annotation_font_color=C_MUTED,
                  annotation_position="bottom right")
    fig.update_layout(
        title=dict(text=f"<b>{kid}</b> — {row_s['kr_nombre']}", font_color=C_TEXT, font_size=12),
        paper_bgcolor=C_CARD, plot_bgcolor=C_BG,
        margin=dict(l=30,r=20,t=48,b=30), height=250,
        font=dict(color=C_MUTED, size=10),
        xaxis=dict(showgrid=False, tickfont_color=C_MUTED, tickangle=-45, nticks=8),
        yaxis=dict(showgrid=True, gridcolor="#1E293B", tickfont_color=C_MUTED),
        showlegend=False,
    )
    cols_ch[idx % n_cols].plotly_chart(fig, use_container_width=True)

# ── Tabla resumen ──────────────────────────────────────────────────────────────
st.markdown('<div class="sec">Tabla resumen de OKRs</div>', unsafe_allow_html=True)

tbl = snap[["pivote","objetivo_id","objetivo_nombre","kr_id","kr_nombre",
            "valor_actual","unidad","meta","pct_avance","semaforo","cadencia","owner"]].copy()
tbl.columns = ["Pivote","Obj","Objetivo","KR","Key Result","Actual","Unidad",
               "Meta","% Avance","Semáforo","Cadencia","Owner"]
tbl["% Avance"] = tbl["% Avance"].map(lambda x: f"{x:.0f}%")
st.dataframe(tbl, use_container_width=True,
             height=min(60+36*len(tbl), 500), hide_index=True)

# ── Insights accionables ───────────────────────────────────────────────────────
st.markdown('<div class="sec">💡 Insights accionables</div>', unsafe_allow_html=True)

def insights(sn):
    out = []
    rojos = sn[sn["semaforo"]=="🔴 Rojo"]
    if not rojos.empty:
        names = ", ".join(rojos["kr_nombre"].tolist()[:2])
        out.append(f"🚨 **Atención inmediata:** {len(rojos)} KR(s) en rojo — *{names}*. "
                   f"Convocar check-in de emergencia con el owner esta semana.")
    if not sn.empty:
        best = sn.loc[sn["pct_avance"].idxmax()]
        out.append(f"✅ **Mayor avance:** *{best['kr_nombre']}* al **{best['pct_avance']:.0f}%** "
                   f"({best['valor_actual']} {best['unidad']} vs meta {best['meta']}). "
                   f"Usar como quick win para comunicar momentum a los bureaus.")
    cult = sn[sn["pivote"]=="Liderazgo Digital y Cultural"]["pct_avance"].mean()
    tec  = sn[sn["pivote"]=="Alineamiento Dinámico"]["pct_avance"].mean()
    if not (np.isnan(cult) or np.isnan(tec)):
        diff = tec - cult
        if diff > 10:
            out.append(f"⚠️ **Brecha cultura vs. estructura:** Alineamiento Dinámico en {tec:.0f}% "
                       f"vs. Liderazgo Cultural en {cult:.0f}% (brecha {diff:.0f} pp). "
                       f"Priorizar activación de change agents y encuestas de seguridad psicológica.")
        elif diff < -10:
            out.append(f"⚠️ **Brecha estructura vs. cultura:** Cambio cultural avanza más rápido "
                       f"({cult:.0f}%) que reconfiguración del portafolio ({tec:.0f}%). "
                       f"Acelerar revisión del portafolio y formalizar check-ins de estrategia.")
        else:
            out.append(f"🔵 **Avance balanceado entre pivotes:** Alineamiento Dinámico {tec:.0f}% · "
                       f"Liderazgo Cultural {cult:.0f}%. Co-evolución saludable. Mantener cadencia actual.")
    return out[:3]

for ins in insights(snap):
    st.markdown(f'<div class="ibox">{ins}</div>', unsafe_allow_html=True)

# ── Notas de interpretación ────────────────────────────────────────────────────
st.markdown('<div class="sec">📖 Notas de interpretación</div>', unsafe_allow_html=True)
with st.expander("Cómo leer este dashboard", expanded=False):
    st.markdown(f"""
<div style="color:{C_TEXT};line-height:1.85;font-size:.9rem">

**¿Qué son estos OKRs?**
OKRs (Objectives and Key Results) combinan una ambición cualitativa (Objetivo) con resultados cuantificables (Key Results). A diferencia de los KPIs tradicionales, tienen tolerancia al error y admiten ajuste continuo — propios del Alineamiento Dinámico.

**Sistema de semáforo**
- 🟢 **Verde** — ≥90% de la meta. Trayectoria de éxito.
- 🟡 **Amarillo** — 70–89% de la meta. Requiere atención táctica.
- 🔴 **Rojo** — <70% de la meta. Intervención ejecutiva urgente.

**Cálculo del % de avance**
- KRs donde *más es mejor*: `valor_actual / meta × 100`
- KRs donde *menos es mejor* (ej. O&M, lead time): `meta / valor_actual × 100`

**Cadencias**
- Semanal: métricas de alta frecuencia (scrums, lead time prototipo)
- Mensual: flujo moderado (% O&M, check-ins realizados)
- Trimestral: impacto cultural y portafolio (encuestas, change agents)

**Pivotes del Marco Evolución Digital (Barahona, INCAE 2026)**
- **Alineamiento Dinámico**: la estrategia es una hipótesis que se valida continuamente, no una arquitectura fija.
- **Liderazgo Digital y Cultural**: la autoridad se construye diariamente mediante orquestación y aprendizaje, no por jerarquía.

**Nota:** Todos los datos son simulados con base en hechos del caso FCC (Desouza, Denford & Krishnamurthy, 2019).

</div>""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(f"""
<div style="text-align:center;color:{C_MUTED};font-size:.72rem;padding:10px 0">
  Caso FCC · Desouza, Denford &amp; Krishnamurthy (2019) &nbsp;|&nbsp;
  Marco: Barahona, J.C. (2026), <i>Evolución Digital</i>, INCAE Business School &nbsp;|&nbsp;
  Dashboard académico · Datos 100% simulados
</div>
""", unsafe_allow_html=True)
