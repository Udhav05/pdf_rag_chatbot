import requests

def query_ollama(prompt, model="llama2"):
    url = "http://localhost:11434/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 200
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"
