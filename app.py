import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Dual-Core Coach AI", layout="wide", initial_sidebar_state="expanded")

# --- STYLE VISUEL (CSS) ---
st.markdown("""
<style>
    /* Fond de l'application */
    .stApp { background: radial-gradient(circle at top, #1e1e2f 0%, #0d0d12 100%) !important; color: #e0e0e0 !important; }
    
    /* Titres des cartes de stats */
    .stat-card { padding: 20px; border-radius: 20px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 255, 204, 0.2); text-align: center; margin-bottom: 20px; backdrop-filter: blur(10px); }
    .stat-card h2 { color: #00ffcc !important; font-size: 2.2rem !important; margin: 0; }
    
    /* --- COULEUR BLEU NÉON POUR TOUS LES LABELS (NET ET PRÉCIS) --- */
    label, .stMarkdown p, .stSelectbox label, .stSlider label, .stNumberInput label, [data-testid="stWidgetLabel"] p {
        color: #00ffcc !important;
        font-weight: bold !important;
        text-shadow: none !important; /* On retire l'ombre qui fait baver le texte */
        font-size: 1rem !important;
    }

    /* Rendre spécifiquement les textes Jour, Semaine, Mois très clairs */
    div[data-testid="stRadio"] label p {
        color: #00ffcc !important;
        text-shadow: none !important;
    }

    /* Style des onglets */
    .stTabs [data-baseweb="tab-active"] { color: #ff6600 !important; border-bottom-color: #ff6600 !important; }
    
    /* Bouton Valider personnalisé */
    div.stButton > button {
        background-color: #ff6600 !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

    # --- BASE DE DONNÉES EXERCICES (Avec Icônes) ---
exercices_db = {
    "胸 Pectoraux": ["Développé Couché", "Développé Incliné", "Écartés Poulie", "Dips", "Pompes Lestées", "Chest Press", "Développé Haltères", "Pull-over", "Écartés Haltères", "Machine convergente"],
    "背 Dos": ["Tractions", "Tirage Poitrine", "Rowing Barre", "Tirage Horizontal", "Lumbaires", "Rowing Haltère", "Tirage Vertical Large", "Facepull", "Shrugs Barre", "Pull-down bras tendus"],
    "肩 Épaules": ["Développé Militaire", "Élévations Latérales", "Oiseau Poulie", "Développé Arnold", "Développé Haltères Assis", "Tirage Menton", "Élévations Frontales", "Reverse Pec Deck", "Push Press", "L-Fly"],
    "🦵 Jambes": ["Squat", "Presse à Cuisses", "Leg Extension", "Leg Curl", "Fentes", "Hack Squat", "SDT Jambes Tendues", "Sissy Squat", "Step-up", "Bulgarian Split Squat"],
    "💪 Bras": ["Curl Barre", "Curl Marteau", "Curl Incliné", "Extension Triceps Poulie", "Barre au Front", "Curl Larry Scott", "Dips Triceps", "Kickback", "Spider Curl", "Triceps Pushdown Corde"],
    "🍑 Fessiers/Mollets": ["Mollets Debout", "Mollets Assis", "Hip Thrust", "Abducteurs", "Kickback Fessier", "Presse Mollets", "Glute Bridge", "Fentes Croisées", "Mollets à la Presse", "Donkey Calf Raise"],
    "🍫 Abdos": ["Crunch", "Gainage", "Levé de Jambes", "Russian Twist", "Roulette Abdos", "Mountain Climbers", "Sit-ups", "Planche Latérale", "V-ups", "Leg Raise suspendu"],
    "🫀 Cardio": ["Course à pied", "Vélo", "Rameur", "Corde à sauter", "Elliptique", "Natation", "HIIT", "Burpees", "Marche inclinée", "Assault Bike"]
}


# --- MÉMOIRE DE L'APP ---
if 'historique_charges' not in st.session_state:
    # On initialise un dictionnaire vide pour stocker les charges par exercice
    st.session_state.historique_charges = {ex: [50, 52, 55, 55, 58, 60, 62] for muscle in exercices_db for ex in exercices_db[muscle]}

if 'poids_corps' not in st.session_state:
    st.session_state.poids_corps = [75.0, 74.8, 75.2, 74.9, 74.5, 74.2, 75.0]

jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

# --- BARRE LATÉRALE (PROFIL UNIQUEMENT) ---
with st.sidebar:
    st.title("👤 Profil Athlète")
    poids = st.number_input("Poids actuel (kg)", value=75.0, step=0.1)
    taille = st.number_input("Taille (cm)", value=180)
    objectif = st.selectbox("Objectif", ["Prise de masse", "Maintien", "Sèche"])
    st.info(f"Mode : {objectif}")

# --- CONTENU PRINCIPAL ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🏋️ Entraînement", "🍎 Nutrition", "🤖 Coach AI"])

# --- TAB 1 : DASHBOARD ---
with tab1:
    st.title("Performance Hub 🚀")
    imc = round(poids / ((taille/100)**2), 1)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="stat-card"><h3>IMC</h3><h2>{imc}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="stat-card"><h3>CALORIES</h3><h2>2850</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card"><h3>SÉANCES/SEM</h3><h2>5</h2></div>', unsafe_allow_html=True)
    
    st.subheader("📉 Évolution du Poids")
    fig_p = px.line(x=jours, y=st.session_state.poids_corps, markers=True, color_discrete_sequence=['#00ffcc'])
    fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig_p, use_container_width=True)

# --- TAB 2 : ENTRAÎNEMENT (LA PARTIE TECHNIQUE) ---
with tab2:
    st.title("🏋️ Gestion des Séances")
    
    col_input, col_graph = st.columns([1, 2])
    
    with col_input:
        st.subheader("📝 Noter ma Charge")
        muscle_select = st.selectbox("Groupe Musculaire", list(exercices_db.keys()))
        exercice_select = st.selectbox("Exercice", exercices_db[muscle_select])
        
        charge = st.number_input("Charge soulevée (kg)", value=60.0, step=2.5)
        reps = st.slider("Nombre de répétitions", 1, 30, 10)
        series = st.slider("Nombre de séries", 1, 10, 4)
        
        if st.button("VALIDER LA SÉANCE"):
            st.session_state.historique_charges[exercice_select].append(charge)
            st.success(f"Enregistré : {exercice_select} à {charge}kg")
            st.rerun()

    with col_graph:
        periode = st.radio("Vue de la progression :", ["Jour", "Semaine", "Mois"], horizontal=True)
        st.subheader(f"📈 Progression : {exercice_select}")
        
        # Récupération de TOUTES les données enregistrées pour cet exercice
        y_data = st.session_state.historique_charges[exercice_select]
        
        # On crée des étiquettes simples (Séance 1, Séance 2...) pour éviter les erreurs de dates
        x_label = [f"Séance {i+1}" for i in range(len(y_data))]

        # On adapte la vue selon le bouton, mais SEULEMENT si on a assez de données
        if periode == "Jour" and len(y_data) > 7:
            y_data = y_data[-7:]
            x_label = x_label[-7:]
        elif periode == "Semaine" and len(y_data) > 4:
            # On affiche un point par groupe de 4 séances pour simuler les semaines
            y_data = y_data[::4]
            x_label = [f"Sem {i+1}" for i in range(len(y_data))]

        # Création du graphique sécurisé
        fig_ex = px.area(x=x_label, y=y_data, markers=True, color_discrete_sequence=['#ff6600'])
        
        fig_ex.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="white"),
            xaxis_title="Chronologie des séances",
            yaxis_title="Charge (kg)"
        )
        
        st.plotly_chart(fig_ex, use_container_width=True)

# --- TAB 3 : NUTRITION ---
with tab3:
    st.title("🍎 Nutrition & Macros")
    st.subheader("Suivi hebdomadaire")
    data_nutri = pd.DataFrame({"Jour": jours, "Proteines": [150, 160, 155, 170, 150, 140, 160], "Lipides": [70, 75, 70, 65, 80, 85, 70], "Glucides": [300, 320, 310, 290, 330, 350, 300]})
    fig_n = px.line(data_nutri, x="Jour", y=["Proteines", "Lipides", "Glucides"], color_discrete_map={"Proteines": "#00ff00", "Lipides": "#ffff00", "Glucides": "#0000ff"})
    fig_n.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), legend_font_color="white")
    st.plotly_chart(fig_n, use_container_width=True)

# --- TAB 4 : AGENT AI ---
with tab4:
    st.title("🤖 Dual-Core Coach AI : Expert Omniscient")
    st.markdown('<p style="color:#00ffcc; font-weight:bold;">Analyse Multimodale : Sommeil, Nutrition, Récupération & Biomécanique.</p>', unsafe_allow_html=True)
    
    # --- SECTION RÉCUPÉRATION ---
    col_recup1, col_recup2 = st.columns(2)
    with col_recup1:
        sommeil = st.select_slider("Qualité du sommeil (h)", options=[4, 5, 6, 7, 8, 9, 10], value=7)
    with col_recup2:
        fatigue = st.select_slider("État nerveux / Fatigue", options=["Épuisé", "Fatigué", "Normal", "En forme", "Explosif"], value="Normal")

    st.markdown("---")

    # --- CHAT INTERACTIF ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Salut Athlète. Je suis ton coach. Je suis prêt à analyser ton frigo ou à t'expliquer un mouvement en vidéo. Que fait-on ?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- ENTRÉE UTILISATEUR (TEXTE + PHOTO DU FRIGO) ---
    with st.expander("📸 Envoyer une photo au coach (Frigo, Assiette, Exercice)"):
        photo_coach = st.file_uploader("Le coach analysera tes macros ou ta forme", type=['jpg', 'jpeg', 'png'], key="coach_photo")

    if prompt := st.chat_input("Pose ta question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # LOGIQUE DU COACH
            if "shrugs" in prompt.lower() or "exercice" in prompt.lower():
                reponse = "Voici une démonstration visuelle pour les **Shrugs Barre**. Concentre-toi sur la montée verticale sans rouler les épaules."
                st.markdown(reponse)
                # ICI ON SIMULE L'EXEMPLE VISUEL (GIF/Vidéo)
                st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Y2ZzR3ZzR3ZzR3ZzR3ZzR3ZzR3ZzR3ZzR3ZzR3ZzR3ZzR3JmcmVzaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKMGpxP5O5Q8L9S/giphy.gif", caption="Démonstration Shrugs")
            
            elif photo_coach:
                reponse = f"Analyse de ton frigo terminée. Vu ton objectif de **{objectif}**, je vois des œufs et des légumes. Prépare une omelette avec 3 œufs et 150g de riz pour tes macros."
                st.markdown(reponse)
            
            else:
                reponse = f"Analyse récupération : Avec {sommeil}h de sommeil et une fatigue {fatigue}, je te conseille de réduire le volume sur ta séance de **{muscle_select}** aujourd'hui pour protéger ton système nerveux."
                st.markdown(reponse)
                
            st.session_state.messages.append({"role": "assistant", "content": reponse})
