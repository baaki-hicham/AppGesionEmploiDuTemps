import sys
import os
import re

# Ensure project root is on sys.path so `import app` works when running this script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()

with app.test_client() as client:
    # ensure a logged-in session (routes use session['user_id'])
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    # GET the create page
    r = client.get('/enseignants/create')
    print('GET /enseignants/create status:', r.status_code)
    html = r.get_data(as_text=True)
    m = re.search(r'name="csrf_token" value="([^"]+)"', html)
    if not m:
        print('CSRF token not found in form HTML')
        raise SystemExit(2)
    token = m.group(1)
    print('Found csrf token:', token[:8] + '...')

    # POST the form with token
    data = {
        'nom': 'Test',
        'prenom': 'User',
        'email': 'testuser@example.com',
        'telephone': '000',
        'specialite': 'Test',
        'disponibilite': 'Lundi',
        'csrf_token': token
    }
    p = client.post('/enseignants/create', data=data, follow_redirects=False)
    print('POST /enseignants/create status:', p.status_code)
    if p.status_code in (302, 303):
        print('POST redirect location:', p.headers.get('Location'))
        print('CSRF POST succeeded')
        raise SystemExit(0)
    else:
        print('POST response body:', p.get_data(as_text=True)[:500])
        print('CSRF POST failed')
        raise SystemExit(1)
