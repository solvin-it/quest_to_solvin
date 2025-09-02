# 🏰 Quest to Solvin

*A medieval-fantasy RPG chatbot powered by LLMs, built with Streamlit and OpenAI’s GPT-5-nano.*

---

## 🚀 Introduction

**Quest to Solvin** is an interactive AI-powered RPG demo that blends storytelling, worldbuilding, and generative AI.  
Designed as a portfolio project, it demonstrates how large language models and multimodal AI can drive dynamic narratives, character generation, and user engagement in a game-like setting.

- **AI-driven NPCs:** Each character is generated on the fly, with unique personalities, backgrounds, and professions.
- **Procedural Quests:** NPCs issue custom quests based on your chat history and their own context.
- **Pixel Art Portraits:** NPCs are visualized with DALL·E-generated pixel art.
- **Rich Lore:** The world’s lore and background are loaded from markdown files for easy expansion.

---

## 🌐 Live Demo

👉 [Try Quest to Solvin on GCP](https://quest.solvin.co)  

---

## 🎮 Features

- **Dynamic NPCs:** Each NPC has a unique personality, background, and profession, generated via GPT-5-nano.  
- **Personalized Quests:** NPCs issue quests tailored to their role and your chat history.  
- **Pixel Art Portraits:** NPC portraits created using DALL·E for a retro RPG feel.  
- **Rich Lore:** Game world background and lore are loaded from markdown files for extensibility.  
- **Interactive Chat:** Users engage with NPCs through a chat interface, driving the story forward.  

---

## 🛠️ How It Works

1. **World Loading:** Lore and background are loaded from markdown files at startup.
2. **NPC Generation:** When the game begins, an NPC is generated with a unique backstory and portrait.
3. **Interactive Chat:** Users chat with the NPC, who responds in character and guides the conversation toward a quest.
4. **Quest Creation:** When the NPC deems the time right, a custom quest is generated and displayed, including objectives, conditions, and rewards.

---

## 📂 Project Structure

```
├── app/
│   ├── main.py            # Streamlit UI and app entry point
│   ├── npc.py             # NPC logic: creation, chat, quest & image generation
│   ├── quest.py           # Quest data structure
│   ├── world.py           # World settings and lore loader
│   ├── settings/
│   │   ├── lore.md        # Game world lore
│   │   └── background.md  # World background details
│   └── static/css/        # Custom CSS for UI
├── requirements.txt       # Python dependencies
├── .env_template          # Example environment config
├── README.md              # Project documentation
```

---

## 🖥️ Setup & Run

1. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   - Copy `.env_template` to `.env`.
   - Add your `OPENAI_API_KEY`.

3. **Run the app**
   ```sh
   streamlit run app/main.py
   ```

4. **Open in your browser**
   - The app will open automatically.
   - Chat with NPCs and embark on AI-generated quests.

---

## 📸 Screenshots

**Chat Interface**  
![chat ui](https://github.com/solvin-it/quest_to_solvin/blob/main/documentation/sample_chat1.png?raw=true)

**Generated NPC Portraits**
![npc portraits: Blacksmith](https://github.com/solvin-it/quest_to_solvin/blob/main/documentation/sample_npc1.png?raw=true)

![npc portraits: Inn Keeper](https://github.com/solvin-it/quest_to_solvin/blob/main/documentation/sample_npc2.png?raw=true)

**Quest Example**  
![quest example](https://github.com/solvin-it/quest_to_solvin/blob/main/documentation/sample_quest1.png?raw=true)

---

## 🔭 Future Work

Planned improvements for **Quest to Solvin** include:

- **Richer NPC interactions** — expand dialogue depth, branching paths, and continuity across sessions.  
- **Enhanced lore & worldbuilding** — grow the markdown-based lore system for a more immersive setting.  
- **Quest window improvements** — redesign the quest interface for clarity, objectives tracking, and visual appeal.  
- **Player features** — add a status window and basic character creation so players can build their own persona in Solvin.  
- **LLM & multimodal exploration** — experiment with newer LLMs, image models, and multimodal integrations to push storytelling further.  

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **OpenAI** — for GPT-5-nano and DALL·E APIs
- **Streamlit** — for rapid prototyping and interactive UI
- **Community inspiration** — isekai stories, RPGs, and worldbuilding enthusiasts

---

### ✨ Recruiter-Friendly Closing Note

This project was an **early experiment** (built \~2 years ago) but remains one of my favorites because it captures my **curiosity about AI** and my desire to see how far language models can go beyond text — into **worldbuilding, creativity, and interactivity**.