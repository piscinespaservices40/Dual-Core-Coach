import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Dual-Core Coach", layout="wide", initial_sidebar_state="expanded")

# --- STYLE VISUEL ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at top, #1e1e2f 0%, #0d0d12 100%) !important; color: #e0e0e0 !important; }
    .stat-card { padding: 20px; border-radius: 20px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 255, 204, 0.2); text-align: center; margin-bottom: 20px; backdrop-filter: blur(10px); }
    .stat-card h2 { color: #00ffcc !important; font-size: 2.5rem !important; margin: 0; }
    .stTabs [data-baseweb="tab-active"] { color: #00ffcc !important; border-bottom-color: #00ffcc !important; }
</style>
""", unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("👤 Profil Athlète")
    poids_actuel = st.number_input("Poids (kg)", value=75.0, step=0.1)
    taille = st.number_input("Taille (cm)", value=180)
    objectif = st.selectbox("Objectif", ["Prise de masse", "Maintien", "Sèche"])
    
    st.markdown("---")
    st.subheader("📝 Noter ma séance")
    nouveau_poids = st.number_input("Poids du jour (kg)", value=float(poids_actuel), step=0.1)
    nouvelle_charge = st.number_input("Charge DC (kg)", value=65.0, step=2.5)
    
    if st.button("ENREGISTRER LES DONNÉES"):
        st.session_state.historique_poids[-1] = nouveau_poids
        st.session_state.charge_max[-1] = nouvelle_charge
        st.success("Données enregistrées !")
        st.rerun()

# --- MÉMOIRE DE L'APP ---
if 'historique_poids' not in st.session_state:
    st.session_state.historique_poids = [74.5, 74.8, 75.2, 74.9, 74.5, 74.2, poids_actuel]
if 'charge_max' not in st.session_state:
    st.session_state.charge_max = [60, 60, 62.5, 62.5, 65, 65, 67.5]

jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
data_poids = pd.DataFrame({"Jour": jours, "Poids": st.session_state.historique_poids})
data_entrainement = pd.DataFrame({"Jour": jours, "Charge (kg)": st.session_state.charge_max})
data_nutrition = pd.DataFrame({"Jour": jours, "Proteines": [150, 165, 140, 170, 155, 130, 160], "Lipides": [70, 80, 75, 65, 85, 90, 70], "Glucides": [300, 350, 320, 280, 340, 400, 310]})

# --- ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🏋️ Entraînement", "🍎 Nutrition"])

with tab1:
    st.title("Dual-Core Coach 🚀")
    imc = round(poids_actuel / ((taille/100)**2), 1)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="stat-card"><h3>IMC</h3><h2>{imc}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="stat-card"><h3>CALORIES</h3><h2>2850</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card"><h3>OBJECTIF</h3><h2>{objectif}</h2></div>', unsafe_allow_html=True)
    
    st.subheader("📉 Évolution du Poids (kg)")
    fig_p = px.line(data_poids, x="Jour", y="Poids", markers=True, color_discrete_sequence=['#00ffcc'])
    fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig_p, use_container_width=True)

with tab2:
    st.title("🏋️ Ma Progression")
    st.subheader("📈 Charge Max : Développé Couché")
    fig_c = px.line(data_entrainement, x="Jour", y="Charge (kg)", markers=True, color_discrete_sequence=['#ff6600'])
    fig_c.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig_c, use_container_width=True)

with tab3:
    st.title("🍎 Nutrition")
    fig_n = px.line(data_nutrition, x="Jour", y=["Proteines", "Lipides", "Glucides"], color_discrete_map={"Proteines": "#00ff00", "Lipides": "#ffff00", "Glucides": "#0000ff"})
    fig_n.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), legend_font_color="white")
    st.plotly_chart(fig_n, use_container_width=True)
