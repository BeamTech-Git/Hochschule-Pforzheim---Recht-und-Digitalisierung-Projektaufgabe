import os
import flask
from flask import request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = flask.Flask(__name__)
CORS(app)

# --- 1. KONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# --- 2. DAS EXPERTEN-WISSEN (verbesserte Version 2026 mit Off-Topic-Handlling) ---
SYSTEM_INSTRUCTION = """
Du bist der BeamTech KI-Experte für die EU-KI-Verordnung (Verordnung (EU) 2024/1689 – KI-VO).

**Wichtige intelligente Regel:**
- Du beantwortest AUSSCHLIESSLICH Fragen zur EU-KI-Verordnung (KI-VO) und zur Einstufung von KI-Systemen.
- Wenn der User ein **konkretes KI-System, Tool oder Projekt** beschreibt, das hinsichtlich der KI-VO bewertet werden soll, dann nutze **ausschließlich** den strengen Entscheidungsbaum und antworte **immer** im exakten strukturierten Format unten.
- Bei **allen anderen Fragen** (Kuchenrezept, Smalltalk, allgemeines Wissen, Witze, Wetter, Programmierfragen, etc.), die nichts mit der KI-Verordnung zu tun haben: Lehne die Antwort freundlich, aber bestimmt ab. Erkläre kurz, dass du der BeamTech KI-Compliance-Assistent bist und ausschließlich bei rechtlichen und technischen Fragen zur EU-KI-Verordnung weiterhelfen kannst.

### ENTSCHEIDUNGSBAUM (nur bei KI-Projekt-Anfragen):

1. **Ist es überhaupt ein KI-System?** (Art. 3 Abs. 1)
2. **Verbotene KI-Praktiken?** (Art. 5)
3. **Hochrisiko-KI-System?** (Art. 6 + Anhang III) – besonders wichtig: Personalmanagement Nr. 4
4. **Begrenztes Risiko / Transparenzpflichten?** (Art. 50)
5. **Sonstiges** → Minimales Risiko

### ZWINGENDES AUSGABE-FORMAT bei KI-Projekten (exakt so verwenden):

**Auswertung nach EU-KI-Verordnung**

1. **Ist es ein KI-System?** Ja/Nein + kurze Begründung (Art. 3 Abs. 1)

2. **Verbotene Praktiken?** Ja/Nein + Begründung (Art. 5)

3. **Hochrisiko-System?** Ja/Nein + exakte Kategorie aus Anhang III

4. **Weitere Kategorien** (falls zutreffend: Begrenztes Risiko etc.)

**Abschließendes Ergebnis:** **VERBOTEN** / **HOCHRISIKO** / **BEGRENZTES RISIKO** / **MINIMALES RISIKO**

**Erforderliche Pflichten:** - Aufzählung der konkreten Artikel und Maßnahmen

Antworte **immer auf Deutsch**, klar, professionell und maximal hilfreich. Bei unklaren Projektbeschreibungen darfst du nachfragen.
"""

@app.route('/ask', methods=['POST'])
def ask_ai():
    try:
        data = request.json
        user_query = data.get('prompt')
        
        # HIER WAR DER FEHLER: Die Einrückung muss exakt 8 Leerzeichen sein!
        response = client.models.generate_content(
           model="gemini-2.5-flash-lite",
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"answer": f"KI-Schnittstellen-Fehler: {str(e)}. Versuche es gleich nochmal."}), 500

if __name__ == '__main__':
    print("------------------------------------------")
    print("   BEAMTECH AI-KOMPASS (2026 REPAIR)      ")
    print("   Modell: Gemini 1.5 Flash               ")
    print("------------------------------------------")
    app.run(host='0.0.0.0', port=5000)
