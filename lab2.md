https://github.com/blejdzior/azure/blob/main/lab2.md

## Zadanie 10. - Program w Python pozwalający na tłumaczenie tekstu z dowolnego języka na wybrany przy pomocy OpenAI API.

### 1. Wygenerowanie klucza API OpenAI 

#### a. Wejdź na [platformę OpenAI API](https://platform.openai.com)

#### b. Przejdź do "Settings" -> "API Keys".

#### c. Kliknij "Create new secret key".

### 2. Przypisz wygenerowany klucz API do zmiennej środowiskowej **OPENAI_API_KEY**

#### a. Utwórz plik **.env** w folderze z plikiem z kodem źródłowym programu.

#### b. W utworzonym wpliku wpisz tekst:
```Python
OPENAI_API_KEY="Your_API_Key"
```

### 3. Program w Python

#### a. Dołączanie bibliotek oraz odczytanie zmiennych środowiskowych:
```Python
import openai
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv() # odczytanie zmiennych środowiskowych z pliku .env
```

#### b. Zdefiniowanie funkcji wywołującej API OpenAI
```Python
# text - tekst do przetłumaczenia
# target_language - język, na któy zostanie przetłumaczony tekst
def translate_text( text, target_language):
    # Utworzenie klienta do komunikacji z API, konstruktor OpenAI() standardowo odczytuje klucz API ze zmiennej środowiskowej.
    client = OpenAI()
    try:
        # Zapytanie API typu tekstowego. 
        response = client.chat.completions.create( 
            model="gpt-4o-mini",  # Wybór modelu, który zostanie wykorzystany do wygenerowania odpowiedzi 
            messages=[
                # Wiadomości roli System określają odgórne instrukcje co do zachowania i/lub funkcji modelu
                {"role": "system", "content": "You are a helpful translator."},  
                # Wiadomość roli User jest wiadomością wejściową dla modelu, na tę wiadomość zostanie udzielona odpowiedź
                {"role": "user", "content": f"Translate the following text to {target_language}:\n{text}"}  
        )
        # Funkcja zwraca odpowiedź od API
        translated_text = response.choices[0].message.content
        return translated_text
    
    # Obsługa dowolnego błędu API -- Wszystkie błędy w API OpenAI dziedziczą po APIError
    except openai.APIError as e:
        return f"Error while accessing OpenAI API: {str(e)}"
```

#### c. Obsługa inputu od użytkownika, wywołanie funkcji translate_text, wyświetlenie tłumaczenia
```Python
if __name__ == "__main__":
    text = input("Enter the text you want to translate: ")
    target_language = input("Enter the target language (e.g., English): ")
    translation = translate_text(text, target_language)
    print("\nTranslated Text:")
    print(translation)
````

#### d. Przykład działania

> Enter the text you want to translate:
>
> Je m’appelle Jessica. Je suis une fille, je suis française et j’ai treize ans. Je vais à l’école à Nice, mais j’habite à Cagnes-Sur-Mer. J’ai deux frères. Le premier s’appelle Thomas, il a quatorze ans. Le second s’appelle Yann et il a neuf ans. Mon papa est italien et il est fleuriste. Ma mère est allemande et est avocate. Mes frères et moi parlons français, italien et allemand à la maison. Nous avons une grande maison avec un chien, un poisson et deux chats.
> 
> Enter the target language (e.g., English): Polish

>
>Translated Text:
>
>Nazywam się Jessica. Jestem dziewczyną, jestem Francuzką i mam trzynaście lat. Chodzę do szkoły w Nicei, ale mieszkam w Cagnes-Sur-Mer. Mam dwóch braci. Pierwszy nazywa się Thomas, ma czternaście lat. Drugi nazywa się Yann i ma dziewięć lat. Mój tata jest Włochem i jest kwiaciarzem. Moja mama jest Niemką i jest prawniczką. Moi bracia i ja mówimy po francusku, włosku i niemiecku w domu. Mamy duży dom z psem, rybą i dwoma kotami.

