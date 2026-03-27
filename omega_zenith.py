import os
import json
import time
import base64
import requests
import re
import random
import threading
from datetime import datetime
from ppadb.client import Client as AdbClient

# ==========================================================
# OMEGA v11.0 - LE ZÉNITH (ÉDITION ULTIME - SINGLE FILE)
# ==========================================================
# IA d'Automatisation de Niveau Divin - Optimisé pour Gemini 3
# ==========================================================

API_KEYS = [
    "AIzaSyDwEQ79fx8VC4-eqohcVnEU_XP3GkR-9nM",
    "AIzaSyDKGmiJ1A5get3bTq3kv6GaAWKI99ijlTI",
    "AIzaSyAjj9_74wHXor9KxsNVJ9PEtcvrgyh8gX8",
    "AIzaSyA66ysmvWZeTxYALtZy98k2GhgfcOsuOdQ"
]

MODEL_ID = "gemini-2.5-flash"
ADB_TARGET = "192.168.1.67:33231"
MEMORY_FILE = "omega_memory.json"
UI_MAP_FILE = "omega_ui_map.json"

class OmegaZenith:
    def __init__(self):
        # Configuration du Noyau
        self.key_index = 0
        self.retry_count = 0 # Compteur Anti-Boucle 429
        self.model_id = MODEL_ID
        self.adb_target = ADB_TARGET
        self.memory_file = MEMORY_FILE
        self.ui_map_file = UI_MAP_FILE
        
        # Initialisation des Matrices
        self.memory = self.load_json(self.memory_file, {"aliases": {}, "history": []})
        self.ui_map = self.load_json(self.ui_map_file, {})
        self.device = self.connect_adb()
        self.is_running = False
        self.last_action_time = 0

    def load_json(self, filepath, default):
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f: return json.load(f)
            except: pass
        return default

    def save_json(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def connect_adb(self):
        """ Connexion au corps physique via ADB """
        os.system(f"adb connect {self.adb_target} > /dev/null 2>&1")
        client = AdbClient(host="127.0.0.1", port=5037)
        try:
            devices = client.devices()
            if devices:
                print(f"✅ OMEGA : Connexion neuronale établie ({self.adb_target})")
                return devices[0]
        except Exception as e:
            print(f"❌ OMEGA : Échec de connexion ADB : {e}")
        return None

    def get_eyesight(self):
        """ Capture d'écran haute performance (Vision d'OMEGA) """
        if not self.device: return None
        try:
            # Capture directe en mémoire pour une latence minimale
            result = self.device.screencap()
            return base64.b64encode(result).decode('utf-8')
        except:
            return None

    def get_current_app(self):
        """ Analyse du processus actif """
        if not self.device: return "unknown"
        try:
            out = self.device.shell("dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'")
            match = re.search(r'([a-zA-Z0-9\.]+)/', out)
            return match.group(1) if match else "unknown"
        except: return "unknown"

    def call_ai(self, prompt, is_gaming=False):
        """ Appel au noyau cognitif Gemini (Vision + Raisonnement) """
        # BOUCLIER ANTI-429 (CIRCUIT BREAKER)
        if self.retry_count >= len(API_KEYS):
            print("\n⏳ [ANTI-BAN] Toutes les clés sont épuisées. Refroidissement de 30 secondes...")
            time.sleep(30)
            self.retry_count = 0
            return self.call_ai(prompt, is_gaming)

        b64_image = self.get_eyesight()
        current_app = self.get_current_app()
        app_memory = self.ui_map.get(current_app, {})
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:generateContent?key={API_KEYS[self.key_index]}"
        
        system_instruction = f"""
        Tu es OMEGA v11.0, l'IA d'automatisation de niveau divin.
        APPLICATION ACTUELLE : {current_app}
        MÉMOIRE LOCALE : {json.dumps(app_memory)}

        RÈGLES ABSOLUES :
        1. NE TAPE JAMAIS DE COMMANDES TECHNIQUES SUR LE CLAVIER VIRTUEL. Utilise `system_shell`.
        2. Sois concis. Analyse l'image et décide de l'action la plus efficace.
        3. Si le Maître demande de jouer, utilise la boucle autonome.

        ACTIONS DISPONIBLES :
        - tap: {{"x": int, "y": int}} -> Clic précis (jitter ±2px auto).
        - swipe: {{"x1": int, "y1": int, "x2": int, "y2": int, "duration": int}} -> Glissement.
        - type: {{"text": str}} -> Saisie de texte humain.
        - wait: {{"seconds": int}} -> Pause stratégique.
        - system_shell: {{"cmd": str}} -> Commande ADB directe (ex: 'am start ...').
        - learn_ui: {{"buttons": {{"nom": {{"x": int, "y": int}}}}}} -> Mémorisation de l'interface.

        RÉPONDS STRICTEMENT AU FORMAT JSON :
        {{
          "analyse": "Ton raisonnement stratégique",
          "action": "tap|swipe|type|wait|system_shell|learn_ui",
          "params": {{}},
          "reponse": "Message clair pour le Maître"
        }}
        """

        payload = {
            "contents": [{
                "parts": [
                    {"text": system_instruction},
                    {"inlineData": {"mimeType": "image/png", "data": b64_image}} if b64_image else {"text": "[Vision aveugle]"},
                    {"text": f"MAÎTRE : {prompt}" if prompt else "INSTRUCTION SYSTÈME : Analyse l'écran et agis."}
                ]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json"
            }
        }

        try:
            res = requests.post(url, json=payload, timeout=30)
            
            if res.status_code == 429:
                self.retry_count += 1
                print(f"🔄 Clé {self.key_index+1} saturée ({self.retry_count}/{len(API_KEYS)}). Rotation...")
                self.key_index = (self.key_index + 1) % len(API_KEYS)
                return self.call_ai(prompt, is_gaming)

            if res.status_code == 200:
                self.retry_count = 0 # Reset si succès
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            
            print(f"⚠️ OMEGA : Erreur API ({res.status_code}) - {res.text[:100]}")
        except Exception as e:
            print(f"⚠️ OMEGA : Erreur de communication : {e}")
        return None

    def execute(self, decision_raw):
        """ Traduction des ordres cognitifs en actions physiques """
        if not decision_raw: return
        try:
            d = json.loads(decision_raw)
            act = d.get('action', 'wait')
            p = d.get('params', {})
            
            print(f"\n🧠 [PENSÉE] : {d.get('analyse')}")
            print(f"🤖 OMEGA : {d.get('reponse')}")

            if not self.device: return

            if act == "tap":
                # Anti-bot : variation aléatoire
                rx, ry = p['x'] + random.randint(-2, 2), p['y'] + random.randint(-2, 2)
                self.device.shell(f"input tap {rx} {ry}")
                print(f"🖱️ Action : Tap ({rx}, {ry})")
            
            elif act == "swipe":
                self.device.shell(f"input swipe {p['x1']} {p['y1']} {p['x2']} {p['y2']} {p.get('duration', 300)}")
                print(f"↔️ Action : Swipe")
            
            elif act == "type":
                self.device.shell(f"input text '{p['text']}'")
                print(f"⌨️ Action : Type '{p['text']}'")
            
            elif act == "wait":
                sec = p.get('seconds', 2)
                print(f"⏸️ Action : Attente {sec}s")
                time.sleep(sec)
            
            elif act == "system_shell":
                self.device.shell(p['cmd'])
                print(f"💻 Action : Shell '{p['cmd']}'")
            
            elif act == "learn_ui":
                app = self.get_current_app()
                if app not in self.ui_map: self.ui_map[app] = {}
                self.ui_map[app].update(p.get('buttons', {}))
                self.save_json(self.ui_map_file, self.ui_map)
                print(f"👁️ Action : Interface mémorisée pour {app}")

        except Exception as e:
            print(f"❌ OMEGA : Erreur d'exécution : {e}")

    def start_autonomous_loop(self, prompt="Continue l'automatisation."):
        """ Activation du mode Zénith (Boucle infinie) """
        self.is_running = True
        print("\n🚀 [MODE ZÉNITH ACTIVÉ] OMEGA prend le contrôle...")
        
        def loop():
            while self.is_running:
                decision = self.call_ai(prompt)
                if decision:
                    self.execute(decision)
                time.sleep(1.5) # Délai de sécurité pour le quota API

        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self.is_running = False
        print("\n⏹️ [MODE ZÉNITH DÉSACTIVÉ]")

if __name__ == "__main__":
    omega = OmegaZenith()
    
    print("==========================================")
    print("   OMEGA v11.0 - LE ZÉNITH (PYTHON)       ")
    print("==========================================")
    
    if not API_KEYS:
        print("⚠️ ATTENTION : Aucune clé API configurée.")
        exit(1)

    while True:
        try:
            cmd = input("\n🎮 Maître > ")
            if cmd.lower() in ["exit", "quit", "quitter"]:
                omega.stop()
                break
            
            if "boucle" in cmd.lower() or "auto" in cmd.lower() or "joue" in cmd.lower():
                omega.start_autonomous_loop(cmd)
            elif "stop" in cmd.lower():
                omega.stop()
            else:
                dec = omega.call_ai(cmd)
                omega.execute(dec)
                
        except KeyboardInterrupt:
            omega.stop()
            break
        except Exception as e:
            print(f"⚠️ Erreur imprévue : {e}")
