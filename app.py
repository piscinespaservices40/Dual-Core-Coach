import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Dual-Core Coach AI", layout="wide", initial_sidebar_state="expanded")

# --- STYLE VISUEL (CSS) ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at top, #1e1e2f 0%, #0d0d12 100%) !important; }
    
    /* Texte global */
    html, body, [class*="st-"] { color: #ffffff !important; }

    /* Titres Bleu Néon */
    h1, h2, h3, .stSubheader { color: #00ffcc !important; text-shadow: 0 0 10px rgba(0, 255, 204, 0.3); }

    /* Labels des formulaires */
    label, [data-testid="stWidgetLabel"] p { color: #00ffcc !important; font-weight: bold !important; }

    /* --- FIX DU BOUTON VALIDER --- */
    div.stButton > button {
        background-color: #ff6600 !important;
        color: white !important; /* Force le texte en blanc */
        border: none !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
    }
    div.stButton > button:hover {
        background-color: #ff8533 !important;
        color: white !important;
    }

    /* Fix pour les tableaux */
    .stTable, table { color: white !important; }
    thead tr th { color: #00ffcc !important; }
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
if "historique_repas" not in st.session_state:
    st.session_state.historique_repas = [] # Liste de dictionnaires pour stocker chaque jour
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
    st.title("🍎 Nutrition & Macros Intelligentes")
    
    # --- LOGIQUE DE CALCUL (Maintien des calculs précédents) ---
    maintenance = (10 * poids) + (6.25 * taille) - (5 * 25) + 5
    if objectif == "Prise de masse":
        cible_calorique, ratio_p, ratio_l, ratio_g = maintenance + 400, 2.0, 0.9, 4.5 
    elif objectif == "Sèche":
        cible_calorique, ratio_p, ratio_l, ratio_g = maintenance - 500, 2.4, 0.8, 2.0 
    else: 
        cible_calorique, ratio_p, ratio_l, ratio_g = maintenance, 1.8, 1.0, 3.5

    prot, lip = round(poids * ratio_p), round(poids * ratio_l)
    glu = max(50, round((cible_calorique - (prot * 4 + lip * 9)) / 4))

    # --- 1. DASHBOARD MACROS ---
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="stat-card"><h3>Calories</h3><h2>{int(cible_calorique)}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><h3>Prot (g)</h3><h2>{prot}</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card"><h3>Lip (g)</h3><h2>{lip}</h2></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="stat-card"><h3>Glu (g)</h3><h2>{glu}</h2></div>', unsafe_allow_html=True)

    # --- 2. LE MENU & VALIDATION ---
    st.subheader("🍽️ Menu du jour & Enregistrement")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.write(f"**Matin:** Omelette & {round(glu*0.2)}g Avoine")
        st.write(f"**Midi:** {round(prot*0.35)}g Poulet & {round(glu*0.35)}g Riz")
    with col_m2:
        st.write(f"**Collation:** Whey & {round(lip*0.3)}g Amandes")
        st.write(f"**Soir:** {round(prot*0.3)}g Dinde & {round(glu*0.25)}g Patate douce")

    if st.button("✅ VALIDER ET ENREGISTRER MA JOURNÉE"):
        nouvel_entree = {
            "Date": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "Calories": int(cible_calorique),
            "P": prot, "L": lip, "G": glu,
            "Objectif": objectif
        }
        st.session_state.historique_repas.append(nouvel_entree)
        st.success("Journée enregistrée dans ton historique !")

    st.markdown("---")
    
    # --- 3. CALENDRIER & HISTORIQUE ---
    st.subheader("📅 Historique de Nutrition")
    
    if st.session_state.historique_repas:
        df_hist = pd.DataFrame(st.session_state.historique_repas)
        
        # Affichage sous forme de tableau propre
        st.table(df_hist.tail(7)) # Affiche les 7 derniers jours
        
        # Petit graphique de suivi calorique sur le temps
        fig_hist = px.line(df_hist, x="Date", y="Calories", title="Évolution de ton apport calorique", markers=True)
        fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("Aucun repas enregistré pour le moment. Clique sur 'Valider' pour commencer ton historique.")

    # --- 4. RÉPARTITION VISUELLE (Légende corrigée) ---
    with st.expander("📊 Voir la répartition théorique des macros"):
        df_macro = pd.DataFrame({"Macro": ["Protéines", "Lipides", "Glucides"], "Grammes": [prot, lip, glu]})
        fig_pie = px.pie(df_macro, values="Grammes", names="Macro", hole=0.6, 
                         color_discrete_map={"Protéines":"#00ffcc", "Lipides":"#ffff00", "Glucides":"#ff6600"})
        
        # C'est ici qu'on rend la légende blanche
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            legend=dict(font=dict(color="white")), # Légende en blanc
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 4 : AGENT AI ---
with tab4:
    st.title("🤖 Dual-Core Coach AI : Expert Omniscient")
    st.markdown('<p style="color:#00ffcc; font-weight:bold;">Analyse Multimodale : Sommeil, Nutrition & Récupération Nerveuse.</p>', unsafe_allow_html=True)
    
    # --- PILIERS DE RÉCUPÉRATION ---
    col_recup1, col_recup2, col_recup3 = st.columns(3)
    with col_recup1:
        sommeil = st.select_slider("🌙 Sommeil (Qualité/Durée)", options=[4, 5, 6, 7, 8, 9, 10], value=7)
    with col_recup2:
        mental = st.select_slider("🧠 État Psychologique", options=["Stressé", "Anxieux", "Neutre", "Motivé", "Focus"], value="Neutre")
    with col_recup3:
        nerveux = st.select_slider("⚡ Fatigue Nerveuse", options=["Burnout", "Fatigué", "Ok", "Frais", "Explosif"], value="Ok")

    st.markdown("---")

    # --- HISTORIQUE DE DISCUSSION ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Salut Athlète. Ton mode **{objectif}** est actif. Comment puis-je t'aider ?"}]

    # On affiche les messages existants
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- ENTRÉE TEXTE ---
    if prompt := st.chat_input("Pose ta question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            p = prompt.lower()
            
            # LOGIQUE DE DÉTECTION AMÉLIORÉE
            if "shrugs" in p:
                reponse = "Pour les **Shrugs**, concentre-toi sur tes trapèzes supérieurs. Monte les épaules vers les oreilles, marque une pause de 1s en haut, puis contrôle la descente."
                st.image("https://media.giphy.com/media/3o7TKMGpxP5O5Q8L9S/giphy.gif")
            
            elif "fatigué" in p or "fatigue" in p or "séance" in p:
                if nerveux in ["Burnout", "Fatigué"] or sommeil < 6:
                    reponse = f"⚠️ Vu ton sommeil de {sommeil}h et ta fatigue {nerveux}, je te déconseille une séance lourde. Pour ton objectif de {objectif}, fais une séance de rappel léger ou du cardio zone 2."
                else:
                    reponse = f"Ta fatigue nerveuse est '{nerveux}'. Tu peux tenter ta séance de **{muscle_select}**, mais surveille tes temps de repos !"
            
            elif "pectoraux" in p or "pecs" in p:
                reponse = "Pour les Pectoraux, privilégie le Développé Couché en début de séance pour la force, puis des écartés poulie pour l'isolation et le stretch."
            
            elif "manger" in p or "repas" in p or "faim" in p:
                reponse = f"En phase de **{objectif}**, ton dernier repas doit comporter au moins 40g de protéines. Utilise le module photo juste en dessous pour que j'analyse ton frigo !"
            
            else:
                reponse = f"Analyse Coach : Pour optimiser tes {poids}kg, assure-toi d'être à l'échec technique sur tes dernières séries de {exercice_select}. As-tu une question sur ta récupération ?"
            
            st.markdown(reponse)
            st.session_state.messages.append({"role": "assistant", "content": reponse})

    st.markdown("---")
    # --- ANALYSE PHOTO (PLACÉE EN BAS) ---
    with st.expander("📸 ANALYSER MON FRIGO OU MON REPAS"):
        upload_frigo = st.file_uploader("Prends une photo de l'intérieur de ton frigo ou de ton assiette", type=['jpg', 'png'])
        if upload_frigo:
            st.success("Photo bien reçue ! (Le moteur d'analyse visuelle sera activé lors de la connexion API)")
            st.info(f"Conseil rapide pour **{objectif}** : Privilégie les sources de protéines brutes visibles sur ta photo.")
