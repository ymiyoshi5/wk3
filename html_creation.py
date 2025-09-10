import requests
import wikipedia

# Base URL
url = "https://rickandmortyapi.com/api/character"

# Fetch character data
response = requests.get(url)
data = response.json()

# Wikipedia configuration
wikipedia.set_lang("en")

def get_summary(name):
    try:
        return wikipedia.summary(name, sentences=2)
    except Exception:
        return None  # Return None if no backstory is found

# HTML header template (with nav + main starts)
def html_header(title, other_file, other_label):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
</head>
<body>
  <header>
    <h1 id="top">{title}</h1>
    <nav>
      <a href="{other_file}">See {other_label}</a>
    </nav>
  </header>
  <main>
"""

# HTML footer closes main and body
html_footer = """
  </main>
</body>
</html>
"""

humans = html_header("Rick and Morty Humans", "aliens.html", "Aliens")
aliens = html_header("Rick and Morty Aliens", "humans.html", "Humans")

for char in data["results"]:
    episodes_count = len(char.get("episode", []))

    # Get backstory only for humans
    backstory = get_summary(char["name"]) if char['species'].lower() == "human" else None

    # Build origin with link if available
    origin_name = char["origin"]["name"]
    origin_url = char["origin"]["url"]
    if origin_url:
        origin_html = f'<a href="{origin_url}" target="_blank">{origin_name}</a>'
    else:
        origin_html = origin_name

    # Location with link
    location_name = char["location"]["name"]
    location_url = char["location"]["url"]
    location_html = f'<a href="{location_url}" target="_blank">{location_name}</a>' if location_url else location_name

    # Character API link
    char_api_link = f'<a href="{char["url"]}" target="_blank">{char["name"]} API</a>'

    # Character block
    char_block = f"""
    <div>
      <img src="{char['image']}" width="100" alt="{char['name']}">
      <h2>{char['name']}</h2>
      <dl>
        <dt>Status:</dt>
        <dd>{char['status']}</dd>
        <dt>Origin:</dt>
        <dd>{origin_html}</dd>
        <dt>Location:</dt>
        <dd>{location_html}</dd>
        <dt>Episodes:</dt>
        <dd>{episodes_count}</dd>
        <dt>Character Info:</dt>
        <dd>{char_api_link}</dd>
    """

    # Only add backstory if available (humans only)
    if backstory:
        char_block += f"""
        <dt>Backstory:</dt>
        <dd>{backstory}</dd>
        """

    # Add "Back to Top" link with class
    char_block += """
      </dl>
      <p><a href="#top" class="top_jumper">Back to Top</a></p>
    </div>
    """

    if char['species'].lower() == "human":
        humans += char_block
    else:
        aliens += char_block

humans += html_footer
aliens += html_footer

# Write final files
with open("humans.html", "w", encoding="utf-8") as f:
    f.write(humans)
with open("aliens.html", "w", encoding="utf-8") as f:
    f.write(aliens)

print("Created humans.html and aliens.html")