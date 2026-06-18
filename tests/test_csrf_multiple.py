import sys
import os
import re

# Ensure project root is on sys.path so `import app` works when running this script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()

endpoints = [
    {
        'blueprint': 'classes',
        'create_url': '/classes/create',
        'create_data': {'nom': 'TestClass', 'niveau': '1', 'effectif': '30'},
        'model': ('models.classe', 'Classe'),
        'id_field': 'id'
    },
    {
        'blueprint': 'matieres',
        'create_url': '/matieres/create',
        'create_data': {'nom': 'TestMatiere', 'volume_horaire': '20'},
        'model': ('models.matiere', 'Matiere'),
        'id_field': 'id'
    },
    {
        'blueprint': 'salles',
        'create_url': '/salles/create',
        'create_data': {'nom': 'SalleTest', 'type': 'TP', 'capacite': '40'},
        'model': ('models.salle', 'Salle'),
        'id_field': 'id'
    },
    {
        'blueprint': 'creneaux',
        'create_url': '/creneaux/create',
        'create_data': {'jour': 'Lundi', 'heure_debut': '08:00', 'heure_fin': '09:00'},
        'model': ('models.creneau', 'Creneau'),
        'id_field': 'id'
    }
]


def run():
    failures = []
    with app.test_client() as client:
        # ensure logged-in session
        with client.session_transaction() as sess:
            sess['user_id'] = 1

        for ep in endpoints:
            print('\nTesting', ep['create_url'])
            r = client.get(ep['create_url'])
            print(' GET status', r.status_code)
            html = r.get_data(as_text=True)
            m = re.search(r'name="csrf_token" value="([^"]+)"', html)
            if not m:
                print('  ✗ CSRF token not found on', ep['create_url'])
                failures.append(ep['create_url'])
                continue
            token = m.group(1)
            data = dict(ep['create_data'])
            data['csrf_token'] = token
            p = client.post(ep['create_url'], data=data, follow_redirects=False)
            print(' POST status', p.status_code)
            if p.status_code not in (302, 303):
                print('  ✗ Create POST failed for', ep['create_url'])
                failures.append(ep['create_url'])
                continue

            # import model to find the created record id
            module_name, class_name = ep['model']
            try:
                mod = __import__(module_name, fromlist=[class_name])
                Model = getattr(mod, class_name)
            except Exception as e:
                print('  ! Could not import model', module_name, class_name, e)
                failures.append(ep['create_url'])
                continue

            # query last created
            with app.app_context():
                from extensions import db
                last = db.session.query(Model).order_by(getattr(Model, ep['id_field']).desc()).first()
                if not last:
                    print('  ! No record found after create for', ep['create_url'])
                    failures.append(ep['create_url'])
                    continue
                last_id = getattr(last, ep['id_field'])
                print('  Created id:', last_id)

            # attempt delete using blueprint delete route
            delete_path = f"/{ep['blueprint']}/delete/{last_id}"
            # reuse token (same session)
            p2 = client.post(delete_path, data={'csrf_token': token}, follow_redirects=False)
            print(' DELETE', delete_path, 'status', p2.status_code)
            if p2.status_code not in (302, 303):
                print('  ✗ Delete failed for', delete_path)
                failures.append(delete_path)
                continue
            print('  ✓ create/delete succeeded for', ep['blueprint'])

    if failures:
        print('\nFailures:', failures)
        raise SystemExit(1)
    print('\nAll tests passed')


if __name__ == '__main__':
    run()
