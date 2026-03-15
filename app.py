import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Dual-Core Coach", layout="wide", initial_sidebar_state="expanded")

# --- STYLE VISUEL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stat-card { 
        padding: 20px; border-radius: 15px; background-color: #262730; 
        border: 1px solid #464b5d; margin-bottom: 15px; color: white !important; text-align: center;
    }
    .exercice-box {
        background-color: #1e1e26; padding: 15px; border-left: 5px solid #00ffcc;
        border-radius: 5px; margin-bottom: 10px; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("👤 Profil Athlète")
    poids_input = st.number_input("Poids actuel (kg)", value=75.0)
    taille_input = st.number_input("Taille (cm)", value=180)
    
    st.divider()
    mode_objectif = st.selectbox(
        "Objectif actuel",
        ["Prise de masse", "Maintien", "Sèche"]
    )
    st.success(f"Mode : {mode_objectif}")

# --- NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🏋️ Entraînement", "🍎 Nutrition"])

# --- DASHBOARD ---
with tab1:
    st.title("Tableau de Bord 🚀")
    col1, col2, col3 = st.columns(3)
    imc = round(poids_input / ((taille_input/100)**2), 1)
    with col1: st.markdown(f'<div class="stat-card"><h3>MON IMC</h3><h2>{imc}</h2></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="stat-card"><h3>CALORIES CIBLES</h3><h2>2850</h2></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="stat-card"><h3>OBJECTIF</h3><h2>{mode_objectif}</h2></div>', unsafe_allow_html=True)

# --- ENTRAÎNEMENT ---
with tab2:
    st.title("💪 Plan d'Entraînement")
    
    col_prog, col_input = st.columns([1.5, 1])
    
    with col_prog:
        st.subheader("📅 Sélection du Programme")
        # MODIFICATION : Ajout des 5 séances
        seance = st.radio(
            "Quelle séance fais-tu aujourd'hui ?", 
            [
                "Séance A : Pectoraux / Épaules / Triceps", 
                "Séance B : Dos / Épaules / Biceps", 
                "Séance C : Jambes / Abdos",
                "Séance D : Marche",
                "Séance E : Footing"
            ]
        )
        
        # Logique d'affichage des exercices par séance
        if "Séance A" in seance:
            exercices_liste = ["Développé Couché", "Développé Incliné Haltères", "Dips", "Développé Militaire", "Élévations Latérales", "Extensions Triceps"]
            focus = "Pectoraux, Épaules et Triceps"
        elif "Séance B" in seance:
            exercices_liste = ["Tractions", "Rowing Barre", "Tirage Vertical", "Oiseau (Arrière épaules)", "Curl Biceps Barre", "Curl Marteau"]
            focus = "Dos, Arrière Épaules et Biceps"
        elif "Séance C" in seance:
            exercices_liste = ["Squat", "Presse à cuisses", "Leg Extension", "Leg Curl", "Relevé de jambes (Abdos)", "Gainage (secondes)"]
            focus = "Cuisses, Ischios et Sangle Abdominale"
        elif "Séance D" in seance:
            exercices_liste = ["Marche Rapide", "Marche Inclinaison", "Marche Active Extérieur"]
            focus = "Récupération active / Cardio modéré"
        else:
            exercices_liste = ["Footing Zone 2", "Fractionné", "Endurance Fondamentale"]
            focus = "Cardio / Endurance"

        st.markdown(f'<div class="exercice-box"><b>Focus :</b> {focus}</div>', unsafe_allow_html=True)

    with col_input:
        st.subheader("📝 Suivi de Performance")
        ex_choisi = st.selectbox("Sélectionner l'exercice", exercices_liste)
        
        # Adaptation des curseurs si c'est du cardio (Marche/Footing)
        if "Séance D" in seance or "Séance E" in seance:
            temps = st.select_slider("Durée (minutes)", options=range(1, 121), value=30)
            intensite = st.select_slider("Intensité / Vitesse", options=range(1, 21), value=8)
            if st.button("Enregistrer le cardio"):
                st.success(f"Bravo ! {ex_choisi} : {temps} min à intensité {intensite}")
        else:
            pds = st.select_slider("Charge (kg)", options=range(1, 301), value=60)
            reps = st.select_slider("Répétitions", options=range(1, 21), value=10)
            series = st.select_slider("Nombre de séries", options=range(1, 7), value=4)
            if st.button("Enregistrer la série"):
                st.balloons()
                st.success(f"Enregistré : {ex_choisi} | {series}x{reps} à {pds}kg")
        
        st.divider()
        st.subheader("🤖 Coach IA")
        question = st.text_input("Pose une question au coach sur cette séance :")
        if question: st.info("Le Coach IA prépare une réponse basée sur votre programme...")

# --- NUTRITION ---
with tab3:
    st.title("🍎 Nutrition & Macros")
    st.write(f"Plan alimentaire adapté au mode : **{mode_objectif}**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Glucides", "350g")
    c2.metric("Protéines", "165g")
    c3.metric("Lipides", "75g")
