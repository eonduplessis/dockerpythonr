import logging

from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract

import azure.functions as func

def pdf_to_png(company_name, companies_house_pdf_file_data):
    # Store Pdf with convert_from_path function
    images = convert_from_bytes(companies_house_pdf_file_data)
    image_list = []

    i = 0     
    for image in images:
        # Save pages as images in the pdf
        image_name = company_name + 'page'+ str(i) +'.png'
        logging.info(f"Saving image: {image_name}")
        image.save(image_name, 'PNG')
        logging.info(f"Saving image complete: {image_name}")
        image_list.append(image_name)
        i = i + 1
    
    return image_list

def png_ocr(png_file_path):
    text = pytesseract.image_to_string(Image.open(png_file_path))
    return text

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    logging.info(f"Converting blob bytestream to PNG")
    image_list = pdf_to_png(myblob.name[15:-4], myblob.read())
    logging.info(f"Converting blob bytestream to PNG complete")

    content = ""
    

    logging.info(f"Executing OCR on PNG payload")
    for image in image_list:
        logging.info(f"Processing image: {image}")
        text = png_ocr(image)
        logging.info(f"Processing image complete: {image} \n"
                     f"Content size: {len(text)}")
        content = content + text
    
    logging.info(f"Processing PDF complete. \n"
                 f"Document content size: {len(content)}")
