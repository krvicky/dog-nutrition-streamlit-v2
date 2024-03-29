from openai import OpenAI
import streamlit as st
import time

def stream_data(text_to_stream):
    for word in text_to_stream.split():
        yield word + " "
        time.sleep(0.02)

st.title("🐶Dog Nutrition assistant")
st.write("Paw-sitively Informed 🐾: Your Go-To Hub for Canine Nutrition Q&A with Our Expert Agents! 🐕💬")


#CODE FOR SIDEBAR
def is_api_key_valid():
    try:
        test_call = api_test_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages= [{"role": "user", "content": "Say this is a test!"}]
            )
    except:
        return False
    else:
        return True

if 'session_ready' not in st.session_state:
    st.session_state.session_ready = False

#app_ready = False

#Sidebar
api_key_sidebar = st.sidebar.text_input(
    "Enter you OpenAI API key", type = "password"
)

if st.sidebar.button("Proceed", type = "primary") or st.session_state.session_ready:
    api_test_client = OpenAI(api_key=api_key_sidebar)

    # Check the validity of the API key
    if is_api_key_valid():
        st.sidebar.write("Your API key is valid ✅")
        st.sidebar.write("🐾 Welcome to your Dog Nutrition Companion! Ready to chat with our friendly agent?")
        st.sidebar.info("Disclaimer: Our responses are generated by AI agents. While we strive to provide accurate information, please use your discretion and consult with a veterinary professional for personalized advice regarding your pet's health and nutrition. ",icon="ℹ️")             
        #app_ready = True
        st.session_state.session_ready = True
    else:
        st.sidebar.write("Oops! 🐾 Looks like that key didn't unlock the door. Please enter a valid API key to unleash the magic. 🌟🔑")



#api_key_user = st.text_input('Enter your OpenAI API key', 'SH++++', type = 'password')
#st.write(api_key_user)
client = OpenAI(api_key=api_key_sidebar)


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

delimiter = "####"
cor_system_message = f"""
As a world-class dog nutritionist, pet parents seek your expertise for their furry companions. You will provide answers that are personalised \
     to the individual user's query about their specific dog and not general advice. Follow these steps to address their queries, delimited by four hashtags, i.e., {delimiter}.

Step 1:{delimiter} Grasp the specifics of the pet parent's inquiry regarding their dog's nutrition.
Step 2:{delimiter} Assess if any assumptions are made by the pet parent. If there are any wrong assumptions, politely craft a response to correct their assumption
Step 3:{delimiter} Unless covered in the conversation, craft a generic advice for the query
Step 4:{delimiter} Now to provide a quantitative, personalised and actionable reponse, assess what additional information you would need.  \ 
If you need these additional information, go to next step else you can skip the next step
Step 5:{delimiter} Formulate a precise follow-up question to gather specific details about their dog.  \ 
Elucidate how the provided information will shape personalized guidance.
Step 6: {delimiter} \ 
Craft a response that addresses the specific inquiry made by the pet parent. If there are any assumptions in their inquiry (as per Step 2), gently steer things in the right \ 
direction with a friendly correction. Move on to provide \ 
a short, casual yet informative response, including the generic advice mentioned in Step 3. Keep it light, concise and conversational, like chatting with a friend who's \ 
seeking advice on their dog's diet. Conclude the response by inviting them to share any additional details about their dog, \ 
as mentioned in Step 5, and emphasize how this information would contribute to tailoring personalized guidance for their pet. Short, sweet, and to the point.

Provide the response in the following format WITHOUT skipping any step and add {delimiter} to separate every step:
Step 1:{delimiter} <step 1 reasoning> \n
Step 2:{delimiter} <step 2 reasoning> \n
Step 3:{delimiter} <step 3 reasoning> \n
Step 4:{delimiter} <step 4 reasoning> \n
Step 5:{delimiter} <step 5 reasoning> \n
Step 6:{delimiter} <step 6 reasoning> \n

Maintain the above structure to provide a response.  Make sure to include {delimiter} to separate every step
"""

if st.session_state.session_ready:
    st.text("Let's go 🚀")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        cor_response_messages =  {'role':'system', 'content': cor_system_message}
        st.session_state.messages.append(cor_response_messages )

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about dog nutrition!🐶💡"):
        
        with st.spinner('Finding answers...'):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            st.spinner("Looking for answers...")
            with st.chat_message("assistant", avatar= "🤖"):

                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=False,
                )
                pre_final_response = stream.choices[0].message.content.split("Step 6:")[-1].strip()
                final_response = pre_final_response.split(delimiter)[-1].strip()
                # Using a generator expression
                #streamer = (char for char in final_response)
                response = st.write_stream(stream_data(final_response))
                
            
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.text_area("","Hey there! 🌟 Ready to kick things off? Just pop in your valid OpenAI key on the left sidebar to harness the capabilities of our agent. 🚀🔑")
