import io
import streamlit as st
import jinja2
import os
import subprocess
import base64
from PIL import Image

# ==========================================
# 1. CONFIGURATION DE LA PAGE & CSS "DARK GOLD"
# ==========================================
st.set_page_config(page_title="Omni-Bot CV Architect", page_icon="🤖", layout="wide")

# Injection du CSS de folie (Noir & Or, Majuscules)
st.markdown("""
<style>
    /* FOND NOIR ABSOLU POUR TOUTE L'APP */
    .stApp, .stApp > header {
        background-color: #050505 !important;
    }
    
    /* CACHER LES MENUS POUR FAIRE LOGICIEL AUTONOME */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* TOUT LE TEXTE EN MAJUSCULES (Visuel uniquement, n'affecte pas le PDF) */
    * {
        text-transform: uppercase !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        letter-spacing: 0.5px;
    }
    
    /* COULEUR OR POUR TOUS LES TEXTES */
    p, span, label, h1, h2, h3, h4, h5, h6, li, div {
        color: #D4AF37 !important; /* Code couleur du Jaune Or Métallique */
    }

    /* MENUS DÉROULANTS (EXPANDERS) */
    .streamlit-expanderHeader {
        background-color: #111111 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 8px;
        padding: 10px 15px !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: #222222 !important;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }
    div[data-testid="stExpanderDetails"] {
        background-color: #0A0A0A !important;
        border-left: 1px solid #D4AF37 !important;
        border-right: 1px solid #D4AF37 !important;
        border-bottom: 1px solid #D4AF37 !important;
        border-radius: 0 0 8px 8px;
    }

    /* CHAMPS DE SAISIE */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #111111 !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        box-shadow: 0 0 8px #D4AF37 !important;
        border-color: #FFD700 !important;
    }

    /* ZONE D'UPLOAD DE FICHIER */
    [data-testid="stFileUploader"] {
        background-color: #0A0A0A !important;
        border: 1px dashed #D4AF37 !important;
        border-radius: 8px;
    }

    /* BOUTONS STANDARDS */
    .stButton>button {
        background-color: #050505 !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 6px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
    }

    /* BOUTON SPÉCIAL : TÉLÉCHARGEMENT DU PDF */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #D4AF37, #AA8000) !important;
        color: #000000 !important;
        border: none !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        border-radius: 8px;
    }
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #FFD700, #D4AF37) !important;
        transform: scale(1.02);
        box-shadow: 0 6px 15px rgba(212, 175, 55, 0.6);
    }

    /* CADRE DU LECTEUR PDF */
    iframe {
        border: 2px solid #D4AF37;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.15);
    }
    
    /* MESSAGES D'ALERTE / INFO */
    .stAlert {
        background-color: #111111 !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
    }
</style>
""", unsafe_allow_html=True)

import json

# Fichier où seront stockées tes données
DB_FILE = "data_omni_bot.json"

def sauvegarder_donnees():
    # On prépare les données à sauver (exclure les objets complexes de session_state)
    data = {
        "reseaux": st.session_state.reseaux,
        "competences": st.session_state.competences,
        "experiences": st.session_state.experiences,
        "formations": st.session_state.formations,
        "certifications": st.session_state.certifications,
        "realisations": st.session_state.realisations
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def charger_donnees():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


if st.button("💾 SAUVEGARDER DÉFINITIVEMENT TOUTE LA SAISIE"):
    sauvegarder_donnees()
    st.success("Toute votre saisie est maintenant sécurisée sur le disque !")
# ==========================================
# 2. INITIALISATION DE LA MÉMOIRE (Session State)
# ==========================================
# Charger les données existantes au démarrage
donnees_sauvegardees = charger_donnees()

# Initialisation avec priorité à la sauvegarde
if "reseaux" not in st.session_state:
    st.session_state.reseaux = donnees_sauvegardees["reseaux"] if donnees_sauvegardees else [{"nom": "LinkedIn", "url": ""}]
if "competences" not in st.session_state:
    st.session_state.competences = donnees_sauvegardees["competences"] if donnees_sauvegardees else [{"categorie": "", "details": ""}]
if "experiences" not in st.session_state:
    st.session_state.experiences = donnees_sauvegardees["experiences"] if donnees_sauvegardees else [{"poste": "", "entreprise": "", "date": "", "sous_titre": "", "puces": [""]}]
if "formations" not in st.session_state:
    st.session_state.formations = donnees_sauvegardees["formations"] if donnees_sauvegardees else [{"titre": "", "ecole": "", "date": "", "puces": [""]}]
if "certifications" not in st.session_state:
    st.session_state.certifications = donnees_sauvegardees["certifications"] if donnees_sauvegardees else []
if "realisations" not in st.session_state:
    st.session_state.realisations = donnees_sauvegardees["realisations"] if donnees_sauvegardees else []

def ajouter_item(liste, template): st.session_state[liste].append(template)
def supprimer_item(liste, index): st.session_state[liste].pop(index)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return f"{int(hex_color[0:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:6], 16)}"

# ==========================================
# 3. COMPILATION LATEX -> PDF
# ==========================================
def compiler_pdf(donnees):
    dossier_actuel = os.getcwd()
    template_loader = jinja2.FileSystemLoader(searchpath=dossier_actuel)
    template_env = jinja2.Environment(loader=template_loader)
    
    try:
        template = template_env.get_template("cv_template.tex")
        cv_tex = template.render(donnees)
        
        tex_path = os.path.join(dossier_actuel, "cv_genere.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(cv_tex)
            
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "cv_genere.tex"], cwd=dossier_actuel, capture_output=True, text=True)
        return os.path.join(dossier_actuel, "cv_genere.pdf")
    except Exception as e:
        st.error(f"Erreur système : {e}")
        return None

def afficher_pdf(chemin_pdf):
    if os.path.exists(chemin_pdf):
        with open(chemin_pdf, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

# ==========================================
# 4. INTERFACE UTILISATEUR (STREAMLIT)
# ==========================================
col_logo, col_titre = st.columns([1, 11])
with col_logo:
    try:
        st.image("logon.png", width=80)
    except:
        st.write("🤖")
with col_titre:
    st.title("OMNI-BOT : ARCHITECTE DE CV")
    st.markdown("✨ *REMPLISSEZ LE FORMULAIRE, VOTRE DESIGN S'AJUSTE EN TEMPS RÉEL.*")

col_form, col_space, col_preview = st.columns([1.2, 0.05, 1])

with col_form:
    
    with st.expander("🎨 Personnalisation Graphique", expanded=True):
        c1, c2 = st.columns(2)
        # Par défaut, le CV généré sera Noir et Or pour matcher avec l'application !
        color_primary_hex = c1.color_picker("Couleur Principale (Titres)", "#000000")
        color_accent_hex = c2.color_picker("Couleur Secondaire (Puces, Icônes)", "#D4AF37")
        
        photo_upload = st.file_uploader("🖼️ PHOTO DE PROFIL", type=["png", "jpg", "jpeg"])

        if photo_upload:
            # On lit l'image sans l'écrire sur le disque
            img = Image.open(photo_upload).convert("RGB")
            # On la prépare pour LaTeX en tant que flux de données
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            # On peut toujours sauvegarder localement si on est en DEV
            with open("cv.png", "wb") as f:
                f.write(img_byte_arr.getvalue())
            st.success("PHOTO CHARGÉE AVEC SUCCÈS")

    with st.expander("👤 Informations Personnelles & Contacts"):
        c3, c4 = st.columns(2)
        prenom = c3.text_input("Prénom", "Jean")
        nom = c4.text_input("Nom", "Dupont")
        titre_job = st.text_input("Poste visé (Titre du CV)", "DATA ANALYST")
        
        c5, c6 = st.columns(2)
        email = c5.text_input("Email", "jean@email.com")
        tel = c6.text_input("Téléphone", "+33 6 00 00 00 00")
        
        c7, c8 = st.columns(2)
        ville = c7.text_input("Ville & Pays", "Paris")
        age = c8.text_input("Âge", "25")
        
        profil_text = st.text_area("Résumé du Profil (Phrase d'accroche)", "Expert en data...", height=100)

        st.markdown("---")
        st.markdown("**🔗 Réseaux Sociaux & Liens**")
        for i, res in enumerate(st.session_state.reseaux):
            cr1, cr2, cr3 = st.columns([3, 5, 1.5])
            res["nom"] = cr1.text_input("Nom", res["nom"], key=f"res_nom_{i}", label_visibility="collapsed", placeholder="Ex: LinkedIn")
            res["url"] = cr2.text_input("URL", res["url"], key=f"res_url_{i}", label_visibility="collapsed", placeholder="https://...")
            if cr3.button("🗑️", key=f"del_res_{i}"):
                supprimer_item("reseaux", i)
                st.rerun()
        st.button("➕ Ajouter un lien", on_click=lambda: ajouter_item("reseaux", {"nom": "", "url": ""}), key="add_res", type="primary")

    with st.expander("⚡ Compétences Techniques"):
        st.info("💡 Séparez vos compétences par des virgules. (Utilisez '\\\&' pour le symbole '&')")
        for i, comp in enumerate(st.session_state.competences):
            c_cat, c_det, c_del = st.columns([3, 5, 1])
            comp["categorie"] = c_cat.text_input(f"Catégorie", comp["categorie"], key=f"cat_{i}", label_visibility="collapsed")
            comp["details"] = c_det.text_input(f"Détails", comp["details"], key=f"det_{i}", label_visibility="collapsed")
            if c_del.button("🗑️", key=f"del_comp_{i}"):
                supprimer_item("competences", i)
                st.rerun()
        st.button("➕ Ajouter une compétence", on_click=lambda: ajouter_item("competences", {"categorie": "", "details": ""}), key="add_comp", type="primary")

    with st.expander("💼 Expériences Professionnelles"):
        for i, exp in enumerate(st.session_state.experiences):
            st.markdown(f"#### Expérience {i+1}")
            ce1, ce2 = st.columns(2)
            exp["poste"] = ce1.text_input(f"Poste", exp["poste"], key=f"p_{i}")
            exp["entreprise"] = ce2.text_input(f"Entreprise", exp["entreprise"], key=f"e_{i}")
            
            ce3, ce4 = st.columns([1, 2])
            exp["date"] = ce3.text_input(f"Date", exp["date"], key=f"d_{i}", placeholder="2023 - 2024")
            exp["sous_titre"] = ce4.text_input(f"Contexte (Optionnel)", exp["sous_titre"], key=f"s_{i}")
            
            st.markdown("**Missions (Puces) :**")
            for j, puce in enumerate(exp["puces"]):
                cp1, cp2 = st.columns([9, 1])
                exp["puces"][j] = cp1.text_input(f"Puce {j+1}", puce, key=f"exp_{i}_puce_{j}", label_visibility="collapsed")
                if cp2.button("❌", key=f"del_puce_exp_{i}_{j}") and len(exp["puces"]) > 1:
                    exp["puces"].pop(j)
                    st.rerun()
            
            st.button("➕ Ajouter une puce", key=f"add_puce_exp_{i}", on_click=lambda idx=i: st.session_state.experiences[idx]["puces"].append(""))
            st.button(f"🗑️ Supprimer l'expérience {i+1}", key=f"del_exp_{i}", on_click=supprimer_item, args=("experiences", i))
            st.markdown("---")
        st.button("➕ Ajouter une expérience", on_click=lambda: ajouter_item("experiences", {"poste": "", "entreprise": "", "date": "", "sous_titre": "", "puces": [""]}), key="add_exp", type="primary")

    with st.expander("🎓 Formations & Diplômes"):
        for i, form in enumerate(st.session_state.formations):
            st.markdown(f"#### Formation {i+1}")
            cf1, cf2 = st.columns(2)
            form["titre"] = cf1.text_input(f"Diplôme", form["titre"], key=f"ft_{i}")
            form["ecole"] = cf2.text_input(f"École", form["ecole"], key=f"fe_{i}")
            form["date"] = st.text_input(f"Date", form["date"], key=f"fd_{i}")
            
            st.markdown("**Détails (Puces) :**")
            for j, puce in enumerate(form["puces"]):
                cp1, cp2 = st.columns([9, 1])
                form["puces"][j] = cp1.text_input(f"Puce {j+1}", puce, key=f"form_{i}_puce_{j}", label_visibility="collapsed")
                if cp2.button("❌", key=f"del_puce_form_{i}_{j}") and len(form["puces"]) > 1:
                    form["puces"].pop(j)
                    st.rerun()
            
            st.button("➕ Ajouter une puce", key=f"add_puce_form_{i}", on_click=lambda idx=i: st.session_state.formations[idx]["puces"].append(""))
            st.button(f"🗑️ Supprimer la formation {i+1}", key=f"del_form_{i}", on_click=supprimer_item, args=("formations", i))
            st.markdown("---")
        st.button("➕ Ajouter une formation", on_click=lambda: ajouter_item("formations", {"titre": "", "ecole": "", "date": "", "puces": [""]}), key="add_form", type="primary")

    with st.expander("🏆 Certifications (Optionnel)"):
        for i, cert in enumerate(st.session_state.certifications):
            cc1, cc2, cc3 = st.columns([3, 3, 2])
            cert["titre"] = cc1.text_input("Titre", cert["titre"], key=f"cert_t_{i}")
            cert["organisme"] = cc2.text_input("Organisme", cert["organisme"], key=f"cert_o_{i}")
            cert["date"] = cc3.text_input("Date", cert["date"], key=f"cert_d_{i}")
            st.button(f"🗑️ Supprimer", key=f"del_cert_{i}", on_click=supprimer_item, args=("certifications", i))
            st.markdown("---")
        st.button("➕ Ajouter une certification", on_click=lambda: ajouter_item("certifications", {"titre": "", "organisme": "", "date": ""}), key="add_cert", type="primary")

    with st.expander("🚀 Projets & Réalisations (Optionnel)"):
        for i, proj in enumerate(st.session_state.realisations):
            st.markdown(f"#### Projet {i+1}")
            cpj1, cpj2 = st.columns([3, 1])
            proj["titre"] = cpj1.text_input("Nom du projet", proj["titre"], key=f"proj_t_{i}")
            proj["date"] = cpj2.text_input("Date", proj["date"], key=f"proj_d_{i}")
            proj["contexte"] = st.text_input("Contexte / Technologies", proj["contexte"], key=f"proj_c_{i}")
            
            st.markdown("**Détails (Puces) :**")
            for j, puce in enumerate(proj["puces"]):
                cp1, cp2 = st.columns([9, 1])
                proj["puces"][j] = cp1.text_input(f"Puce {j+1}", puce, key=f"proj_{i}_puce_{j}", label_visibility="collapsed")
                if cp2.button("❌", key=f"del_puce_proj_{i}_{j}") and len(proj["puces"]) > 1:
                    proj["puces"].pop(j)
                    st.rerun()
            
            st.button("➕ Ajouter une puce", key=f"add_puce_proj_{i}", on_click=lambda idx=i: st.session_state.realisations[idx]["puces"].append(""))
            st.button(f"🗑️ Supprimer le projet {i+1}", key=f"del_proj_{i}", on_click=supprimer_item, args=("realisations", i))
            st.markdown("---")
        st.button("➕ Ajouter un projet", on_click=lambda: ajouter_item("realisations", {"titre": "", "date": "", "contexte": "", "puces": [""]}), key="add_proj", type="primary")

    with st.expander("🌍 Atouts (Langues & Soft Skills)"):
        langues = st.text_input("Langues", "Anglais : Courant")
        soft_skills = st.text_input("Soft Skills", "Autonomie, Rigueur")

# ==========================================
# 5. GÉNÉRATION ET APERÇU EN DIRECT
# ==========================================
donnees_cv = {
    "titre_job": titre_job, "prenom": prenom, "nom": nom,
    "telephone": tel, "email": email, "ville": ville, "age": age,
    "profil_text": profil_text, "langues": langues, "soft_skills": soft_skills,
    "color_primary": hex_to_rgb(color_primary_hex),
    "color_accent": hex_to_rgb(color_accent_hex),
    "reseaux": st.session_state.reseaux,
    "competences": st.session_state.competences,
    "experiences": st.session_state.experiences,
    "formations": st.session_state.formations,
    "certifications": st.session_state.certifications,
    "realisations": st.session_state.realisations
}

with col_preview:
    st.markdown("<h3 style='text-align: center; color: #D4AF37;'>👁️ APERÇU DU CV</h3>", unsafe_allow_html=True)
    chemin_pdf = compiler_pdf(donnees_cv)
    
    if chemin_pdf:
        # Magnifique bouton de téléchargement Or
        with open(chemin_pdf, "rb") as pdf_file:
            st.download_button(
                label="📥 TÉLÉCHARGER LE CV (PDF)",
                data=pdf_file,
                file_name=f"CV_{prenom.strip()}_{nom.strip()}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
        st.write("") # Petit espace
        afficher_pdf(chemin_pdf)