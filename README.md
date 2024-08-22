# AI-Meal-Planner

## Overview

AI-Meal-Planner is a web application that helps users create personalized meal plans based on their physical attributes and dietary goals. The application leverages OpenAI's GPT-3.5-turbo model to generate a detailed meal plan tailored to user inputs, including gender, weight, age, height, and dietary preferences.

## Files

- **`ai_meal_planner.py`**: Main script that sets up the Streamlit interface, gathers user inputs, and generates meal plans using OpenAI's API.
- **`online_module.py`**: Contains utility functions for setting up the OpenAI client and generating text.
- **`.env`**: Environment file to store the OpenAI API key. Ensure this file is present with the correct key (`OPENAI_API_KEY`).
- **`requirements.txt`**: Lists the Python dependencies required for the project.

## Setup

### 1. Clone the Repository

- git clone https://github.com/yourusername/AI-Meal-Planner.git
- cd AI-Meal-Planner
  
### 2. Install Dependencies

- pip install -r requirements.txt

### 3. Configure Environment Variables

- OPENAI_API_KEY=your_openai_api_key

### 4. Run the Application

- streamlit run ai_meal_planner.py

## Usage

### 1. Input User Data

- Gender: Select from 'Male', 'Female', or 'Other'.
- Weight (kg): Enter your weight.
- Age: Enter your age.
- Height (cm): Enter your height.
- Aim: Select your goal (Lose, Gain, or Maintain weight).
- Diet Type: Choose between 'Veg' or 'Veg + Non-Veg'.

### 2. Generate Meal Plan

- Click the "Generate Meal Plan" button.
- The application will process the input data and display a personalized meal plan for 7 days, including ideal weight range, target weight, BMI, total days to reach the target weight, weight to lose or gain per week, and daily meal suggestions.
