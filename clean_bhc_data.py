import re
import json

# Open your scraped .txt file
with open("bhc_site_data.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# Split into sections per page
pages = raw.split("="*60)

cleaned_data = []

for page in pages:
    if not page.strip():
        continue

    # Extract URL
    url_match = re.search(r"URL:\s*(https?://\S+)", page)
    url = url_match.group(1) if url_match else "UNKNOWN"

    # Extract headings
    heading_block = re.search(r"Headings:\n(.+?)\nParagraphs:", page, re.DOTALL)
    headings_raw = heading_block.group(1) if heading_block else ""
    headings = [line.strip() for line in headings_raw.split("\n") if line.strip() and not re.match(r"^[-. ]+$", line)]

    # Extract paragraphs
    para_block = re.search(r"Paragraphs:\n(.+)", page, re.DOTALL)
    paras_raw = para_block.group(1) if para_block else ""
    paragraphs = [
        line.strip()
        for line in paras_raw.split("\n")
        if line.strip()
        and not re.match(r"^[-. ]+$", line)
        and "©" not in line
        and "LinkedIn" not in line
        and "POWERCONNECT.AI" not in line
        and "About Us" not in line
        and "Contact" not in line
        and "Services" not in line
    ]

    cleaned_data.append({
        "url": url,
        "headings": headings,
        "content": " ".join(paragraphs)
    })

# Save to JSON
with open("bhc_cleaned_data.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=2)

print("✅ Cleaned data saved to bhc_cleaned_data.json")
