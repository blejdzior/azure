import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from fpdf import FPDF
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes, OperationStatusCodes

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# Azure configuration
CUSTOM_VISION_ENDPOINT = "https://jk20241112custom-prediction.cognitiveservices.azure.com"
CUSTOM_VISION_API_KEY = "3OxS3QDN75puqOxezJFLozER72uaBDdO08ifHE3G2hOotAjtbwwdJQQJ99ALACPV0roXJ3w3AAAIACOGnEOf"
CUSTOM_VISION_PROJECT_ID = "811993ed-b609-4b0d-a0dd-909da9e823ba"
CUSTOM_VISION_MODEL_NAME = "Iteration3"

OCR_ENDPOINT = "https://jk11122024.cognitiveservices.azure.com/"
OCR_API_KEY = "2griPNS1eWM1EcUQklUi49z2mTSFNlgtU9kqW0BCUhycdOuVQml2JQQJ99ALACPV0roXJ3w3AAAFACOGMvax"

# Initialize Azure clients
cv_credentials = ApiKeyCredentials(in_headers={"Prediction-key": CUSTOM_VISION_API_KEY})
cv_client = CustomVisionPredictionClient(CUSTOM_VISION_ENDPOINT, cv_credentials)

computervision_client = ComputerVisionClient(OCR_ENDPOINT, ApiKeyCredentials({"Ocp-Apim-Subscription-Key": OCR_API_KEY}))

from urllib.parse import urlparse, urljoin


def get_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        base_tag = soup.find('base')
        if base_tag and 'href' in base_tag.attrs:
            base_url = base_tag['href']
        else:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        paragraphs = soup.find_all('p')
        images = soup.find_all('img')
        text = ' '.join([p.get_text() for p in paragraphs])

        image_urls = [urljoin(base_url, img['src']) for img in images if 'src' in img.attrs]

        return text, image_urls
    else:
        return None, None


# def convert_svg_to_png(svg_data):
#     return cairosvg.svg2png(bytestring=svg_data)

# Step 2: Check if images contain text
def image_contains_text(image_url):
    try:
        # Fetch the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Check if the content type is SVG
        content_type = response.headers.get('Content-Type', '')
        if 'svg' in content_type or image_url.lower().endswith('.svg'):
            print(f"Skipped SVG image: {image_url}")
            return False

        # Validate and convert the image using Pillow
        with Image.open(BytesIO(response.content)) as img:
            buffer = BytesIO()
            img.convert("RGB").save(buffer, format="JPEG")  # Ensure JPEG format
            buffer.seek(0)

            # Send image to Custom Vision
            results = cv_client.classify_image(CUSTOM_VISION_PROJECT_ID, CUSTOM_VISION_MODEL_NAME, buffer.read())

        # Analyze predictions
        for prediction in results.predictions:
            if prediction.tag_name == "Text" and prediction.probability > 0.5:
                return True

    except Exception as e:
        print(f"Error processing image: {image_url}. Error: {e}")

    return False



import io
import time
# Step 3: Perform OCR on images
def extract_text_from_image(image_url):
    try:
        print(f"Downloading image from: {image_url}")
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = io.BytesIO(response.content)

        print("Sending image data to Azure Computer Vision for OCR...")
        read_response = computervision_client.read_in_stream(image_data, raw=True)
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        print("Waiting for the OCR operation to complete...")
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        if read_result.status == OperationStatusCodes.succeeded:
            extracted_text = ""
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    extracted_text += line.text + " "
            print(f"Extracted text: {extracted_text.strip()}")
            return extracted_text.strip()
        else:
            print("OCR operation did not succeed.")
            return 'Error extracting text from image'
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return 'Error extracting text from image'
    except Exception as e:
        print(f"Error extracting text from image: {image_url}. Error: {e}")
        return 'Error extracting text from image'



def summarize_text(content):
    print('Summarizing text...')
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful summarizer."},
            {"role": "user",
             "content": f"Summarize the following text, answer with just the summarized text:\n{content}"}]
    )
    summary = response.choices[0].message.content
    return summary



def save_summary_to_pdf(summary, output_path):
    print("Saving summary to PDF...")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    print(summary)
    pdf.output(output_path)

# Main workflow
def summarize_article_from_url(url):
    article_text, images = get_article_content(url)
    summarized_text = summarize_text(article_text)
    i = 1
    for image_url in images:
        if image_contains_text(image_url):
            print(f"Processing image with text: {image_url}")
            extracted_text = extract_text_from_image(image_url)
            if extracted_text != 'Error extracting text from image' and extracted_text != '':
                summarized_text += "\nPicture " + str(i) + ": " + extracted_text
                i += 1

    return summarized_text



def summarize_plain_text(content):
    summary = summarize_text(content)
    return summary
