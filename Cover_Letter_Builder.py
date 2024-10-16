import streamlit as st
from openai import OpenAI, AuthenticationError, APIError

# Page title
st.title("Cover Letter Builder for Product Managers")

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

def generate_cover_letter(name, role, jd, cv):
    cv_delimiter = "####"
    jd_delimiter = "$$$$"
    system_message = f"""
    You are an AI Cover Letter builder for Product Managers. \
    The resume of the candidate will be given to you \
    delimited by \
    {cv_delimiter} characters.
    The job description of the role will be given to you \
    delimited by \
    {jd_delimiter} characters.
    Generate a perfect Cover Letter that will maximize the \
    chances of the candidate in landing the role.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{cv_delimiter}{cv}{cv_delimiter}{jd_delimiter}{jd}{jd_delimiter}"},
    ]
    response = get_completion_from_messages(messages)
    return response


st.sidebar.title("Cover Letter Builder")
name = st.sidebar.text_input("Name")
role = st.sidebar.selectbox("Role", ["Product Manager", "Product Owner", "Business Analyst", "Senior Product Manager", "Senior Product Owner", "Head of Product", "Chief Product Officer"])
jd = st.sidebar.text_area("Job Description")
cv = st.sidebar.text_area("Resume")


if st.sidebar.button("AI Generate Cover Letter"):
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key m.")
    elif client is None:
        st.sidebar.error("Invalid OpenAI API Key. Please verify your key at the [OpenAI API Keys page](https://platform.openai.com/account/api-keys).")
    else:
        cover_letter = generate_cover_letter(name, role, jd, cv)
        if cover_letter:
            st.sidebar.success("Cover Letter Generated!")
            st.write(cover_letter)
        else:
            st.sidebar.error("Failed to generate a cover letter. Please check your inputs and try again.")
