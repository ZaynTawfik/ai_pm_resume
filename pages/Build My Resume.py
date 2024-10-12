import streamlit as st

st.sidebar.title("PMResumes")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature,
    max_tokens=max_tokens)
    return response.choices[0].message.content

def generate_nresume(name, phone, linkedin, location, education_list, experience_list, certifications_list, skills_list):
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
        {'role': 'user', 'content': f"{cv_delimiter}{cv_delimiter}{jd_delimiter}{jd_delimiter}"},
    ]
    #response = get_completion_from_messages(messages)
    response = "n res response"
    return response

# Page title
st.title("Product Resume Generator")

# --- PERSONAL INFO ---
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
if st.sidebar.button("AI Generate Cover Letter"):
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key.")
    else:
        nresume = generate_nresume(name, phone, linkedin, location, education_list, experience_list, certifications_list, skills_list)
        st.sidebar.success("Resume Generated!")
        st.write(nresume)
        st.write(certifications_list)
        st.write(skills_list)
        st.write(skills_input)
        

