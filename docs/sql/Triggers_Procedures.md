# Documentation : Triggers et Procédures - Automatisation et Intégrité

**Projet :** Gestion intelligente des emplois du temps scolaires  
**Date :** 2026  
**Version :** 1.0

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture des contrôles et automatisations](#architecture-des-contrôles-et-automatisations)
3. [Triggers SQL](#triggers-sql)
4. [Vues SQL (Views)](#vues-sql-views)
5. [Procédures et fonctions](#procédures-et-fonctions)
6. [Limitations SQLite et solutions](#limitations-sqlite-et-solutions)
7. [Implémentation au niveau application](#implémentation-au-niveau-application)
8. [Checklist de vérification](#checklist-de-vérification)

---

## Vue d'ensemble

**SQLite et les stored procedures :**

SQLite ne supporte **PAS** les procédures stockées ou les fonctions utilisateur (UDF) de manière native. Cependant, SQLite supporte les **triggers** pour automatiser certains contrôles d'intégrité.

Cette documentation détaille :

1. **Triggers SQL** : Automatisations possibles en SQLite
2. **Vues SQL** : Simplification des requêtes complexes
3. **Solutions au niveau application** : Logique métier implémentée en Python/Flask
4. **Migrations et intégrité** : Approches pour garantir la cohérence des données

### Règles métier à appliquer

| Règle | Niveau | Implémentation |
|-------|--------|-----------------|
| Pas 2 cours enseignant au même créneau | Trigger + App | UNIQUE constraint + Python |
| Pas 2 cours salle au même créneau | Trigger + App | UNIQUE constraint + Python |
| Pas 2 cours classe au même créneau | Trigger + App | UNIQUE constraint + Python |
| Capacité salle ≥ effectif classe | App | CHECK constraint + Python |
| Volume horaire par classe couvert | App | Python (ScheduleGenerator) |
| Enseignant disponible ce jour | App | Python (ScheduleGenerator) |
| Pas doublon email | Trigger | UNIQUE constraint |
| Audit des modifications | Trigger + App | TRIGGER + Application logs |

---

## Architecture des contrôles et automatisations

### Niveaux de contrôle

```
┌────────────────────────────────────────────────────────────┐
│              NIVEAUX D'INTÉGRITÉ ET SÉCURITÉ               │
├────────────────────────────────────────────────────────────┤
│ 1. DATABASE CONSTRAINTS (SQLite)                           │
│    ├─ PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL          │
│    ├─ CHECK constraints                                    │
│    └─ UNIQUE indexes                                       │
├────────────────────────────────────────────────────────────┤
│ 2. TRIGGERS (SQLite)                                       │
│    ├─ BEFORE INSERT/UPDATE/DELETE                         │
│    ├─ AFTER INSERT/UPDATE/DELETE                          │
│    └─ Actions : RAISE, LOG, UPDATE other rows             │
├────────────────────────────────────────────────────────────┤
│ 3. APPLICATION LOGIC (Python/Flask)                        │
│    ├─ Validation métier complexe                          │
│    ├─ ScheduleGenerator                                   │
│    ├─ ConflictDetector                                    │
│    └─ Business Services                                   │
├────────────────────────────────────────────────────────────┤
│ 4. VIEWS (SQLite)                                          │
│    ├─ Vues simplifiées pour requêtes communes            │
│    └─ Vues de contrôle d'intégrité                       │
└────────────────────────────────────────────────────────────┘
```

---

## Triggers SQL

SQLite supporte les triggers avec la syntaxe :

```sql
CREATE TRIGGER [IF NOT EXISTS] trigger_name
[BEFORE | AFTER | INSTEAD OF] [INSERT | UPDATE | DELETE] ON table_name
[FOR EACH ROW]
BEGIN
    -- Actions SQL
END;
```

### 1. Trigger : Validation d'email unique (USER)

**Objectif :** Empêcher l'insertion/modification d'un email déjà existant  
**Événement :** BEFORE INSERT, BEFORE UPDATE  
**Table :** users

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_users_email_unique_before_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM users WHERE email = NEW.email) > 0
        THEN RAISE(ABORT, 'Email must be unique')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_users_email_unique_before_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM users WHERE email = NEW.email AND id != NEW.id) > 0
        THEN RAISE(ABORT, 'Email must be unique')
    END;
END;
```

**Effet :** Lève une exception ABORT si l'email existe déjà

---

### 2. Trigger : Validation d'email unique (ENSEIGNANT)

**Objectif :** Idem que trigger 1 pour table enseignants  
**Événement :** BEFORE INSERT, BEFORE UPDATE  
**Table :** enseignants

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_enseignants_email_unique_before_insert
BEFORE INSERT ON enseignants
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM enseignants WHERE email = NEW.email) > 0
        THEN RAISE(ABORT, 'Email must be unique')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_enseignants_email_unique_before_update
BEFORE UPDATE ON enseignants
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM enseignants WHERE email = NEW.email AND id != NEW.id) > 0
        THEN RAISE(ABORT, 'Email must be unique')
    END;
END;
```

---

### 3. Trigger : Validation contrainte CHECK (CLASSES)

**Objectif :** Empêcher un effectif ≤ 0  
**Événement :** BEFORE INSERT, BEFORE UPDATE  
**Table :** classes

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_classes_effectif_positive_before_insert
BEFORE INSERT ON classes
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.effectif <= 0
        THEN RAISE(ABORT, 'Effectif must be > 0')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_classes_effectif_positive_before_update
BEFORE UPDATE ON classes
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.effectif <= 0
        THEN RAISE(ABORT, 'Effectif must be > 0')
    END;
END;
```

---

### 4. Trigger : Validation contrainte CHECK (MATIERES)

**Objectif :** Empêcher un volume horaire ≤ 0  
**Événement :** BEFORE INSERT, BEFORE UPDATE  
**Table :** matieres

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_matieres_volume_positive_before_insert
BEFORE INSERT ON matieres
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.volume_horaire <= 0
        THEN RAISE(ABORT, 'Volume horaire must be > 0')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_matieres_volume_positive_before_update
BEFORE UPDATE ON matieres
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.volume_horaire <= 0
        THEN RAISE(ABORT, 'Volume horaire must be > 0')
    END;
END;
```

---

### 5. Trigger : Validation contrainte CHECK (SALLES)

**Objectif :** Empêcher une capacité ≤ 0  
**Événement :** BEFORE INSERT, BEFORE UPDATE  
**Table :** salles

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_salles_capacite_positive_before_insert
BEFORE INSERT ON salles
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.capacite <= 0
        THEN RAISE(ABORT, 'Capacite must be > 0')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_salles_capacite_positive_before_update
BEFORE UPDATE ON salles
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.capacite <= 0
        THEN RAISE(ABORT, 'Capacite must be > 0')
    END;
END;
```

---

### 6. Trigger : Validation horaires créneaux

**Objectif :** Empêcher heure_debut ≥ heure_fin  
**Événement :** BEFORE INSERT, BEFORE UPDATE  
**Table :** creneaux

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_creneaux_heures_valides_before_insert
BEFORE INSERT ON creneaux
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.heure_debut >= NEW.heure_fin
        THEN RAISE(ABORT, 'heure_debut must be < heure_fin')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_creneaux_heures_valides_before_update
BEFORE UPDATE ON creneaux
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.heure_debut >= NEW.heure_fin
        THEN RAISE(ABORT, 'heure_debut must be < heure_fin')
    END;
END;
```

---

### 7. Trigger : Validation capacité salle vs effectif classe

**Objectif :** Empêcher une séance avec classe trop grande pour la salle  
**Événement :** BEFORE INSERT, BEFORE UPDATE  
**Table :** seances

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_seances_capacite_before_insert
BEFORE INSERT ON seances
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT effectif FROM classes WHERE id = NEW.classe_id) >
             (SELECT capacite FROM salles WHERE id = NEW.salle_id)
        THEN RAISE(ABORT, 'Classe trop grande pour cette salle')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_seances_capacite_before_update
BEFORE UPDATE ON seances
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT effectif FROM classes WHERE id = NEW.classe_id) >
             (SELECT capacite FROM salles WHERE id = NEW.salle_id)
        THEN RAISE(ABORT, 'Classe trop grande pour cette salle')
    END;
END;
```

---

### 8. Trigger : Détection conflit enseignant

**Objectif :** Empêcher un enseignant d'avoir 2 séances au même créneau  
**Événement :** BEFORE INSERT  
**Table :** seances

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_seances_conflit_enseignant_before_insert
BEFORE INSERT ON seances
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM seances 
              WHERE enseignant_id = NEW.enseignant_id 
              AND creneau_id = NEW.creneau_id) > 0
        THEN RAISE(ABORT, 'Enseignant a deja une seance ce creneau')
    END;
END;
```

---

### 9. Trigger : Détection conflit salle

**Objectif :** Empêcher qu'une salle soit occupée par 2 séances au même créneau  
**Événement :** BEFORE INSERT  
**Table :** seances

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_seances_conflit_salle_before_insert
BEFORE INSERT ON seances
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM seances 
              WHERE salle_id = NEW.salle_id 
              AND creneau_id = NEW.creneau_id) > 0
        THEN RAISE(ABORT, 'Salle est deja occupee ce creneau')
    END;
END;
```

---

### 10. Trigger : Détection conflit classe

**Objectif :** Empêcher qu'une classe ait 2 séances au même créneau  
**Événement :** BEFORE INSERT  
**Table :** seances

#### Code SQL

```sql
CREATE TRIGGER IF NOT EXISTS trg_seances_conflit_classe_before_insert
BEFORE INSERT ON seances
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM seances 
              WHERE classe_id = NEW.classe_id 
              AND creneau_id = NEW.creneau_id) > 0
        THEN RAISE(ABORT, 'Classe a deja une seance ce creneau')
    END;
END;
```

---

### 11. Trigger : Audit - Journalisation insertion seance

**Objectif :** Enregistrer chaque insertion de séance pour audit  
**Événement :** AFTER INSERT  
**Table :** seances

#### Création de la table d'audit

```sql
CREATE TABLE IF NOT EXISTS audit_seances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action VARCHAR(50) NOT NULL,
    seance_id INTEGER,
    classe_id INTEGER,
    enseignant_id INTEGER,
    matiere_id INTEGER,
    salle_id INTEGER,
    creneau_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_email VARCHAR(150)
);
```

#### Code du trigger

```sql
CREATE TRIGGER IF NOT EXISTS trg_seances_audit_after_insert
AFTER INSERT ON seances
FOR EACH ROW
BEGIN
    INSERT INTO audit_seances (action, seance_id, classe_id, enseignant_id, matiere_id, salle_id, creneau_id)
    VALUES ('INSERT', NEW.id, NEW.classe_id, NEW.enseignant_id, NEW.matiere_id, NEW.salle_id, NEW.creneau_id);
END;
```

---

### 12. Trigger : Audit - Journalisation suppression seance

**Objectif :** Enregistrer chaque suppression de séance pour audit  
**Événement :** AFTER DELETE  
**Table :** seances

#### Code du trigger

```sql
CREATE TRIGGER IF NOT EXISTS trg_seances_audit_after_delete
AFTER DELETE ON seances
FOR EACH ROW
BEGIN
    INSERT INTO audit_seances (action, seance_id, classe_id, enseignant_id, matiere_id, salle_id, creneau_id)
    VALUES ('DELETE', OLD.id, OLD.classe_id, OLD.enseignant_id, OLD.matiere_id, OLD.salle_id, OLD.creneau_id);
END;
```

---

### 13. Trigger : Mise à jour timestamp (updated_at)

**Objectif :** Mettre à jour automatiquement la colonne updated_at lors d'une modification  
**Événement :** BEFORE UPDATE  
**Table :** users (et autres)

#### Code du trigger

```sql
CREATE TRIGGER IF NOT EXISTS trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_enseignants_updated_at
BEFORE UPDATE ON enseignants
FOR EACH ROW
BEGIN
    UPDATE enseignants SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_classes_updated_at
BEFORE UPDATE ON classes
FOR EACH ROW
BEGIN
    UPDATE classes SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_matieres_updated_at
BEFORE UPDATE ON matieres
FOR EACH ROW
BEGIN
    UPDATE matieres SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_salles_updated_at
BEFORE UPDATE ON salles
FOR EACH ROW
BEGIN
    UPDATE salles SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_creneaux_updated_at
BEFORE UPDATE ON creneaux
FOR EACH ROW
BEGIN
    UPDATE creneaux SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_seances_updated_at
BEFORE UPDATE ON seances
FOR EACH ROW
BEGIN
    UPDATE seances SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

---

## Vues SQL (Views)

Les vues simplifient les requêtes complexes et permettent de créer des abstractions utiles.

### Vie 1 : Emploi du temps complet

**Objectif :** Afficher l'emploi du temps avec tous les détails

```sql
CREATE VIEW IF NOT EXISTS vw_emploi_du_temps AS
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
    sa.type,
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
INNER JOIN creneaux cr ON s.creneau_id = cr.id;
```

**Utilisation :**

```sql
SELECT * FROM vw_emploi_du_temps WHERE classe_nom = '1ère A';
```

---

### Vue 2 : Détection de conflits

**Objectif :** Afficher tous les conflits détectés

```sql
CREATE VIEW IF NOT EXISTS vw_conflits AS
SELECT 
    s1.id as seance1_id,
    s2.id as seance2_id,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin,
    'Enseignant' as type_conflit,
    e.nom || ' ' || e.prenom as element_en_conflit
FROM seances s1
JOIN seances s2 ON s1.enseignant_id = s2.enseignant_id 
                   AND s1.creneau_id = s2.creneau_id 
                   AND s1.id < s2.id
JOIN enseignants e ON s1.enseignant_id = e.id
JOIN creneaux cr ON s1.creneau_id = cr.id

UNION ALL

SELECT 
    s1.id as seance1_id,
    s2.id as seance2_id,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin,
    'Salle' as type_conflit,
    sa.nom as element_en_conflit
FROM seances s1
JOIN seances s2 ON s1.salle_id = s2.salle_id 
                   AND s1.creneau_id = s2.creneau_id 
                   AND s1.id < s2.id
JOIN salles sa ON s1.salle_id = sa.id
JOIN creneaux cr ON s1.creneau_id = cr.id

UNION ALL

SELECT 
    s1.id as seance1_id,
    s2.id as seance2_id,
    cr.jour,
    cr.heure_debut,
    cr.heure_fin,
    'Classe' as type_conflit,
    c.nom as element_en_conflit
FROM seances s1
JOIN seances s2 ON s1.classe_id = s2.classe_id 
                   AND s1.creneau_id = s2.creneau_id 
                   AND s1.id < s2.id
JOIN classes c ON s1.classe_id = c.id
JOIN creneaux cr ON s1.creneau_id = cr.id;
```

**Utilisation :**

```sql
SELECT * FROM vw_conflits ORDER BY type_conflit, jour, heure_debut;
```

---

### Vue 3 : Occupations et statistiques

**Objectif :** Afficher les taux d'occupation

```sql
CREATE VIEW IF NOT EXISTS vw_occupation_salles AS
SELECT 
    sa.id,
    sa.nom as salle_nom,
    sa.type,
    sa.capacite,
    COUNT(s.id) as nombre_seances,
    ROUND(100.0 * COUNT(s.id) / (SELECT COUNT(*) FROM creneaux), 1) as taux_occupation_pct
FROM salles sa
LEFT JOIN seances s ON sa.id = s.salle_id
GROUP BY sa.id, sa.nom, sa.type, sa.capacite;
```

**Utilisation :**

```sql
SELECT * FROM vw_occupation_salles WHERE taux_occupation_pct > 50;
```

---

### Vue 4 : Volume horaire couvert

**Objectif :** Afficher le pourcentage de volume horaire couvert

```sql
CREATE VIEW IF NOT EXISTS vw_volume_horaire_couvert AS
SELECT 
    c.nom as classe_nom,
    m.nom as matiere_nom,
    m.volume_horaire as heures_requises,
    COUNT(s.id) as heures_assignees,
    ROUND(100.0 * COUNT(s.id) / m.volume_horaire, 1) as pourcentage_couvert,
    m.volume_horaire - COUNT(s.id) as heures_manquantes
FROM classes c
CROSS JOIN matieres m
LEFT JOIN seances s ON c.id = s.classe_id AND m.id = s.matiere_id
GROUP BY c.id, c.nom, m.id, m.nom, m.volume_horaire;
```

**Utilisation :**

```sql
SELECT * FROM vw_volume_horaire_couvert 
WHERE pourcentage_couvert < 100 
ORDER BY heures_manquantes DESC;
```

---

## Procédures et fonctions

SQLite ne supporte **pas** les procédures stockées ni les fonctions UDF standard. Cependant, on peut simuler certains comportements.

### Approche 1 : Transactions pour opérations composites

**Objectif :** Générer et valider un emploi du temps en une seule transaction

```sql
BEGIN TRANSACTION;
-- Suppression des séances précédentes
DELETE FROM seances;

-- Insertion de nouvelles séances (via application)
INSERT INTO seances (...) VALUES (...);
INSERT INTO seances (...) VALUES (...);
...

-- Vérification : si un conflit est détecté, ROLLBACK
SELECT CASE 
    WHEN (SELECT COUNT(*) FROM vw_conflits) > 0
    THEN RAISE(ABORT, 'Conflits détectés: génération annulée')
END;

COMMIT;
```

---

### Approche 2 : Fonction SQL personnalisée (JavaScript pour SQLite Web)

Pour SQLite Web ou d'autres interfaces supportant les fonctions UDF :

```javascript
// Pseudo-code pour fonction personnalisée
function check_capacity(classe_id, salle_id) {
    const classe = query('SELECT effectif FROM classes WHERE id = ?', classe_id)[0];
    const salle = query('SELECT capacite FROM salles WHERE id = ?', salle_id)[0];
    return classe.effectif <= salle.capacite;
}

// Utilisation en SQL (si support UDF)
// SELECT * FROM seances WHERE check_capacity(classe_id, salle_id) = 1;
```

---

## Limitations SQLite et solutions

### Limitations

| Limitation | SQLite | Impact |
|-----------|--------|--------|
| Procédures stockées | ❌ Non supporté | Logique complexe → Python |
| Fonctions UDF | ❌ Limité (scripts seulement) | Calculs → Python |
| Triggers INSTEAD OF | ⚠️ Partiel | Vues non updatable |
| Contraintes d'assertion | ❌ Non supporté | Vérifications → Python/Triggers |
| Niveaux de isolation | ⚠️ READ_UNCOMMITTED, SERIALIZABLE | Concurrence → Application |
| Transactions imbriquées | ⚠️ Savepoints seulement | Gestion → Application |

---

### Solutions au niveau application

Puisque SQLite a des limitations, la logique métier complexe est implémentée en Python.

#### 1. ScheduleGenerator (Génération d'emploi du temps)

**Fichier :** [services/schedule_service.py](../../services/schedule_service.py)

**Responsabilités :**
- Allocation intelligente des créneaux
- Respect des disponibilités enseignant
- Respect des volumes horaires
- Vérification de capacité des salles

**Pseudocode :**

```python
def generate(self):
    self.clear_seances()
    available_creneaux = self._build_available_slots()
    self._assign_courses(available_creneaux)
    db.session.commit()
```

---

#### 2. ConflictDetector (Détection des conflits)

**Fichier :** [services/conflict_service.py](../../services/conflict_service.py)

**Responsabilités :**
- Détection conflits enseignant
- Détection conflits salle
- Détection conflits classe
- Détection conflits créneau

**Pseudocode :**

```python
def detect_conflicts(self):
    conflicts = {
        'enseignant': [],
        'salle': [],
        'classe': [],
        'creneau': []
    }
    # ... logique de détection
    return conflicts
```

---

#### 3. AuthService (Sécurité)

**Fichier :** [services/auth_service.py](../../services/auth_service.py)

**Responsabilités :**
- Hachage sécurisé des mots de passe (bcrypt)
- Vérification d'authentification

```python
@staticmethod
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
```

---

#### 4. Validations au niveau contrôleur

**Fichier :** [controllers/entity_controller.py](../../controllers/entity_controller.py)

```python
class EntityController:
    def create(self, **kwargs):
        # Validation métier avant insertion
        entity = self.entity_model(**kwargs)
        entity.save()
        return entity
```

---

## Implémentation au niveau application

### Intégration des triggers et vues

1. **Au démarrage de l'application :** Tous les triggers et vues sont créés
2. **Lors d'un INSERT/UPDATE/DELETE :** Les triggers SQLite s'exécutent
3. **Lors d'une opération métier :** La logique Python s'ajoute

### Exemple d'intégration

```python
# app.py
with app.app_context():
    db.create_all()
    init_triggers(app)  # Crée tous les triggers
    init_views(app)     # Crée toutes les vues
    init_default_admin(app)
```

### Script d'initialisation des triggers

**Fichier :** `scripts/init_db_triggers.sql`

```sql
-- Script complet d'initialisation
-- À exécuter après db.create_all()

-- 1. Triggers de validation
-- ... (tous les triggers documentés ci-dessus)

-- 2. Vues
-- ... (toutes les vues documentées ci-dessus)

-- 3. Audit table
CREATE TABLE IF NOT EXISTS audit_seances (...);

-- 4. Index
CREATE INDEX ...;
```

---

## Checklist de vérification

Utilisez cette checklist pour vérifier que tous les triggers, vues et protections sont en place.

### Triggers de validation

- [ ] Trigger email unique (users) - INSERT
- [ ] Trigger email unique (users) - UPDATE
- [ ] Trigger email unique (enseignants) - INSERT
- [ ] Trigger email unique (enseignants) - UPDATE
- [ ] Trigger effectif positif (classes) - INSERT
- [ ] Trigger effectif positif (classes) - UPDATE
- [ ] Trigger volume horaire positif (matieres) - INSERT
- [ ] Trigger volume horaire positif (matieres) - UPDATE
- [ ] Trigger capacité positive (salles) - INSERT
- [ ] Trigger capacité positive (salles) - UPDATE
- [ ] Trigger horaires valides (creneaux) - INSERT
- [ ] Trigger horaires valides (creneaux) - UPDATE

### Triggers de contraintes métier

- [ ] Trigger capacité salle vs classe (seances) - INSERT
- [ ] Trigger capacité salle vs classe (seances) - UPDATE
- [ ] Trigger conflit enseignant (seances) - INSERT
- [ ] Trigger conflit salle (seances) - INSERT
- [ ] Trigger conflit classe (seances) - INSERT

### Triggers d'audit

- [ ] Trigger audit insertion (seances) - AFTER INSERT
- [ ] Trigger audit suppression (seances) - AFTER DELETE
- [ ] Trigger updated_at (users)
- [ ] Trigger updated_at (enseignants)
- [ ] Trigger updated_at (classes)
- [ ] Trigger updated_at (matieres)
- [ ] Trigger updated_at (salles)
- [ ] Trigger updated_at (creneaux)
- [ ] Trigger updated_at (seances)

### Vues

- [ ] Vue emploi du temps complet (vw_emploi_du_temps)
- [ ] Vue détection conflits (vw_conflits)
- [ ] Vue occupation salles (vw_occupation_salles)
- [ ] Vue volume horaire couvert (vw_volume_horaire_couvert)

### Contraintes et indexes

- [ ] Constraint PRIMARY KEY sur toutes les tables
- [ ] Constraint FOREIGN KEY sur seances
- [ ] Constraint UNIQUE sur emails
- [ ] Constraint UNIQUE sur (classe_id, creneau_id)
- [ ] Constraint UNIQUE sur (enseignant_id, creneau_id)
- [ ] Constraint UNIQUE sur (salle_id, creneau_id)
- [ ] Index sur FK de seances
- [ ] Index sur emails
- [ ] Index composite sur seances(classe_id, creneau_id)
- [ ] Index composite sur seances(enseignant_id, creneau_id)
- [ ] Index composite sur seances(salle_id, creneau_id)

### Logique application

- [ ] ScheduleGenerator.generate() respecte les disponibilités
- [ ] ScheduleGenerator respecte volume horaire
- [ ] ScheduleGenerator vérifie capacité salles
- [ ] ConflictDetector.detect_conflicts() détecte conflits enseignant
- [ ] ConflictDetector détecte conflits salle
- [ ] ConflictDetector détecte conflits classe
- [ ] AuthService.hash_password() utilise bcrypt
- [ ] EntityController valide avant insertion

### Tests

- [ ] Test : Insertion email doublon → ABORT
- [ ] Test : Insertion effectif ≤ 0 → ABORT
- [ ] Test : Insertion heure_debut ≥ heure_fin → ABORT
- [ ] Test : Insertion classe > salle → ABORT
- [ ] Test : Insertion avec conflit enseignant → ABORT
- [ ] Test : Insertion avec conflit salle → ABORT
- [ ] Test : Insertion avec conflit classe → ABORT
- [ ] Test : Génération emploi du temps réussit
- [ ] Test : Détection conflits fonctionne
- [ ] Test : Vues retournent données correctes
- [ ] Test : Audit enregistre modifications
- [ ] Test : Authentification vérifie bcrypt

### Documentation

- [ ] Tous les triggers documentés (objectif, événement, tables)
- [ ] Toutes les vues documentées (objectif, colonnes)
- [ ] Limitations SQLite documentées
- [ ] Solutions application documentées
- [ ] Exemples d'utilisation présents
- [ ] Gestion des erreurs expliquée

---

## Conclusion

Cette documentation couvre :

1. **Triggers SQL** : 13 triggers pour validation, contraintes, audit
2. **Vues SQL** : 4 vues pour simplifier les requêtes complexes
3. **Limitations SQLite** : Pas de procédures → logique en Python
4. **Solutions application** : ScheduleGenerator, ConflictDetector, AuthService
5. **Intégrité des données** : Contraintes multiniveaux (SQL + App)

L'approche hybride (SQL + Python) offre :
- ✅ Performance (validation rapide au niveau DB)
- ✅ Flexibilité (logique complexe en Python)
- ✅ Maintenabilité (séparation des responsabilités)
- ✅ Audit (triggers d'enregistrement)
- ✅ Sécurité (contraintes et validations)

Le fichier `Triggers_Procedures.sql` doit contenir tous les triggers et vues documentés ici pour assurer la cohérence et la robustesse de la base de données.
