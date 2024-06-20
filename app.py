import os
import google.generativeai as genai
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('google_api_key'))

# prepare model

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

# convert image into bytes 

def get_input_text(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {

            'mime_type' : uploaded_file.type,
            'data': bytes_data
            }
        ]
        return image_parts
    
    else:
        raise FileNotFoundError("No File Is Uploaded")
    
#streamlit app

st.header("Health Advisor :smile: ")
uploaded_file=st.sidebar.file_uploader('upload your file..',type=['jpg','png','jpeg'])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption='your pic')


submit=st.sidebar.button(" Calories Present")
age=st.sidebar.number_input("age")
weight=st.sidebar.number_input("weight")

st.sidebar.markdown("# Weight Loss")
submit1=st.sidebar.button("Food you should avoid ")
submit2=st.sidebar.button("Food you should add")


# desinging Prompt

input_prompt='''
    You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
'''

input_prompt1='''
    You are an expert in nutritionist where you need to see the food items from the image
    based on age :{age} and weight: {weight} provide the person age and weight in response ,

    calculate the total calories present in food item in an image,
    your task is to suggest what food item should intake if person want to loose weight, 
    and what food item should avoid on the basis of image .

    Briefly summarize the overall  meal and suggest if it aligns with your weight loss goals.

'''

input_prompt2='''
     You are an expert in nutritionist where you need to see the food items from the image,
     If applicable, suggests a food item based on age :{age} and weight: {weight} which is provided by people ,
     from the image that could be beneficial for weight loss.

     Includes the name and a short description amd the total calories.

  """

'''


if submit:
    if uploaded_file is not None:
        image_data=get_input_text(uploaded_file)
        response=get_gemini_response(input_prompt,image_data)

        st.subheader("Calories Present in your food : ")
        st.write(response)


if submit1:
    if uploaded_file is not None:
        image_data=get_input_text(uploaded_file)
        response=get_gemini_response(input_prompt1,image_data)

        st.subheader("The Response Is")
        st.write(response)


if submit2:
    if uploaded_file is not None:
        image_data=get_input_text(uploaded_file)
        response=get_gemini_response(input_prompt2,image_data)

        st.subheader("The Response Is")
        st.write(response)