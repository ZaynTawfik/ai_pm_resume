import streamlit as st
from openai import OpenAI, AuthenticationError, APIError

# Page title
st.title("AI Resume Builder for Product Managers")

st.sidebar.title("PMResumes")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

client = None  # Initialize client as None

# Try to initialize OpenAI client with the provided key
if openai_api_key:
    try:
        client = OpenAI(api_key=openai_api_key)
    except AuthenticationError:
        st.sidebar.error("Invalid OpenAI API Key. Please check your key or get a new one from the [OpenAI API Keys page](https://platform.openai.com/account/api-keys).")
        client = None  # Ensure client remains None if there's an authentication error


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    # Prevent API call if the client is None
    if client is None:
        st.error("OpenAI client is not initialized due to an invalid API key.")
        return None
    
    # Catch potential API call errors and display a friendly message
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except APIError as e:
        st.error(f"An error occurred while making a request to OpenAI: CHeck your API Key")
        return None

def generate_resume(name, role, jd, cv):
    cv_delimiter = "####"
    jd_delimiter = "$$$$"
    system_message = f"""
    You are an AI Resume builder for Product Managers. \
    The job description of the role will be given to you \
    delimited by \
    {jd_delimiter} characters.
    The current resume of the candidate will be given to you \
    delimited by \
    {jd_delimiter} characters.    
    Generate a perfect Resume that will maximize the \
    chances of the candidate in landing the role by modifying the existing resume.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{cv_delimiter}{cv}{cv_delimiter}{jd_delimiter}{jd}{jd_delimiter}"},
    ]
    response = get_completion_from_messages(messages)
    #response = "response"
    return response

st.sidebar.title("AI Resume Builder")
name = st.sidebar.text_input("Name")
role = st.sidebar.selectbox("Role", ["Product Manager", "Product Owner", "Business Analyst", "Senior Product Manager", "Senior Product Owner", "Head of Product", "Chief Product Officer"])
jd = st.sidebar.text_area("Job Description")
cv = st.sidebar.text_area("Current Resume")

if st.sidebar.button("AI Generate Resume"):
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key.")
    elif client is None:
        st.sidebar.error("Invalid OpenAI API Key. Please verify your key at the [OpenAI API Keys page](https://platform.openai.com/account/api-keys).")
    else:
        resume = generate_resume(name, role, jd, cv)
        if resume:
            st.sidebar.success("Resume Generated!")
            st.write(resume)
        else:
            st.sidebar.error("Failed to generate Resume. Please check your inputs and try again.")    
