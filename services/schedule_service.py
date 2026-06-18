from collections import defaultdict
from extensions import db
from models.enseignant import Enseignant
from models.classe import Classe
from models.matiere import Matiere
from models.salle import Salle
from models.creneau import Creneau
from models.seance import Seance


class ScheduleGenerator:
    """Schedule generator avec gestion de conflits, disponibilités et volume horaire."""

    def __init__(self):
        self.classes = Classe.query.all()
        self.enseignants = Enseignant.query.all()
        self.matieres = Matiere.query.all()
        self.salles = Salle.query.all()
        self.creneaux = Creneau.query.all()
        self.assignments = []

    def generate(self):
        self.clear_seances()
        available_creneaux = self._build_available_slots()
        self._assign_courses(available_creneaux)
        db.session.commit()
        return self.assignments

    def clear_seances(self):
        Seance.query.delete()
        db.session.commit()

    def _build_available_slots(self):
        slot_map = defaultdict(list)
        for creneau in self.creneaux:
            for enseignant in self.enseignants:
                if enseignant.disponibilite and creneau.jour in enseignant.disponibilite:
                    slot_map[creneau.id].append(enseignant.id)
                elif not enseignant.disponibilite:
                    slot_map[creneau.id].append(enseignant.id)
        return slot_map

    def _assign_courses(self, available_creneaux):
        self.creneaux.sort(key=lambda item: item.jour)
        self.matieres.sort(key=lambda item: -item.volume_horaire)
        for classe in self.classes:
            needed_hours = {matiere.id: matiere.volume_horaire for matiere in self.matieres}
            for creneau in self.creneaux:
                if all(hours <= 0 for hours in needed_hours.values()):
                    break
                if self._has_classe_conflict(classe.id, creneau.id):
                    continue
                for matiere in self.matieres:
                    if needed_hours[matiere.id] <= 0:
                        continue
                    enseignant_id = self._find_teacher_for_subject(matiere.id, creneau.id, available_creneaux)
                    salle_id = self._find_room(classe, creneau)
                    if enseignant_id and salle_id:
                        seance = Seance(
                            classe_id=classe.id,
                            enseignant_id=enseignant_id,
                            matiere_id=matiere.id,
                            salle_id=salle_id,
                            creneau_id=creneau.id
                        )
                        db.session.add(seance)
                        db.session.flush()
                        self.assignments.append(seance)
                        needed_hours[matiere.id] -= 1
                        break

    def _find_teacher_for_subject(self, matiere_id, creneau_id, available_creneaux):
        for enseignant in self.enseignants:
            if enseignant.id not in available_creneaux.get(creneau_id, []):
                continue
            if self._has_teacher_conflict(enseignant.id, creneau_id):
                continue
            return enseignant.id
        return None

    def _find_room(self, classe, creneau):
        for salle in self.salles:
            if salle.capacite >= classe.effectif and not self._has_room_conflict(salle.id, creneau.id):
                return salle.id
        return None

    def _has_teacher_conflict(self, enseignant_id, creneau_id):
        return Seance.query.filter_by(enseignant_id=enseignant_id, creneau_id=creneau_id).first() is not None

    def _has_room_conflict(self, salle_id, creneau_id):
        return Seance.query.filter_by(salle_id=salle_id, creneau_id=creneau_id).first() is not None

    def _has_classe_conflict(self, classe_id, creneau_id):
        return Seance.query.filter_by(classe_id=classe_id, creneau_id=creneau_id).first() is not None
