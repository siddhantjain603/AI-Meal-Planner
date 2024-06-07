from online_module import * 
from dotenv import load_dotenv
import json
import time
import os

# Calling api key from .env
load_dotenv()
apikey = os.getenv  ('OPENAI_API_KEY')
 
st.markdown('<p class="title">AI Meal Planner</p>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
        /* Style for title */
        .title {
            text-align: center !important;
            padding-bottom: 20px;
            color: white;
            font-size: 60px;
            font-weight: bold;
    </style>
    """,
    unsafe_allow_html=True
)
 
client = setup_openai(apikey)
 
# Create columns for inputs
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox('Gender', ('Male', 'Female', 'Other'))
    weight = st.number_input('Weight (kg):', min_value=30, value=80)
    aim = st.selectbox('Aim', ('Lose', 'Gain', 'Maintain'))
with col2:
    age = st.number_input('Age', min_value=18, max_value=120, step=1, value=30)
    height = st.number_input('Height (cm)', min_value=1, max_value=250, step=1, value=170)
    diet_type = st.selectbox('Diet Type', ('Veg', 'Veg + Non-Veg'))
 

 
user_data = f""" - I am a {gender}"
                - My weight is {weight} kg"
                - I am {age} years old"
                - My height is {height} cm"
                - My aim is to {aim} weight"
                - I want a {diet_type} diet
             """
output_format = """ "range":"Range of ideal weight",
                    "target":"Target weight",
                    "difference":"Weight i need to loose or gain",
                    "bmi":"my BMI",
                    "meal_plan":"Complete Meal plan for 7 days in pointers",
                    "total_days":"Total days to reach target weight",
                    "weight_per_week":"Weight to loose or gain per week",
                                    """
 
prompt = user_data + (" given the information ,follow the output format as follows."
                      " Give only json format nothing else ") + output_format
 
if st.button("Generate Meal Plan"):

    progress_bar = st.progress(5)
    with st.spinner('Creating Meal plan'):

        text_area_placeholder = st.empty()
        meal_plan = generate_text_openai_streamlit(client, prompt)

        progress_bar.progress(10)
        for percent_complete in range(10, 101, 10):
            progress_bar.progress(percent_complete)
            time.sleep(0.2) 
        # progress_bar.progress(100)
        # Check if the string starts with ```json and remove it
        if meal_plan.startswith("```json"):
            meal_plan = meal_plan.replace("```json\n", "", 1)  # Remove the first occurrence
        if meal_plan.endswith("```"):
            meal_plan = meal_plan.rsplit("```", 1)[0]  # Remove the trailing part
 
        meal_plan_json = json.loads(meal_plan)
 
        st.title("Meal Plan")
        col1, col2, col3 = st.columns(3)    
        with col1:
            st.subheader("Range")
            st.write(meal_plan_json["range"])
            st.subheader("Target")
            st.write(meal_plan_json["target"])
        with col2:
            st.subheader("BMI")
            st.write(meal_plan_json["bmi"])
            st.subheader("Days")
            st.write(meal_plan_json["total_days"])
 
        with col3:
            st.subheader(f"{aim}")
            st.write(meal_plan_json["difference"])
            st.subheader("Per week")
            st.write(meal_plan_json["weight_per_week"])
 
        st.subheader("Meal plan for 7 days")

        for i in range(1,8):
            st.subheader("Day "+str(i))
            diets = meal_plan_json["meal_plan"]["Day "+str(i)].split(',')
            for diet in diets:
                st.write(diet)