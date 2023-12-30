import os
import re
import requests
from bs4 import BeautifulSoup

def rename_images(path):
  # Get a list of all files in the current directory:
  files = os.listdir(path)

  # Read urls.txt and load each line into a list:
  with open('urls.txt', 'r') as f:
    urls = f.readlines()

  for i in range(len(files)):
    # Use regex to parse filename:
    match = re.search(r'Christmas2023_.+?_Layer-([0-9]+).png', files[i])

    if not match:
      continue

    layer = int(match.group(1))

    url = urls[layer - 1 if layer < 28 else layer - 2]

    match = re.search(r'https://store.steampowered.com/app/[0-9]+?/([A-Za-z-_]+)', url)

    if not match:
      raise Exception('Failed to parse URL')

    new_name = match.group(1) + '.png'

    print(new_name)

    # Rename each file in the current directory:
    os.rename(files[i], new_name)

def get_steam_tags_for_game(url):
  # Get the HTML for the game's store page:
  response = requests.get(url)

  if response.status_code != 200:
    raise Exception('Failed to get HTML')

  # Parse the HTML:
  soup = BeautifulSoup(response.text, 'html.parser')

  # Get the tags:
  tags = soup.find_all('a', {'class': 'app_tag'})

  # Get the tag names:
  tag_names = [tag.text.strip() for tag in tags]

  return tag_names

def generate_html():
  # Read urls.txt and load each line into a list:
  with open('urls.txt', 'r') as f:
    urls = f.readlines()

  for i in range(len(urls)):
    url = urls[i].strip()
    match = re.search(r'https://store.steampowered.com/app/[0-9]+?/([A-Za-z-_]+)', url)

    if not match:
      raise Exception('Failed to parse URL')

    image = match.group(1) + '.png'

    tags = get_steam_tags_for_game(url)

    text = ', '.join(tags)

    print('''
<div class="col">
  <div class="card shadow-sm">
    <a href="{}"><img src="/img/{}" width="100%" height="215" role="img"></a>
    <div class="card-body">
      <p class="card-text">{}</p>
    </div>
  </div>
</div>
    '''.format(url, image, text))

if __name__ == '__main__':
  generate_html()
