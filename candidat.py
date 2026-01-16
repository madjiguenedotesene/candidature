from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import traceback
# 1. NOUVEAUX IMPORTS POUR GÉRER L'URL
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def se_connecter_labonneboite(identifiant, mot_de_passe):
    """
    Automatise la connexion (Code inchangé)
    """
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://labonneboite.francetravail.fr/")

    try:
        # Gérer la bannière de cookies
        try:
            cookie_banner = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "pe-cookies"))
            )
            accepter_button = WebDriverWait(cookie_banner, 10).until(
                EC.element_to_be_clickable((By.XPATH, ".//*[contains(text(), 'Tout accepter')]"))
            )
            accepter_button.click()
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.TAG_NAME, "pe-cookies"))
            )
            print("Bannière de cookies gérée.")
        except:
            print("Bannière de cookies non trouvée.")

        # Connexion
        se_connecter_btn_labonneboite = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login"))
        )
        se_connecter_btn_labonneboite.click()

        identifiant_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifiant"))
        )
        identifiant_field.send_keys(identifiant)

        mot_de_passe_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        mot_de_passe_field.send_keys(mot_de_passe)

        connexion_btn_france_travail = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit"))
        )
        connexion_btn_france_travail.click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".main-container"))
        )
        print("Connexion à La Bonne Boîte réussie.")
        return driver

    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")
        if 'driver' in locals():
            driver.quit()
        return None
# 2. FONCTION  POUR CHANGER LE NUMÉRO DE PAGE DANS L'URL
def regenerer_url_page(url, numero_page):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params['page'] = [str(numero_page)]
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def candidature_automatique(driver, metier="Ingénieur / Ingénieure télécoms ", localisation="Ile-de-France"):
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "page-home > section.border-b"))
        )
        metier_field = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "job-input"))
        )
        metier_field.send_keys(metier)
        input("Sélectionnez le métier et appuyez sur Entrée...")

        localisation_field = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "location-input"))
        )
        localisation_field.send_keys(localisation)
        time.sleep(1)
        input("Sélectionnez la localisation et appuyez sur Entrée...")

        trouve_travail = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.ID, "search"))
        )
        trouve_travail.click()

        # 3. ON CAPTURE L'URL DE BASE ICI (IMPORTANT)
        print("Recherche lancée. Capture de l'URL de base...")
        time.sleep(1) # On attend que l'URL change bien
        url_de_base = driver.current_url

        page_number = 1

        while True:
            # On prépare l'URL de la page actuelle (ex: page 1, page 2...)
            url_page_actuelle = regenerer_url_page(url_de_base, page_number)
            print(f">>> PAGE {page_number}")

            for i in range(6):  # i de 0 à 5
                try:
                    print(f"--- Traitement Offre {i} ---")

                    # On s'assure d'être sur la bonne page avant de cliquer
                    # Si on n'est pas sur la liste (ex: resté sur une offre précédente), on recharge
                    if "recherche" not in driver.current_url:
                        driver.get(url_page_actuelle)


                    # Cliquer sur l'offre d'emploi
                    job_offer_id = f"result-{i}"
                    try:
                        job_offer = WebDriverWait(driver, 1).until(
                            EC.element_to_be_clickable((By.ID, job_offer_id))
                        )
                        # Petit scroll pour éviter les erreurs
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_offer)

                        job_offer.click()
                    except:
                        print(f"Offre {i} non trouvée ou impossible à cliquer. On passe.")
                        continue

                    # Tenter de cliquer sur le bouton "Débuter votre candidature"
                    try:
                        debuter_candidature_btn = WebDriverWait(driver, 1).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Débuter votre candidature')]"))
                        )
                        print("Bouton trouvé. Lancement...")
                        debuter_candidature_btn .click()

                        # Sélectionner les fichiers
                        try:
                            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "doc-0-select"))).click()
                            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "doc-1-select"))).click()

                            # Continuer
                            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "send-application"))).click()

                            # Envoyer la candidature
                            envoyer_candidature_btn = WebDriverWait(driver, 1).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Envoyer la candidature')]"))
                            )
                            envoyer_candidature_btn.click()
                            print(f"✅ Candidature envoyée pour l'offre {i}.")

                            time.sleep(2) # On laisse le message de succès s'afficher

                            # 4. LE FIX EST ICI : AU LIEU DE RETOUR ACCUEIL, ON RECHARGE LA PAGE ACTUELLE
                            print("Retour à la liste via URL...")
                            driver.get(url_page_actuelle)
                            # On attend que la liste revienne
                            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, f"result-{i}")))

                        except Exception as e:
                            print(f"Echec envoi candidature: {e}")
                            # En cas d'erreur dans le formulaire, on revient aussi à la liste via URL
                            driver.get(url_page_actuelle)

                    except:
                        # Si le bouton "Débuter" n'est pas là
                        print(f"Pas de candidature spontanée pour l'offre {i}.")
                        # On retourne à la liste pour passer à la suivante (car le clic sur l'offre a changé la page)
                        driver.get(url_page_actuelle)
                        pass

                except Exception as e:
                    print(f"Erreur lors du traitement de l'offre {i}: {e}")
                    # Sécurité : On recharge la page pour être sûr d'être prêt pour i+1
                    driver.get(url_page_actuelle)
                    continue

            # Passage à la page suivante
            try:
                # 5. ON MET A JOUR LE NUMERO DE PAGE
                page_number += 1
                url_suivante = regenerer_url_page(url_de_base, page_number)
                print(f"Passage à la page suivante (URL): {page_number}")
                driver.get(url_suivante)
                time.sleep(1)

                # Vérification qu'il y a des résultats sur la nouvelle page
                try:
                    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "result-0")))
                except:
                    print("Plus de résultats trouvés. Fin du programme.")
                    break

            except Exception as e:
                print(f"Erreur changement de page: {e}")
                break

    except Exception as e:
        print(f"Une erreur s'est produite: {e}")
    finally:
        print("Processus de candidature terminé.")
        # driver.quit() # Décommente quand tu es sûr que tout marche

if __name__ == '__main__':
    mon_identifiant ="10512925005"
    mon_mot_de_passe = "Dote96200@"
    metier_rechercher = "Ingénieur / Ingénieure télécoms"
    localisation = "Île-de-France"

    driver = se_connecter_labonneboite(mon_identifiant, mon_mot_de_passe)
    if driver:
        print("Démarrage des candidatures spontanées...")
        succes_candidature = candidature_automatique(driver, metier=metier_rechercher, localisation=localisation)
        if succes_candidature:
            print("le nombre_candidatures_souhaitees tentatives de candidature effectuées.")
        else:
            print("Le processus de candidature a rencontré des erreurs.")
        driver.quit()
