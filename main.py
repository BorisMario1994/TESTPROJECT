import PyPDF2
from PIL import Image
import pytesseract
import xml.etree.ElementTree as ET
import re
from io import BytesIO
from pdf2image import convert_from_path


def extract_text_from_pdf(pdf_path):
    text = ""
    images = convert_from_path(pdf_path, dpi=300)  # Adjust the DPI as needed
    for image in images:
        extracted_text = pytesseract.image_to_string(image)
        text += extracted_text + "\n"

    return text


def clean_text(text):
    cleaned_text = text.strip()
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text


def convert_text_to_xml(text):
    root = ET.Element("pdf_data")
    for line in text.splitlines():
        line_element = ET.SubElement(root, "line")
        line_element.text = line
    return root


def save_xml_to_file(xml_element, xml_path):
    xml_tree = ET.ElementTree(xml_element)
    xml_tree.write(xml_path, encoding="utf-8", xml_declaration=True)

    # Format the extracted text into separate lines for readability
    with open(xml_path, "r", encoding="utf-8") as xml_file:
        lines = xml_file.readlines()
    formatted_lines = ["\n" + line.strip() for line in lines if line.strip()]
    with open(xml_path, "w", encoding="utf-8") as xml_file:
        xml_file.writelines(formatted_lines)


def main():
    pdf_path = r"D:\readpdftoexcel\sample.pdf"
    xml_path = "output.xml"

    # Step 1: Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    # print(extracted_text)
    # Step 2 (optional): Clean and format the extracted text
    cleaned_text = clean_text(extracted_text)

    # Step 3: Convert the cleaned text to XML
    xml_element = convert_text_to_xml(cleaned_text)

    # Step 4: Save the XML to a file
    save_xml_to_file(xml_element, xml_path)


if __name__ == "__main__":
    main()
