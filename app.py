import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Dual-Core Coach", layout="wide", initial_sidebar_state="expanded")

# --- STYLE VISUEL (NOUVEAU FOND DYNAMIQUE) ---
# J'ai ajouté un dégradé linéaire discret pour le fond
st.markdown("""
    <style>
    /* RELOOKING DYNAMIQUE : SPORTSWEAR FUSION
       Objectif : Ambiance sombre, technique, énergisante, unisexe.
    */
    
    /* --- FOND DE PAGE AVEC DÉGRADÉ ÉNERGISANT --- */
    .stApp { 
        background-image: linear-gradient(135deg, #10101d 0%, #1e1e30 40%, #10101d 100%) !important;
        background-attachment: fixed !important;
        color: white !important;
    }
    
    /* --- STYLE DES CADRANS DE STATISTIQUES (Technique & Lumineux) --- */
    .stat-card { 
        padding: 25px; 
        border-radius: 20px; 
        background-color: rgba(25, 25, 35, 0.6); /* Semi-transparent, effet verre dépoli */
        border: 1px solid rgba(0, 255, 204, 0.3); /* Bordure discrète bleu-vert */
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); /* Ombre portée douce */
        backdrop-filter: blur(8px); /* Effet de flou sur le fond */
        -webkit-backdrop-filter: blur(8px);
        margin-bottom: 25px; 
        color: white !important; 
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease; /* Animation au survol */
    }
    .stat-card:hover {
        transform: translateY(-5px); /* Soulèvement au survol */
        box-shadow: 0 12px 40px 0 rgba(0, 255, 204, 0.3); /* Lueur plus forte au survol */
    }
    .stat-card h3 { color: #808495 !important; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .stat-card h2 { color: white !important; font-size: 2.5rem; font-weight: 900; margin: 0; text-shadow: 0 0 10px rgba(255, 255, 255, 0.5); }
    
    /* --- STYLE DES CADRANS D'EXERCICES (Sportswear) --- */
    .exercice-box {
        background-color: rgba(30, 30, 40, 0.8);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #ff6600; /* Touche d'orange énergisant */
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        margin-bottom: 15px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
    }
    
    /* --- STYLE DES TITRES ET SOUS-TITRES --- */
    h1, h2, h3, h4, .stSubheader { 
        color: #ffffff !important; 
        font-weight: 800 !important; 
        text-transform: uppercase; 
        letter-spacing: 1px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Bouton principal luminescent (Sportswear) */
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc 0%, #00ccaa 100%) !important;
        color: #10101d !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        border-radius: 30px !important; /* Bords très arrondis */
        border: none !important;
        padding: 12px 25px !important;
        box-shadow: 0 5px 15px rgba(0, 255, 204, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        box-shadow: 0 8px 25px rgba(0, 255, 204, 0.7) !important;
        transform: scale(1.05); /* Léger grossissement */
    }
    
    /* Couleur des éléments de saisie, sliders */
    .stNumberInput input, .stSlider div { color: white !important; background-color: rgba(255, 255, 255, 0.1) !important; border-radius: 10px; }
    .stSlider [data-baseweb="slider"] div { background-color: #00ffcc !important; } /* Couleur de la barre du slider */
    .stSlider [data-baseweb="slider"] div[role="slider"] { background-color: #ff6600 !important; border: 2px solid white; } /* Couleur du bouton du slider */
    
    /* Onglets stylisés */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #808495 !important; font-weight: 700; text-transform: uppercase; padding: 10px 20px; }
    .stTabs [data-baseweb="tab--active"] { color: #00ffcc !important; border-bottom-color: #00ffcc !important; }
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
        
        # --- LOGIQUE IA (À CONFIGURER DANS STREAMLIT SECRETS) ---
        if question:
            # On vérifie si la clé API est configurée
            try:
                # Si tu utilises OpenAI
                # import openai
                # openai.api_key = st.secrets["OPENAI_API_KEY"]
                # response = openai.ChatCompletion.create(...)
                # st.write(f"**Réponse du Coach :** {response.choices[0].message.content}")
                
                # En attendant, on laisse le placeholder pour l'exemple
                st.info("Le Coach IA se connecte au serveur... (Configurez votre clé API dans Streamlit Secrets)")
                
            except Exception as e:
                st.error("Le Coach n'est pas encore connecté. Configurez votre clé API dans Streamlit Secrets.")

# --- NUTRITION & MACROS ---
with tab3:
    st.title("🍎 Nutrition & Performance")
    
    # Rappel de l'objectif et infos générales
    st.markdown(f'<div class="exercice-box"><b>Objectif actuel :</b> {mode_objectif}</div>', unsafe_allow_html=True)
    st.write("Votre plan nutritionnel est la clé de votre progression. Voici vos objectifs de macros et des exemples pour vous guider.")
    
    # Cadrans de macros stylisés
    c1, c2, c3 = st.columns(3)
    c1.metric("Glucides", "350g")
    c2.metric("Protéines", "165g")
    c3.metric("Lipides", "75g")
    
    st.divider()
    
    # --- EXEMPLES DE REPAS (ADAPTÉS À L'OBJECTIF) ---
    st.subheader("🍽️ Idées de Repas pour votre Journée")
    
    # Logique pour adapter les repas selon l'objectif
    if mode_objectif == "Prise de masse":
        pdej = "80g d'avoine, 3 œufs entiers, 1 banane, 1 poignée d'amandes."
        dej = "150g Poulet blanc, 200g Riz pesé cuit, Brocolis à volonté, 1 c.à.s Huile d'olive."
        collation = "1 Shaker de Whey, 2 galettes de riz, 1 pomme."
        diner = "150g Poisson blanc (type cabillaud), 200g Patate douce, Haricots verts, 1 c.à.s Huile de colza."
    elif mode_objectif == "Maintien":
        pdej = "60g d'avoine, 2 œufs entiers + 2 blancs, 1 pomme, quelques noix."
        dej = "120g Poulet blanc, 150g Quinoa pesé cuit, Salade mixte, 1 c.à.s Huile d'olive."
        collation = "1 Shaker de Whey ou 1 yaourt grec, 1 poignée de baies."
        diner = "120g Poisson blanc, 150g Pommes de terre vapeur, Épinards frais, 1 c.à.s Huile de colza."
    else: # Sèche
        pdej = "40g d'avoine, 1 œuf entier + 3 blancs, 1 pamplemousse."
        dej = "100g Poulet blanc, 100g Riz complet pesé cuit, Salade verte à volonté, 1/2 c.à.s Huile d'olive."
        collation = "1 yaourt nature 0% ou 1 Shaker de caséine, 1 poignée de framboises."
        diner = "100g Poisson blanc, 100g Patate douce, Asperges grillées, 1/2 c.à.s Huile de colza."

    # Affichage des repas dans des boîtes stylisées
    with st.expander("🌅 Petit-Déjeuner", expanded=True):
        st.write(pdej)
    with st.expander("☀️ Déjeuner"):
        st.write(dej)
    with st.expander("🕒 Collation"):
        st.write(collation)
    with st.expander("🌙 Dîner"):
        st.write(diner)
        
    st.divider()
    
    # --- ASSISTANT NUTRITION (DÉBUT) ---
    st.subheader("🍴 Assistant Nutrition")
    repas_q = st.text_input("Besoin d'un menu personnalisé pour ce soir ?")
    if repas_q: st.warning("Recherche de recettes adaptées...")
st.divider()
    st.subheader("📸 Le Frigo Intelligent (Bientôt disponible)")
    st.write("Imaginez : vous prenez une photo de votre frigo, et l'IA vous propose instantanément des recettes adaptées à votre objectif et à ce que vous avez sous la main. C'est notre prochaine grande fonctionnalité en développement !")
    
    # Zone d'upload d'image (pour l'instant, c'est juste visuel)
    uploade_file = st.file_uploader("Faites un test : chargez une photo de votre frigo !", type=["jpg", "jpeg", "png"])
    if uploade_file:
        st.image(uploade_file, caption="Photo de votre frigo analysée...", use_column_width=True)
        st.info("Fonctionnalité d'analyse en cours de développement. Bientôt, l'IA vous proposera des repas basés sur cette image !")
