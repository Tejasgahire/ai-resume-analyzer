import pytesseract
from pdf2image import convert_from_path

from config.config import (
    TESSERACT_PATH,
    POPPLER_PATH,
    RESUME_PDF,
    EXTRACTED_TEXT
)


# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

print("Converting PDF to image...")

# Convert PDF pages into images
images = convert_from_path(
    RESUME_PDF,
    dpi=300,
    poppler_path=POPPLER_PATH
)

print(f"Pages found: {len(images)}")

resume_text = ""

# Run OCR on every page
for i, image in enumerate(images, start=1):
    print(f"Running OCR on page {i}...")

    text = pytesseract.image_to_string(
        image,
        lang="eng"
    )

    resume_text += text + "\n"


print("\n--- OCR RESUME TEXT ---\n")
print(resume_text)

# Save extracted text
with open(EXTRACTED_TEXT, "w", encoding="utf-8") as file:
    file.write(resume_text)

print("\n--- OCR EXTRACTION SUCCESSFUL ---")
print(f"Saved to: {EXTRACTED_TEXT}")