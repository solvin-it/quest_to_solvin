import streamlit as st
from world import World
from npc import NPC
import time


# Set the title of the page
st.title("Chapter One: The Beginning")

# Initialize the world
if 'world' not in st.session_state:
    st.session_state.world = World()

# Print the background story to the screen
# message_placeholder = st.empty()
# full_response = ""

# Simulate stream of response with milliseconds delay
# for chunk in st.session_state.world.background.split():
#     full_response += chunk + " "
#     time.sleep(0.05)
#     # Add a blinking cursor to simulate typing
#     message_placeholder.markdown(full_response + "▌")
# message_placeholder.markdown(full_response)

# Initialize  chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Initialize the user's name
if "name" not in st.session_state:
    st.session_state.name = None

if "npc" not in st.session_state:
    st.session_state.npc = NPC()

if st.session_state.messages == []:
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = st.session_state.npc.generate_response([{"role": "assistant", "content": "Welcome the user to the village."}])

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

if prompt := st.chat_input("Say something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        messages = st.session_state.messages.copy()
        assistant_response = st.session_state.npc.generate_response(messages)
        
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Display a generated image of the beginner village

# Ask the user for their name, age, class, and weapon

# Ask the user where they want to go based on the choices

# Display a generated image of the location

# Describe the location to the user

# Ask the user who they want to talk to based on the choices

# Generate NPC information such as name, age, profession, personality, and image

# Display the NPC image to the user

# Start a conversation with the NPC

# Once the NPC learns enough from the user or the user asks for a quest, generate a quest

# Display the quest to the user

# Ask the user if they want to accept the quest

# Continue the conversation with the NPC after the user accepts or rejects the quest and end the conversation
