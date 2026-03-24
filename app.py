import streamlit as st
import pandas as pd
import plotly.express as px
# Configuration de la page
st.set_page_config(page_title="Dual-Core Coach", layout="wide", initial_sidebar_state="expanded")

# --- STYLE VISUEL : SPORTSWEAR FUSION ---
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #1e1e2f 0%, #0d0d12 100%) !important;
        color: #e0e0e0 !important;
    }
    .stat-card { 
        padding: 20px; border-radius: 20px; background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 204, 0.2); text-align: center; margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    .stat-card h2 { color: #00ffcc !important; font-size: 2.5rem !important; margin: 0; }
    .exercice-box {
        background: rgba(0, 255, 204, 0.03); border-left: 5px solid #ff6600;
        padding: 15px; border-radius: 8px; margin-bottom: 15px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff6600 0%, #ff3300 100%) !important;
        color: white !important; border-radius: 50px !important; font-weight: bold !important;
        text-transform: uppercase; width: 100%;
    }
    .stTabs [data-baseweb="tab--active"] { color: #00ffcc !important; border-bottom-color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("👤 Profil Athlète")
    poids = st.number_input("Poids (kg)", value=75.0)
    taille = st.number_input("Taille (cm)", value=180)
    objectif = st.selectbox("Objectif", ["Prise de masse", "Maintien", "Sèche"])
    st.info(f"Mode activé : {objectif}")
# Données pour les graphiques
jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
data_nutrition = pd.DataFrame({
    "Jour": jours,
    "Proteines": [150, 165, 140, 170, 155, 130, 160],
    "Lipides": [70, 80, 75, 65, 85, 90, 70],
    "Glucides": [300, 350, 320, 280, 340, 400, 310]
})
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🏋️ Entraînement", "🍎 Nutrition"])
# Données pour le suivi du poids
data_poids = pd.DataFrame({
    "Jour": jours,
    "Poids": [poids - 0.5, poids - 0.3, poids, poids - 0.2, poids - 0.6, poids - 0.8, poids]
})
# --- TAB 1 : DASHBOARD ---
with tab1:
    st.title("Dual-Core Coach 🚀")
    c1, c2, c3 = st.columns(3)
    imc = round(poids / ((taille/100)**2), 1)
    with c1: st.markdown(f'<div class="stat-card"><h3>IMC</h3><h2>{imc}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><h3>CALORIES</h3><h2>2850</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card"><h3>OBJECTIF</h3><h2>{objectif}</h2></div>', unsafe_allow_html=True)
st.markdown("---")
    st.subheader("📉 Évolution du Poids (kg)")

    # Création du graphique de poids (couleur néon comme ton IMC)
    fig_poids = px.line(data_poids, x="Jour", y="Poids", 
                        markers=True,
                        color_discrete_sequence=['#00ffcc']) 

    # Style pour fond sombre
    fig_poids.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color="white"),
        hovermode="x unified"
    )
    
    # On ajuste l'axe Y pour que la courbe soit jolie
    fig_poids.update_yaxes(range=[poids-2, poids+2])

    st.plotly_chart(fig_poids, use_container_width=True)
# --- TAB 2 : ENTRAÎNEMENT ---
with tab2:
    col_left, col_right = st.columns([1.5, 1])
    with col_left:
        st.subheader("📅 Programme")
        seance = st.radio("Séance du jour :", ["A: Pecs/Epaules/Triceps", "B: Dos/Epaules/Biceps", "C: Jambes/Abdos", "D: Marche", "E: Footing"])
        
        ex_dict = {
            "A: Pecs/Epaules/Triceps": ["Développé Couché", "Dips", "Développé Militaire"],
            "B: Dos/Epaules/Biceps": ["Tractions", "Rowing", "Curl Biceps"],
            "C: Jambes/Abdos": ["Squat", "Presse", "Gainage"],
            "D: Marche": ["Marche Rapide"], "E: Footing": ["Running"]
        }
        exercices = ex_dict[seance]
        st.markdown(f'<div class="exercice-box"><b>Focus :</b> {seance}</div>', unsafe_allow_html=True)

    with col_right:
        st.subheader("📝 Performance")
        ex_sel = st.selectbox("Exercice", exercices)
        pds = st.select_slider("Poids (kg)", options=range(0, 301), value=60)
        reps = st.select_slider("Répétitions", options=range(1, 21), value=10)
        sets = st.select_slider("Séries", options=range(1, 7), value=4)
        if st.button("ENREGISTRER"):
            st.success("Série validée !")

        st.divider()
        st.subheader("🤖 Coach IA")
        q = st.text_input("Pose une question :")
        if q:
            # Simulation d'IA intelligente sans clé API
            st.info(f"Coach : Pour le {ex_sel} en mode {objectif}, assure-toi de contrôler la descente. Vise l'échec sur la dernière série !")

# --- TAB 3 : NUTRITION ---
with tab3:
    st.title("🍎 Nutrition Sportive")
    col1, col2, col3 = st.columns(3)
    col1.metric("Glucides", "350g")
    col2.metric("Protéines", "165g")
    col3.metric("Lipides", "75g")
    
    st.subheader("🍽️ Journée Type")
    with st.expander("Consulter mes repas", expanded=True):
        if objectif == "Prise de masse":
            st.write("- **Matin:** Avoine, 3 œufs, 1 banane\n- **Midi:** Poulet, Riz, Brocolis\n- **Soir:** Poisson, Patate douce")
        else:
            st.write("- **Matin:** Blancs d'œufs, 1 fruit\n- **Midi:** Dinde, Quinoa, Salade\n- **Soir:** Poisson blanc, Légumes verts")
    
    st.divider()
    st.subheader("📸 Scan ton Frigo")
    img = st.file_uploader("Prends une photo de tes ingrédients :", type=["jpg", "png"])
    if img:
        st.image(img, caption="Analyse en cours...", use_container_width=True)
        st.warning("L'analyse visuelle nécessite la connexion au cerveau GPT-4 Vision.")
# --- GRAPHIQUE NUTRITION ---
    st.markdown("---")
    st.subheader("🥗 Suivi des Macros (g)")
    
    # On crée le graphique avec tes couleurs
    fig_nutri = px.line(data_nutrition, x="Jour", 
                        y=["Proteines", "Lipides", "Glucides"],
                        color_discrete_map={
                            "Proteines": "#00ff00", # Vert
                            "Lipides": "#ffff00",   # Jaune
                            "Glucides": "#0000ff"   # Bleu
                        })

 # On rend tout le texte du graphique blanc, y compris la légende
    fig_nutri.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color="white"), # Force TOUTE la police en blanc
        legend_title_font_color="white",
        legend_font_color="white",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_nutri, use_container_width=True)
