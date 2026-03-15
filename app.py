import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Dual-Core Coach", page_icon="💪", layout="wide")

# Style CSS personnalisé pour un look sportif
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stat-card { 
        padding: 20px; 
        border-radius: 10px; 
        background-color: #262730; 
        border: 1px solid #464b5d; 
        margin-bottom: 10px;
        color: white !important; /* Force le texte en blanc */
    }
    .stat-card h3, .stat-card h2, .stat-card p {
        color: white !important; /* Force tout le contenu en blanc */
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Profil & Matériel) ---
st.sidebar.title("👤 Profil Athlète")
poids = st.sidebar.number_input("Poids (kg)", value=70.5, step=0.1)
taille = st.sidebar.number_input("Taille (cm)", value=166)
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Matériel disponible")
st.sidebar.info("Haltères (4-22kg), Barre, Rack, Banc, Kettlebells, Tapis 6km/h")

# --- NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🏋️ Entraînement", "🍎 Nutrition"])

# --- TAB 1 : DASHBOARD ---
with tab1:
    st.title("Dual-Core Coach 🚀")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-card"><h3>IMC</h3><h2>25.6</h2><p>Normal/Athlétique</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><h3>Objectif Pas</h3><h2>10 000</h2><p>Tapis: 6km/h conseillé</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><h3>Statut</h3><h2>🔥 En forme</h2><p>Surcharge progressive active</p></div>', unsafe_allow_html=True)

    st.subheader("📈 Suivi de Progression")
    chart_data = pd.DataFrame({'Poids': [71, 70.8, 70.5]}, index=['Sem 1', 'Sem 2', 'Sem 3'])
    st.line_chart(chart_data)

# --- TAB 2 : ENTRAÎNEMENT (Agent IRON) ---
with tab2:
    st.header("🦾 Agent IRON : Musculation")
    st.write("Programme optimisé pour : **Haltères max 22kg + Barre**")
    
    seance = st.selectbox("Choisir la séance", ["Push (Pectoraux/Epaules/Triceps)", "Pull (Dos/Biceps)", "Legs (Jambes/Abdos)"])
    
    st.warning("🔄 **Technique Anti-Stagnation :** Tempo 4-2-1 (4s descente, 2s pause, 1s montée)")

    if "Push" in seance:
        st.checkbox("Développé Couché Incliné (Barre) : 4 x 8-10 reps")
        st.checkbox("Développé Militaire (Haltères 22kg) : 3 x 10 reps")
        st.checkbox("Élévations Latérales (Haltères) : 4 x 15 reps")
        st.checkbox("Dips au banc : 3 x échec")
    elif "Pull" in seance:
        st.checkbox("Rowing Barre : 4 x 8 reps")
        st.checkbox("Rowing unilatéral (Haltère 22kg) : 3 x 12 reps")
        st.checkbox("Oiseau haltères : 3 x 15 reps")
        st.checkbox("Curl Haltères : 3 x 12 reps")
    else:
        st.checkbox("Fentes Bulgares (Haltères 22kg) : 3 x 10 reps/jambe")
        st.checkbox("Squat au Rack : 4 x 8-10 reps")
        st.checkbox("Kettlebell Swings : 3 x 45 sec")
        st.checkbox("Gainage : 3 x 1 min")

# --- TAB 3 : NUTRITION (Agent KITCHEN) ---
with tab3:
    st.header("🥗 Agent KITCHEN : Nutrition")
    st.info(f"Objectif : Recomposition pour {poids} kg")
    
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.metric("Calories Cibles", "2150 kcal")
        st.metric("Protéines", "150g")
    with col_n2:
        st.metric("Lipides", "70g")
        st.metric("Glucides", "230g")

    st.subheader("📝 Menu du jour conseillé")
    st.write("- **Matin :** 3 œufs + 50g Avoine")
    st.write("- **Midi :** 150g Poulet + 60g Riz (cru) + Brocolis")
    st.write("- **Collation :** 200g Fromage Blanc + 20g Amandes")
    st.write("- **Soir :** 150g Poisson + 200g Patate douce + Salade")

st.sidebar.success("Application Opérationnelle ✅")
