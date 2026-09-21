# -*- coding: utf-8 -*-
"""Données de référence pour l'enquête E-CNPS Employeurs - Volet Prestations."""

TAILLE_ENTREPRISE = [
    "1 à 5 salariés", "6 à 20 salariés", "21 à 100 salariés",
    "Plus de 100 salariés", "Employeur de personnel domestique",
]

ROLE = [
    "Chef d'entreprise / dirigeant", "Responsable RH / paie", "Comptable / gestionnaire",
    "Mandataire / prestataire externe", "Autre",
]

DEMANDES_PRESTATION = [
    "Indemnité journalière de maternité pour une salariée",
    "Déclaration d'accident du travail / maladie professionnelle",
    "Demande d'attestation liée aux prestations",
    "Prestations / allocations familiales",
    "Constitution ou suivi d'un dossier de pension (retraite)",
    "Autre",
]

FREQUENCE = ["Chaque mois", "Chaque trimestre", "Quelques fois par an", "Première utilisation"]

SUPPORT = ["Ordinateur", "Téléphone / tablette", "Les deux"]

SEXE = ["Masculin", "Féminin"]

CSAT = ["Très satisfait(e)", "Satisfait(e)", "Insatisfait(e)", "Très insatisfait(e)"]

SATISFACTION_ROWS = [
    ("p_acces", "Accès au compte et à la rubrique « prestations »"),
    ("p_comprehension_pieces", "Compréhension des pièces à fournir"),
    ("p_televersement", "Téléversement / envoi des documents en ligne"),
    ("p_instruction", "Instruction et traitement du dossier"),
    ("p_info_montant", "Information sur le calcul et le montant de la prestation"),
    ("p_delai_versement", "Délai jusqu'au versement / à l'obtention"),
    ("p_suivi", "Suivi de l'état d'avancement du dossier"),
]
SATISFACTION_SCALE = ["Très satisfait(e)", "Satisfait(e)", "Insatisfait(e)", "Très insatisfait(e)"]

CES = ["Très facile", "Facile", "Difficile", "Très difficile"]

ERGONOMIE_ROWS = [
    ("erg_clarte_ecrans", "Clarté et lisibilité des écrans"),
    ("erg_trouver_rubrique", "Facilité à trouver la bonne rubrique / le bon service"),
    ("erg_vocabulaire", "Clarté du vocabulaire et des libellés"),
    ("erg_liste_pieces", "Clarté de la liste des pièces à fournir"),
    ("erg_rapidite", "Rapidité de chargement et stabilité"),
    ("erg_televerser", "Facilité de téléversement des documents"),
    ("erg_messages", "Qualité des messages d'erreur et des aides"),
    ("erg_mobile", "Confort d'utilisation sur mobile"),
]
ERGONOMIE_SCALE = ["Excellent", "Bon", "Passable", "Mauvais"]

FCR = [
    "Oui, entièrement en ligne", "Non, appel au centre de relation client",
    "Non, déplacement en agence", "Non, les deux",
]

DELAI = ["Plus rapide que prévu", "Conforme à mes attentes", "Plus lent que prévu", "Sans comparaison"]

CONTINUITE = [
    "Oui, systématiquement", "Oui, pour certaines démarches",
    "Non, je préfère l'agence", "Je ne sais pas encore",
]
