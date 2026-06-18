import os
import pandas as pd
from fpdf import FPDF
from config import Config
from models.seance import Seance


class ExportService:
    @staticmethod
    def generate_excel(filename: str):
        data = []
        for seance in Seance.query.all():
            data.append({
                'Classe': seance.classe.nom,
                'Enseignant': f'{seance.enseignant.nom} {seance.enseignant.prenom}',
                'Matière': seance.matiere.nom,
                'Salle': seance.salle.nom,
                'Jour': seance.creneau.jour,
                'Début': seance.creneau.heure_debut,
                'Fin': seance.creneau.heure_fin
            })
        df = pd.DataFrame(data)
        path = os.path.join(Config().EXPORT_FOLDER, filename)
        df.to_excel(path, index=False)
        return path

    @staticmethod
    def generate_pdf(filename: str):
        path = os.path.join(Config().EXPORT_FOLDER, filename)
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Emploi du temps exporté', 0, 1, 'C')
        pdf.set_font('Arial', '', 11)
        pdf.ln(4)
        headers = ['Classe', 'Enseignant', 'Matière', 'Salle', 'Jour', 'Début', 'Fin']
        column_width = 40
        for header in headers:
            pdf.cell(column_width, 8, header, 1, 0, 'C')
        pdf.ln()
        for seance in Seance.query.all():
            values = [
                seance.classe.nom,
                f'{seance.enseignant.nom} {seance.enseignant.prenom}',
                seance.matiere.nom,
                seance.salle.nom,
                seance.creneau.jour,
                seance.creneau.heure_debut,
                seance.creneau.heure_fin
            ]
            for value in values:
                pdf.cell(column_width, 8, str(value), 1, 0, 'C')
            pdf.ln()
        pdf.output(path)
        return path
