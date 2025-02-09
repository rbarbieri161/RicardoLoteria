from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import json
import os

app = Flask(__name__)

LOTERIAS = {
    'megasena': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena',
    'lotofacil': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil',
    'quina': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/quina',
    'timemania': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/timemania',
    'duplasena': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/duplasena',
    'diadesorte': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/diadesorte'
}

def get_lottery_results():
    results = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for lottery_id, url in LOTERIAS.items():
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                results[lottery_id] = response.json()
        except:
            continue
    
    return results

@app.route('/')
def index():
    results = get_lottery_results()
    return render_template('index.html', results=results)

@app.route('/atualizar')
def update():
    try:
        results = get_lottery_results()
        return jsonify({'success': True, 'message': 'Resultados atualizados!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))