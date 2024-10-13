import streamlit as st
from openai import OpenAI

st.title("Cover Letter Builder for Product Managers")

st.sidebar.title("PMResumes")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

try:
  client = OpenAI(api_key=openai_api_key)
except AuthenticationError as e:
  # Handle the error and display a user-friendly message
  error_message = str(e).split(" - ")[1]  # Extract error details
  st.error(f"Invalid OpenAI API Key: {error_message}. Please check your key and try again.")
  client = None  # Set client to None to prevent further API calls


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature,
    max_tokens=max_tokens)
    return response.choices[0].message.content

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
    #response = "response"
    return response


st.sidebar.title("Cover Letter Builder")
name = st.sidebar.text_input("Name")
role = st.sidebar.selectbox("Role", ["Product Manager", "Product Owner", "Business Analyst", "Senior Product Manager", "Senior Product Owner", "Head of Product", "Chief Product Officer"])
jd = st.sidebar.text_area("Job Description")
cv = st.sidebar.text_area("Resume")

if st.sidebar.button("AI Generate Cover Letter"):
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key.")
    else:
        cover_letter = generate_cover_letter(name, role, jd, cv)
        st.sidebar.success("Cover Letter Generated!")
        st.write(cover_letter)
