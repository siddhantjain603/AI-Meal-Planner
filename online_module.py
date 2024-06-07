from openai import OpenAI
import os
import streamlit as st
from PIL import Image
import requests
from io import BytesIO


#########################################33
#Setup openAi

def setup_openai(apikey):

    os.environ['OPENAI_API_KEY'] = apikey
    OpenAI.api_key = apikey
    client = OpenAI()

    return client

#################################################################
#############################################################

# Generating text from audio
def generate_text_from_audio_openai(client, audio_file,model="whisper-1",response_format="text"):
    
    response = client.audio.transcriptions.create(
        model = model,
        file = audio_file,
        response_format = response_format
    )

    return response

def generate_image_openai(client, prompt,model="dall-e-2",size="1024x1024",quality="standard",n=1):

    response = client.images.generate(
        model = model,
        prompt=prompt,
        size = size,
        quality = quality,
        n = n
    )

    image_url = response.data[0].url
    image = requests.get(image_url)
    image = Image.open(BytesIO(image.content))

    return image

def generate_text_openai_streamlit(client, prompt,text_area_placeholder=None,
                                   model="gpt-3.5-turbo", temperature=0.5,
                                   max_tokens=3000, top_p=1, frequency_penalty=0,
                                   presence_penalty=0, stream=True, html=False):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stream=stream
    )
    complete_response = []
    for chunk in response:
        # Ensure that chunk content is not None before appending
        if chunk.choices[0].delta.content:
            complete_response.append(chunk.choices[0].delta.content)
            result_string = ''.join(complete_response)  # Join without additional spaces
 
            # Auto Scroll
            lines = result_string.count('\n') + 1
            avg_chars_per_line = 80  # Adjust based on expected average line length
            lines += len(result_string) // avg_chars_per_line
            height_per_line = 20  # Adjust as needed
            total_height = lines * height_per_line
 
 
            if text_area_placeholder:
                if html:
                    text_area_placeholder.markdown(result_string, unsafe_allow_html=True)
                else:
                    text_area_placeholder.text_area("Generated Text", value=result_string,height=total_height)
 
    result_string = ''.join(complete_response)
    words = len(result_string.split())  # This is an approximation
    # st.text(f"Total Words Generated: {words}")
 
    return result_string


def main():
    pass
    
    client = setup_openai(apikey)

    #  # ##### Text generation ####
    # st.title("Text Generation using OpenAI API")
    # prompt = st.text_input("Enter your prompt", value="Write an essay on computer vision")
    # text_area_placeholder = st.empty()
    # if st.button("Generate Text"):
    #     result = generate_text_openai_streamlit(client, prompt, text_area_placeholder,html=True)

    ######### IMAGE GENERATION #############333
    st.title("Image generation using OpenAI")
    prompt = st.text_input("Enter your prompt", value="A cute cat jumping over a fence, cartoon, colorful.")

    if st.button("Generate Image"):
        with st.spinner("Generating image..."):
            image = generate_image_openai(client, prompt)                            
            st.image(image)



    ########## AUDIO TRANSCRIPTION ###################333
    # st.title("Audio transcription using OpenAI")
    # audio_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav"])

    # if audio_file:
    #     if st.button("Transcribe"):
    #         st.audio(audio_file, format='audio/wav')
    #         with st.spinner('Transcribing audio...'):
    #             response = generate_text_from_audio_openai(client, audio_file)
    #             st.write(response)

if __name__=="__main__":
    main()