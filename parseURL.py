import requests
from bs4 import BeautifulSoup

def print_decoding_secret_msg(doc_url):
    response = requests.get(doc_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    if not table:
        print("No table found.")
        return

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

    for y in range(max_y + 1):
        line = ''
        for x in range(max_x + 1):
            line += char_map.get((x, y), ' ')
        print(line)

doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
print_decoding_secret_msg(doc_url)
