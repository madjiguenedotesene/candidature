import io
import streamlit as st
import jinja2
import os
import subprocess
import base64
import json
from PIL import Image

# ==========================================
# 1. CONFIGURATION & DESIGN SYSTEM
# ==========================================
st.set_page_config(page_title="ELANPRO | ARCHITECTE CV", page_icon="🔹", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000000 !important; }
    .block-container {
        background-color: #F8FAFC; 
        padding: 40px !important;
        border: 2px solid #334155; 
        border-radius: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    [data-testid="stSidebar"] { 
        background-color: #0F172A !important; 
        min-width: 180px !important;
        max-width: 220px !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    .stWidget label p {
        color: #1E293B !important; 
        font-weight: 900 !important; 
        text-transform: uppercase !important;
        background-color: #E2E8F0 !important; 
        padding: 3px 8px !important;
        border-radius: 4px !important;
        display: inline-block;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: white !important;
        color: black !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    h1, h2, h3, h4, p, span { color: #0F172A !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. GESTION DES DONNÉES
# ==========================================
DB_FILE = "data_omni_bot.json"

def charger_donnees():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {}

db = charger_donnees()

def ajouter_item(section, default_dict):
    st.session_state[section].append(default_dict)

def supprimer_item(section, index):
    st.session_state[section].pop(index)

# INITIALISATION DES VARIABLES
if "reseaux" not in st.session_state: st.session_state.reseaux = db.get("reseaux", [{"nom": "LinkedIn", "url": ""}])
if "competences" not in st.session_state: st.session_state.competences = db.get("competences", [{"details": "OUTILS"}])
if "experiences" not in st.session_state: st.session_state.experiences = db.get("experiences", [{"poste": "", "entreprise": "", "date": "", "puces": [""]}])
if "formations" not in st.session_state: st.session_state.formations = db.get("formations", [{"titre": "", "ecole": "", "date": "", "puces": [""]}])
if "certifications" not in st.session_state: st.session_state.certifications = db.get("certifications", [{"titre": "", "organisme": "", "date": "", "puces": [""]}])
if "realisations" not in st.session_state: st.session_state.realisations = db.get("realisations", [{"titre": "", "puces": [""]}])
if "langues_list" not in st.session_state: st.session_state.langues_list = db.get("langues_list", ["Anglais"])
if "soft_list" not in st.session_state: st.session_state.soft_list = db.get("soft_list", ["Autonomie"])

def hex_to_rgb(h):
    h = h.lstrip('#')
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"

# ==========================================
# 3. BARRE LATÉRALE
# ==========================================
with st.sidebar:
    try:
        st.image("logon.png", use_container_width=True)
    except:
        st.title("ELANPRO")
    
    st.markdown("---")
    menu = st.radio("MENU", ["DESIGN", "PROFIL", "COMPÉTENCES", "EXPÉRIENCES", "FORMATIONS", "PROJETS", "CERTIFICATIONS", "ATOUTS"])
    cp = st.color_picker("PRINCIPALE", "#1A365D")
    ca = st.color_picker("ACCENT", "#D4AF37")
    
    if st.button("SAUVEGARDER"):
        keys = ["reseaux", "competences", "experiences", "formations", "certifications", "realisations", "langues_list", "soft_list"]
        data_to_save = {k: st.session_state[k] for k in keys}
        with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data_to_save, f, indent=4)
        st.success("SYNCHRO")

# ==========================================
# 4. INTERFACE DE SAISIE
# ==========================================
st.markdown(f"## Elanpro votre générateur de CV anti ATS !")
col_in, col_out = st.columns([1, 1])

with col_in:
    def render_puces(data_list, key_prefix):
        for j, p in enumerate(data_list):
            c_p1, c_p2 = st.columns([9, 1])
            data_list[j] = c_p1.text_input(f"Puce", p, key=f"{key_prefix}_{j}", label_visibility="collapsed")
            if c_p2.button("❌", key=f"del_{key_prefix}_{j}"):
                data_list.pop(j); st.rerun()

    if menu == "DESIGN":
        photo = st.file_uploader("Choisir une image", type=["png", "jpg", "jpeg"])
        if photo: 
            Image.open(photo).convert("RGB").save("cv.png")
            st.image("cv.png", width=100)

    elif menu == "PROFIL":
        st.session_state.prenom = st.text_input("Prénom", st.session_state.get('prenom', 'Madji'))
        st.session_state.nom = st.text_input("Nom", st.session_state.get('nom', 'SENE'))
        st.session_state.titre_job = st.text_input("Titre du CV", st.session_state.get('titre_job', 'DATA ANALYST'))
        c1, c2 = st.columns(2)
        st.session_state.email = c1.text_input("Email", st.session_state.get('email', ''))
        st.session_state.tel = c2.text_input("Téléphone", st.session_state.get('tel', ''))
        c3, c4 = st.columns(2)
        st.session_state.ville = c3.text_input("Ville & Pays", st.session_state.get('ville', 'Paris, France'))
        st.session_state.age = c4.text_input("Âge", st.session_state.get('age', '25'))
        st.session_state.bio = st.text_area("Résumé", st.session_state.get('bio', ''), height=100)
        
        for i, res in enumerate(st.session_state.reseaux):
            cr1, cr2, cr3 = st.columns([3, 5, 1])
            res["nom"] = cr1.text_input("Nom", res["nom"], key=f"r_n_{i}", label_visibility="collapsed")
            res["url"] = cr2.text_input("URL", res["url"], key=f"r_u_{i}", label_visibility="collapsed")
            if cr3.button("🗑️", key=f"r_d_{i}"): supprimer_item("reseaux", i); st.rerun()
        st.button("➕ Lien", on_click=lambda: ajouter_item("reseaux", {"nom": "", "url": ""}))

    elif menu == "COMPÉTENCES":
        st.subheader("⚡ Mes Compétences")
        if isinstance(st.session_state.competences, str): st.session_state.competences = [{"details": st.session_state.competences}]
        for i in range(len(st.session_state.competences)):
            c1, c2 = st.columns([8, 1])
            st.session_state.competences[i]["details"] = c1.text_input(f"C_{i}", st.session_state.competences[i].get("details", ""), key=f"c_in_{i}", label_visibility="collapsed")
            if c2.button("🗑️", key=f"c_del_{i}"): st.session_state.competences.pop(i); st.rerun()
        if st.button("➕ Ajouter"): st.session_state.competences.append({"details": ""}); st.rerun()

    elif menu == "EXPÉRIENCES":
        for i, ex in enumerate(st.session_state.experiences):
            with st.expander(f"💼 {ex['poste'] or 'Expérience ' + str(i+1)}", expanded=True):
                ex["poste"] = st.text_input("Poste", ex["poste"], key=f"ex_p_{i}")
                ex["entreprise"] = st.text_input("Entreprise", ex["entreprise"], key=f"ex_e_{i}")
                ex["date"] = st.text_input("Date", ex["date"], key=f"ex_d_{i}")
                render_puces(ex["puces"], f"ex_m_{i}")
                col1, col2 = st.columns([1,1])
                if col1.button("+ Mission", key=f"ex_am_{i}"): ex["puces"].append(""); st.rerun()
                if col2.button("🗑️ Supprimer Expérience", key=f"ex_del_{i}"): st.session_state.experiences.pop(i); st.rerun()
        st.button("➕ Ajouter Expérience", on_click=lambda: ajouter_item("experiences", {"poste":"","entreprise":"","date":"","puces":[""]}))

    elif menu == "FORMATIONS":
        for i, f in enumerate(st.session_state.formations):
            with st.expander(f"🎓 {f['titre'] or 'Formation ' + str(i+1)}", expanded=True):
                f["titre"] = st.text_input("Diplôme", f["titre"], key=f"f_t_{i}")
                f["ecole"] = st.text_input("École", f["ecole"], key=f"f_e_{i}")
                f["date"] = st.text_input("Année", f["date"], key=f"f_d_{i}")
                if st.button("🗑️ Supprimer Formation", key=f"f_del_{i}"): st.session_state.formations.pop(i); st.rerun()
        st.button("➕ Ajouter Formation", on_click=lambda: ajouter_item("formations", {"titre":"","ecole":"","date":"","puces":[""]}))

    elif menu == "PROJETS":
        for i, pr in enumerate(st.session_state.realisations):
            with st.expander(f"🚀 {pr['titre'] or 'Projet ' + str(i+1)}", expanded=True):
                pr["titre"] = st.text_input("Nom du projet", pr["titre"], key=f"pr_t_{i}")
                render_puces(pr["puces"], f"pr_m_{i}")
                col1, col2 = st.columns([1,1])
                if col1.button("+ Détail", key=f"pr_ad_{i}"): pr["puces"].append(""); st.rerun()
                if col2.button("🗑️ Supprimer Projet", key=f"pr_del_{i}"): st.session_state.realisations.pop(i); st.rerun()
        st.button("➕ Ajouter Projet", on_click=lambda: ajouter_item("realisations", {"titre":"","puces":[""]}))

    elif menu == "CERTIFICATIONS":
        for i, ct in enumerate(st.session_state.certifications):
            with st.expander(f"🏆 {ct['titre'] or 'Certification ' + str(i+1)}", expanded=True):
                ct["titre"] = st.text_input("Nom de la certif", ct["titre"], key=f"ct_t_{i}")
                ct["organisme"] = st.text_input("Organisme", ct["organisme"], key=f"ct_o_{i}")
                ct["date"] = st.text_input("Date/Année", ct.get("date", ""), key=f"ct_d_{i}")
                if st.button("🗑️ Supprimer Certif", key=f"ct_del_{i}"): st.session_state.certifications.pop(i); st.rerun()
        st.button("➕ Ajouter Certif", on_click=lambda: ajouter_item("certifications", {"titre":"","organisme":"","date":"","puces":[""]}))

    elif menu == "ATOUTS":
        st.subheader("LANGUES")
        for i, l in enumerate(st.session_state.langues_list):
            c1, c2 = st.columns([9, 1])
            st.session_state.langues_list[i] = c1.text_input(f"L_{i}", l, key=f"l_in_{i}", label_visibility="collapsed")
            if c2.button("🗑️", key=f"l_del_{i}"): st.session_state.langues_list.pop(i); st.rerun()
        st.button("+ Langue", on_click=lambda: st.session_state.langues_list.append(""))

        st.subheader("SOFT SKILLS")
        for i, s in enumerate(st.session_state.soft_list):
            c1, c2 = st.columns([9, 1])
            st.session_state.soft_list[i] = c1.text_input(f"S_{i}", s, key=f"s_in_{i}", label_visibility="collapsed")
            if c2.button("🗑️", key=f"s_del_{i}"): st.session_state.soft_list.pop(i); st.rerun()
        st.button("+ Soft Skill", on_click=lambda: st.session_state.soft_list.append(""))

# ==========================================
# 5. GÉNÉRATION PDF
# ==========================================
with col_out:
    donnees_cv = {
        "prenom": st.session_state.get('prenom', 'Madji'),
        "nom": st.session_state.get('nom', 'SENE'),
        "titre_job": st.session_state.get('titre_job', 'DATA ANALYST'),
        "email": st.session_state.get('email', ''),
        "telephone": st.session_state.get('tel', ''),
        "ville": st.session_state.get('ville', 'Paris, France'),
        "age": st.session_state.get('age', '25'),
        "profil_text": st.session_state.get('bio', ''),
        "color_primary": hex_to_rgb(cp), "color_accent": hex_to_rgb(ca),
        "experiences": st.session_state.experiences,
        "formations": st.session_state.formations,
        "certifications": st.session_state.certifications,
        "realisations": st.session_state.realisations,
        "competences": [c for c in st.session_state.competences if c.get("details")], 
        "langues": ", ".join([l for l in st.session_state.langues_list if l]),
        "soft_skills": ", ".join([s for s in st.session_state.soft_list if s]),
        "reseaux": st.session_state.reseaux
    }

    try:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
        template = env.get_template("cv_template.tex")
        with open("cv_genere.tex", "w", encoding="utf-8") as f: f.write(template.render(donnees_cv))
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "cv_genere.tex"], capture_output=True)
        if os.path.exists("cv_genere.pdf"):
            with open("cv_genere.pdf", "rb") as f: b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="800px" style="border-radius:12px;"></iframe>', unsafe_allow_html=True)
            st.download_button("📥 TÉLÉCHARGER LE PDF", open("cv_genere.pdf", "rb"), f"CV_{donnees_cv['nom']}.pdf")
    except: st.info("Saisie en cours...")