import os
import glob
import json
import pdfplumber
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Load semantic model
model = SentenceTransformer('all-MiniLM-L6-v2')

# === OCR-based Heading Extraction (Fallback) ===
def extract_headings_with_ocr(pdf_path):
    headings = []
    try:
        images = convert_from_path(pdf_path)
        for page_num, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            lines = text.split("\n")
            for line in lines:
                clean = line.strip()
                if len(clean) >= 3:
                    headings.append({
                        "document": os.path.basename(pdf_path),
                        "page_number": page_num + 1,
                        "heading_text": clean,
                        "font_size": None,
                        "font": "OCR",
                        "heading_level": "H2"  # Default heuristic for OCR
                    })
    except Exception as e:
        print(f"[!] OCR extraction failed for {pdf_path}: {e}")
    return headings

# === Extract Headings with Font Size Heuristics or OCR fallback ===
def extract_headings(pdf_path):
    headings = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                words = page.extract_words(extra_attrs=["size", "fontname"])
                if not words:  # If no text is found (likely an image-based PDF)
                    raise ValueError("No text found, fallback to OCR")
                for w in words:
                    text = w['text'].strip()
                    if not text or len(text) < 3:
                        continue
                    size = w['size']
                    font = w['fontname'].lower()

                    # Heuristic rules
                    if size > 15:
                        level = "H1"
                    elif size > 13:
                        level = "H2"
                    elif size > 11:
                        level = "H3"
                    else:
                        continue

                    headings.append({
                        "document": os.path.basename(pdf_path),
                        "page_number": page_num + 1,
                        "heading_text": text,
                        "font_size": size,
                        "font": font,
                        "heading_level": level
                    })
    except:
        headings = extract_headings_with_ocr(pdf_path)
    return headings

# === Compute Semantic Similarity ===
def rank_headings_by_prompt(headings, prompt):
    prompt_embedding = model.encode(prompt, convert_to_tensor=True)

    for h in headings:
        h_embedding = model.encode(h["heading_text"], convert_to_tensor=True)
        similarity = float(util.cos_sim(h_embedding, prompt_embedding))
        h["similarity_score"] = similarity

    return sorted(headings, key=lambda x: x["similarity_score"], reverse=True)

# === Main Function ===
def process_documents(pdf_folder, persona, job_to_be_done, output_path="challenge1b_output.json"):
    prompt = f"{persona} needs to {job_to_be_done}"

    pdf_paths = glob.glob(os.path.join(pdf_folder, "*.pdf"))
    if not pdf_paths:
        print(f"[!] No PDF files found in: {pdf_folder}")
        return

    all_results = []

    for pdf_path in pdf_paths:
        print(f"Processing: {os.path.basename(pdf_path)}")
        headings = extract_headings(pdf_path)
        ranked = rank_headings_by_prompt(headings, prompt)

        for i, item in enumerate(ranked[:5]):  # Top 5 relevant
            all_results.append({
                "document": item["document"],
                "page_number": item["page_number"],
                "heading": item["heading_text"],
                "heading_level": item["heading_level"],
                "importance_rank": i + 1,
                "score": item["similarity_score"]
            })

    final_json = {
        "metadata": {
            "documents": [os.path.basename(p) for p in pdf_paths],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.now().isoformat()
        },
        "matched_headings": all_results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)

    print(f"[✓] Headings matched and saved to: {output_path}")


# === Example Run ===
if __name__ == "__main__":
    process_documents(
        pdf_folder="Collection 2/PDFs",
        persona="New Acrobat User",
        job_to_be_done="Learn how to edit, export, use generative AI, and test Acrobat features like fill and sign",
        output_path="Collection 2/challenge1b_output.json"
    )

