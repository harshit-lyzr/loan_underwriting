import os
import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
api = os.getenv('OPENAI_API_KEY')

st.set_page_config(
    page_title="Loan Underwriting Expert🏦",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.sidebar.title("Loan Underwriting Expert")
st.sidebar.markdown("## Welcome to the Lyzr Loan Underwriting Expert!")
st.sidebar.markdown("You Have to Enter Your Personal And Business Details.This app Will Generates Executive Summary,Business Description and Sector Analysis.")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)


def generate_underwriting():
    loan_agent = Agent(
        role="Loan Consultant",
        prompt_persona=f"You are an Expert Loan Underwriter.Your Task is to generate Executive summary,Business Description and sector analysis."
    )

    prompt = f"""
    You are a loan Underwriting expert.Your Task is to generate Executive summary,Business Description and sector analysis.
    Based On Below Input:
    Name:{st.session_state.form1_data['name']}
    Age: {st.session_state.form1_data['age']}
    Employment Type: {st.session_state.form1_data['employment_type']}
    Country: {st.session_state.form1_data['country']}
    Business Name: {st.session_state.form2_data['business_name']}
    Business Description: {st.session_state.form2_data['business_description']}
    Business Sector: {st.session_state.form2_data['sector']}
    Credit Score: {st.session_state.form2_data['credit_score']}
    Loan Amount: {st.session_state.form2_data['loan_amount']}

    Example:
    Certainly, here's how you might structure those sections for a loan underwriting document:

    **Executive Summary:**
    The executive summary provides a concise overview of the loan request, highlighting key points for consideration by the underwriter.

    Executive Summary:
    [Business Name] is seeking a [Loan Amount] loan to [Purpose of Loan]. With [Number of Years] years of successful operation in the [Industry/Sector], [Business Name] has demonstrated steady growth and profitability. The requested funds will be used to [Briefly Explain Purpose]. [Business Name] has a strong management team with [Number of Years] years of combined experience, and the collateral provided offers sufficient security for the loan. The financial projections indicate the ability to comfortably service the debt, with a projected [Repayment Plan]. Overall, the loan presents a low risk with significant potential for mutual benefit.

    **Business Description:**
    The business description provides detailed information about the company, its history, operations, products/services, market position, and management team.

    Business Description:
    [Business Name] is a [Type of Business] located in [Location]. Established in [Year], the company specializes in [Products/Services]. Our target market includes [Target Market Description]. [Business Name] distinguishes itself through [Unique Selling Proposition]. Our management team includes [Names and Positions], each bringing [Number of Years] years of experience in [Industry/Sector]. With a focus on [Core Values or Objectives], [Business Name] has built a strong reputation for [Quality/Service/Innovation]. We operate from [Number of Locations] locations and have a workforce of [Number of Employees].

    **Sector Analysis:**
    The sector analysis provides an overview of the industry or sector in which the business operates, including market trends, competition, regulatory environment, and growth opportunities.

    Sector Analysis:
    The [Industry/Sector] is characterized by [Key Trends], including [Trend 1], [Trend 2], and [Trend 3]. Market demand for [Products/Services] continues to grow due to [Reasons for Growth]. However, the sector faces challenges such as [Challenges], including [Challenge 1] and [Challenge 2]. Competition is intense, with major players including [Competitors] dominating market share. Regulatory factors such as [Regulatory Factor 1] and [Regulatory Factor 2] impact industry operations. Despite challenges, the sector presents opportunities for growth, particularly in [Opportunity Areas]. [Business Name] is well-positioned to capitalize on these opportunities due to [Strengths], including [Strength 1] and [Strength 2].

    These sections provide a comprehensive overview of the business and its operating environment, aiding the underwriter in assessing the loan request.
    """

    loan_task = Task(
        name="loan Consult",
        model=open_ai_text_completion_model,
        agent=loan_agent,
        instructions=prompt,
    )

    output = LinearSyncPipeline(
        name="loan underwriting Pipline",
        completion_message="pipeline completed",
        tasks=[
            loan_task
        ],
    ).run()

    answer = output[0]['task_output']

    return answer


# Main function to run the Streamlit app
def main():
    # Initialize session state to store form data
    if 'form1_data' not in st.session_state:
        st.session_state.form1_data = {"name": "", "age": "", "employment_type": "", "country": ""}
    if 'form2_data' not in st.session_state:
        st.session_state.form2_data = {"credit_score": "", "loan_amount": "", "business_name": "", "business_description": "", "sector": ""}

    # Create sidebar navigation
    page = st.sidebar.radio("Navigation", ["Personal Information", "Business Information", "Result"])

    if page == "Personal Information":
        st.title("Personal Information")
        with st.form(key='form1'):
            st.session_state.form1_data['name'] = st.text_input("Enter your name:", st.session_state.form1_data['name'])
            st.session_state.form1_data['age'] = st.text_input("Enter your age:", st.session_state.form1_data['age'])
            st.session_state.form1_data['employment_type'] = st.selectbox("Enter your age:", ["Full Time", "Part Time", "Contract", "Freelance"], index=0 if st.session_state.form1_data['employment_type'] == "" else ["Full Time", "Part Time", "Contract", "Freelance"].index(st.session_state.form1_data['employment_type']))
            st.session_state.form1_data['country'] = st.selectbox("Select your country:", ["USA", "Canada", "UK", "Australia"], index=0 if st.session_state.form1_data['country'] == "" else ["USA", "Canada","UK","Australia"].index(st.session_state.form1_data['country']))
            submit_button = st.form_submit_button(label='Submit Form 1')
            if st.session_state.form1_data['name'] == "":
                st.error("Enter Your Name")

    elif page == "Business Information":
        st.title("Business Information")
        with st.form(key='form2'):
            st.session_state.form2_data['business_name'] = st.text_input("Business Name:",st.session_state.form2_data['business_name'])
            st.session_state.form2_data['business_description'] = st.text_input("Business Description:",st.session_state.form2_data['business_description'])
            st.session_state.form2_data['sector'] = st.text_input("Business Sector:",st.session_state.form2_data['sector'])
            st.session_state.form2_data['credit_score'] = st.text_input("Credit Score:", st.session_state.form2_data['credit_score'])
            st.session_state.form2_data['loan_amount'] = st.text_input("Loan Amount:", st.session_state.form2_data['loan_amount'])

            submit_button = st.form_submit_button(label='Submit Form 2')

    elif page == "Result":
        st.title("Result Page")
        result = generate_underwriting()
        st.markdown(result)

if __name__ == "__main__":
    main()
