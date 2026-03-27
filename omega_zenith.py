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
# OMEGA v11.0 - LE ZÉNITH (ÉDITION PYTHON ULTIME)
# ==========================================================
# Optimisé pour Gemini 3 Flash & Automatisation de Niveau Divin
# ==========================================================

class OmegaZenith:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model_id = "gemini-3-flash-preview"
        self.adb_target = "192.168.1.67:33231"
        self.memory_file = "omega_memory.json"
        self.ui_map_file = "omega_ui_map.json"
        
        self.memory = self.load_json(self.memory_file, {"aliases": {}, "history": []})
        self.ui_map = self.load_json(self.ui_map_file, {})
        self.device = self.connect_adb()
        self.is_running = False

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
        """ Capture d'écran haute performance """
        if not self.device: return None
        try:
            # Capture directe en mémoire pour éviter les écritures disque inutiles
            result = self.device.screencap()
            return base64.b64encode(result).decode('utf-8')
        except:
            return None

    def call_ai(self, prompt, is_gaming=False):
        """ Appel au noyau Gemini 3 avec vision """
        if not self.api_key: return None
        
        b64_image = self.get_eyesight()
        current_app = self.get_current_app()
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:generateContent?key={self.api_key}"
        
        system_instruction = f"""
        Tu es OMEGA v11.0, l'IA d'automatisation la plus puissante.
        CONTEXTE : {current_app}
        MÉMOIRE : {json.dumps(self.ui_map.get(current_app, {}))}

        ACTIONS DISPONIBLES :
        - tap: {{"x": int, "y": int}}
        - swipe: {{"x1": int, "y1": int, "x2": int, "y2": int, "duration": int}}
        - type: {{"text": str}}
        - wait: {{"seconds": int}}
        - system_shell: {{"cmd": str}}
        - learn_ui: {{"buttons": {{"name": {{"x": int, "y": int}}}}}}

        RÉPONDS UNIQUEMENT EN JSON :
        {{
          "analyse": "Court raisonnement",
          "action": "tap|swipe|type|wait|system_shell|learn_ui",
          "params": {{}},
          "reponse": "Message pour le Maître"
        }}
        """

        payload = {
            "contents": [{
                "parts": [
                    {"text": system_instruction},
                    {"inlineData": {"mimeType": "image/png", "data": b64_image}} if b64_image else {"text": "[Pas de vue disponible]"},
                    {"text": f"ORDRE : {prompt}"}
                ]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }

        try:
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            print(f"⚠️ Erreur AI ({res.status_code})")
        except Exception as e:
            print(f"⚠️ Erreur Réseau : {e}")
        return None

    def get_current_app(self):
        if not self.device: return "unknown"
        try:
            out = self.device.shell("dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'")
            match = re.search(r'([a-zA-Z0-9\.]+)/', out)
            return match.group(1) if match else "unknown"
        except: return "unknown"

    def execute(self, decision_raw):
        if not decision_raw: return
        try:
            d = json.loads(decision_raw)
            act = d.get('action')
            p = d.get('params', {})
            
            print(f"🧠 [PENSÉE] : {d.get('analyse')}")
            print(f"🤖 OMEGA : {d.get('reponse')}")

            if act == "tap":
                # Anti-bot : jitter de ±2px
                x, y = p['x'] + random.randint(-2, 2), p['y'] + random.randint(-2, 2)
                self.device.shell(f"input tap {x} {y}")
            
            elif act == "swipe":
                self.device.shell(f"input swipe {p['x1']} {p['y1']} {p['x2']} {p['y2']} {p.get('duration', 300)}")
            
            elif act == "type":
                self.device.shell(f"input text '{p['text']}'")
            
            elif act == "wait":
                time.sleep(p.get('seconds', 2))
            
            elif act == "system_shell":
                self.device.shell(p['cmd'])
            
            elif act == "learn_ui":
                app = self.get_current_app()
                if app not in self.ui_map: self.ui_map[app] = {}
                self.ui_map[app].update(p.get('buttons', {}))
                self.save_json(self.ui_map_file, self.ui_map)

        except Exception as e:
            print(f"❌ Erreur d'exécution : {e}")

    def run_loop(self, prompt):
        self.is_running = True
        print("🚀 OMEGA : Entrée en boucle autonome...")
        while self.is_running:
            decision = self.call_ai(prompt)
            if decision:
                self.execute(decision)
            time.sleep(1)

if __name__ == "__main__":
    # Récupération de la clé depuis l'environnement ou saisie
    KEY = os.getenv("GEMINI_API_KEY")
    omega = OmegaZenith(KEY)
    
    print("\n--- OMEGA v11.0 ZENITH (PYTHON CORE) ---")
    while True:
        cmd = input("\n🎮 Maître > ")
        if cmd.lower() in ["exit", "quit"]: break
        
        if "boucle" in cmd.lower() or "auto" in cmd.lower():
            threading.Thread(target=omega.run_loop, args=(cmd,), daemon=True).start()
        else:
            dec = omega.call_ai(cmd)
            omega.execute(dec)
