import openai
from openai import OpenAI



def translate_text( text, target_language):
    print('Translating...')
    client = OpenAI()
    try:
        response = client.chat.completions.create( 
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": f"Translate the following text to {target_language}, answer with just the translated text:\n{text}"}]
            )
        translated_text = response.choices[0].message.content
        return translated_text
    except openai.APIError as e:
        return f"Error while accessing OpenAI API: {str(e)}"




