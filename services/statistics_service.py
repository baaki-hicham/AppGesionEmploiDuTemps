from models.enseignant import Enseignant
from models.classe import Classe
from models.matiere import Matiere
from models.salle import Salle
from models.seance import Seance
from models.creneau import Creneau


class StatisticsService:
    @staticmethod
    def count_enseignants():
        return Enseignant.query.count()

    @staticmethod
    def count_classes():
        return Classe.query.count()

    @staticmethod
    def count_matieres():
        return Matiere.query.count()

    @staticmethod
    def count_salles():
        return Salle.query.count()

    @staticmethod
    def count_seances():
        return Seance.query.count()

    @staticmethod
    def occupation_salles():
        results = []
        for salle in Salle.query.all():
            results.append({'salle': salle.nom, 'occupation': len(salle.seances)})
        return results

    @staticmethod
    def occupation_enseignants():
        results = []
        for enseignant in Enseignant.query.all():
            results.append({'enseignant': f'{enseignant.nom} {enseignant.prenom}', 'cours': len(enseignant.seances)})
        return results

    @staticmethod
    def volume_horaire_par_matiere():
        return [{'matiere': matiere.nom, 'volume': matiere.volume_horaire} for matiere in Matiere.query.all()]
