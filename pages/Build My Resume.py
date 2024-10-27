import streamlit as st
from openai import OpenAI, AuthenticationError, APIError
import streamlit.components.v1 as components

# Page title
st.title("Product Resume Generator")


openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

st.sidebar.title("PMResumes")

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


def generate_nresume(role, name, phone, linkedin, location, education_list, experience_list, certifications_list, skills_input):
    inp_delimiter = "####"
    htm_delimiter = "$$$$"
    system_message = f"""
    You are an AI Resume builder for {role} \
    The details of the candidate required to generate the resume will be provided to you delimited by
    {inp_delimiter} characters.
    The generated resume should be outputted in html format. The template for the html will be \
    provided to you delimited by {htm_delimiter} characters.
    Replace all placeholders in the HTML template (e.g., __full_name__, __job_title_1__, etc.) with the corresponding candidate information.   
    Generate a perfect Resume that will maximize the \
    chances of the candidate in landing the role.
    The summary section should accurately reflect the candidates fit for the role.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{inp_delimiter}Name:{name}, Phone:{phone}, LinkedIn Profile Link:{linkedin}, Location:{location}, Education (as a list): {education_list}, Work Experiences (as a list){experience_list}, Additional Qualifications or Certifications (as a list): {certifications_list}, Skills (seperated by commas){skills_list}{inp_delimiter}{htm_delimiter}{html_template}{htm_delimiter}"},
    ]
    response = get_completion_from_messages(messages)
    #response = "n res response"
    return response

role = st.sidebar.selectbox("Role", ["Product Manager", "Product Owner", "Business Analyst", "Senior Product Manager", "Senior Product Owner", "Head of Product", "Chief Product Officer"])
st.sidebar.header("Personal Information")
name = st.sidebar.text_input("Full Name")
phone = st.sidebar.text_input("Phone Number")
linkedin = st.sidebar.text_input("LinkedIn Profile Link")
location = st.sidebar.text_input("Location (City, Country)")

# --- EDUCATION SECTION ---
st.sidebar.header("Education")
education_list = []
if 'education_count' not in st.session_state:
    st.session_state.education_count = 1

for i in range(st.session_state.education_count):
    st.sidebar.subheader(f"Education {i+1}")
    university = st.sidebar.text_input(f"University {i+1}", key=f'university_{i}')
    degree = st.sidebar.text_input(f"Degree {i+1}", key=f'degree_{i}')
    grad_year = st.sidebar.text_input(f"Graduation Year {i+1}", key=f'grad_year_{i}')
    education_list.append({
        "university": university,
        "degree": degree,
        "grad_year": grad_year
    })

if st.sidebar.button("Add Education"):
    st.session_state.education_count += 1

# --- WORK EXPERIENCE SECTION ---
st.sidebar.header("Work Experience")
experience_list = []
if 'work_experience_count' not in st.session_state:
    st.session_state.work_experience_count = 1

for i in range(st.session_state.work_experience_count):
    st.sidebar.subheader(f"Work Experience {i+1}")
    org = st.sidebar.text_input(f"Organization {i+1}", key=f'org_{i}')
    job_title = st.sidebar.text_input(f"Job Title {i+1}", key=f'job_title_{i}')
    work_location = st.sidebar.text_input(f"Location {i+1}", key=f'work_location_{i}')
    start_date = st.sidebar.text_input(f"Start Date {i+1} (MM/YYYY)", key=f'start_date_{i}')
    end_date = st.sidebar.text_input(f"End Date {i+1} (MM/YYYY)", key=f'end_date_{i}')
    experience_list.append({
        "organization": org,
        "job_title": job_title,
        "work_location": work_location,
        "start_date": start_date,
        "end_date": end_date
    })

if st.sidebar.button("Add Work Experience"):
    st.session_state.work_experience_count += 1

# --- CERTIFICATIONS/QUALIFICATIONS SECTION ---
st.sidebar.header("Certifications and Additional Qualifications")
certifications_list = []
if 'cert_count' not in st.session_state:
    st.session_state.cert_count = 1

for i in range(st.session_state.cert_count):
    st.sidebar.subheader(f"Certification {i+1}")
    cert_name = st.sidebar.text_input(f"Certification/Qualification Name {i+1}", key=f'cert_name_{i}')
    cert_location = st.sidebar.text_input(f"Location {i+1}", key=f'cert_location_{i}')
    issuing_org = st.sidebar.text_input(f"Issuing Organization {i+1}", key=f'issuing_org_{i}')
    cert_date = st.sidebar.text_input(f"Date or Year {i+1}", key=f'cert_date_{i}')
    certifications_list.append({
        "cert_name": cert_name,
        "cert_location": cert_location,
        "issuing_org": issuing_org,
        "cert_date": cert_date
    })

if st.sidebar.button("Add Certification"):
    st.session_state.cert_count += 1

# --- SKILLS SECTION ---
st.sidebar.header("Skills")
skills_input = st.sidebar.text_input("List your skills (separated by commas)")
skills_list = [skill.strip() for skill in skills_input.split(",") if skill]

# --- FINAL SUBMISSION ---
if st.sidebar.button("AI Generate Resume"):
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key.")
    elif client is None:
        st.sidebar.error("Invalid OpenAI API Key. Please verify your key at the [OpenAI API Keys page](https://platform.openai.com/account/api-keys).")    
    else:
        nresume = generate_nresume(role, name, phone, linkedin, location, education_list, experience_list, certifications_list, skills_input)
        if nresume:
            st.sidebar.success("Resume Generated!")
            #st.markdown(nresume, unsafe_allow_html=True)
            components.html(nresume, height=1000, scrolling=True)
            #st.write(nresume)
        else:
            st.sidebar.error("Failed to generate the resume. Please check your inputs and try again.")
        st.write(certifications_list)
        st.write(skills_list)
        st.write(skills_input)
