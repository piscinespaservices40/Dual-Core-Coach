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
    st.markdown("---")
    st.subheader("📝 Noter ma séance")
    
    # Formulaire pour le poids de corps
    nouveau_poids = st.number_input("Poids du jour (kg)", value=float(poids), step=0.1)
    
    # Formulaire pour la muscu (ex: Développé Couché)
    nouvelle_charge = st.number_input("Charge DC (kg)", value=65.0, step=2.5)
    
    if st.button("Enregistrer les données"):
        # On met à jour la mémoire (le dernier jour de la semaine)
        st.session_state.historique_poids[-1] = nouveau_poids
        st.session_state.charge_max[-1] = nouvelle_charge
        st.success("Données enregistrées !")
        st.rerun()
# Données pour les graphiques
# --- MÉMOIRE DE L'APP (Session State) ---
if 'historique_poids' not in st.session_state:
    st.session_state.historique_poids = [75.0, 74.8, 75.2, 74.9, 74.5, 74.2, 75.0]

if 'charge_max' not in st.session_state:
    # On prépare déjà ton suivi d'exercices (ex: Développé Couché)
    st.session_state.charge_max = [60, 60, 62.5, 62.5, 65, 65, 67.5]

jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

# On crée les tableaux à partir de cette mémoire
data_poids = pd.DataFrame({"Jour": jours, "Poids": st.session_state.historique_poids})
data_entrainement = pd.DataFrame({"Jour": jours, "Charge (kg)": st.session_state.charge_max})

# On garde tes données de nutrition ici aussi
data_nutrition = pd.DataFrame({
    "Jour": jours,
    "Proteines": [150, 165, 140, 170, 155, 130, 160],
    "Lipides": [70, 80, 75, 65, 85, 90, 70],
    "Glucides": [300, 350, 320, 280, 340, 400, 310]
})

# --- TAB 1 : DASHBOARD ---
with tab1:
    st.title("Dual-Core Coach 🚀")
    c1, c2, c3 = st.columns(3)
    
    # Calcul de l'IMC sécurisé
    imc = round(poids / ((taille/100)**2), 1) if taille > 0 else 0
    
    with c1:
        st.markdown(f'<div class="stat-card"><h3>IMC</h3><h2>{imc}</h2></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><h3>CALORIES</h3><h2>2850</h2></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><h3>OBJECTIF</h3><h2>{objectif}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📉 Évolution du Poids (kg)")
    fig_poids = px.line(data_poids, x="Jour", y="Poids", markers=True, color_discrete_sequence=['#00ffcc'])
    fig_poids.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), hovermode="x unified")
    st.plotly_chart(fig_poids, use_container_width=True)

# --- TAB 2 : ENTRAÎNEMENT ---
with tab2:
    st.title("🏋️ Ma Séance")
    
    # Simulation de données d'intensité
    data_train = pd.DataFrame({"Jour": jours, "Intensité (%)": [80, 40, 90, 70, 85, 20, 0]})
    
    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        st.write(f"Focus : **{objectif}**")
        st.info("Routine : 4 séries de 10 répétitions")
    
    with col_t2:
        st.subheader("📈 Progression : Développé Couché")
        
        # On utilise data_entrainement qu'on a créé avec la mémoire
        fig_charge = px.line(data_entrainement, x="Jour", y="Charge (kg)", 
                             markers=True,
                             color_discrete_sequence=['#ff6600']) # Ton orange néon
        
        fig_charge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="white"),
            hovermode="x unified"
        )
        
        # On ajuste l'axe pour que ce soit lisible
        fig_charge.update_yaxes(range=[min(st.session_state.charge_max)-5, max(st.session_state.charge_max)+5])
        
        st.plotly_chart(fig_charge, use_container_width=True)

# --- TAB 3 : NUTRITION ---
with tab3:
    st.title("🍎 Nutrition Sportive")
    
    # Tes textes actuels
    st.markdown("### 🍳 Journée Type")
    with st.expander("Consulter mes repas"):
        st.write("- **Matin** : Avoine, 3 œufs, 1 banane")
        st.write("- **Midi** : Poulet, Riz, Brocolis")
        st.write("- **Soir** : Poisson, Patate douce")

    st.markdown("---")
    st.subheader("🥗 Suivi des Macros (g)")
    fig_nutri = px.line(data_nutrition, x="Jour", y=["Proteines", "Lipides", "Glucides"],
                        color_discrete_map={"Proteines": "#00ff00", "Lipides": "#ffff00", "Glucides": "#0000ff"})
    fig_nutri.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), legend_font_color="white", hovermode="x unified")
    st.plotly_chart(fig_nutri, use_container_width=True)
    
    st.markdown("### 📸 Scan ton Frigo")
    st.file_uploader("Prends une photo de tes ingrédients", type=['jpg', 'png', 'jpeg'])
