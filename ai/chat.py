# ai.py
import json
import re
import requests
from openai import OpenAI
import config

history = {}

def generate_text(prompt, chat_id):
    client = OpenAI(api_key=config.gpt_key)

    # Construir prompt del sistema
    system_prompt = {
        "role": "system",
        "content": config.ai_prompt_system + "\n\nCONTEXTO:\n" + prompt
    }

    # Inicializar historial si es necesario
    if chat_id not in history:
        history[chat_id] = []

    # Limitar historial
    max_pairs = 4
    if len(history[chat_id]) > max_pairs * 2:
        history[chat_id] = history[chat_id][-(max_pairs * 2):]

    # Construir mensaje inicial
    messages = [system_prompt] + history[chat_id] + [{"role": "user", "content": prompt}]

    print(f"--- Enviado a OpenAI (Chat ID: {chat_id}) ---")
    print(json.dumps(messages, indent=2, ensure_ascii=False))
    print("--------------------------------------------")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.1,
            max_tokens=1000
        )

        reply = response.choices[0].message.content
        answer = reply

        # Intentar extraer JSON clínico
        json_pattern = r"\{[\s\S]*?\}"
        match = re.search(json_pattern, reply)

        params = {}
        predict_result = None
        final_response = reply

        if match:
            try:
                params = json.loads(match.group())
                print("🎯 JSON clínico detectado:", params)
                predict_result = hacer_prediccion_si_hay_datos(params)

                # Generar nuevo mensaje a OpenAI con la predicción
                if predict_result:
                    interpret_prompt = f"""Con base en estos datos agronómicos:
{json.dumps(params, indent=2)}
y este resultado de recomendación:
{json.dumps(predict_result, indent=2)}

genera una explicación amigable para el agrónomo. Usa un tono científico positivo y claro."""
                    
                    final_response = generate_final_output(interpret_prompt, chat_id)

            except json.JSONDecodeError as e:
                print("❌ JSON inválido:", e)

        # Guardar historial
        history[chat_id].append({"role": "user", "content": prompt})
        history[chat_id].append({"role": "assistant", "content": answer})

        return {
            "response": final_response,
            "params": params,
            "predict": predict_result
        }

    except Exception as e:
        print(f"❌ Error en llamada a OpenAI: {e}")
        return {
            "response": "Lo siento, ocurrió un error al procesar tu solicitud.",
            "params": {},
            "predict": None
        }


def hacer_prediccion_si_hay_datos(params):
    campos = ["Tipo de Cultivo", "Tipo de Suelo", " Nivel de Fosforo", "Nivel de Potasio", "Nivel de Calcio", "MaxHR"]
    if not all(k in params for k in campos):
        return None

    url = "https://ai-app-a441e0d147d0.herokuapp.com/predict"
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error en la predicción:", e)
        return None


def generate_final_output(text_prompt, chat_id):
    client = OpenAI(api_key=config.gpt_key)

    messages = [
        {"role": "system", "content": "Eres un agente experto en nutrición vegetal agronomica, tu objetivo es entregar recomendaciones de fertilizantes primarios y secundarios para diversos cultivos como maiz, tomate, paltas, limones, etc.."},
        {"role": "user", "content": text_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error generando salida final:", e)
        return "La predicción se realizó, pero no se pudo generar una explicación textual."
