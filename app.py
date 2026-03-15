import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Dual-Core Coach", layout="wide", initial_sidebar_state="expanded")

# --- STYLE VISUEL (TEXTE BLANC & CADRANS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stat-card { 
        padding: 20px; 
        border-radius: 15px; 
        background-color: #262730; 
        border: 1px solid #464b5d; 
        margin-bottom: 15px;
        color: white !important;
        text-align: center;
    }
    .stat-card h3 { color: #808495 !important; font-size: 0.9rem; margin-bottom: 5px; }
    .stat-card h2 { color: white !important; font-size: 1.8rem; margin: 0; }
    .stat-card p { color: #00ffcc !important; font-size: 0.8rem; margin-top: 5px; }
    
    .exercice-box {
        background-color: #1e1e26;
        padding: 15px;
        border-left: 5px solid #00ffcc;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("👤 Profil Athlète")
    poids_input = st.number_input("Poids actuel (kg)", value=75.0)
    taille_input = st.number_input("Taille (cm)", value=180)
    st.divider()
    st.success("Application Opérationnelle ✅")
    st.info("Mode : Prise de masse")

# --- NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🏋️ Entraînement", "🍎 Nutrition"])

# --- DASHBOARD ---
with tab1:
    st.title("Tableau de Bord 🚀")
    col1, col2, col3 = st.columns(3)
    imc = round(poids_input / ((taille_input/100)**2), 1)
    
    with col1:
        st.markdown(f'<div class="stat-card"><h3>MON IMC</h3><h2>{imc}</h2><p>Athlétique</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><h3>CALORIES CIBLES</h3><h2>2850</h2><p>+300 kcal surplus</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><h3>PROTÉINES</h3><h2>165g</h2><p>2.2g / kg</p></div>', unsafe_allow_html=True)

    st.subheader("📈 Évolution du poids")
    st.line_chart(pd.DataFrame([poids_input-1, poids_input-0.5, poids_input], columns=["Poids"]))

# --- ENTRAÎNEMENT (RETOUR DES PROGRAMMES) ---
with tab2:
    st.title("💪 Programmes de Musculation")
    
    col_prog, col_input = st.columns([2, 1])
    
    with col_prog:
        with st.expander("📅 Séance A : Pectoraux / Triceps", expanded=True):
            st.markdown("""
            <div class="exercice-box">
                <b>Développé Couché :</b> 4 séries x 8-10 reps (Repos 2min)<br>
                <b>Développé Incliné Haltères :</b> 3 séries x 12 reps<br>
                <b>Dips :</b> 3 séries x Max reps<br>
                <b>Extensions Triceps poulie :</b> 3 séries x 15 reps
            </div>
            """, unsafe_allow_html=True)
            
        with st.expander("📅 Séance B : Dos / Biceps"):
            st.markdown("""
            <div class="exercice-box">
                <b>Tractions :</b> 4 séries x Max reps<br>
                <b>Rowing Barre :</b> 4 séries x 10 reps<br>
                <b>Curl Barre :</b> 3 séries x 12 reps<br>
                <b>Hammer Curl :</b> 3 séries x 12 reps
            </div>
            """, unsafe_allow_html=True)

    with col_input:
        st.subheader("📝 Noter ma séance")
        ex = st.text_input("Exercice fait", placeholder="ex: Couché")
        pds = st.number_input("Charge (kg)", min_value=0)
        reps = st.number_input("Répétitions", min_value=0)
        if st.button("Enregistrer"):
            st.success("Séance sauvegardée !")
        
        st.divider()
        st.subheader("🤖 Coach IA")
        question = st.text_input("Question technique ?")
        if question: st.info("Analyse en cours...")

# --- NUTRITION (RETOUR DES MACROS) ---
with tab3:
    st.title("🍎 Plan Nutritionnel")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Glucides", "350g", "50%")
    c2.metric("Protéines", "165g", "25%")
    c3.metric("Lipides", "75g", "25%")

    st.subheader("🍽️ Idée de repas type")
    st.info("**Petit-Déjeuner :** 80g d'avoine, 3 oeufs, 1 banane.\n\n**Déjeuner :** 150g Poulet, 200g Riz pesé cuit, Légumes verts.\n\n**Dîner :** 150g Poisson blanc, Patate douce, Huile d'olive.")
    
    st.divider()
    st.subheader("🍴 Assistant Nutrition")
    repas_q = st.text_input("Besoin d'un menu pour ce soir ?")
    if repas_q: st.warning("Recherche de recettes adaptées...")
