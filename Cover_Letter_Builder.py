import streamlit as st
from openai import OpenAI, AuthenticationError, APIError
import streamlit.components.v1 as components

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

def generate_cover_letter(name, role, jd, cv):
    cv_delimiter = "####"
    jd_delimiter = "$$$$"
    cov_delimiter = "^^^^"
    system_message = f"""
    You are an AI Cover Letter builder for Product Managers. \
    The resume of the candidate will be given to you \
    delimited by \
    {cv_delimiter} characters.
    The job description of the role will be given to you \
    delimited by \
    {jd_delimiter} characters.
    The generated resume should be an html string. The template for the html will be \
    provided to you delimited by {cov_delimiter} characters.
    Replace all placeholders in the HTML template (e.g., __full_name__, __job_title_1__, etc.) with the corresponding candidate information.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{cv_delimiter}{cv}{cv_delimiter}{jd_delimiter}{jd}{jd_delimiter}{cov_delimiter}{cover_template}{cov_delimiter}"},
    ]
    response = get_completion_from_messages(messages)
    return response

cover_template="""
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 40px;
      color: #333;
    }
    .letter-container {
      max-width: 800px;
      margin: auto;
      padding: 20px;
      border: 1px solid #ddd;
      background-color: #f9f9f9;
    }
    .header, .footer {
      font-size: 16px;
    }
    .header p, .footer p {
      margin: 5px 0;
    }
    .date {
      text-align: right;
    }
    .body {
      margin-top: 20px;
    }
    .closing {
      margin-top: 20px;
    }
  </style>
</head>
<body>

  <div class="letter-container">
    <!-- Header Section -->
    <div class="header">
      <p><strong>[APPLICANT_NAME (if any)]</strong></p>
      <p>[APPLICANT_ADDRESS (if any)]</p>
      <p>[APPLICANT_CITY_STATE_ZIP (if any)]</p>
      <p>Email: [APPLICANT_EMAIL (if any)]</p>
      <p>Phone: [APPLICANT_PHONE (if any)]</p>
    </div>

    <!-- Date -->
    <div class="date">
      <p>[DATE]</p>
    </div>

    <!-- Recipient Section -->
    <div class="header">
      <p><strong>[RECIPIENT_NAME (if any)]</strong></p>
      <p>[RECIPIENT_TITLE (if any)]</p>
      <p>[COMPANY_NAME (if any)]</p>
      <p>[COMPANY_ADDRESS (if any)]</p>
    </div>

    <!-- Greeting -->
    <div class="body">
      <p>Dear Hiring Manager,</p>

      <!-- Cover Letter Body -->
      <p>[COVER_LETTER_BODY]</p>

      <!-- Closing Statement -->
      <p>Thank you for considering my application. I look forward to the opportunity to discuss how my background, skills, and enthusiasm align with the goals of [COMPANY_NAME]. Please feel free to reach out via [APPLICANT_PHONE] or [APPLICANT_EMAIL] to arrange a conversation.</p>
    </div>

    <!-- Closing Signature -->
    <div class="closing">
      <p>Sincerely,</p>
      <p><strong>[APPLICANT_NAME]</strong></p>
    </div>

    <!-- Footer Section (Optional) -->
    <div class="footer">
      <p>LinkedIn: <a href="[APPLICANT_LINKEDIN_URL]" target="_blank">[APPLICANT_LINKEDIN_URL]</a></p>
      <p>Portfolio: <a href="[APPLICANT_PORTFOLIO_URL]" target="_blank">[APPLICANT_PORTFOLIO_URL]</a></p>
    </div>
  </div>

</body>
"""

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
            components.html(cover_letter, height=1000, scrolling=True)
            #st.html(cover_letter)
            
        else:
            st.sidebar.error("Failed to generate a cover letter. Please check your inputs and try again.")
