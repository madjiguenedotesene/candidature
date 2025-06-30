#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 17:59:36 2025

@author: madjiguenedotesene
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import traceback


def se_connecter_labonneboite(identifiant, mot_de_passe):
    """
    Automatise la connexion à La Bonne Boîte en utilisant les identifiants France Travail.
    Gère également la bannière de cookies.
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
            print("Bannière de cookies non trouvée ou impossible à gérer.")

        # Connexion à La Bonne Boîte via France Travail
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
        traceback.print_exc()
        if 'driver' in locals():
            driver.quit()
        return None


def naviguer_candidature_spontanee(driver, metier="Ingénieur / Ingénieure télécoms ", localisation="Ile-de-France",
                                    nombre_candidatures=20):
    try:
        WebDriverWait(driver, 9).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "page-home > section.border-b"))
        )
        metier_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "job-input"))
        )
        metier_field.send_keys(metier)
        input("Sélectionnez le métier et appuyez sur Entrée...")
        localisation_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "location-input"))
        )
        localisation_field.send_keys(localisation)
        time.sleep(1)
        input("Sélectionnez la localisation et appuyez sur Entrée...")
        trouve_travail = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "search"))
        )
        trouve_travail.click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[id^='result-']"))
        )
        nombre_candidatures = 10000
        candidatures_effectuees = 0
        page_number = 1
        for j in range(1, 10000):
            id_page = "/page/next"
            # Navigation de page
            if candidatures_effectuees < nombre_candidatures:
                try:
                    next_page_button = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.ID, id_page))  # Utilisez l'ID correct
                    )
                    next_page_button.click()
                    print(f"Navigation vers la page {page_number + 1}.")
                    while candidatures_effectuees < nombre_candidatures:
                        print(f"--- Traitement de la page {page_number} ---")
                        results = driver.find_elements(By.CSS_SELECTOR, "li[id^='result-']")
                        num_results_on_page = len(results)
                        print(f"Nombre de résultats sur cette page : {num_results_on_page}")

                        for i in range(num_results_on_page):
                            if candidatures_effectuees >= nombre_candidatures:
                                break

                            result_id = f"result-{i}"
                            try:
                                result_element = WebDriverWait(driver, 1).until(
                                    EC.presence_of_element_located((By.ID, result_id))
                                )
                                result_element.click()
                                print(f"Cliqué sur : {result_id}")
                                time.sleep(1)

                                # Tenter la candidature spontanée
                                try:
                                    debuter_candidature_button_xpath = WebDriverWait(driver, 1).until(
                                        EC.element_to_be_clickable((By.XPATH,
                                                                     "//button[@id='create-application' and contains(text(), 'Débuter votre candidature spontanée')]"))
                                    )
                                    debuter_candidature_button_xpath.click()
                                    print(f"Début candidature pour : {result_id}")
                                    time.sleep(1)

                                    try:
                                        select_cv_button_xpath = WebDriverWait(driver, 1).until(
                                            EC.element_to_be_clickable((By.ID, "doc-0-select"))
                                        )
                                        select_cv_button_xpath.click()
                                        select_cv_button_xpath = WebDriverWait(driver, 1).until(
                                            EC.element_to_be_clickable((By.ID, "doc-1-select"))
                                        )
                                        select_cv_button_xpath.click()
                                        print(f"CV sélectionné pour : {result_id}")
                                        time.sleep(1)
                                    except TimeoutException:
                                        print(f"CV déjà sélectionné ou bouton non trouvé pour : {result_id}")

                                    try:
                                        continuer_button_xpath = WebDriverWait(driver, 1).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//button[@id='send-application' and contains(text(), 'Continuer')]"))
                                        )
                                        continuer_button_xpath.click()
                                        print("Clique sur 'Continuer'.")
                                        time.sleep(1)
                                    except TimeoutException:
                                        print("'Continuer' non trouvé.")

                                    try:
                                        # Augmentation du temps d'attente et changement de stratégie
                                        envoyer_button_xpath = WebDriverWait(driver, 1).until(
                                            EC.presence_of_element_located(
                                                (By.XPATH, "//button[contains(text(), 'Envoyer la candidature')]"))
                                        )
                                        envoyer_button_xpath.click()
                                        print(f"Candidature envoyée pour : {result_id}")
                                        time.sleep(1)
                                        candidatures_effectuees += 1

                                        retour_button = WebDriverWait(driver, 1).until(
                                            EC.element_to_be_clickable((By.ID, "go-to-home"))
                                        )
                                        retour_button.click()
                                        trouve_travail_again = WebDriverWait(driver, 1).until(
                                            EC.element_to_be_clickable((By.ID, "search"))
                                        )
                                        trouve_travail_again.click()

                                        WebDriverWait(driver, 1).until(
                                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[id^='result-']"))
                                        )
                                        time.sleep(1)

                                        print("Retour à la recherche.")
                                        WebDriverWait(driver, 1).until(
                                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[id^='result-']"))
                                        )
                                        time.sleep(1)
                                        continue

                                    except TimeoutException:
                                        print("'Envoyer' non trouvé après 15 secondes. Abandon de la candidature.")
                                        retour_button = WebDriverWait(driver, 1).until(
                                            EC.element_to_be_clickable((By.ID, "go-to-home"))
                                        )
                                        retour_button.click()
                                        print("Retour à la liste des résultats après échec d'envoi.")

                                        WebDriverWait(driver, 1).until(
                                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[id^='result-']"))
                                        )
                                        time.sleep(1)
                                        continue  # Passer à l'offre suivante
                                    except NoSuchElementException:
                                        print("'Envoyer' non trouvé dans le DOM. Abandon de la candidature.")
                                        retour_button = WebDriverWait(driver, 1).until(
                                            EC.element_to_be_clickable((By.ID, "go-to-home"))
                                        )
                                        retour_button.click()
                                        print("Retour à la liste des résultats après échec d'envoi.")
                                        WebDriverWait(driver, 1).until(
                                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[id^='result-']"))
                                        )
                                        time.sleep(1)
                                        continue

                                except TimeoutException:
                                    print(f"Bouton 'Débuter...' non trouvé pour : {result_id}.")
                                    pass

                            except Exception as e_candidature:
                                print(f"Erreur lors de la candidature pour {result_id}: {e_candidature}")
                                traceback.print_exc()
                                try:
                                    retour_button = WebDriverWait(driver, 1).until(
                                        EC.element_to_be_clickable((By.ID, "go-to-home"))
                                    )
                                    retour_button.click()
                                    print("Retour à la liste des résultats après erreur.")
                                    WebDriverWait(driver, 1).until(
                                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[id^='result-']"))
                                    )
                                    time.sleep(1)
                                except TimeoutException:
                                    print(
                                        "Erreur lors du retour à la liste des résultats après erreur de candidature.")
                                    break

                        try:
                            next_page_button = WebDriverWait(driver, 1).until(
                                EC.element_to_be_clickable((By.ID, f"page-{page_number + 1}"))
                            )
                            next_page_button.click()
                            page_number += 1
                            print(f"Navigation vers la page {page_number}.")
                            WebDriverWait(driver, 1).until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[id^='result-']"))
                            )
                        except TimeoutException:
                            print("Fin des pages de résultats ou bouton de page suivante non trouvé.")
                            break

                except TimeoutException:
                    print("Bouton de navigation de page non trouvé.")
                    break
                except Exception as e:
                    print(f"Erreur lors de la navigation entre les pages : {e}")
                    traceback.print_exc()
                    break

        print(f"Nombre total de candidatures effectuées : {candidatures_effectuees}")
        return True

    except Exception as e:
        print(f"Erreur globale lors de la navigation : {e}")
        traceback.print_exc()
        return False


if __name__ == '__main__':
    mon_identifiant = "Madjiguene19"
    mon_mot_de_passe = "Dote96200@"
    metier_rechercher = "Ingénieur / Ingénieure télécoms"
    localisation = "Île-de-France"
    nombre_candidatures_souhaitees = 80000

    driver = se_connecter_labonneboite(mon_identifiant, mon_mot_de_passe)
    if driver:
        print("Démarrage des candidatures spontanées...")
        succes_candidature = naviguer_candidature_spontanee(driver, metier=metier_rechercher, localisation=localisation, nombre_candidatures=nombre_candidatures_souhaitees)
        if succes_candidature:
            print(f"{nombre_candidatures_souhaitees} tentatives de candidature effectuées.")
        else:
            print("Le processus de candidature a rencontré des erreurs.")
        driver.quit()
