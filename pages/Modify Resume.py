import streamlit as st
from openai import OpenAI, AuthenticationError, APIError
import streamlit.components.v1 as components

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


def get_completion_from_messages(messages, model="gpt-4o", temperature=0, max_tokens=8192):
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

html_template= """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 20px;
    }
    h1, h2, h3, h4 {
      color: #333;
    }
    .section-title {
      font-size: 24px;
      font-weight: bold;
      margin-top: 20px;
      border-bottom: 1px solid #ddd;
    }
    .section-content {
      margin-bottom: 20px;
    }
    .personal-info {
      font-size: 18px;
      margin-bottom: 20px;
    }
    .contact-info {
      font-size: 16px;
    }
    .job-title {
      font-weight: bold;
    }
    .job-duration {
      font-style: italic;
      color: #555;
    }
    ul {
      margin: 5px 0;
      padding-left: 20px;
    }
    a {
      color: #0066cc;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <!-- Personal Information -->
  <div class="personal-info">
    <h1>__full_name__</h1>
    <p class="contact-info">
      __location__ | <a href="__linkedin_url__">LinkedIn</a> | __phone__ | __email__ | 
      GitHub: <a href="__github_url__">GitHub</a>
    </p>
  </div>

  <!-- Summary -->
  <div class="section-content">
    <div class="section-title">SUMMARY</div>
    <p>__summary_text__</p>
  </div>

  <!-- Employment and Work Experience -->
  <div class="section-content">
    <div class="section-title">EMPLOYMENT AND WORK EXPERIENCE</div>

    <div class="job">
      <p class="job-title">__job_title_1__ at __company_1__</p>
      <p class="job-duration">__job_duration_1__</p>
      <ul>
        <li>__job_responsibility_1a__</li>
        <li>__job_responsibility_1b__</li>
        <li>__job_responsibility_1c__</li>
      </ul>
    </div>

    <div class="job">
      <p class="job-title">__job_title_2__ at __company_2__</p>
      <p class="job-duration">__job_duration_2__</p>
      <ul>
        <li>__job_responsibility_2a__</li>
        <li>__job_responsibility_2b__</li>
        <li>__job_responsibility_2c__</li>
      </ul>
    </div>
  </div>

  <!-- Education -->
  <div class="section-content">
    <div class="section-title">EDUCATION</div>

    <div class="degree">
      <p><strong>__degree_1__</strong> – __university_1__ | __graduation_date_1__</p>
      <ul>
        <li>GPA: __gpa_1__</li>
        <li>Relevant coursework: __coursework_1a__, __coursework_1b__</li>
        <li>Project: __project_1__</li>
      </ul>
    </div>
  </div>

  <!-- Skills -->
  <div class="section-content">
    <div class="section-title">SKILLS</div>
    <ul>
      <li>__skill_1__</li>
      <li>__skill_2__</li>
      <li>__skill_3__</li>
    </ul>
  </div>

</body>
</html>
"""

def generate_resume(name, role, jd, cv):
    cv_delimiter = "####"
    jd_delimiter = "$$$$"
    htm_delimiter = "^^^^"
    system_message = f"""
    You are an AI Resume builder for Product Roles. \
    The job description of the role will be given to you \
    delimited by \
    {jd_delimiter} characters.
    The current resume of the candidate will be given to you \
    delimited by \
    {jd_delimiter} characters.    
    Generate a perfect Resume that will maximize the \
    chances of the candidate in landing the role by modifying the existing resume.
    The generated resume should be outputted in html format. The template for the html will be \
    provided to you delimited by {htm_delimiter} characters.
    Replace all placeholders in the HTML template (e.g., __full_name__, __job_title_1__, etc.) with the corresponding candidate information.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{cv_delimiter}{cv}{cv_delimiter}{jd_delimiter}{jd}{jd_delimiter}{htm_delimiter}{html_template}{htm_delimiter}"},
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
            components.html(resume, height=1000, scrolling=True)
            st.html(resume)
        else:
            st.sidebar.error("Failed to generate Resume. Please check your inputs and try again.")    
