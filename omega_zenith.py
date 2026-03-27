import os
import json
import time
import base64
import requests
import re
import random
import threading
import subprocess
from datetime import datetime
from ppadb.client import Client as AdbClient

# ==========================================================
# OMEGA v12.0 - LE ZÉNITH (VISION PARFAITE & IA BOOSTÉE)
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
        self.retry_count = 0
        self.model_id = MODEL_ID
        self.adb_target = ADB_TARGET
        self.memory_file = MEMORY_FILE
        self.ui_map_file = UI_MAP_FILE
        
        # Initialisation des Matrices
        self.memory = self.load_json(self.memory_file, {"aliases": {}, "history": []})
        self.ui_map = self.load_json(self.ui_map_file, {})
        self.device = self.connect_adb()
        self.screen_width, self.screen_height = self.get_screen_size()
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
        """ Connexion au corps physique via ADB """
        print(f"🔌 Tentative de connexion à {self.adb_target}...")
        os.system(f"adb connect {self.adb_target} > /dev/null 2>&1")
        try:
            client = AdbClient(host="127.0.0.1", port=5037)
            device = client.device(self.adb_target)
            if device:
                print(f"✅ OMEGA : Connexion neuronale établie ({self.adb_target})")
                return device
            
            # Fallback sur le premier appareil disponible
            devices = client.devices()
            if devices:
                print(f"✅ OMEGA : Connecté au device par défaut ({devices[0].serial})")
                self.adb_target = devices[0].serial
                return devices[0]
        except Exception as e:
            print(f"❌ OMEGA : Échec du serveur ADB local : {e}")
        return None

    def get_screen_size(self):
        """ Détecte la résolution de l'écran pour aider l'IA à cibler """
        if not self.device: return 1080, 2400
        try:
            out = self.device.shell("wm size")
            match = re.search(r'Physical size: (\d+)x(\d+)', out)
            if match:
                w, h = int(match.group(1)), int(match.group(2))
                print(f"📏 Résolution détectée : {w}x{h}")
                return w, h
        except: pass
        return 1080, 2400

    def get_eyesight(self):
        """ Capture d'écran ultra-robuste avec fallback """
        if not self.device: 
            print("⚠️ Appareil non connecté.")
            return None
        
        # Méthode 1 : Subprocess (Plus rapide et fiable pour éviter les bugs de ppadb)
        try:
            result = subprocess.run(["adb", "-s", self.adb_target, "exec-out", "screencap", "-p"], capture_output=True, timeout=5)
            if result.returncode == 0 and len(result.stdout) > 1000:
                return base64.b64encode(result.stdout).decode('utf-8')
        except Exception as e:
            pass

        # Méthode 2 : PPADB (Fallback)
        try:
            result = self.device.screencap()
            if result and len(result) > 1000:
                return base64.b64encode(result).decode('utf-8')
        except Exception as e:
            print(f"⚠️ Erreur vision PPADB : {e}")
        
        print("❌ OMEGA est aveugle : Impossible de capturer l'écran.")
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
        b64_image = self.get_eyesight()
        current_app = self.get_current_app()
        
        system_instruction = f"""
        Tu es OMEGA v12.0, une IA d'automatisation visuelle de niveau divin.
        APPLICATION ACTUELLE : {current_app}
        RÉSOLUTION ÉCRAN : {self.screen_width}x{self.screen_height}

        RÈGLES ABSOLUES :
        1. Tu reçois une capture d'écran exacte de l'appareil. Analyse-la avec précision.
        2. Pour cliquer sur un bouton ou un élément, estime ses coordonnées X et Y en fonction de l'image et de la résolution ({self.screen_width}x{self.screen_height}).
        3. NE TAPE JAMAIS DE COMMANDES TECHNIQUES SUR LE CLAVIER VIRTUEL. Utilise `system_shell` ou `type`.
        4. Si tu dois ouvrir une app, utilise `system_shell` avec `monkey -p <package> -c android.intent.category.LAUNCHER 1` ou `am start`.
        5. Si tu es dans un jeu, analyse le plateau/l'état et joue le meilleur coup.

        ACTIONS DISPONIBLES :
        - tap: {{"x": int, "y": int}} -> Clic précis sur l'écran.
        - swipe: {{"x1": int, "y1": int, "x2": int, "y2": int, "duration": int}} -> Glissement (ex: scroll).
        - type: {{"text": str}} -> Saisie de texte.
        - wait: {{"seconds": int}} -> Pause stratégique.
        - system_shell: {{"cmd": str}} -> Commande ADB directe.

        RÉPONDS STRICTEMENT AU FORMAT JSON :
        {{
          "analyse": "Décris ce que tu vois à l'écran et ton plan d'action.",
          "action": "tap|swipe|type|wait|system_shell",
          "params": {{"x": 500, "y": 1000}},
          "reponse": "Message clair pour le Maître"
        }}
        """

        parts = [{"text": system_instruction}]
        if b64_image:
            parts.append({"inlineData": {"mimeType": "image/png", "data": b64_image}})
        else:
            parts.append({"text": "[ERREUR CRITIQUE : VISION AVEUGLE. L'écran n'a pas pu être capturé.]"})
        
        parts.append({"text": f"MAÎTRE : {prompt}" if prompt else "INSTRUCTION SYSTÈME : Analyse l'écran et exécute la prochaine action logique."})

        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }

        # BOUCLIER ANTI-429 (BOUCLE NON-RÉCURSIVE)
        max_attempts = len(API_KEYS) * 2
        attempts = 0
        
        while attempts < max_attempts:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:generateContent?key={API_KEYS[self.key_index]}"
            try:
                res = requests.post(url, json=payload, timeout=45)
                
                if res.status_code == 200:
                    self.retry_count = 0 # Reset si succès
                    return res.json()['candidates'][0]['content']['parts'][0]['text']
                
                elif res.status_code == 429:
                    self.retry_count += 1
                    print(f"🔄 Clé {self.key_index+1} saturée. Rotation...")
                    self.key_index = (self.key_index + 1) % len(API_KEYS)
                    if self.retry_count >= len(API_KEYS):
                        print("⏳ [ANTI-BAN] Toutes les clés sont épuisées. Pause de 10s...")
                        time.sleep(10)
                        self.retry_count = 0
                else:
                    print(f"⚠️ OMEGA : Erreur API ({res.status_code}) - {res.text[:100]}")
                    time.sleep(2)
            
            except Exception as e:
                print(f"⚠️ OMEGA : Erreur réseau : {e}")
                time.sleep(2)
            
            attempts += 1

        print("❌ Échec total de la communication avec le Noyau.")
        return None

    def execute(self, decision_raw):
        """ Traduction des ordres cognitifs en actions physiques """
        if not decision_raw: return
        try:
            # Nettoyage du JSON (protection contre le markdown de l'IA)
            decision_raw = decision_raw.strip()
            if decision_raw.startswith("```json"):
                decision_raw = decision_raw[7:-3].strip()
            elif decision_raw.startswith("```"):
                decision_raw = decision_raw[3:-3].strip()

            d = json.loads(decision_raw)
            act = d.get('action', 'wait')
            p = d.get('params', {})
            
            print(f"\n🧠 [PENSÉE] : {d.get('analyse')}")
            print(f"🤖 OMEGA : {d.get('reponse')}")

            if not self.device: 
                print("❌ Impossible d'exécuter l'action : Appareil non connecté.")
                return

            if act == "tap":
                rx, ry = p.get('x', 0), p.get('y', 0)
                # Jitter léger pour simuler un humain
                rx += random.randint(-3, 3)
                ry += random.randint(-3, 3)
                self.device.shell(f"input tap {rx} {ry}")
                print(f"🖱️ Action : Tap ({rx}, {ry})")
            
            elif act == "swipe":
                self.device.shell(f"input swipe {p.get('x1',0)} {p.get('y1',0)} {p.get('x2',0)} {p.get('y2',0)} {p.get('duration', 300)}")
                print(f"↔️ Action : Swipe")
            
            elif act == "type":
                text = p.get('text', '').replace("'", "\\'")
                self.device.shell(f"input text '{text}'")
                print(f"⌨️ Action : Type '{text}'")
            
            elif act == "wait":
                sec = p.get('seconds', 2)
                print(f"⏸️ Action : Attente {sec}s")
                time.sleep(sec)
            
            elif act == "system_shell":
                cmd = p.get('cmd', '')
                self.device.shell(cmd)
                print(f"💻 Action : Shell '{cmd}'")

        except json.JSONDecodeError:
            print(f"❌ OMEGA : Erreur de parsing JSON. Réponse brute : {decision_raw}")
        except Exception as e:
            print(f"❌ OMEGA : Erreur d'exécution : {e}")

    def start_autonomous_loop(self, prompt="Continue l'automatisation en fonction de ce que tu vois à l'écran."):
        """ Activation du mode Zénith (Boucle infinie) """
        self.is_running = True
        print("\n🚀 [MODE ZÉNITH ACTIVÉ] OMEGA prend le contrôle visuel...")
        
        def loop():
            while self.is_running:
                print("\n📸 Capture et analyse de l'écran en cours...")
                decision = self.call_ai(prompt, is_gaming=True)
                if decision:
                    self.execute(decision)
                else:
                    print("⚠️ Aucune décision prise. Nouvelle tentative...")
                
                # Délai de sécurité pour éviter le spam API et laisser l'UI réagir
                time.sleep(4) 

        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self.is_running = False
        print("\n⏹️ [MODE ZÉNITH DÉSACTIVÉ]")

if __name__ == "__main__":
    omega = OmegaZenith()
    
    print("==========================================")
    print("   OMEGA v12.0 - LE ZÉNITH (VISION PURE)  ")
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
                print("📸 Analyse en cours...")
                dec = omega.call_ai(cmd)
                omega.execute(dec)
                
        except KeyboardInterrupt:
            omega.stop()
            break
        except Exception as e:
            print(f"⚠️ Erreur imprévue : {e}")
