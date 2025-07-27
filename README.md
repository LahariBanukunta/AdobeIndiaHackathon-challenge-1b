# Adobe-India-Hackathon25

# 📄 Challenge 1B — Persona-Driven Document Intelligence

## ✨ Overview

This solution extracts and prioritizes the most relevant sections from a set of PDF documents based on a given **persona** and their **job-to-be-done**.

---

## 🧠 Approach

1. **PDF Structure Parsing**:  
   Each document is parsed using `PyMuPDF`, extracting headings (H1, H2, H3) and text along with page numbers.

2. **Persona Understanding**:  
   The `persona` and `job description` are processed using basic NLP — extracting important terms using keyword-based or TF-IDF-like techniques.

3. **Section Relevance Scoring**:  
   Each section in the documents is scored against persona/job keywords. Top-ranked sections are selected.

4. **Sub-section Refinement**:  
   Relevant paragraphs or sentences from the top sections are further refined and ranked for detailed analysis.

5. **Output**:  
   Results are returned in a JSON format with metadata, extracted sections, and refined sub-section analysis.

---

## 📦 Models / Libraries Used

| Library       | Purpose                          |
|---------------|----------------------------------|
| PyMuPDF       | PDF parsing (text, font, layout) |
| nltk          | Tokenization, stopword removal   |
| scikit-learn  | TF-IDF / cosine similarity       |
| Python stdlib | os, json, datetime, re           |

📝 No pretrained model is used. Entire solution works **offline** and **on CPU**.

---

## 🐳 How to Build and Run

### 1. Build Docker Image

```bash
docker build --platform=linux/amd64 -t personaextractor:xyz456 .
2. Run Docker Container
bash
Copy
Edit
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  personaextractor:xyz456
Input: Place PDF files and persona config inside /input

Output: The extracted result.json will be saved to /output

📁 Input Format (Expected)
Place your files in input/:

doc1.pdf, doc2.pdf, ... (at least 3)

persona.json (example below)

json
Copy
Edit
{
  "persona": "Investment Analyst",
  "job": "Analyze revenue trends, R&D investments, and market positioning strategies"
}
📄 Output Format (result.json)
json
Copy
Edit
{
  "metadata": {
    "documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Investment Analyst",
    "job_to_be_done": "Analyze revenue trends, R&D investments, and market positioning strategies",
    "timestamp": "2025-07-27T18:30:00Z"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page": 4,
      "section_title": "Revenue Trends Analysis",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "page": 4,
      "refined_text": "Company A's revenue increased by 18% YoY in 2023, mainly due to growth in cloud services...",
      "importance_rank": 1
    }
  ]
}
✅ Constraints Met
Constraint	Status
Offline Execution	✅ Yes
CPU-only, amd64-compatible	✅ Yes
Model size ≤ 1GB	✅ Yes
Runtime ≤ 60 seconds (3–5 PDFs)	✅ Yes

