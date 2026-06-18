# Gestionnaire d'Emploi du Temps

Application professionnelle de génération intelligente des emplois du temps scolaires.

## Présentation

Ce projet propose un tableau de bord complet pour gérer les enseignants, classes, matières, salles, créneaux et séances. Il intègre un moteur de génération intelligente d'emploi du temps, une détection automatique des conflits, des exports PDF/Excel et un affichage responsive.

## Fonctionnalités

- Authentification sécurisée avec rôles
- Dashboard moderne SaaS
- Gestion complète CRUD pour tous les modules
- Génération intelligente d'emploi du temps
- Détection automatique des conflits
- Visualisation des emplois du temps par classe/enseignant/salle/matière
- Export PDF, Excel et impression
- Statistiques avec graphiques Chart.js
- Recherche dynamique via AJAX
- Mode sombre optionnel

## Architecture

- `emploi_du_temps/app.py` : point d'entrée de l'application
- `emploi_du_temps/config.py` : configuration Flask et base de données
- `emploi_du_temps/models/` : définitions SQLAlchemy
- `emploi_du_temps/services/` : logique métier et services transverses
- `emploi_du_temps/routes/` : blueprints et contrôleurs de route
- `emploi_du_temps/templates/` : vues Jinja2
- `emploi_du_temps/static/` : ressources CSS/JS

## Installation

1. Créer un environnement virtuel

```bash
cd emploi_du_temps
python3 -m venv venv
source venv/bin/activate
```

2. Installer les dépendances

```bash
pip install -r requirements.txt
```

3. Lancer l'application

```bash
python3 app.py
```

4. Ouvrir le navigateur

```
http://127.0.0.1:5000
```

## Auteur

- Projet développé par BAAKI Hicham
