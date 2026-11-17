import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION DES CHEMINS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR
EXPORT_DIR = os.path.join(BASE_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

st.set_page_config(
    page_title="Atlas Climatique & Prospective RDC (1981–2040)",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_all_data():
    with open(os.path.join(DATA_DIR, "rdc_provinces.geojson"), "r", encoding="utf-8") as f:
        geojson = json.load(f)
    df_hist = pd.read_parquet(os.path.join(DATA_DIR, "historique_1981_2024.parquet"))
    df_atlas = pd.read_parquet(os.path.join(DATA_DIR, "atlas_enrichi_rdc.parquet"))
    df_proj = pd.read_parquet(os.path.join(DATA_DIR, "projections_2026_2040.parquet"))
    return geojson, df_hist, df_atlas, df_proj

geojson, df_hist, df_atlas, df_proj = load_all_data()

# --- GESTION DE L'ÉTAT (PROVINCE & THÈME) ---
if "province_active" not in st.session_state:
    st.session_state.province_active = "Ensemble de la RDC"
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Clair"

# --- CSS ÉDITORIAL HAUT DE GAMME ---
bg_color = "#ffffff" if st.session_state.theme_mode == "Clair" else "#0e1117"
card_bg = "#f8fafc" if st.session_state.theme_mode == "Clair" else "#1e293b"
text_main = "#0f172a" if st.session_state.theme_mode == "Clair" else "#f8fafc"
border_col = "#cbd5e1" if st.session_state.theme_mode == "Clair" else "#334155"
accent_blue = "#1d5fa7"

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_color}; color: {text_main}; }}
    .hero-box {{
        padding: 1.5rem 2rem;
        border-bottom: 1px solid {border_col};
        margin-bottom: 1rem;
    }}
    .hero-title {{
        font-size: 2.4rem;
        font-weight: 800;
        color: {accent_blue};
        line-height: 1.15;
        margin: 0;
    }}
    .hero-sub {{
        font-size: 0.95rem;
        color: #64748b;
        margin-top: 0.5rem;
    }}
    .kpi-card {{
        background-color: {card_bg};
        border: 1px solid {border_col};
        border-radius: 10px;
        padding: 1rem 1.2rem;
        height: 100%;
    }}
    .kpi-label {{ font-size: 0.82rem; color: #64748b; font-weight: 600; }}
    .kpi-val {{ font-size: 1.65rem; font-weight: 800; color: {text_main}; margin: 0.25rem 0; }}
    .kpi-sub {{ font-size: 0.78rem; color: #475569; }}
    .method-note {{
        background-color: #eff6ff;
        border-left: 4px solid {accent_blue};
        padding: 0.9rem 1.2rem;
        border-radius: 6px;
        color: #1e3a8a;
        font-size: 0.88rem;
        margin: 1rem 0;
    }}
    .section-title {{
        font-size: 1.35rem;
        font-weight: 700;
        color: {accent_blue};
        margin-top: 1.2rem;
        margin-bottom: 0.2rem;
    }}
</style>
""", unsafe_allow_html=True)

# --- BANDEAU SUPÉRIEUR ---
st.markdown(f"""
<div style="background:{accent_blue}; color:white; padding:6px 20px; font-size:0.78rem; letter-spacing:0.06em; display:flex; justify-content:space-between; border-radius:4px;">
    <span>Ir. STEPHIN MBOKOLO · PORTAIL CLIMATIQUE NATIONAL RDC</span>
    <span>NORMALES 1991–2020 · OBSERVATIONS 1981–2024 · PROJECTIONS CMIP6 2026–2040</span>
</div>
""", unsafe_allow_html=True)

# --- HERO HEADER ---
c_hero1, c_hero2 = st.columns([1.4, 1])
with c_hero1:
    st.markdown(f"""
    <div class="hero-box">
        <div style="font-weight:700; color:{accent_blue}; font-size:1.1rem; margin-bottom:0.4rem;">atlas RDC · Prospective 2040</div>
        <h1 class="hero-title">Atlas climatique et projections de la République démocratique du Congo</h1>
    </div>
    """, unsafe_allow_html=True)
with c_hero2:
    st.markdown("""
    <div style="padding: 2.2rem 1rem 1rem 1rem; color:#475569; font-size:0.95rem; line-height:1.5;">
        Observations satellitaires et réanalyses <b>CHIRPS & ERA5-Land (1981–2024)</b> et projections multi-modèles 
        <b>NASA NEX-GDDP-CMIP6 (SSP2-4.5 & SSP5-8.5, 2026–2040)</b> pour les 26 provinces de la RDC. 
        Indices climatiques, pentes de Theil-Sen testées par Mann-Kendall, scores composites de risque et analyse sectorielle.
    </div>
    """, unsafe_allow_html=True)

# --- PANNEAU DE CONTRÔLE (THÈME + PILULES DES 26 PROVINCES) ---
with st.container(border=True):
    top_ctrl1, top_ctrl2, top_ctrl3 = st.columns([1, 1.5, 1.5])
    with top_ctrl1:
        theme_choice = st.radio("APPARENCE", ["Clair", "Sombre"], horizontal=True, index=0 if st.session_state.theme_mode == "Clair" else 1)
        if theme_choice != st.session_state.theme_mode:
            st.session_state.theme_mode = theme_choice
            st.rerun()
    with top_ctrl2:
        scen_choice = st.radio("SCÉNARIO CMIP6 (2026–2040)", ["SSP2-4.5", "SSP5-8.5"], horizontal=True)
    with top_ctrl3:
        st.markdown(f"<div style='text-align:right; font-size:0.82rem; color:#64748b; padding-top:1rem;'>26 provinces · 60 ans (1981–2040)<br>Normale de référence 1991–2020 · v2.5</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.78rem; font-weight:700; color:#1d5fa7; margin-top:0.5rem;'>ÉCHELLE D'ANALYSE (CLIQUER SUR UN TERRITOIRE)</div>", unsafe_allow_html=True)
    territoires = ["Ensemble de la RDC"] + sorted(df_atlas["Province"].unique().tolist())

    # Grille de boutons pilules pour les 27 entités (Ensemble + 26 provinces)
    cols_pills = st.columns(9)
    for idx, terr in enumerate(territoires):
        col_idx = idx % 9
        is_active = (st.session_state.province_active == terr)
        if cols_pills[col_idx].button(
            terr, key=f"pill_{terr}",
            type="primary" if is_active else "secondary",
            use_container_width=True
        ):
            st.session_state.province_active = terr
            st.rerun()

prov_sel = st.session_state.province_active

# --- FILTRAGE DES DONNÉES SELON LE TERRITOIRE SÉLECTIONNÉ ---
if prov_sel == "Ensemble de la RDC":
    hist_sub = df_hist.groupby("Annee", as_index=False).mean(numeric_only=True)
    norm_sub = df_atlas.mean(numeric_only=True)
    proj_sub = df_proj[df_proj["Scenario"] == scen_choice].groupby("Annee", as_index=False).mean(numeric_only=True)
    proj_245 = df_proj[df_proj["Scenario"] == "SSP2-4.5"].groupby("Annee", as_index=False).mean(numeric_only=True)
    proj_585 = df_proj[df_proj["Scenario"] == "SSP5-8.5"].groupby("Annee", as_index=False).mean(numeric_only=True)
else:
    hist_sub = df_hist[df_hist["Province"] == prov_sel].sort_values("Annee")
    norm_sub = df_atlas[df_atlas["Province"] == prov_sel].iloc[0]
    proj_sub = df_proj[(df_proj["Province"] == prov_sel) & (df_proj["Scenario"] == scen_choice)].sort_values("Annee")
    proj_245 = df_proj[(df_proj["Province"] == prov_sel) & (df_proj["Scenario"] == "SSP2-4.5")].sort_values("Annee")
    proj_585 = df_proj[(df_proj["Province"] == prov_sel) & (df_proj["Scenario"] == "SSP5-8.5")].sort_values("Annee")

# --- NAVIGATION PAR ONGLETS ÉDITORIAUX ---
tabs = st.tabs([
    "VUE D'ENSEMBLE",
    "CARTOGRAPHIE",
    "CLIMAT OBSERVÉ (1981–2024)",
    "PROJECTIONS & PROBLÈMES (2026–2040)",
    "CLIMAT & SANTÉ",
    "MÉTHODES & EXPORTS"
])

# ==============================================================================
# ONGLET 1 : VUE D'ENSEMBLE (PORTRAIT + CLASSEMENT + THEIL-SEN)
# ==============================================================================
with tabs[0]:
    st.markdown(f"<div class='section-title'>Portrait climatique : {prov_sel}</div>", unsafe_allow_html=True)
    st.caption("Normales 1991–2020 · tendances observées 1981–2024 · horizon projeté 2026–2040")

    delta_t_2040 = proj_sub["Temp_Proj_C"].iloc[-1] - norm_sub["Temp_Moy_C"]
    delta_p_pct = ((proj_sub["Precip_Proj_mm"].mean() - norm_sub["Precip_mm"]) / norm_sub["Precip_mm"]) * 100

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.markdown(f"""<div class="kpi-card"><div class="kpi-label">Pluie annuelle (1991–2020)</div>
        <div class="kpi-val">{norm_sub['Precip_mm']:.0f} mm/an</div>
        <div class="kpi-sub">Tendance : {norm_sub['Sen_Precip']:+.1f} mm/déc.</div></div>""", unsafe_allow_html=True)

    k2.markdown(f"""<div class="kpi-card"><div class="kpi-label">Température moyenne</div>
        <div class="kpi-val">{norm_sub['Temp_Moy_C']:.1f} °C</div>
        <div class="kpi-sub">Tendance : {norm_sub['Sen_Temp']:+.2f} °C/déc.</div></div>""", unsafe_allow_html=True)

    k3.markdown(f"""<div class="kpi-card"><div class="kpi-label">Température max. annuelle</div>
        <div class="kpi-val">{norm_sub['Temp_Max_C']:.1f} °C</div>
        <div class="kpi-sub">Amplitude thermique élevée</div></div>""", unsafe_allow_html=True)

    k4.markdown(f"""<div class="kpi-card"><div class="kpi-label">Pluie extrême (P95)</div>
        <div class="kpi-val">{norm_sub['Pluie_Extreme_P95']:.1f} mm/j</div>
        <div class="kpi-sub">Tendance : {norm_sub['Sen_Ext']:+.2f} mm/déc.</div></div>""", unsafe_allow_html=True)

    k5.markdown(f"""<div class="kpi-card"><div class="kpi-label">Score de risque composite</div>
        <div class="kpi-val">{norm_sub['Score_Composite']:.2f} / 1.0</div>
        <div class="kpi-sub">Indice multi-aléas (1991–2020)</div></div>""", unsafe_allow_html=True)

    k6.markdown(f"""<div class="kpi-card"><div class="kpi-label">Réchauffement 2040 ({scen_choice})</div>
        <div class="kpi-val" style="color:#dc2626;">+{delta_t_2040:.2f} °C</div>
        <div class="kpi-sub">Pluie : {delta_p_pct:+.1f}% vs normale</div></div>""", unsafe_allow_html=True)

    if prov_sel == "Ensemble de la RDC":
        st.markdown("""<div class="method-note">
        ℹ️ À l'échelle « Ensemble de la RDC », les indices sont calculés sur la moyenne nationale des 26 provinces. 
        Moyenner dans l'espace atténue les extrêmes locaux : un pic de pluie torrentielle ou une vague de chaleur provinciale se dilue. 
        Sélectionnez une province ci-dessus pour lire les extrêmes locaux.
        </div>""", unsafe_allow_html=True)

    # --- SECTION : CLASSEMENT DES PROVINCES (CARTE + BARRES EMPILÉES 3 COMPOSANTES) ---
    st.markdown("<div class='section-title'>Classement des provinces</div>", unsafe_allow_html=True)
    st.caption("Scores composites : combinaison pondérée de rangs percentiles entre provinces (0 à 1). Chaque segment vaut un tiers du score.")

    col_left, col_right = st.columns([1.05, 1.15])
    with col_left:
        st.markdown("**Score composite de risque climatique (Normales 1991–2020)**")
        fig_comp_map = px.choropleth_map(
            df_atlas, geojson=geojson, locations="Province", featureidkey="properties.NAME_1",
            color="Score_Composite", color_continuous_scale="YlOrRd", range_color=[0.2, 0.85],
            map_style="carto-positron", zoom=3.6, center={"lat": -2.8, "lon": 23.6}, opacity=0.82
        )
        fig_comp_map.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=490)
        st.plotly_chart(fig_comp_map, use_container_width=True)

    with col_right:
        st.markdown("**Les trois composantes du score (Inondation · Sécheresse · Stress thermique)**")
        df_sorted = df_atlas.sort_values("Score_Composite", ascending=True)
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(y=df_sorted["Province"], x=df_sorted["Score_Inondation"], name="Risque d'inondation", orientation="h", marker_color="#1d5fa7"))
        fig_bar.add_trace(go.Bar(y=df_sorted["Province"], x=df_sorted["Score_Secheresse"], name="Risque de sécheresse", orientation="h", marker_color="#d97706"))
        fig_bar.add_trace(go.Bar(y=df_sorted["Province"], x=df_sorted["Score_Thermique"], name="Risque de stress thermique", orientation="h", marker_color="#dc2626"))
        fig_bar.update_layout(
            barmode="stack", height=510, margin={"r":10,"t":10,"l":10,"b":20},
            xaxis_title="Score composite (0–1)", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- SECTION : SIGNAUX DE CHANGEMENT OBSERVÉS (FOREST PLOT THEIL-SEN + IC 95%) ---
    st.markdown("<div class='section-title'>Signaux de changement observés (1981–2024)</div>", unsafe_allow_html=True)
    st.caption("Tendance 1981–2024 par province, estimée par la pente de Theil-Sen et testée par Mann-Kendall. Trait horizontal = intervalle de confiance à 95 %.")

    var_sen = st.radio("VARIABLE :", ["Température moyenne (°C/déc.)", "Cumul annuel de pluie (mm/déc.)", "Pluie extrême P95 (mm/déc.)"], horizontal=True)

    if "Température" in var_sen:
        col_val, col_low, col_high, col_p, unit = "Sen_Temp", "Sen_Temp_Low", "Sen_Temp_High", "PVal_Sen_Temp", "°C / décennie"
    elif "Cumul" in var_sen:
        col_val, col_low, col_high, col_p, unit = "Sen_Precip", "Sen_Precip_Low", "Sen_Precip_High", "PVal_Sen_Precip", "mm / décennie"
    else:
        col_val, col_low, col_high, col_p, unit = "Sen_Ext", "Sen_Ext_Low", "Sen_Ext_High", "PVal_Sen_Ext", "mm/j / décennie"

    df_sen_plot = df_atlas.sort_values(col_val, ascending=True)
    fig_forest = go.Figure()

    # Lignes d'intervalle de confiance à 95%
    for _, row in df_sen_plot.iterrows():
        fig_forest.add_trace(go.Scatter(
            x=[row[col_low], row[col_high]], y=[row["Province"], row["Province"]],
            mode="lines", line=dict(color="#94a3b8", width=2), showlegend=False, hoverinfo="skip"
        ))

    # Points pleins (p < 0.05) vs cercles vides (non significatif)
    sig_df = df_sen_plot[df_sen_plot[col_p] < 0.05]
    nonsig_df = df_sen_plot[df_sen_plot[col_p] >= 0.05]

    fig_forest.add_trace(go.Scatter(
        x=sig_df[col_val], y=sig_df["Province"], mode="markers", name="Tendance significative (p < 0,05)",
        marker=dict(color="#ea580c", size=9, symbol="circle")
    ))
    fig_forest.add_trace(go.Scatter(
        x=nonsig_df[col_val], y=nonsig_df["Province"], mode="markers", name="Non significative",
        marker=dict(color="white", size=9, symbol="circle", line=dict(color="#ea580c", width=2))
    ))
    fig_forest.add_vline(x=0, line_dash="dash", line_color="#64748b")
    fig_forest.update_layout(
        height=560, xaxis_title=unit, margin={"r":20,"t":30,"l":10,"b":30},
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0)
    )
    st.plotly_chart(fig_forest, use_container_width=True)

# ==============================================================================
# ONGLET 2 : CARTOGRAPHIE THÉMATIQUE INTERACTIVE
# ==============================================================================
with tabs[1]:
    st.markdown("<div class='section-title'>Cartographie provinciale comparative</div>", unsafe_allow_html=True)
    var_map_choice = st.selectbox("Choisir l'indicateur à cartographier :", [
        "Temp_Moy_C", "Temp_Max_C", "Precip_mm", "Pluie_Extreme_P95", "Sen_Temp", "Score_Composite"
    ])
    fig_m2 = px.choropleth_map(
        df_atlas, geojson=geojson, locations="Province", featureidkey="properties.NAME_1",
        color=var_map_choice, color_continuous_scale="RdYlBu_r" if "Temp" in var_map_choice or "Score" in var_map_choice else "Blues",
        map_style="carto-positron", zoom=4.0, center={"lat": -2.8, "lon": 23.6}, opacity=0.82
    )
    fig_m2.update_layout(height=550, margin={"r":0,"t":10,"l":0,"b":0})
    st.plotly_chart(fig_m2, use_container_width=True)

# ==============================================================================
# ONGLET 3 : CLIMAT OBSERVÉ (1981–2024)
# ==============================================================================
with tabs[2]:
    st.markdown(f"<div class='section-title'>Séries historiques observées (1981–2024) — {prov_sel}</div>", unsafe_allow_html=True)
    fig_h1 = go.Figure()
    fig_h1.add_trace(go.Scatter(x=hist_sub["Annee"], y=hist_sub["Temp_Moy_C"], mode="lines+markers", name="Température moyenne (°C)", line=dict(color="#ea580c", width=2.5)))
    fig_h1.add_hline(y=norm_sub["Temp_Moy_C"], line_dash="dash", line_color="#1e293b", annotation_text="Normale 1991–2020")
    fig_h1.update_layout(title="Température moyenne annuelle (1981–2024)", height=360)
    st.plotly_chart(fig_h1, use_container_width=True)

    fig_h2 = px.bar(hist_sub, x="Annee", y="Precip_mm", title="Cumul pluviométrique annuel (1981–2024)", color_discrete_sequence=["#1d5fa7"])
    fig_h2.add_hline(y=norm_sub["Precip_mm"], line_dash="dash", line_color="#dc2626", annotation_text="Normale 1991–2020")
    fig_h2.update_layout(height=360)
    st.plotly_chart(fig_h2, use_container_width=True)

# ==============================================================================
# ONGLET 4 : PROJECTIONS & PROBLÈMES CLIMATIQUES (2026–2040)
# ==============================================================================
with tabs[3]:
    st.markdown(f"<div class='section-title'>Trajectoires CMIP6 & Évolution des Problèmes (2026–2040) — {prov_sel}</div>", unsafe_allow_html=True)

    c_p1, c_p2 = st.columns(2)
    with c_p1:
        fig_comp_scen = go.Figure()
        fig_comp_scen.add_trace(go.Scatter(x=hist_sub["Annee"].tail(15), y=hist_sub["Temp_Moy_C"].tail(15), name="Observé (2010–2024)", line=dict(color="#64748b")))
        fig_comp_scen.add_trace(go.Scatter(x=proj_245["Annee"], y=proj_245["Temp_Proj_C"], name="CMIP6 SSP2-4.5", line=dict(color="#059669", width=3)))
        fig_comp_scen.add_trace(go.Scatter(x=proj_585["Annee"], y=proj_585["Temp_Proj_C"], name="CMIP6 SSP5-8.5", line=dict(color="#dc2626", width=3, dash="dot")))
        fig_comp_scen.update_layout(title="Comparaison des scénarios thermiques (2026–2040)", height=380)
        st.plotly_chart(fig_comp_scen, use_container_width=True)

    with c_p2:
        # Indices normalisés Base 100 = Normale 1991-2020 (Calibrés)
        proj_risk = proj_sub.copy()
        proj_risk["Crues_Inondations"] = (proj_risk["Pluie_Ext_Proj"] / norm_sub["Pluie_Extreme_P95"]) * 100
        proj_risk["Stress_Thermique"] = ((proj_risk["Temp_Proj_C"] - norm_sub["Temp_Moy_C"]) * 15) + 100
        proj_risk["Deficit_Hydrique"] = (norm_sub["Precip_mm"] / proj_risk["Precip_Proj_mm"]) * 100

        fig_risks = px.line(
            proj_risk, x="Annee", y=["Crues_Inondations", "Stress_Thermique", "Deficit_Hydrique"],
            labels={"value": "Indice de sévérité (Base 100 = 1991–2020)", "variable": "Aléa"},
            title=f"Intensification des aléas majeurs ({scen_choice})"
        )
        fig_risks.add_hline(y=100, line_dash="dot", line_color="gray", annotation_text="Référence 1991–2020")
        fig_risks.update_layout(height=380)
        st.plotly_chart(fig_risks, use_container_width=True)

    st.markdown("### Matrice Prospective des 5 Problèmes Majeurs en RDC (2026 → 2040)")
    st.dataframe(pd.DataFrame({
        "Problème Climatique": [
            "1. Crues fluviales & inondations urbaines",
            "2. Stress thermique & vagues de chaleur",
            "3. Perturbation des saisons agricoles",
            "4. Risques hydriques & vectoriels (Choléra/Paludisme)",
            "5. Fragilisation des tourbières & feux de brousse"
        ],
        "Référence (1991–2020)": [
            "Crues décennales localisées",
            "Rares pics > 35°C en saison sèche",
            "Saisons A et B régulières",
            "Endémicité saisonnière",
            "Humidité permanente en Cuvette Centrale"
        ],
        "Horizon Court (2026–2032)": [
            "+10 à +15% d'intensité des pluies extrêmes (P95)",
            "+0,6 à +0,9°C ; hausse des nuits chaudes",
            "Décalage de 5 à 10 jours du démarrage des pluies",
            "Pics épidémiques post-pluies torrentielles",
            "Baisse saisonnière du niveau des nappes"
        ],
        "Horizon Moyen (2033–2040)": [
            "Inondations récurrentes (Kinshasa, Fleuve Congo, Kasaï)",
            "+1,1 à +1,5°C ; baisse de productivité agricole",
            "Sécheresses intra-saisonnières (Katanga/Kasaï)",
            "Expansion altitudinale (Kivu/Tanganyika)",
            "Risque critique d'incendies sur tourbières"
        ]
    }), use_container_width=True)

# ==============================================================================
# ONGLET 5 : CLIMAT & SANTÉ (ONE HEALTH)
# ==============================================================================
with tabs[4]:
    st.markdown(f"<div class='section-title'>Vulnérabilité Sanitaire & Approche One Health — {prov_sel}</div>", unsafe_allow_html=True)
    st.write("""
    Le croisement des anomalies climatiques (1981–2040) avec les déterminants épidémiologiques de la RDC met en évidence trois mécanismes prioritaires :
    - **Maladies hydriques (Choléra, diarrhées aiguës) :** Corrélation directe avec les événements de précipitations extrêmes (`P95`) et les crues dans les provinces riveraines du fleuve Congo et des Grands Lacs (Tanganyika, Nord-Kivu, Sud-Kivu, Kinshasa).
    - **Maladies à transmission vectorielle (Paludisme, arboviroses) :** Le réchauffement observé (`+0,18 à +0,60 °C/décennie`) favorise la survie et la reproduction d'*Anopheles* dans les zones d'altitude auparavant protégées (Kivu, Ituri).
    - **Risques zoonotiques et déforestation :** L'assèchement saisonnier des forêts et tourbières de la Cuvette Centrale (Mai-Ndombe, Équateur, Tshuapa) accroît la fragmentation des habitats et les interfaces faune-humains.
    """)

# ==============================================================================
# ONGLET 6 : MÉTHODES & EXPORTS DIRECTS (D:\Portail_Climatique_RDC\exports)
# ==============================================================================
with tabs[5]:
    st.markdown("<div class='section-title'>Méthodologie & Exportation des Bases de Données</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Observations historiques (1981–2024) :** Précipitations journalières **CHIRPS v2.0** (5 km) et températures **ERA5-Land** (9 km), agrégées sur les limites administratives **GADM 4.1** (26 provinces).
    - **Normales climatiques :** Période de référence standard **1991–2020** (Organisation Météorologique Mondiale).
    - **Statistiques de tendance :** Pente non-paramétrique de **Theil-Sen** avec intervalle de confiance à 95 % et test de significativité de **Mann-Kendall** ($\alpha = 0,05$).
    - **Projections 2026–2040 :** Ensemble multi-modèles **NASA NEX-GDDP-CMIP6** (`ACCESS-CM2`, `GFDL-ESM4`, `MPI-ESM1-2-HR`, `MRI-ESM2-0`) sous **SSP2-4.5** et **SSP5-8.5**.
    """)

    c_exp1, c_exp2 = st.columns(2)
    with c_exp1:
        if st.button("💾 Sauvegarder le tableau complet des 26 provinces (CSV)"):
            path_all = os.path.join(EXPORT_DIR, "Atlas_Climatique_RDC_26_Provinces.csv")
            df_atlas.to_csv(path_all, index=False, encoding="utf-8-sig")
            st.success(f"Fichier enregistré dans : `{path_all}`")
    with c_exp2:
        if st.button(f"💾 Sauvegarder les projections 2026–2040 ({prov_sel})"):
            path_p = os.path.join(EXPORT_DIR, f"Projections_2026_2040_{prov_sel.replace(' ', '_')}.csv")
            proj_sub.to_csv(path_p, index=False, encoding="utf-8-sig")
            st.success(f"Fichier enregistré dans : `{path_p}`")


st.markdown("---")
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; color:#475569; font-size:0.88rem; padding-bottom:1.5rem;">
    <div>
        <b style="color:#0f172a; font-size:1rem;">Ir. Stephin Mbokolo</b><br>
        Modélisation Appliquée en Santé Globale, Changement Climatique & Sciences de l'Environnement · RDC<br>
        <i>Source : CHIRPS v2.0 & ERA5-Land (1981–2024), Normale OMM (1991–2020), Projections NASA NEX-GDDP-CMIP6 (2026–2040).</i>
    </div>
</div>
""", unsafe_allow_html=True)
