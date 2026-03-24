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
    
    /* --- COULEUR BLEU NÉON POUR TOUS LES LABELS --- */
    label, .stMarkdown p, .stSelectbox label, .stSlider label, .stNumberInput label, [data-testid="stWidgetLabel"] {
        color: #00ffcc !important;
        font-weight: bold !important;
        text-shadow: 0 0 5px rgba(0, 255, 204, 0.5);
    }

    /* Couleur pour les boutons radio (Jour, Semaine, Mois) */
    div[data-testid="stRadio"] label {
        color: #00ffcc !important;
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

# --- BASE DE DONNÉES EXERCICES ---
exercices_db = {
    "Pectoraux": ["Développé Couché", "Développé Incliné", "Écartés Poulie", "Dips", "Pompes Lestées", "Chest Press", "Développé Haltères", "Pull-over", "Écartés Haltères", "Machine convergente"],
    "Dos": ["Tractions", "Tirage Poitrine", "Rowing Barre", "Tirage Horizontal", "Lumbaires", "Rowing Haltère", "Tirage Vertical Large", "Facepull", "Shrugs Barre", "Pull-down bras tendus"],
    "Épaules": ["Développé Militaire", "Élévations Latérales", "Oiseau Poulie", "Développé Arnold", "Développé Haltères Assis", "Tirage Menton", "Élévations Frontales", "Reverse Pec Deck", "Push Press", "L-Fly"],
    "Jambes (Quad/Ischios)": ["Squat", "Presse à Cuisses", "Leg Extension", "Leg Curl", "Fentes", "Hack Squat", "SDT Jambes Tendues", "Sissy Squat", "Step-up", "Bulgarian Split Squat"],
    "Bras (Biceps/Triceps)": ["Curl Barre", "Curl Marteau", "Curl Incliné", "Extension Triceps Poulie", "Barre au Front", "Curl Larry Scott", "Dips Triceps", "Kickback", "Spider Curl", "Triceps Pushdown Corde"],
    "Mollets/Fessiers": ["Mollets Debout", "Mollets Assis", "Hip Thrust", "Abducteurs", "Kickback Fessier", "Presse Mollets", "Glute Bridge", "Fentes Croisées", "Mollets à la Presse", "Donkey Calf Raise"],
    "Abdos": ["Crunch", "Gainage", "Levé de Jambes", "Russian Twist", "Roulette Abdos", "Mountain Climbers", "Sit-ups", "Planche Latérale", "V-ups", "Leg Raise suspendu"],
    "Cardio": ["Course à pied", "Vélo", "Rameur", "Corde à sauter", "Elliptique", "Natation", "HIIT", "Burpees", "Marche inclinée", "Assault Bike"]
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
        # --- SÉLECTEUR DE PÉRIODE ---
        periode = st.radio("Vue de la progression :", ["Jour", "Semaine", "Mois"], horizontal=True)
        
        st.subheader(f"📈 Progression : {exercice_select}")
        
        # Récupération des données
        base_data = st.session_state.historique_charges[exercice_select]
        
        if periode == "Jour":
            # On affiche les 7 derniers jours
            y_data = base_data[-7:]
            x_label = jours
        elif periode == "Semaine":
            # On simule une vue par semaine (moyenne des points)
            y_data = base_data[-28:] # On prend plus de données
            x_label = [f"Sem {i+1}" for i in range(len(y_data)//4 + 1)][-7:]
            y_data = y_data[::4] # On prend un point toutes les 4 séances pour l'exemple
        else: # Mois
            # On simule une vue annuelle/mensuelle
            y_data = [base_data[0], base_data[-1]] # Début vs Fin
            x_label = ["Mois Précédent", "Mois Actuel"]

        fig_ex = px.area(x=x_label, y=y_data, markers=True, color_discrete_sequence=['#ff6600'])
        
        fig_ex.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="white"),
            xaxis_title=f"Période ({periode})",
            yaxis_title="Charge (kg)"
        )
        
        st.plotly_chart(fig_ex, use_container_width=True)
        st.write(f"**Focus actuel :** {series} séries de {reps} répétitions sur {exercice_select}")

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
    st.title("🤖 Coach AI Personnel")
    st.write("Pose tes questions à ton coach pour optimiser tes cycles de progression.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ex: Comment améliorer mon développé couché ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            st.markdown("Je suis prêt à analyser tes performances pour ajuster tes prochaines séances.")
