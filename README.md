![](https://private-user-images.githubusercontent.com/72875404/447570526-f8dfe875-fe24-4f74-99b4-bd7f4bed17c1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDgyNjM4ODAsIm5iZiI6MTc0ODI2MzU4MCwicGF0aCI6Ii83Mjg3NTQwNC80NDc1NzA1MjYtZjhkZmU4NzUtZmUyNC00Zjc0LTk5YjQtYmQ3ZjRiZWQxN2MxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA1MjYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNTI2VDEyNDYyMFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWNkMTIwOTkyNWEzZTY0ZTQwZmZkNWQwMmY0MWU2YTVlZjkwMDllZmY0ZDY4ZTZmYTgyM2NhZmQ1YWYxZjhjYmMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.Ew97yg6Ov9CE3LOcK_7uQuoXL04kloLs-a9Q4UIe2dQ)

E ai, Dev! 👋

Preparado para integrar a API **Jetrom** e dar um upgrade no seu projeto com o poder do Gemini? Este tutorial vai te guiar passo a passo, de forma clara e direta. Vamos lá!

---

### **Visão Geral da API**

A API foi criada para ser simples e intuitiva. Ela possui um único endpoint principal que recebe suas solicitações para gerar texto.

* **Formato:** REST
* **Comunicação:** JSON

---

### **Endpoint: `/generate`**

Este é o coração da API. É aqui que a mágica acontece.

* **URL:** `https://ask-jetrom.vercel.app/generate`
* **Método HTTP:** `POST`
* **Descrição:** Envia um texto (prompt) e recebe uma resposta gerada pela inteligência artificial.

**Ponto Importante:** A API gerencia a chave de acesso do Google (Gemini) no servidor. Isso significa que **você não precisa enviar nenhuma chave de autenticação** na sua requisição. Mais simples, impossível!

---

### **Como Fazer a Requisição**

Para se comunicar com a API, você precisa montar uma requisição `POST` com a estrutura correta.

#### **Cabeçalhos (Headers)**

Sua requisição deve incluir o seguinte cabeçalho para indicar que você está enviando dados em JSON:

```
Content-Type: application/json
```

#### **Corpo da Requisição (Body)**

O corpo da requisição deve ser um objeto JSON contendo a chave `prompt`:

```json
{
  "prompt": "Sua pergunta ou instrução para a IA vai aqui."
}
```

* `prompt` (string): Este campo é **obrigatório** e contém o texto que você quer que a IA processe.

---

### **O que Esperar da Resposta**

#### **✅ Sucesso**

Se tudo correr bem (Status `200 OK`), a resposta será um objeto JSON com o texto gerado:

```json
{
  "generated_text": "A resposta da IA para o seu prompt aparecerá aqui."
}
```

#### **❌ Erros**

A API é configurada para retornar mensagens de erro claras:

* **`400 Bad Request`**: Acontece se você esquecer o campo `prompt` ou enviar um formato diferente de JSON.
* **`429 Too Many Requests`**: A API tem um limite de requisições (10 por hora) para cada IP. Se você exceder, receberá este erro.
* **`500 Internal Server Error`**: Indica um problema do lado do servidor, como uma falha na comunicação com a IA.

---

### **💻 Mão na Massa: Exemplos de Código**

Veja como é fácil integrar a API em diferentes ambientes. Não se esqueça de substituir `SUA_URL_BASE/generate` pela URL real da sua API.

#### **cURL (Terminal)**

Perfeito para fazer um teste rápido na linha de comando.

```bash
curl -X POST "https://ask-jetrom.vercel.app/generate" \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Explique o que é uma API de forma simples e divertida."
}'
```

#### **Python (para Backend)**

Ideal para integrar em seus serviços ou scripts Python. Você precisará da biblioteca `requests` (`pip install requests`).

```python
import requests
import json

api_url = "https://ask-jetrom.vercel.app/generate"
headers = {
    'Content-Type': 'application/json'
}
payload = {
    'prompt': 'Crie uma pequena história sobre um robô que sonhava em ser chef de cozinha.'
}

try:
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()

    result = response.json()
    print(result['generated_text'])

except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro: {e}")
    if response:
        print(f"Resposta do servidor: {response.text}")

```

#### **JavaScript (para Frontend)**

Use a `Workspace API` para consumir a API diretamente de uma página web.

```javascript
async function callGuiaCuriosoAPI(promptText) {
    const apiUrl = 'https://ask-jetrom.vercel.app/generate';

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: promptText
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erro na API: ${errorData.error || response.statusText}`);
        }

        const data = await response.json();
        console.log(data.generated_text);
        // Exemplo: document.getElementById('result').innerText = data.generated_text;

    } catch (error) {
        console.error("Falha ao buscar dados:", error);
    }
}

callGuiaCuriosoAPI("Qual a distância entre a Terra e a Lua em quilômetros?");
```

E é isso! Agora você tem tudo o que precisa para começar a construir coisas incríveis com a API **Jetrom**. Boas implementações! ✨
