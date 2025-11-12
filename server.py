from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Directory to store submissions
SUBMISSIONS_DIR = 'submissions'
if not os.path.exists(SUBMISSIONS_DIR):
    os.makedirs(SUBMISSIONS_DIR)

@app.route('/')
def index():
    return open('index.html', 'r', encoding='utf-8').read()

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('name') or not data.get('email'):
            return jsonify({'success': False, 'message': 'Nome e email são obrigatórios'}), 400
        
        # Create submission object
        submission = {
            'timestamp': datetime.now().isoformat(),
            'name': data.get('name'),
            'email': data.get('email'),
            'service': data.get('service', 'Não especificado'),
            'message': data.get('message', '')
        }
        
        # Save to JSON file
        filename = f"{SUBMISSIONS_DIR}/submission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(submission, f, ensure_ascii=False, indent=2)
        
        # Log to console
        print(f"\n✅ Nova submissão recebida:")
        print(f"   Nome: {submission['name']}")
        print(f"   Email: {submission['email']}")
        print(f"   Serviço: {submission['service']}")
        print(f"   Mensagem: {submission['message']}")
        print(f"   Salvo em: {filename}\n")
        
        return jsonify({
            'success': True, 
            'message': 'Sua solicitação foi recebida com sucesso! Entraremos em contato em breve.'
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao processar formulário: {str(e)}")
        return jsonify({'success': False, 'message': 'Erro ao processar sua solicitação'}), 500

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """Endpoint para visualizar todas as submissões (apenas para admin)"""
    try:
        submissions = []
        if os.path.exists(SUBMISSIONS_DIR):
            for filename in sorted(os.listdir(SUBMISSIONS_DIR), reverse=True):
                if filename.endswith('.json'):
                    with open(os.path.join(SUBMISSIONS_DIR, filename), 'r', encoding='utf-8') as f:
                        submissions.append(json.load(f))
        return jsonify(submissions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Servidor iniciado em http://localhost:5000")
    print("📧 Formulários serão salvos em: submissions/")
    app.run(debug=True, port=5000, host='0.0.0.0')
