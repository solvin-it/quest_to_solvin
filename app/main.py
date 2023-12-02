import streamlit as st
from world import World
from npc import NPC
import time
from openai import OpenAI

def simulate_typing(text):
    message_placeholder = st.empty()
    full_response = ""
    for chunk in text.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)

def main(world):

    # Set the sidebar
    with st.sidebar:
        # Set the title of the page
        st.title("Chapter One: The Beginning")

        if "OPENAI_API_KEY" in st.secrets:
            st.success("OpenAI API Key found!", icon="🔑")
        else:
            OpenAI.api_key = st.text_input("OpenAI API Key", type="password")
            if not OpenAI.api_key.startswith('sk-') and len (OpenAI.api_key ) == 51:
                st.error("Invalid API Key")
            else:
                st.success("OpenAI API Key found!", icon="🔑")

        if 'npc' in st.session_state:
            st.markdown("### Character Window:")
            st.image(st.session_state.npc.image, caption=st.session_state.npc.name)
            st.markdown(f"Name: {st.session_state.npc.name}")
            st.markdown(f"Age: {st.session_state.npc.age}")
            st.markdown(f"Profession: {st.session_state.npc.profession}")
            st.markdown(f"Personality: {st.session_state.npc.personality}")
            st.markdown(f"Description: {st.session_state.npc.description}")


    # Initialize the world and start the introduction.
    if 'world' not in st.session_state:
        st.session_state.world = world

        # Display the image of the empire
        # st.image(st.session_state.world.get_location_image("solvin_empire"), caption="The Empire of Solvin")
        
        # Print the background story to the screen
        for line in st.session_state.world.background:
            message_placeholder = st.empty()
            message_placeholder.markdown(line)

        # Display a generated image of the beginner village
        st.image(st.session_state.world.get_location_image("eldertree"), caption="The Eldertree Village")

    if 'start' not in st.session_state:
        st.session_state.start = False        

    if st.session_state.start:
        # Initialize  chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display the chat history
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

        # Start a conversation with the NPC
        if st.session_state.messages == []:
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                task = "Welcome the user to the Eldertree village."
                assistant_response = st.session_state.npc.generate_response([{"role": "assistant", "content": task}])
                
                simulate_typing(assistant_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
       
        if prompt := st.chat_input("Say something..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                messages = st.session_state.messages.copy()
                assistant_response = st.session_state.npc.generate_response(messages)
                
                # Simulate stream of response with milliseconds delay
                simulate_typing(assistant_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            # Once the NPC learns enough from the user or the user asks for a quest, generate a quest

            # Display the quest to the user

            # Ask the user if they want to accept the quest

            # Continue the conversation with the NPC after the user accepts or rejects the quest and end the conversation
    else:
        if st.button("Start"):
            st.session_state.start = True
            # Initialize the NPC
            if "npc" not in st.session_state:
                st.session_state.npc = NPC(
                    settings=st.session_state.world.settings
                )
            st.rerun()

if __name__ == "__main__":
    main(World())