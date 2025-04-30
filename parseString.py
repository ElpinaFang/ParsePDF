import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import pytesseract

def extract_unicode_message(doc_url):
    response = requests.get(doc_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    if not table:
        print("No table found.")
        return ""

    char_map = {}
    max_x = max_y = 0

    rows = table.find_all('tr')[1:]
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 3:
            continue
        try:
            x = int(cells[0].text.strip())
            char = cells[1].text.strip()
            y = int(cells[2].text.strip())
            char_map[(x, y)] = char
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        except ValueError:
            continue

    # Create an image to draw the grid
    cell_size = 20
    img_width = (max_x + 1) * cell_size
    img_height = (max_y + 1) * cell_size

    image = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for (x, y), char in char_map.items():
        draw.text((x * cell_size, y * cell_size), char, font=font, fill="black")

    # Use OCR to read the drawn letters
    message = pytesseract.image_to_string(image, config="--psm 6").strip().replace(" ", "").replace("\n", "")
    
    image.show()  # Optional: opens the image window
    return message

doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
secret = extract_unicode_message(doc_url)
print("SECRET MESSAGE:", secret)
