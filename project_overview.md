# Quest to Solvin – Project Overview

## What is Quest to Solvin?

Quest to Solvin is a medieval-fantasy RPG chatbot built with Streamlit. It leverages OpenAI’s GPT-3.5 to generate:

- **NPCs (Non-Playable Characters):** Each with unique personalities, backgrounds, and professions.
- **Dynamic Quests:** Tailored to user interactions and the NPC’s context.
- **Pixel Art Portraits:** For NPCs, generated using DALL-E.

The world is rich in lore and background, loaded from markdown files. Users interact with NPCs in a chat interface, and NPCs guide users toward quests.

---

## How It Works

- **Streamlit App (`app/main.py`):** Entry point for the UI and main logic.
- **NPC Logic (`app/npc.py`):** Handles NPC creation, chat responses, quest and image generation.
- **Quest Structure (`app/quest.py`):** Defines the quest data structure.
- **World Settings (`app/world.py`):** Loads lore and background from markdown files.
- **Lore/Background (`app/settings/lore.md`, `app/settings/background.md`):** Game world details.

### Flow

1. The app loads world lore and background.
2. An NPC is generated with a unique background and image.
3. The user chats with the NPC.
4. When the NPC responds with `"CREATE QUEST"`, a quest is generated and displayed.

---

## How to Run and Test

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Create a `.env` file (use `.env_template` as a base if available).
   - Set your `OPENAI_API_KEY` and paths for lore/background files.

3. **Run the Streamlit app:**
   ```sh
   streamlit run app/main.py
   ```

4. **Interact in your browser:**
   - The app will open automatically.
   - Chat with the NPC and follow the prompts.

---

## Key Files

- `app/main.py` – Streamlit UI and main logic
- `app/npc.py` – NPC logic, quest/image generation
- `app/quest.py` – Quest data structure
- `app/world.py` – Loads lore/background
- `app/settings/lore.md`, `app/settings/background.md` – Game world lore and background

---

## How to Expand

- Add new professions, personalities, or quest types in `app/npc.py`.
- Expand lore/background in the markdown files.
- Improve UI in `app/static/css/main.css`.
