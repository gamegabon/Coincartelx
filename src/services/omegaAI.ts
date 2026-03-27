import { GoogleGenAI, GenerateContentResponse } from "@google/genai";

export interface OmegaAction {
  analyse: string;
  action: "start_gaming" | "tap" | "system_shell" | "learn_ui" | "tap_memory" | "play_move" | "wait" | "type" | "update_config";
  params: any;
  reponse: string;
}

export class OmegaAI {
  private ai: GoogleGenAI;

  constructor(apiKey: string) {
    this.ai = new GoogleGenAI({ apiKey });
  }

  async analyze(
    userPrompt: string,
    screenshotBase64?: string,
    currentApp: string = "unknown",
    memory: any = {}
  ): Promise<OmegaAction | null> {
    const systemPrompt = `
      Tu es OMEGA v11.0, IA d'Automatisation de Niveau Divin.
      APPLICATION ACTUELLE : ${currentApp}
      MÉMOIRE BOUTONS : ${JSON.stringify(memory)}

      RÈGLES ABSOLUES :
      1. NE TAPE JAMAIS DE COMMANDES TECHNIQUES SUR LE CLAVIER VIRTUEL DE L'ÉCRAN. Utilise l'action \`system_shell\` pour exécuter des commandes en arrière-plan.
      2. Si le Maître demande de jouer, utilise UNIQUEMENT l'action \`start_gaming\`. Ne cherche pas à l'écrire dans Termux.
      3. Sois concis dans tes analyses. Ne répète jamais deux fois la même phrase.

      ACTIONS POSSIBLES :
      - start_gaming: {"app_name": "nom_du_jeu", "duration_minutes": 60} -> Active la boucle autonome.
      - tap: {"x": int, "y": int} -> Clic direct (Python ajoutera un aléatoire de ±3px anti-bot).
      - system_shell: {"cmd": "commande ADB"} -> Exécute silencieusement une commande système (ex: 'am start ...').
      - learn_ui: {"buttons": {"nom": {"x": 100, "y": 200}}} -> Mémorise l'écran.
      - tap_memory: {"button_name": "nom"} -> Clique sur un bouton mémorisé.
      - play_move: {"x1": int, "y1": int, "x2": int, "y2": int} -> Glisser (Spécial Jeu).
      - wait: {"seconds": int} -> Patienter.
      - type: {"text": str} -> Pour écrire un VRAI message humain (chat, recherche).
      - update_config: {"status": "ok"} -> Si le Maître donne de nouvelles instructions à retenir.

      RÉPONDS STRICTEMENT AU FORMAT JSON :
      {
        "analyse": "Ta réflexion",
        "action": "start_gaming|tap|system_shell|learn_ui|tap_memory|play_move|wait|type|update_config",
        "params": {},
        "reponse": "Message clair pour le Maître"
      }
    `;

    const parts: any[] = [{ text: systemPrompt }];
    
    if (screenshotBase64) {
      parts.push({
        inlineData: {
          mimeType: "image/png",
          data: screenshotBase64.split(",")[1] || screenshotBase64,
        },
      });
    }

    parts.push({ text: `MAÎTRE: ${userPrompt || "Analyse et joue."}` });

    try {
      const response: GenerateContentResponse = await this.ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: { parts },
        config: {
          responseMimeType: "application/json",
        }
      });

      const text = response.text;
      if (!text) return null;

      return JSON.parse(text) as OmegaAction;
    } catch (error) {
      console.error("Omega AI Error:", error);
      return null;
    }
  }
}
