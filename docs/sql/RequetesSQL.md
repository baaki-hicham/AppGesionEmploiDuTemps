# Documentation : Requêtes SQL - Opérations et Interrogations

**Projet :** Gestion intelligente des emplois du temps scolaires  
**Date :** 2026  
**Version :** 1.0

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Requêtes CRUD](#requêtes-crud)
3. [Requêtes de recherche](#requêtes-de-recherche)
4. [Requêtes avancées](#requêtes-avancées)
5. [Requêtes métier](#requêtes-métier)
6. [Requêtes de reporting et statistiques](#requêtes-de-reporting-et-statistiques)
7. [Requêtes de maintenance](#requêtes-de-maintenance)
8. [Checklist de requêtes](#checklist-de-requêtes)

---

## Vue d'ensemble

Cette documentation répertorie toutes les requêtes SQL nécessaires pour le fonctionnement de l'application. Les requêtes sont organisées par catégorie :

| Catégorie | Nombre | Objectif |
|-----------|--------|----------|
| CRUD | 28 | Créer, lire, modifier, supprimer les entités |
| Recherche | 12 | Trouver rapidement des entités |
| Avancées | 8 | Jointures, agrégations, sous-requêtes |
| Métier | 15 | Logique spécifique à l'application |
| Reporting | 10 | Statistiques et rapports |
| Maintenance | 5 | Nettoyage et audit |

---

## Requêtes CRUD

### 1. USER (USERS)

#### 1.1 CREATE - Insérer un nouvel utilisateur

```sql
INSERT INTO users (nom, prenom, email, password, role)
VALUES (?, ?, ?, ?, ?);
```

**Paramètres :**
- `nom` (str) : Nom de famille
- `prenom` (str) : Prénom
- `email` (str) : Email unique
- `password` (str) : Mot de passe hashé (bcrypt)
- `role` (str) : Rôle (Admin, Gestionnaire)

**Résultat attendu :** Ligne insérée avec auto-increment id

**Remarques :** Email doit être UNIQUE → vérifier existence avant

---

#### 1.2 READ - Récupérer tous les utilisateurs

```sql
SELECT id, nom, prenom, email, role, created_at, updated_at
FROM users
ORDER BY nom, prenom;
```

**Paramètres :** Aucun

**Résultat attendu :** Liste de tous les utilisateurs avec métadonnées

---

#### 1.3 READ - Récupérer un utilisateur par ID

```sql
SELECT id, nom, prenom, email, role, created_at, updated_at
FROM users
WHERE id = ?;
```

**Paramètres :**
- `id` (int) : Identifiant utilisateur

**Résultat attendu :** 1 ligne ou NULL

---

#### 1.4 READ - Récupérer un utilisateur par email (connexion)

```sql
SELECT id, nom, prenom, email, password, role, created_at, updated_at
FROM users
WHERE email = ?;
```

**Paramètres :**
- `email` (str) : Email de l'utilisateur

**Résultat attendu :** 1 ligne (unique index sur email) ou NULL

**Remarques :** Query critique pour authentification

---

#### 1.5 UPDATE - Modifier un utilisateur

```sql
UPDATE users
SET nom = ?, prenom = ?, email = ?, role = ?, updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```

**Paramètres :**
- `nom`, `prenom`, `email`, `role` : Nouvelles valeurs
- `id` : Identifiant à modifier

**Résultat attendu :** 1 ligne modifiée ou 0

---

#### 1.6 UPDATE - Changer le mot de passe

```sql
UPDATE users
SET password = ?, updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```

**Paramètres :**
- `password` (str) : Nouveau mot de passe hashé
- `id` (int) : Identifiant utilisateur

**Résultat attendu :** 1 ligne modifiée

---

#### 1.7 DELETE - Supprimer un utilisateur

```sql
DELETE FROM users
WHERE id = ?;
```

**Paramètres :**
- `id` (int) : Identifiant à supprimer

**Résultat attendu :** 1 ligne supprimée ou 0 (si N'existe pas)

---

### 2. ENSEIGNANTS

#### 2.1 CREATE - Insérer un enseignant

```sql
INSERT INTO enseignants (nom, prenom, email, telephone, specialite, disponibilite)
VALUES (?, ?, ?, ?, ?, ?);
```

**Paramètres :**
- `nom`, `prenom`, `email` : Identité
- `telephone` : Numéro (nullable)
- `specialite` : Domaine d'enseignement
- `disponibilite` : Format texte "Lundi,Mardi,Jeudi"

**Résultat attendu :** Ligne insérée avec auto-increment id

---

#### 2.2 READ - Lister tous les enseignants

```sql
SELECT id, nom, prenom, email, telephone, specialite, disponibilite, created_at
FROM enseignants
ORDER BY nom, prenom;
```

---

#### 2.3 READ - Récupérer un enseignant par ID

```sql
SELECT id, nom, prenom, email, telephone, specialite, disponibilite
FROM enseignants
WHERE id = ?;
```

---

#### 2.4 UPDATE - Modifier un enseignant

```sql
UPDATE enseignants
SET nom = ?, prenom = ?, email = ?, telephone = ?, specialite = ?, disponibilite = ?,
    updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```

---

#### 2.5 DELETE - Supprimer un enseignant

```sql
DELETE FROM enseignants
WHERE id = ?;
```

**Remarques :** Si des seances référencent cet enseignant, FK RESTRICT empêche la suppression

---

### 3. CLASSES

#### 3.1 CREATE - Insérer une classe

```sql
INSERT INTO classes (nom, niveau, effectif)
VALUES (?, ?, ?);
```

---

#### 3.2 READ - Lister toutes les classes

```sql
SELECT id, nom, niveau, effectif, created_at
FROM classes
ORDER BY niveau, nom;
```

---

#### 3.3 READ - Récupérer une classe par ID

```sql
SELECT id, nom, niveau, effectif
FROM classes
WHERE id = ?;
```

---

#### 3.4 UPDATE - Modifier une classe

```sql
UPDATE classes
SET nom = ?, niveau = ?, effectif = ?, updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```

---

#### 3.5 DELETE - Supprimer une classe

```sql
DELETE FROM classes
WHERE id = ?;
```

**Remarques :** CASCADE → supprime aussi les seances de cette classe

---

### 4. MATIERES

#### 4.1 CREATE - Insérer une matière

```sql
INSERT INTO matieres (nom, volume_horaire)
VALUES (?, ?);
```

---

#### 4.2 READ - Lister toutes les matières

```sql
SELECT id, nom, volume_horaire, created_at
FROM matieres
ORDER BY nom;
```

---

#### 4.3 READ - Récupérer une matière par ID

```sql
SELECT id, nom, volume_horaire
FROM matieres
WHERE id = ?;
```

---

#### 4.4 UPDATE - Modifier une matière

```sql
UPDATE matieres
SET nom = ?, volume_horaire = ?, updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```

---

#### 4.5 DELETE - Supprimer une matière

```sql
DELETE FROM matieres
WHERE id = ?;
```

---

### 5. SALLES

#### 5.1 CREATE - Insérer une salle

```sql
INSERT INTO salles (nom, type, capacite)
VALUES (?, ?, ?);
```

---

#### 5.2 READ - Lister toutes les salles

```sql
SELECT id, nom, type, capacite, created_at
FROM salles
ORDER BY nom;
```

---

#### 5.3 READ - Récupérer une salle par ID

```sql
SELECT id, nom, type, capacite
FROM salles
WHERE id = ?;
```

---

#### 5.4 UPDATE - Modifier une salle

```sql
UPDATE salles
SET nom = ?, type = ?, capacite = ?, updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```

---

#### 5.5 DELETE - Supprimer une salle

```sql
DELETE FROM salles
WHERE id = ?;
```

---

### 6. CRENEAUX

#### 6.1 CREATE - Insérer un créneau

```sql
INSERT INTO creneaux (jour, heure_debut, heure_fin)
VALUES (?, ?, ?);
```

**Paramètres :**
- `jour` : Jour semaine (Lundi, Mardi, etc.)
- `heure_debut`, `heure_fin` : Format HH:MM

---

#### 6.2 READ - Lister tous les créneaux

```sql
SELECT id, jour, heure_debut, heure_fin, created_at
FROM creneaux
ORDER BY CASE jour
    WHEN 'Lundi' THEN 1
    WHEN 'Mardi' THEN 2
    WHEN 'Mercredi' THEN 3
    WHEN 'Jeudi' THEN 4
    WHEN 'Vendredi' THEN 5
    ELSE 6
END, heure_debut;
```

---

#### 6.3 READ - Récupérer un créneau par ID

```sql
SELECT id, jour, heure_debut, heure_fin
FROM creneaux
WHERE id = ?;
```

---

#### 6.4 UPDATE - Modifier un créneau

```sql
UPDATE creneaux
SET jour = ?, heure_debut = ?, heure_fin = ?, updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```

---

#### 6.5 DELETE - Supprimer un créneau

```sql
DELETE FROM creneaux
WHERE id = ?;
```

---

### 7. SEANCES

#### 7.1 CREATE - Insérer une séance

```sql
INSERT INTO seances (classe_id, enseignant_id, matiere_id, salle_id, creneau_id)
VALUES (?, ?, ?, ?, ?);
```

**Paramètres :**
- `classe_id`, `enseignant_id`, `matiere_id`, `salle_id`, `creneau_id` : Identifiants FK

**Validations pré-INSERT :**
1. classe_id existe dans classes
2. enseignant_id existe dans enseignants
3. matiere_id existe dans matieres
4. salle_id existe dans salles
5. creneau_id existe dans creneaux
6. effectif(classe) ≤ capacite(salle)
7. Pas de seance déjà assignée : (classe_id, creneau_id) = unique
8. Pas de seance déjà assignée : (enseignant_id, creneau_id) = unique
9. Pas de seance déjà assignée : (salle_id, creneau_id) = unique

---

#### 7.2 READ - Lister toutes les séances

```sql
SELECT 
    s.id,
    c.nom as classe,
    e.nom as enseignant_nom, e.prenom as enseignant_prenom,
    m.nom as matiere,
    sa.nom as salle,
    cr.jour, cr.heure_debut, cr.heure_fin
FROM seances s
JOIN classes c ON s.classe_id = c.id
JOIN enseignants e ON s.enseignant_id = e.id
JOIN matieres m ON s.matiere_id = m.id
JOIN salles sa ON s.salle_id = sa.id
JOIN creneaux cr ON s.creneau_id = cr.id
ORDER BY cr.jour, cr.heure_debut, c.nom;
```

---

#### 7.3 READ - Récupérer une séance par ID

```sql
SELECT 
    s.id,
    s.classe_id, s.enseignant_id, s.matiere_id, s.salle_id, s.creneau_id
FROM seances s
WHERE s.id = ?;
```

---

#### 7.4 UPDATE - Modifier une séance

```sql
UPDATE seances
SET 
    classe_id = ?, 
    enseignant_id = ?, 
    matiere_id = ?, 
    salle_id = ?, 
    creneau_id = ?,
    updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```

**Remarques :** Les mêmes validations s'appliquent que pour CREATE

---

#### 7.5 DELETE - Supprimer une séance

```sql
DELETE FROM seances
WHERE id = ?;
```

---

## Requêtes de recherche

### 8. Recherche - Enseignants

#### 8.1 Rechercher un enseignant par nom partiel

```sql
SELECT id, nom, prenom, email, specialite
FROM enseignants
WHERE LOWER(nom) LIKE LOWER(?) OR LOWER(prenom) LIKE LOWER(?)
ORDER BY nom, prenom;
```

**Paramètres :**
- `?` : Pattern recherche (ex: "%Martin%")

---

#### 8.2 Lister les enseignants par spécialité

```sql
SELECT id, nom, prenom, email, specialite
FROM enseignants
WHERE LOWER(specialite) = LOWER(?)
ORDER BY nom, prenom;
```

---

#### 8.3 Lister les enseignants disponibles un jour donné

```sql
SELECT DISTINCT id, nom, prenom, specialite
FROM enseignants
WHERE disponibilite LIKE ? OR disponibilite IS NULL
ORDER BY nom, prenom;
```

**Paramètres :**
- `?` : Jour recherché (ex: "%Lundi%")

---

### 9. Recherche - Classes

#### 9.1 Rechercher une classe par nom partiel

```sql
SELECT id, nom, niveau, effectif
FROM classes
WHERE LOWER(nom) LIKE LOWER(?)
ORDER BY niveau, nom;
```

---

#### 9.2 Lister les classes par niveau

```sql
SELECT id, nom, niveau, effectif
FROM classes
WHERE LOWER(niveau) = LOWER(?)
ORDER BY nom;
```

---

### 10. Recherche - Salles

#### 10.1 Rechercher une salle par nom partiel

```sql
SELECT id, nom, type, capacite
FROM salles
WHERE LOWER(nom) LIKE LOWER(?)
ORDER BY nom;
```

---

#### 10.2 Lister les salles par type

```sql
SELECT id, nom, type, capacite
FROM salles
WHERE LOWER(type) = LOWER(?)
ORDER BY nom;
```

---

#### 10.3 Lister les salles avec capacité minimale

```sql
SELECT id, nom, type, capacite
FROM salles
WHERE capacite >= ?
ORDER BY capacite DESC;
```

---

### 11. Recherche - Matières

#### 11.1 Rechercher une matière par nom partiel

```sql
SELECT id, nom, volume_horaire
FROM matieres
WHERE LOWER(nom) LIKE LOWER(?)
ORDER BY nom;
```

---

### 12. Recherche - Emplois du temps

#### 12.1 Rechercher les séances d'une classe dans un créneau

```sql
SELECT 
    s.id,
    e.nom as enseignant_nom, e.prenom as enseignant_prenom,
    m.nom as matiere,
    sa.nom as salle,
    cr.jour, cr.heure_debut, cr.heure_fin
FROM seances s
JOIN enseignants e ON s.enseignant_id = e.id
JOIN matieres m ON s.matiere_id = m.id
JOIN salles sa ON s.salle_id = sa.id
JOIN creneaux cr ON s.creneau_id = cr.id
WHERE s.classe_id = ? AND cr.jour = ?
ORDER BY cr.heure_debut;
```

---

## Requêtes avancées

### 13. JOIN - Emploi du temps complet

#### 13.1 Emploi du temps par classe (vue complète)

```sql
SELECT 
    s.id as seance_id,
    c.id as classe_id,
    c.nom as classe_nom,
    c.niveau,
    c.effectif,
    e.id as enseignant_id,
    e.nom as enseignant_nom,
    e.prenom as enseignant_prenom,
    m.id as matiere_id,
    m.nom as matiere_nom,
    sa.id as salle_id,
    sa.nom as salle_nom,
    sa.type as salle_type,
    sa.capacite,
    cr.id as creneau_id,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin
FROM seances s
INNER JOIN classes c ON s.classe_id = c.id
INNER JOIN enseignants e ON s.enseignant_id = e.id
INNER JOIN matieres m ON s.matiere_id = m.id
INNER JOIN salles sa ON s.salle_id = sa.id
INNER JOIN creneaux cr ON s.creneau_id = cr.id
WHERE c.id = ?
ORDER BY cr.jour, cr.heure_debut;
```

**Paramètres :**
- `classe_id` : ID de la classe

**Résultat attendu :** Toutes les séances de cette classe avec détails complets

---

#### 13.2 Emploi du temps par enseignant

```sql
SELECT 
    s.id as seance_id,
    e.nom as enseignant_nom,
    e.prenom as enseignant_prenom,
    c.id as classe_id,
    c.nom as classe_nom,
    m.nom as matiere_nom,
    sa.nom as salle_nom,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin
FROM seances s
INNER JOIN classes c ON s.classe_id = c.id
INNER JOIN enseignants e ON s.enseignant_id = e.id
INNER JOIN matieres m ON s.matiere_id = m.id
INNER JOIN salles sa ON s.salle_id = sa.id
INNER JOIN creneaux cr ON s.creneau_id = cr.id
WHERE e.id = ?
ORDER BY cr.jour, cr.heure_debut;
```

---

### 14. GROUP BY - Agrégations

#### 14.1 Nombre de séances par classe

```sql
SELECT 
    c.id,
    c.nom as classe_nom,
    c.niveau,
    COUNT(s.id) as nombre_seances
FROM classes c
LEFT JOIN seances s ON c.id = s.classe_id
GROUP BY c.id, c.nom, c.niveau
ORDER BY nombre_seances DESC;
```

---

#### 14.2 Nombre de séances par enseignant

```sql
SELECT 
    e.id,
    e.nom as enseignant_nom,
    e.prenom as enseignant_prenom,
    e.specialite,
    COUNT(s.id) as nombre_seances
FROM enseignants e
LEFT JOIN seances s ON e.id = s.enseignant_id
GROUP BY e.id, e.nom, e.prenom, e.specialite
ORDER BY nombre_seances DESC;
```

---

#### 14.3 Utilisation des salles (nombre de seances par salle)

```sql
SELECT 
    sa.id,
    sa.nom as salle_nom,
    sa.type,
    sa.capacite,
    COUNT(s.id) as nombre_seances
FROM salles sa
LEFT JOIN seances s ON sa.id = s.salle_id
GROUP BY sa.id, sa.nom, sa.type, sa.capacite
ORDER BY nombre_seances DESC;
```

---

#### 14.4 Volume horaire couvert par classe et matière

```sql
SELECT 
    c.nom as classe_nom,
    m.nom as matiere_nom,
    m.volume_horaire as volume_requis,
    COUNT(s.id) as nombre_heures_assignees,
    m.volume_horaire - COUNT(s.id) as heures_manquantes
FROM classes c
CROSS JOIN matieres m
LEFT JOIN seances s ON c.id = s.classe_id AND m.id = s.matiere_id
GROUP BY c.id, c.nom, m.id, m.nom, m.volume_horaire
ORDER BY c.nom, heures_manquantes DESC;
```

---

### 15. HAVING - Filtrage post-agrégation

#### 15.1 Enseignants surchargés (> 10 séances)

```sql
SELECT 
    e.id,
    e.nom as enseignant_nom,
    e.prenom as enseignant_prenom,
    COUNT(s.id) as nombre_seances
FROM enseignants e
LEFT JOIN seances s ON e.id = s.enseignant_id
GROUP BY e.id, e.nom, e.prenom
HAVING COUNT(s.id) > 10
ORDER BY nombre_seances DESC;
```

---

#### 15.2 Salles sous-utilisées (< 2 seances)

```sql
SELECT 
    sa.id,
    sa.nom as salle_nom,
    sa.type,
    COUNT(s.id) as nombre_seances
FROM salles sa
LEFT JOIN seances s ON sa.id = s.salle_id
GROUP BY sa.id, sa.nom, sa.type
HAVING COUNT(s.id) < 2
ORDER BY nombre_seances;
```

---

### 16. ORDER BY - Tri multi-colonnes

#### 16.1 Séances triées par jour et heure

```sql
SELECT 
    c.nom as classe_nom,
    e.nom as enseignant_nom,
    m.nom as matiere_nom,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin
FROM seances s
JOIN classes c ON s.classe_id = c.id
JOIN enseignants e ON s.enseignant_id = e.id
JOIN matieres m ON s.matiere_id = m.id
JOIN creneaux cr ON s.creneau_id = cr.id
ORDER BY 
    CASE cr.jour
        WHEN 'Lundi' THEN 1
        WHEN 'Mardi' THEN 2
        WHEN 'Mercredi' THEN 3
        WHEN 'Jeudi' THEN 4
        WHEN 'Vendredi' THEN 5
        ELSE 6
    END,
    cr.heure_debut;
```

---

### 17. Sous-requêtes

#### 17.1 Trouver les salles avec capacité moyenne

```sql
SELECT 
    id,
    nom,
    type,
    capacite
FROM salles
WHERE capacite >= (
    SELECT AVG(capacite) FROM salles
)
ORDER BY capacite DESC;
```

---

#### 17.2 Enseignants qui ne sont pas assignés

```sql
SELECT 
    e.id,
    e.nom as enseignant_nom,
    e.prenom as enseignant_prenom,
    e.specialite
FROM enseignants e
WHERE e.id NOT IN (
    SELECT DISTINCT enseignant_id FROM seances
)
ORDER BY e.nom;
```

---

## Requêtes métier

### 18. Gestion des conflits

#### 18.1 Détecter les conflits enseignant (2 cours simultanés)

```sql
SELECT DISTINCT
    s1.id as seance1_id,
    s2.id as seance2_id,
    e.nom as enseignant_nom,
    e.prenom as enseignant_prenom,
    c1.nom as classe1,
    c2.nom as classe2,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin
FROM seances s1
JOIN seances s2 ON s1.enseignant_id = s2.enseignant_id 
                   AND s1.creneau_id = s2.creneau_id 
                   AND s1.id < s2.id
JOIN enseignants e ON s1.enseignant_id = e.id
JOIN classes c1 ON s1.classe_id = c1.id
JOIN classes c2 ON s2.classe_id = c2.id
JOIN creneaux cr ON s1.creneau_id = cr.id
ORDER BY e.nom, cr.jour, cr.heure_debut;
```

---

#### 18.2 Détecter les conflits salle (2 cours simultanés)

```sql
SELECT DISTINCT
    s1.id as seance1_id,
    s2.id as seance2_id,
    sa.nom as salle_nom,
    c1.nom as classe1,
    c2.nom as classe2,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin
FROM seances s1
JOIN seances s2 ON s1.salle_id = s2.salle_id 
                   AND s1.creneau_id = s2.creneau_id 
                   AND s1.id < s2.id
JOIN salles sa ON s1.salle_id = sa.id
JOIN classes c1 ON s1.classe_id = c1.id
JOIN classes c2 ON s2.classe_id = c2.id
JOIN creneaux cr ON s1.creneau_id = cr.id
ORDER BY sa.nom, cr.jour, cr.heure_debut;
```

---

#### 18.3 Détecter les conflits classe (2 cours simultanés)

```sql
SELECT DISTINCT
    s1.id as seance1_id,
    s2.id as seance2_id,
    c.nom as classe_nom,
    m1.nom as matiere1,
    m2.nom as matiere2,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin
FROM seances s1
JOIN seances s2 ON s1.classe_id = s2.classe_id 
                   AND s1.creneau_id = s2.creneau_id 
                   AND s1.id < s2.id
JOIN classes c ON s1.classe_id = c.id
JOIN matieres m1 ON s1.matiere_id = m1.id
JOIN matieres m2 ON s2.matiere_id = m2.id
JOIN creneaux cr ON s1.creneau_id = cr.id
ORDER BY c.nom, cr.jour, cr.heure_debut;
```

---

### 19. Disponibilités et vérifications

#### 19.1 Vérifier la capacité des salles (classe > salle)

```sql
SELECT 
    s.id as seance_id,
    c.nom as classe_nom,
    c.effectif,
    sa.nom as salle_nom,
    sa.capacite,
    c.effectif - sa.capacite as surplus_eleves
FROM seances s
JOIN classes c ON s.classe_id = c.id
JOIN salles sa ON s.salle_id = sa.id
WHERE c.effectif > sa.capacite
ORDER BY c.nom;
```

---

#### 19.2 Creneaux disponibles (non occupés)

```sql
SELECT 
    cr.id,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin,
    COUNT(s.id) as nombre_seances_utilisees,
    (SELECT COUNT(*) FROM salles) - COUNT(s.id) as salles_libres
FROM creneaux cr
LEFT JOIN seances s ON cr.id = s.creneau_id
GROUP BY cr.id, cr.jour, cr.heure_debut, cr.heure_fin
ORDER BY cr.jour, cr.heure_debut;
```

---

### 20. Analyses pédagogiques

#### 20.1 Enseignant - Distribution des heures par jour

```sql
SELECT 
    e.nom as enseignant_nom,
    e.prenom as enseignant_prenom,
    cr.jour,
    COUNT(s.id) as nombre_heures,
    GROUP_CONCAT(c.nom, ', ') as classes
FROM seances s
JOIN enseignants e ON s.enseignant_id = e.id
JOIN creneaux cr ON s.creneau_id = cr.id
JOIN classes c ON s.classe_id = c.id
GROUP BY e.id, e.nom, e.prenom, cr.jour
ORDER BY e.nom, 
         CASE cr.jour
             WHEN 'Lundi' THEN 1 WHEN 'Mardi' THEN 2 WHEN 'Mercredi' THEN 3
             WHEN 'Jeudi' THEN 4 WHEN 'Vendredi' THEN 5 ELSE 6
         END;
```

---

#### 20.2 Classe - Volume horaire par matière (pourcentage réalisé)

```sql
SELECT 
    c.nom as classe_nom,
    m.nom as matiere_nom,
    m.volume_horaire as heures_requises,
    COUNT(s.id) as heures_realisees,
    ROUND(100.0 * COUNT(s.id) / m.volume_horaire, 1) as pourcentage_realise
FROM classes c
CROSS JOIN matieres m
LEFT JOIN seances s ON c.id = s.classe_id AND m.id = s.matiere_id
GROUP BY c.id, c.nom, m.id, m.nom, m.volume_horaire
ORDER BY c.nom, pourcentage_realise DESC;
```

---

## Requêtes de reporting et statistiques

### 21. Statistiques globales

#### 21.1 Nombre total d'entités

```sql
SELECT 
    (SELECT COUNT(*) FROM users) as nombre_utilisateurs,
    (SELECT COUNT(*) FROM enseignants) as nombre_enseignants,
    (SELECT COUNT(*) FROM classes) as nombre_classes,
    (SELECT COUNT(*) FROM matieres) as nombre_matieres,
    (SELECT COUNT(*) FROM salles) as nombre_salles,
    (SELECT COUNT(*) FROM creneaux) as nombre_creneaux,
    (SELECT COUNT(*) FROM seances) as nombre_seances;
```

---

#### 21.2 Taux d'occupation global

```sql
SELECT 
    COUNT(DISTINCT s.creneau_id) as creneaux_occupes,
    (SELECT COUNT(*) FROM creneaux) as creneaux_total,
    ROUND(100.0 * COUNT(DISTINCT s.creneau_id) / (SELECT COUNT(*) FROM creneaux), 1) as taux_occupation_creneaux,
    COUNT(DISTINCT s.salle_id) as salles_occupees,
    (SELECT COUNT(*) FROM salles) as salles_total,
    ROUND(100.0 * COUNT(DISTINCT s.salle_id) / (SELECT COUNT(*) FROM salles), 1) as taux_occupation_salles
FROM seances s;
```

---

#### 21.3 Top 5 enseignants les plus actifs

```sql
SELECT 
    e.id,
    e.nom as enseignant_nom,
    e.prenom as enseignant_prenom,
    e.specialite,
    COUNT(s.id) as nombre_heures
FROM enseignants e
LEFT JOIN seances s ON e.id = s.enseignant_id
GROUP BY e.id, e.nom, e.prenom, e.specialite
ORDER BY nombre_heures DESC
LIMIT 5;
```

---

#### 21.4 Top 5 salles les plus utilisées

```sql
SELECT 
    sa.id,
    sa.nom as salle_nom,
    sa.type,
    sa.capacite,
    COUNT(s.id) as nombre_seances
FROM salles sa
LEFT JOIN seances s ON sa.id = s.salle_id
GROUP BY sa.id, sa.nom, sa.type, sa.capacite
ORDER BY nombre_seances DESC
LIMIT 5;
```

---

### 22. Rapports pour export

#### 22.1 Rapport d'emploi du temps pour impression

```sql
SELECT 
    c.nom as classe,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin,
    e.nom || ' ' || e.prenom as enseignant,
    m.nom as matiere,
    sa.nom as salle
FROM seances s
JOIN classes c ON s.classe_id = c.id
JOIN enseignants e ON s.enseignant_id = e.id
JOIN matieres m ON s.matiere_id = m.id
JOIN salles sa ON s.salle_id = sa.id
JOIN creneaux cr ON s.creneau_id = cr.id
WHERE c.id = ?
ORDER BY 
    CASE cr.jour
        WHEN 'Lundi' THEN 1 WHEN 'Mardi' THEN 2 WHEN 'Mercredi' THEN 3
        WHEN 'Jeudi' THEN 4 WHEN 'Vendredi' THEN 5 ELSE 6
    END,
    cr.heure_debut;
```

---

#### 22.2 Rapport d'emploi du temps enseignant

```sql
SELECT 
    e.nom || ' ' || e.prenom as enseignant,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin,
    c.nom as classe,
    m.nom as matiere,
    sa.nom as salle,
    c.effectif
FROM seances s
JOIN enseignants e ON s.enseignant_id = e.id
JOIN classes c ON s.classe_id = c.id
JOIN matieres m ON s.matiere_id = m.id
JOIN salles sa ON s.salle_id = sa.id
JOIN creneaux cr ON s.creneau_id = cr.id
WHERE e.id = ?
ORDER BY 
    CASE cr.jour
        WHEN 'Lundi' THEN 1 WHEN 'Mardi' THEN 2 WHEN 'Mercredi' THEN 3
        WHEN 'Jeudi' THEN 4 WHEN 'Vendredi' THEN 5 ELSE 6
    END,
    cr.heure_debut;
```

---

## Requêtes de maintenance

### 23. Audit et nettoyage

#### 23.1 Séances orphelines (FK orphelines)

```sql
SELECT s.id, s.classe_id, s.enseignant_id, s.matiere_id, s.salle_id, s.creneau_id
FROM seances s
WHERE s.classe_id NOT IN (SELECT id FROM classes)
   OR s.enseignant_id NOT IN (SELECT id FROM enseignants)
   OR s.matiere_id NOT IN (SELECT id FROM matieres)
   OR s.salle_id NOT IN (SELECT id FROM salles)
   OR s.creneau_id NOT IN (SELECT id FROM creneaux);
```

---

#### 23.2 Suppression des séances orphelines

```sql
DELETE FROM seances
WHERE classe_id NOT IN (SELECT id FROM classes)
   OR enseignant_id NOT IN (SELECT id FROM enseignants)
   OR matiere_id NOT IN (SELECT id FROM matieres)
   OR salle_id NOT IN (SELECT id FROM salles)
   OR creneau_id NOT IN (SELECT id FROM creneaux);
```

---

#### 23.3 Historique des modifications (audit)

```sql
SELECT 
    *,
    julianday(updated_at) - julianday(created_at) as jours_depuis_creation
FROM users
UNION ALL
SELECT 
    *,
    julianday(updated_at) - julianday(created_at) as jours_depuis_creation
FROM enseignants
UNION ALL
SELECT 
    *,
    julianday(updated_at) - julianday(created_at) as jours_depuis_creation
FROM classes
ORDER BY updated_at DESC
LIMIT 100;
```

---

## Checklist de requêtes

Utilisez cette checklist pour vérifier que toutes les requêtes SQL nécessaires sont implémentées.

### CRUD Utilisateurs

- [ ] Créer un utilisateur (INSERT)
- [ ] Lister tous les utilisateurs (SELECT)
- [ ] Récupérer 1 utilisateur par ID (SELECT WHERE id)
- [ ] Récupérer 1 utilisateur par email (SELECT WHERE email)
- [ ] Modifier un utilisateur (UPDATE)
- [ ] Changer le mot de passe (UPDATE password)
- [ ] Supprimer un utilisateur (DELETE)

### CRUD Enseignants

- [ ] Créer un enseignant (INSERT)
- [ ] Lister tous les enseignants (SELECT)
- [ ] Récupérer 1 enseignant par ID (SELECT WHERE id)
- [ ] Modifier un enseignant (UPDATE)
- [ ] Supprimer un enseignant (DELETE)

### CRUD Classes

- [ ] Créer une classe (INSERT)
- [ ] Lister toutes les classes (SELECT)
- [ ] Récupérer 1 classe par ID (SELECT WHERE id)
- [ ] Modifier une classe (UPDATE)
- [ ] Supprimer une classe (DELETE)

### CRUD Matières

- [ ] Créer une matière (INSERT)
- [ ] Lister toutes les matières (SELECT)
- [ ] Récupérer 1 matière par ID (SELECT WHERE id)
- [ ] Modifier une matière (UPDATE)
- [ ] Supprimer une matière (DELETE)

### CRUD Salles

- [ ] Créer une salle (INSERT)
- [ ] Lister toutes les salles (SELECT)
- [ ] Récupérer 1 salle par ID (SELECT WHERE id)
- [ ] Modifier une salle (UPDATE)
- [ ] Supprimer une salle (DELETE)

### CRUD Créneaux

- [ ] Créer un créneau (INSERT)
- [ ] Lister tous les créneaux (SELECT)
- [ ] Récupérer 1 créneau par ID (SELECT WHERE id)
- [ ] Modifier un créneau (UPDATE)
- [ ] Supprimer un créneau (DELETE)

### CRUD Séances

- [ ] Créer une séance (INSERT)
- [ ] Lister toutes les séances (SELECT avec JOINs)
- [ ] Récupérer 1 séance par ID (SELECT WHERE id)
- [ ] Modifier une séance (UPDATE)
- [ ] Supprimer une séance (DELETE)

### Recherche Enseignants

- [ ] Rechercher par nom partiel (LIKE)
- [ ] Filtrer par spécialité (WHERE specialite)
- [ ] Filtrer par disponibilité (LIKE jour)

### Recherche Classes

- [ ] Rechercher par nom partiel (LIKE)
- [ ] Filtrer par niveau (WHERE niveau)

### Recherche Salles

- [ ] Rechercher par nom partiel (LIKE)
- [ ] Filtrer par type (WHERE type)
- [ ] Filtrer par capacité minimale (WHERE capacite >=)

### Recherche Matières

- [ ] Rechercher par nom partiel (LIKE)

### Requêtes avancées JOIN

- [ ] Emploi du temps par classe avec tous détails (JOIN 5 tables)
- [ ] Emploi du temps par enseignant (JOIN 5 tables)

### Requêtes avancées GROUP BY

- [ ] Nombre de séances par classe (GROUP BY classe)
- [ ] Nombre de séances par enseignant (GROUP BY enseignant)
- [ ] Utilisation des salles (GROUP BY salle)
- [ ] Volume horaire par classe et matière (GROUP BY classe, matière)

### Requêtes avancées HAVING

- [ ] Enseignants surchargés (HAVING COUNT > 10)
- [ ] Salles sous-utilisées (HAVING COUNT < 2)

### Requêtes avancées ORDER BY

- [ ] Séances triées par jour et heure (ORDER BY jour, heure)

### Requêtes avancées sous-requêtes

- [ ] Salles avec capacité moyenne (sous-requête AVG)
- [ ] Enseignants non assignés (sous-requête NOT IN)

### Requêtes métier - Détection conflits

- [ ] Conflits enseignant (2 cours simultanés)
- [ ] Conflits salle (2 cours simultanés)
- [ ] Conflits classe (2 cours simultanés)

### Requêtes métier - Validations

- [ ] Vérifier capacité des salles
- [ ] Créneaux disponibles (non occupés)
- [ ] Enseignant non assigné

### Requêtes métier - Analyses

- [ ] Distribution heures enseignant par jour
- [ ] Volume horaire par matière pour classe (pourcentage)

### Statistiques

- [ ] Nombre total d'entités (COUNT *)
- [ ] Taux d'occupation global
- [ ] Top 5 enseignants actifs
- [ ] Top 5 salles utilisées

### Rapports

- [ ] Rapport emploi du temps par classe pour impression
- [ ] Rapport emploi du temps par enseignant

### Maintenance

- [ ] Détecter séances orphelines
- [ ] Supprimer séances orphelines
- [ ] Historique modifications (audit)

---

## Conclusion

Ce document énumère **40+ requêtes SQL** couvrant tous les aspects du projet :

- **CRUD** : Toutes les opérations de base de données
- **Recherche** : Filtrage et tri des données
- **Avancées** : Jointures, agrégations, sous-requêtes
- **Métier** : Logique spécifique à l'application (conflits, disponibilités, analyses)
- **Reporting** : Statistiques et rapports pour export
- **Maintenance** : Audit et nettoyage de base de données

Les requêtes sont optimisées pour SQLite et intègrent les paramètres liés aux cas d'usage de l'application.
