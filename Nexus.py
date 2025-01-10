# Import required libraries
from openai import OpenAI
import streamlit as st

def main():
    # Set the title of the Streamlit app
    st.title("Nexus")
    
    # Initialize chat history in session state if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Create text input field for user prompt
    user_input = st.text_input("Enter your prompt:", key="user_input")
    
    st.write("This is Nexus. An AI chatbot built by using NVIDIA's LLM model, OpenAI's GPT-4o model. \n\nOnce you enter a prompt, Nexus will respond to it using the latest NVIDIA LLM model. \n\nTry saying, 'What are some AI models used by large companies that use LLM?', and watch Nexus respond with a detailed list of AI models used by large companies that use LLM.")

    # Create send button and handle click
    if st.button("Send"):
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Create OpenAI client with NVIDIA API endpoint
            client = OpenAI(
                base_url = "https://integrate.api.nvidia.com/v1",
                api_key = "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"
            )

            # Create completion request with specified parameters
            completion = client.chat.completions.create(
                model="meta/llama3-70b-instruct",
                messages=[{"role": "user", "content": user_input}],
                temperature=0.5,  # Controls randomness
                top_p=1,         # Controls diversity
                max_tokens=1024,  # Maximum length of response
                stream=True      # Enable streaming response
            )

            # Create empty placeholder for streaming response
            response_placeholder = st.empty()
            full_response = ""            

            # Stream the response
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})


# Run main function when script is executed directly
if __name__ == "__main__":
    main()
