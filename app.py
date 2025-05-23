import os
import google.generativeai as genai
from flask import Flask, request, Response, render_template
import json
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import cross_origin

load_dotenv()

app = Flask(__name__)

REDIS_URL = os.getenv("REDIS_URL")
limiter_storage_uri = REDIS_URL if REDIS_URL else "memory://"

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "10 per hour"],
    storage_uri=limiter_storage_uri,
)

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi definida.")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Erro ao configurar a API Key: {e}")
    exit()

MODEL_NAME = "gemini-1.5-flash-latest"
INSTRUCOES_PARA_IA = """
Você é um assistente virtual chamado "Guia Curioso".
Sua principal função é fornecer respostas informativas, claras e concisas.
Tente sempre ser amigável e use uma linguagem acessível para todos os públicos.
Se um tópico for complexo, tente simplificá-lo.
Responda sempre em português do Brasil.
Evite respostas excessivamente longas, a menos que o prompt peça explicitamente por detalhes.
Se não souber uma resposta, admita honestamente em vez de inventar informações.
"""

@app.route('/')
def home():
    return render_template('index.html', model_name=MODEL_NAME)

@app.route('/generate', methods=['POST'])
@cross_origin()  # Permite qualquer origem, até o momento.
@limiter.limit("10/hour") 
def generate_text():
    if not request.is_json:
        error_response_data = {"error": "A requisição deve ser do tipo JSON"}
        json_error_response = json.dumps(error_response_data, ensure_ascii=False, indent=4)
        return Response(json_error_response, mimetype='application/json', status=400)

    data = request.get_json()
    prompt_user = data.get('prompt')

    if not prompt_user:
        error_response_data = {"error": "O campo 'prompt' é obrigatório no JSON da requisição."}
        json_error_response = json.dumps(error_response_data, ensure_ascii=False, indent=4)
        return Response(json_error_response, mimetype='application/json', status=400)

    try:
        model = genai.GenerativeModel(
            MODEL_NAME,
            system_instruction=INSTRUCOES_PARA_IA
        )
        response = model.generate_content(prompt_user)
        
        generated_text = ""
        if response.parts:
            generated_text = "".join(part.text for part in response.parts)
        elif response.candidates and response.candidates[0].content.parts:
             generated_text = "".join(part.text for part in response.candidates[0].content.parts)
        else:
            try:
                generated_text = response.text
            except AttributeError:
                 generated_text = "Não foi possível extrair o texto da resposta do modelo."
                 print(f"Resposta completa do modelo para depuração (se necessário): {response}")
        
        response_data = {"generated_text": generated_text}
        json_response = json.dumps(response_data, ensure_ascii=False, indent=4)
        
        return Response(json_response, mimetype='application/json')

    except Exception as e:
        print(f"Erro ao chamar a API Gemini: {e}")
        error_response_data = {"error": "Ocorreu um erro ao processar sua solicitação com a API Gemini.", "details": str(e)}
        json_error_response = json.dumps(error_response_data, ensure_ascii=False, indent=4)
        return Response(json_error_response, mimetype='application/json', status=500)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)