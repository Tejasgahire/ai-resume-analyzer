from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_path

from config.config import (
    TESSERACT_PATH,
    POPPLER_PATH,
    RESUME_PDF,
    EXTRACTED_TEXT
)


def extract_text_from_pdf(pdf_path):
    """Try extracting text directly from the PDF."""

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_text_with_ocr(pdf_path):
    """Extract text from scanned/image-based PDF using OCR."""

    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    print("Switching to OCR...")

    images = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=POPPLER_PATH
    )

    print(f"Pages found: {len(images)}")

    text = ""

    for i, image in enumerate(images, start=1):
        print(f"Running OCR on page {i}...")

        page_text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        text += page_text + "\n"

    return text.strip()


def extract_resume_text(pdf_path):
    """Automatically choose PDF extraction or OCR."""

    print("Trying normal PDF text extraction...")

    text = extract_text_from_pdf(pdf_path)

    if text:
        print("Selectable text found.")
        print("Using normal PDF extraction.")
        return text

    print("No selectable text found.")

    return extract_text_with_ocr(pdf_path)


def main():

    pdf_path = RESUME_PDF

    print(f"Using resume: {pdf_path}")

    text = extract_resume_text(pdf_path)

    if not text:
        print("\nERROR: Could not extract any text from the resume.")
        return

    print("\n--- RESUME TEXT ---\n")
    print(text)

    with open(EXTRACTED_TEXT, "w", encoding="utf-8") as file:
        file.write(text)

    print("\n--- RESUME EXTRACTION SUCCESSFUL ---")
    print(f"Saved to: {EXTRACTED_TEXT}")


if __name__ == "__main__":
    main()