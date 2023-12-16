from pathlib import Path
import streamlit as st
from world import World
from npc import NPC
import time
from openai import OpenAI

# Path settings
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "static" / "css" / "main.css"

def simulate_typing(text):
    message_placeholder = st.empty()
    full_response = ""
    for chunk in text.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)

st.set_page_config(page_title="Quest To Solvin", page_icon=":video_game:",layout="wide")

with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Set the sidebar
with st.sidebar:
    # Set the title of the page
    st.title("Chapter One: The Beginning")

    if "OPENAI_API_KEY" in st.secrets:
        OpenAI.api_key = st.secrets["OPENAI_API_KEY"]
        st.success("OpenAI API Key found!", icon="🔑")
    else:
        OpenAI.api_key = st.text_input("OpenAI API Key", type="password")
        if (not OpenAI.api_key.startswith('sk-') or len (OpenAI.api_key ) != 51) and OpenAI.api_key != "":
            st.error("Invalid API Key", icon="🚫")
        elif OpenAI.api_key.startswith('sk-') and len (OpenAI.api_key ) == 51:
            st.success("OpenAI API Key found!", icon="🔑")

    if 'npc' in st.session_state:
        st.markdown("### Character Window:")
        st.image(st.session_state.npc.image, caption=st.session_state.npc.name)
        st.markdown(f"Name: {st.session_state.npc.name}")
        st.markdown(f"Age: {st.session_state.npc.age}")
        st.markdown(f"Profession: {st.session_state.npc.profession}")
        st.markdown(f"Personality: {st.session_state.npc.personality}")
        st.markdown(f"Description: {st.session_state.npc.description}")

if OpenAI.api_key.startswith('sk-') and len (OpenAI.api_key ) == 51:
    # Initialize the world and start the introduction.
    if 'world' not in st.session_state:
        st.session_state.world = World()

    if 'start' not in st.session_state:
        st.session_state.start = False   

    if 'quest' not in st.session_state:
        st.session_state.quest = ""
        st.session_state.quest_created = False

    # Display the quest to the user
    if not st.session_state.quest_created:
        if not st.session_state.start:
            # Display a generated image of the beginner village
            st.image(st.session_state.world.get_location_image("eldertree"), caption="The Eldertree Village")
            
            # Print the background story to the screen
            for line in st.session_state.world.background:
                st.markdown(line)
            
            if st.button("Start"):
                st.session_state.start = True
                # Initialize the NPC
                if "npc" not in st.session_state:
                    st.session_state.npc = NPC(
                        settings=st.session_state.world.settings
                    )
                st.rerun()
        else:
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

                # Introduce the user to the village
                st.markdown("As you step foot into the village of Eldertree, you encountered with one of its villagers.")
                st.markdown("What do you say to the villager?")

            # Display the chat history
            for message in st.session_state.messages:
                with st.chat_message(message['role']):
                    st.markdown(message['content'])
        
            if prompt := st.chat_input("Say something..."):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    messages = st.session_state.messages.copy()
                    assistant_response = st.session_state.npc.generate_response(messages)

                    if "CREATE QUEST" in assistant_response:
                        st.session_state.quest_created = True
                        st.session_state.quest = st.session_state.npc.generate_quest(st.session_state.messages.copy())
                        st.rerun()
                    
                    # Simulate stream of response with milliseconds delay
                    simulate_typing(assistant_response)

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    else:
        st.markdown("### Quest Window")
        st.markdown(f"Title: {st.session_state.quest.title}")
        st.markdown(f"Description: {st.session_state.quest.description}")
        st.markdown(f"Difficulty: {st.session_state.quest.difficulty}")
        st.markdown(f"Success Condition: {st.session_state.quest.success_condition}")
        st.markdown(f"Failure Condition: {st.session_state.quest.failure_condition}")
        st.markdown(f"Reward: {st.session_state.quest.reward}")