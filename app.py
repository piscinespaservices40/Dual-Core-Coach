import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Dual-Core Coach", layout="wide")

# --- STYLE PERSONNALISÉ (TEXTE BLANC FORCÉ) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stat-card { 
        padding: 20px; 
        border-radius: 10px; 
        background-color: #262730; 
        border: 1px solid #464b5d; 
        margin-bottom: 10px;
        color: white !important;
    }
    .stat-card h3, .stat-card h2, .stat-card p {
        color: white !important;
        margin: 0;
    }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("👤 Profil Athlète")
    poids = st.number_input("Poids (kg)", value=75.0)
    taille = st.number_input("Taille (cm)", value=180)
    st.info("Application Opérationnelle ✅")

# --- LOGIQUE DE NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🏋️ Entraînement", "🍎 Nutrition"])

# --- ONGLET 1 : DASHBOARD ---
with tab1:
    st.title("Dual-Core Coach 🚀")
    col1, col2, col3 = st.columns(3)
    
    imc = round(poids / ((taille/100)**2), 1)
    
    with col1:
        st.markdown(f'<div class="stat-card"><h3>IMC</h3><h2>{imc}</h2><p>Analyse en temps réel</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><h3>Objectif</h3><h2>Prise de Masse</h2><p>Semaine 3/12</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><h3>Calories</h3><h2>2800 kcal</h2><p>Cible journalière</p></div>', unsafe_allow_html=True)

    st.subheader("📈 Suivi de Progression")
    chart_data = pd.DataFrame([poids-1, poids-0.5, poids], columns=["Poids (kg)"])
    st.line_chart(chart_data)

# --- ONGLET 2 : ENTRAÎNEMENT (SUIVI DES CHARGES) ---
with tab2:
    st.header("💪 Séance du jour")
    
    # Formulaire de saisie des charges
    with st.expander("📝 Noter mes performances", expanded=True):
        col_ex, col_poids, col_reps = st.columns([3,1,1])
        with col_ex: ex = st.text_input("Exercice", placeholder="ex: Développé couché")
        with col_poids: p = st.number_input("Poids (kg)", min_value=0)
        with col_reps: r = st.number_input("Reps", min_value=0)
        if st.button("Enregistrer la série"):
            st.success(f"Série enregistrée : {ex} - {p}kg x {r}")

    # Interaction IA Coach
    st.divider()
    st.subheader("🤖 Parler au Coach IA")
    user_coach = st.text_input("Pose ta question (ex: Par quoi remplacer le squat ?)", key="coach_ia")
    if user_coach:
        st.write("**Réponse de l'IA :** Je prépare tes conseils personnalisés...")

# --- ONGLET 3 : NUTRITION (INTERACTION) ---
with tab3:
    st.header("🥗 Suivi Nutritionnel")
    
    col_cal, col_prot = st.columns(2)
    col_cal.metric("Calories consommées", "1200 kcal", "-1600 kcal")
    col_prot.metric("Protéines", "90g", "reste 60g")

    st.divider()
    st.subheader("🍴 Assistant Nutrition")
    user_nutri = st.text_input("Une question sur ton repas ? (ex: Quel petit-déjeuner pour 500 kcal ?)", key="nutri_ia")
    if user_nutri:
        st.write("**Conseil Nutrition :** Voici une idée de menu adaptée à tes macros...")
