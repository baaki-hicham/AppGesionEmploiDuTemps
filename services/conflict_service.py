from models.seance import Seance


class ConflictDetector:
    @staticmethod
    def detect_conflicts():
        conflicts = {
            'enseignant': [],
            'salle': [],
            'classe': [],
            'creneau': []
        }

        seances = Seance.query.all()
        for seance in seances:
            matching = [other for other in seances if other.id != seance.id and other.creneau_id == seance.creneau_id]
            for other in matching:
                if other.enseignant_id == seance.enseignant_id:
                    conflicts['enseignant'].append((seance, other))
                if other.salle_id == seance.salle_id:
                    conflicts['salle'].append((seance, other))
                if other.classe_id == seance.classe_id:
                    conflicts['classe'].append((seance, other))
                if seance.creneau_id == other.creneau_id:
                    conflicts['creneau'].append((seance, other))
        return conflicts
