# Documentation : Script SQL - Création des Tables

**Projet :** Gestion intelligente des emplois du temps scolaires  
**Date :** 2026  
**Version :** 1.0

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture de la base de données](#architecture-de-la-base-de-données)
3. [Diagramme des relations](#diagramme-des-relations)
4. [Description détaillée des tables](#description-détaillée-des-tables)
5. [Ordre de création des tables](#ordre-de-création-des-tables)
6. [Données d'initialisation](#données-dinitialisation)
7. [Indices (Indexes)](#indices-indexes)
8. [Contraintes et validations](#contraintes-et-validations)
9. [Checklist de vérification](#checklist-de-vérification)

---

## Vue d'ensemble

La base de données SQLite supportant l'application de gestion des emplois du temps scolaires repose sur **7 tables principales**:

| Table | Rôle | Type | Relations |
|-------|------|------|-----------|
| `users` | Authentification et gestion des administrateurs | Référence | Aucune (racine) |
| `enseignants` | Gestion du personnel enseignant | Référence | 1 → N Seances |
| `classes` | Gestion des groupes d'élèves | Référence | 1 → N Seances |
| `matieres` | Catalogue des disciplines avec volume horaire | Référence | 1 → N Seances |
| `salles` | Gestion des ressources physiques | Référence | 1 → N Seances |
| `creneaux` | Plages horaires disponibles | Référence | 1 → N Seances |
| `seances` | Affectations pédagogiques (cours) | Jonction | N ← → N |

---

## Architecture de la base de données

### Modèle conceptuel

```
┌─────────────────────────────────────────────────────────────────┐
│                     SEANCES (Table centrale)                    │
│  classe_id (FK) → CLASSES                                       │
│  enseignant_id (FK) → ENSEIGNANTS                               │
│  matiere_id (FK) → MATIERES                                     │
│  salle_id (FK) → SALLES                                         │
│  creneau_id (FK) → CRENEAUX                                     │
└─────────────────────────────────────────────────────────────────┘
         ↑           ↑           ↑          ↑          ↑
         │           │           │          │          │
    ┌────┴─┐  ┌──────┴──┐  ┌────┴────┐ ┌──┴───┐  ┌───┴──────┐
    │      │  │         │  │         │ │      │  │          │
┌───▼──┐ ┌─▼──────┐ ┌──▼──────┐ ┌──▼──┐ ┌──▼─────┐
│CLASSES│ │MATIERES│ │ENSEIGNANTS│ │SALLES│ │CRENEAUX│
└───────┘ └────────┘ └──────────┘ └──────┘ └────────┘

USER (Authentification)
```

---

## Diagramme des relations

### Détail des relations Many-to-Many

La table **SEANCES** établit un lien complet entre :
- 1 **Classe** (groupe d'élèves)
- 1 **Enseignant** (professeur)
- 1 **Matière** (discipline)
- 1 **Salle** (ressource physique)
- 1 **Créneau** (plage horaire)

Pour une même Classe, plusieurs Séances différentes. Même logique pour Enseignant, Matière, etc.

---

## Description détaillée des tables

### 1. Table `USERS`

**Rôle :** Stockage des administrateurs/utilisateurs du système  
**Responsabilité :** Authentification sécurisée et gestion des sessions

#### Structure SQL

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Colonnes

| Colonne | Type | Contraintes | Descriptiο |
|---------|------|-------------|-----------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identifiant unique |
| `nom` | VARCHAR(100) | NOT NULL | Nom de famille de l'utilisateur |
| `prenom` | VARCHAR(100) | NOT NULL | Prénom de l'utilisateur |
| `email` | VARCHAR(150) | NOT NULL, UNIQUE | Email unique (identifiant de connexion) |
| `password` | VARCHAR(255) | NOT NULL | Mot de passe hashé (bcrypt) |
| `role` | VARCHAR(50) | NOT NULL, DEFAULT='Admin' | Rôle (Admin, Gestionnaire, etc.) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de création |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Dernière modification |

#### Relations

- **Aucune relation directe** (table maître pour l'authentification)

#### Données d'initialisation

Un administrateur par défaut doit être inséré :

```sql
INSERT INTO users (nom, prenom, email, password, role) 
VALUES ('Admin', 'Systeme', 'admin@ecole.com', '[hash_bcrypt]', 'Admin');
```

---

### 2. Table `ENSEIGNANTS`

**Rôle :** Gestion du personnel enseignant  
**Responsabilité :** Stockage des données des professeurs et disponibilités

#### Structure SQL

```sql
CREATE TABLE enseignants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telephone VARCHAR(50),
    specialite VARCHAR(100),
    disponibilite VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Colonnes

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identifiant unique |
| `nom` | VARCHAR(100) | NOT NULL | Nom de famille |
| `prenom` | VARCHAR(100) | NOT NULL | Prénom |
| `email` | VARCHAR(150) | NOT NULL, UNIQUE | Email professionnel |
| `telephone` | VARCHAR(50) | NULLABLE | Numéro de téléphone |
| `specialite` | VARCHAR(100) | NULLABLE | Domaine d'enseignement (Mathématiques, Français, etc.) |
| `disponibilite` | VARCHAR(255) | NULLABLE | Jours/créneaux disponibles (format : "Lundi,Mardi;Mercredi") |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de création |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Dernière modification |

#### Relations

- **1 → N** avec `SEANCES` : Un enseignant peut avoir plusieurs séances

#### Remarques métier

- Le champ `disponibilite` stocke les jours/créneaux sous forme de texte (la validation est effectuée au niveau du code)
- Vérifier l'unicité de l'email pour éviter les doublons

---

### 3. Table `CLASSES`

**Rôle :** Gestion des groupes d'élèves  
**Responsabilité :** Stockage des classes avec métadonnées

#### Structure SQL

```sql
CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    niveau VARCHAR(100) NOT NULL,
    effectif INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Colonnes

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identifiant unique |
| `nom` | VARCHAR(100) | NOT NULL | Nom de la classe (ex: "1ère A", "3ème B") |
| `niveau` | VARCHAR(100) | NOT NULL | Niveau scolaire (ex: "1ère année", "Baccalauréat") |
| `effectif` | INTEGER | NOT NULL | Nombre d'élèves dans la classe |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de création |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Dernière modification |

#### Relations

- **1 → N** avec `SEANCES` : Une classe a plusieurs séances/cours

#### Contraintes métier

- `effectif` doit être > 0
- `effectif` doit être ≤ capacité de la salle pour toute séance assignée (vérification au niveau application)

---

### 4. Table `MATIERES`

**Rôle :** Catalogue des disciplines  
**Responsabilité :** Stockage des matières et volumes horaires

#### Structure SQL

```sql
CREATE TABLE matieres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    volume_horaire INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Colonnes

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identifiant unique |
| `nom` | VARCHAR(100) | NOT NULL | Nom de la matière (Mathématiques, Français, etc.) |
| `volume_horaire` | INTEGER | NOT NULL | Nombre d'heures requises pour cette matière |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de création |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Dernière modification |

#### Relations

- **1 → N** avec `SEANCES` : Une matière est enseignée en plusieurs séances

#### Contraintes métier

- `volume_horaire` > 0
- Le volume horaire doit être couvert par des séances pour chaque classe

---

### 5. Table `SALLES`

**Rôle :** Gestion des ressources physiques  
**Responsabilité :** Inventaire des locaux et capacités

#### Structure SQL

```sql
CREATE TABLE salles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    capacite INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Colonnes

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identifiant unique |
| `nom` | VARCHAR(100) | NOT NULL | Nom de la salle (Salle 101, Labo Chimie, etc.) |
| `type` | VARCHAR(100) | NOT NULL | Type de salle (Classe, Labo, Amphithéâtre, Salle Informatique) |
| `capacite` | INTEGER | NOT NULL | Nombre de places disponibles |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de création |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Dernière modification |

#### Relations

- **1 → N** avec `SEANCES` : Une salle accueille plusieurs séances (à créneaux différents)

#### Contraintes métier

- `capacite` ≥ `effectif` de toute classe qui l'utilise
- Une salle ne peut accueillir qu'une seule séance par créneau (contrainte appliquée par trigger)

---

### 6. Table `CRENEAUX`

**Rôle :** Définition des plages horaires  
**Responsabilité :** Stockage des créneaux disponibles

#### Structure SQL

```sql
CREATE TABLE creneaux (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jour VARCHAR(50) NOT NULL,
    heure_debut VARCHAR(10) NOT NULL,
    heure_fin VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Colonnes

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identifiant unique |
| `jour` | VARCHAR(50) | NOT NULL | Jour de la semaine (Lundi, Mardi, etc.) |
| `heure_debut` | VARCHAR(10) | NOT NULL | Heure de début (format HH:MM) |
| `heure_fin` | VARCHAR(10) | NOT NULL | Heure de fin (format HH:MM) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de création |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Dernière modification |

#### Relations

- **1 → N** avec `SEANCES` : Un créneau peut contenir plusieurs séances

#### Contraintes métier

- `heure_debut` < `heure_fin`
- Format des heures : HH:MM (validation au niveau application)
- Les créneaux ne doivent pas se chevaucher pour un même jour (à vérifier via vues/triggers)

#### Exemple de données

```sql
INSERT INTO creneaux (jour, heure_debut, heure_fin) VALUES 
('Lundi', '08:00', '09:00'),
('Lundi', '09:00', '10:00'),
('Lundi', '10:00', '11:00'),
('Lundi', '11:00', '12:00'),
('Lundi', '13:00', '14:00'),
('Lundi', '14:00', '15:00'),
('Lundi', '15:00', '16:00'),
('Mardi', '08:00', '09:00'),
... (à étendre pour chaque jour et créneau)
;
```

---

### 7. Table `SEANCES`

**Rôle :** Modélisation des cours/séances  
**Responsabilité :** Affectation des ressources pédagogiques

#### Structure SQL

```sql
CREATE TABLE seances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classe_id INTEGER NOT NULL,
    enseignant_id INTEGER NOT NULL,
    matiere_id INTEGER NOT NULL,
    salle_id INTEGER NOT NULL,
    creneau_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (classe_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (enseignant_id) REFERENCES enseignants(id) ON DELETE RESTRICT,
    FOREIGN KEY (matiere_id) REFERENCES matieres(id) ON DELETE RESTRICT,
    FOREIGN KEY (salle_id) REFERENCES salles(id) ON DELETE RESTRICT,
    FOREIGN KEY (creneau_id) REFERENCES creneaux(id) ON DELETE RESTRICT
);
```

#### Colonnes

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identifiant unique |
| `classe_id` | INTEGER | NOT NULL, FK → classes(id) | Référence à la classe |
| `enseignant_id` | INTEGER | NOT NULL, FK → enseignants(id) | Référence à l'enseignant |
| `matiere_id` | INTEGER | NOT NULL, FK → matieres(id) | Référence à la matière |
| `salle_id` | INTEGER | NOT NULL, FK → salles(id) | Référence à la salle |
| `creneau_id` | INTEGER | NOT NULL, FK → creneaux(id) | Référence au créneau |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de création |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Dernière modification |

#### Relations (Foreign Keys)

| FK | Table Source | Table Cible | Règle | Raison |
|----|--------------|-------------|-------|--------|
| `classe_id` | seances | classes | CASCADE | Une classe supprimée → ses séances aussi |
| `enseignant_id` | seances | enseignants | RESTRICT | Emp. supprimé → erreur (vérifier séances d'abord) |
| `matiere_id` | seances | matieres | RESTRICT | Matière supprimée → erreur (vérifier séances) |
| `salle_id` | seances | salles | RESTRICT | Salle supprimée → erreur (vérifier séances) |
| `creneau_id` | seances | creneaux | RESTRICT | Créneau supprimé → erreur (vérifier séances) |

#### Contraintes métier

- **Unicité** : Pas de doublon (classe + créneau) → UNQ(classe_id, creneau_id)
- **Unicité** : Pas de doublon (enseignant + créneau) → UNQ(enseignant_id, creneau_id)
- **Unicité** : Pas de doublon (salle + créneau) → UNQ(salle_id, creneau_id)
- **Capacité** : effectif(classe) ≤ capacite(salle)
- **Disponibilité** : enseignant doit être disponible ce jour
- **Volume horaire** : le nombre total de séances par (classe, matière) doit couvrir le volume horaire requis

---

## Ordre de création des tables

**L'ordre de création est crucial** pour respecter les contraintes de clés étrangères :

### Séquence recommandée

1. **`users`** (aucune dépendance)
2. **`enseignants`** (aucune dépendance)
3. **`classes`** (aucune dépendance)
4. **`matieres`** (aucune dépendance)
5. **`salles`** (aucune dépendance)
6. **`creneaux`** (aucune dépendance)
7. **`seances`** (dépend de : classes, enseignants, matieres, salles, creneaux)

---

## Données d'initialisation

### 1. Insérer l'administrateur par défaut

```sql
INSERT INTO users (nom, prenom, email, password, role) 
VALUES ('Admin', 'Systeme', 'admin@ecole.com', '$2b$12$...bcrypt_hash...', 'Admin');
```

**Note :** Le mot de passe doit être pré-hashé en Python via `bcrypt` avant insertion.

### 2. Créneaux horaires standard

```sql
INSERT INTO creneaux (jour, heure_debut, heure_fin) VALUES 
('Lundi', '08:00', '09:00'),
('Lundi', '09:15', '10:15'),
('Lundi', '10:30', '11:30'),
('Lundi', '11:45', '12:45'),
('Lundi', '14:00', '15:00'),
('Lundi', '15:15', '16:15'),
('Lundi', '16:30', '17:30'),
('Mardi', '08:00', '09:00'),
('Mardi', '09:15', '10:15'),
('Mardi', '10:30', '11:30'),
('Mardi', '11:45', '12:45'),
('Mardi', '14:00', '15:00'),
('Mardi', '15:15', '16:15'),
('Mardi', '16:30', '17:30'),
('Mercredi', '08:00', '09:00'),
('Mercredi', '09:15', '10:15'),
('Mercredi', '10:30', '11:30'),
('Mercredi', '11:45', '12:45'),
('Mercredi', '14:00', '15:00'),
('Mercredi', '15:15', '16:15'),
('Mercredi', '16:30', '17:30'),
('Jeudi', '08:00', '09:00'),
('Jeudi', '09:15', '10:15'),
('Jeudi', '10:30', '11:30'),
('Jeudi', '11:45', '12:45'),
('Jeudi', '14:00', '15:00'),
('Jeudi', '15:15', '16:15'),
('Jeudi', '16:30', '17:30'),
('Vendredi', '08:00', '09:00'),
('Vendredi', '09:15', '10:15'),
('Vendredi', '10:30', '11:30'),
('Vendredi', '11:45', '12:45'),
('Vendredi', '14:00', '15:00'),
('Vendredi', '15:15', '16:15'),
('Vendredi', '16:30', '17:30');
```

### 3. Données de test (optionnel)

**Enseignants :**
```sql
INSERT INTO enseignants (nom, prenom, email, telephone, specialite, disponibilite) VALUES
('Dupont', 'Jean', 'jean.dupont@ecole.com', '0600000001', 'Mathématiques', 'Lundi,Mardi,Jeudi'),
('Martin', 'Sophie', 'sophie.martin@ecole.com', '0600000002', 'Français', 'Lundi,Mercredi,Jeudi'),
('Bernard', 'Paul', 'paul.bernard@ecole.com', '0600000003', 'Anglais', 'Mardi,Jeudi,Vendredi'),
('Thomas', 'Marie', 'marie.thomas@ecole.com', '0600000004', 'Sciences', 'Lundi,Mardi,Mercredi');
```

**Classes :**
```sql
INSERT INTO classes (nom, niveau, effectif) VALUES
('1ère A', '1ère année', 30),
('1ère B', '1ère année', 28),
('2ème A', '2ème année', 32),
('2ème B', '2ème année', 29);
```

**Matières :**
```sql
INSERT INTO matieres (nom, volume_horaire) VALUES
('Mathématiques', 3),
('Français', 3),
('Anglais', 2),
('Sciences', 3);
```

**Salles :**
```sql
INSERT INTO salles (nom, type, capacite) VALUES
('Salle 101', 'Classe', 35),
('Salle 102', 'Classe', 35),
('Salle 103', 'Classe', 35),
('Labo Chimie', 'Laboratoire', 25),
('Labo Informatique', 'Informatique', 30);
```

---

## Indices (Indexes)

Les indices améliorent les performances des requêtes fréquentes.

### Index primaires (automatiques)

```sql
-- Tous les PRIMARY KEY créent un index automatique
```

### Index recommandés

#### Index sur emails (recherche de doublons, connexion)

```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_enseignants_email ON enseignants(email);
```

#### Index sur clés étrangères (recherche et jointure)

```sql
CREATE INDEX idx_seances_classe_id ON seances(classe_id);
CREATE INDEX idx_seances_enseignant_id ON seances(enseignant_id);
CREATE INDEX idx_seances_matiere_id ON seances(matiere_id);
CREATE INDEX idx_seances_salle_id ON seances(salle_id);
CREATE INDEX idx_seances_creneau_id ON seances(creneau_id);
```

#### Index sur combinaisons (recherche de conflits)

```sql
CREATE UNIQUE INDEX idx_seances_classe_creneau ON seances(classe_id, creneau_id);
CREATE UNIQUE INDEX idx_seances_enseignant_creneau ON seances(enseignant_id, creneau_id);
CREATE UNIQUE INDEX idx_seances_salle_creneau ON seances(salle_id, creneau_id);
```

#### Index sur jours (recherche par plage horaire)

```sql
CREATE INDEX idx_creneaux_jour ON creneaux(jour);
```

---

## Contraintes et validations

### Contraintes CHECK

#### Table CRENEAUX

```sql
ALTER TABLE creneaux 
ADD CHECK (heure_debut < heure_fin);
```

#### Table CLASSES

```sql
ALTER TABLE classes 
ADD CHECK (effectif > 0);
```

#### Table MATIERES

```sql
ALTER TABLE matieres 
ADD CHECK (volume_horaire > 0);
```

#### Table SALLES

```sql
ALTER TABLE salles 
ADD CHECK (capacite > 0);
```

#### Table SEANCES

```sql
ALTER TABLE seances 
ADD CHECK (
    (SELECT effectif FROM classes WHERE id = classe_id) 
    <= 
    (SELECT capacite FROM salles WHERE id = salle_id)
);
```

### Contraintes NOT NULL

Toutes les colonnes FK et clés métier doivent être NOT NULL (voir structures individuelles).

### Contraintes UNIQUE

```sql
-- Email uniques
ALTER TABLE users ADD CONSTRAINT uk_users_email UNIQUE (email);
ALTER TABLE enseignants ADD CONSTRAINT uk_enseignants_email UNIQUE (email);

-- Pas de doublon pour affectations
ALTER TABLE seances ADD CONSTRAINT uk_seances_classe_creneau UNIQUE (classe_id, creneau_id);
ALTER TABLE seances ADD CONSTRAINT uk_seances_enseignant_creneau UNIQUE (enseignant_id, creneau_id);
ALTER TABLE seances ADD CONSTRAINT uk_seances_salle_creneau UNIQUE (salle_id, creneau_id);
```

### Contraintes Foreign Key

Voir la section "Table SEANCES" pour le détail.

---

## Checklist de vérification

Utilisez cette checklist pour valider que le fichier `ScriptSQL.sql` généré est complet et correct.

### Création des tables

- [ ] Table `users` créée avec colonnes id, nom, prenom, email, password, role
- [ ] Table `enseignants` créée avec colonnes id, nom, prenom, email, telephone, specialite, disponibilite
- [ ] Table `classes` créée avec colonnes id, nom, niveau, effectif
- [ ] Table `matieres` créée avec colonnes id, nom, volume_horaire
- [ ] Table `salles` créée avec colonnes id, nom, type, capacite
- [ ] Table `creneaux` créée avec colonnes id, jour, heure_debut, heure_fin
- [ ] Table `seances` créée avec colonnes id, classe_id, enseignant_id, matiere_id, salle_id, creneau_id

### Clés primaires

- [ ] PRIMARY KEY définie sur `users.id`
- [ ] PRIMARY KEY définie sur `enseignants.id`
- [ ] PRIMARY KEY définie sur `classes.id`
- [ ] PRIMARY KEY définie sur `matieres.id`
- [ ] PRIMARY KEY définie sur `salles.id`
- [ ] PRIMARY KEY définie sur `creneaux.id`
- [ ] PRIMARY KEY définie sur `seances.id`

### Clés étrangères

- [ ] FK `seances.classe_id` → `classes.id` (CASCADE)
- [ ] FK `seances.enseignant_id` → `enseignants.id` (RESTRICT)
- [ ] FK `seances.matiere_id` → `matieres.id` (RESTRICT)
- [ ] FK `seances.salle_id` → `salles.id` (RESTRICT)
- [ ] FK `seances.creneau_id` → `creneaux.id` (RESTRICT)

### Contraintes NOT NULL

- [ ] users.id NOT NULL
- [ ] users.nom NOT NULL
- [ ] users.prenom NOT NULL
- [ ] users.email NOT NULL
- [ ] users.password NOT NULL
- [ ] users.role NOT NULL
- [ ] enseignants.id NOT NULL
- [ ] enseignants.nom NOT NULL
- [ ] enseignants.prenom NOT NULL
- [ ] enseignants.email NOT NULL
- [ ] classes.id NOT NULL
- [ ] classes.nom NOT NULL
- [ ] classes.niveau NOT NULL
- [ ] classes.effectif NOT NULL
- [ ] matieres.id NOT NULL
- [ ] matieres.nom NOT NULL
- [ ] matieres.volume_horaire NOT NULL
- [ ] salles.id NOT NULL
- [ ] salles.nom NOT NULL
- [ ] salles.type NOT NULL
- [ ] salles.capacite NOT NULL
- [ ] creneaux.id NOT NULL
- [ ] creneaux.jour NOT NULL
- [ ] creneaux.heure_debut NOT NULL
- [ ] creneaux.heure_fin NOT NULL
- [ ] seances.id NOT NULL
- [ ] seances.classe_id NOT NULL
- [ ] seances.enseignant_id NOT NULL
- [ ] seances.matiere_id NOT NULL
- [ ] seances.salle_id NOT NULL
- [ ] seances.creneau_id NOT NULL

### Contraintes UNIQUE

- [ ] users.email UNIQUE
- [ ] enseignants.email UNIQUE
- [ ] seances(classe_id, creneau_id) UNIQUE
- [ ] seances(enseignant_id, creneau_id) UNIQUE
- [ ] seances(salle_id, creneau_id) UNIQUE

### Contraintes CHECK

- [ ] creneaux CHECK (heure_debut < heure_fin)
- [ ] classes CHECK (effectif > 0)
- [ ] matieres CHECK (volume_horaire > 0)
- [ ] salles CHECK (capacite > 0)

### Indices recommandés

- [ ] Index sur users.email
- [ ] Index sur enseignants.email
- [ ] Index sur seances.classe_id
- [ ] Index sur seances.enseignant_id
- [ ] Index sur seances.matiere_id
- [ ] Index sur seances.salle_id
- [ ] Index sur seances.creneau_id
- [ ] Index composite sur seances(classe_id, creneau_id)
- [ ] Index composite sur seances(enseignant_id, creneau_id)
- [ ] Index composite sur seances(salle_id, creneau_id)
- [ ] Index sur creneaux.jour

### Données d'initialisation

- [ ] Administrateur par défaut inséré (admin@ecole.com)
- [ ] Au moins 5 créneaux horaires insérés par jour
- [ ] Au moins 35 créneaux total (7 jours × 5 créneaux minimum)

### Validations

- [ ] Les colonnes de date (created_at, updated_at) existent et utilisent CURRENT_TIMESTAMP
- [ ] Pas de relation circulaire détectée
- [ ] Cascade DELETE appliqué uniquement à classe → seances
- [ ] RESTRICT appliqué à tous les autres FK pour éviter suppressions accidentelles
- [ ] La base de données n'autorise pas les valeurs NULL pour les identifiants de FK

### Intégrité référentielle

- [ ] Toute seance.classe_id existe dans classes.id
- [ ] Toute seance.enseignant_id existe dans enseignants.id
- [ ] Toute seance.matiere_id existe dans matieres.id
- [ ] Toute seance.salle_id existe dans salles.id
- [ ] Toute seance.creneau_id existe dans creneaux.id

### Documentation

- [ ] Tous les noms de tables et colonnes suivent la convention (snake_case)
- [ ] Commentaires SQL présents pour chaque table (COMMENT)
- [ ] Documentation des contraintes métier présente
- [ ] Diagrammes ER à jour

---

## Conclusion

Ce document fournit la spécification complète du schéma de base de données SQLite pour l'application de gestion des emplois du temps. La structure proposée est :

- **Normalisée** : 3ème forme normale (3NF)
- **Sécurisée** : Clés étrangères avec cascade appropriée
- **Performante** : Indices sur chemins de requêtes courants
- **Maintenable** : Convention de nommage cohérente et documentation claire

Le fichier `ScriptSQL.sql` doit implémenter exactement cette spécification pour assurer la compatibilité avec l'application Flask/SQLAlchemy.
