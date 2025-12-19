# script to publish products on multiple platforms at once.

import requests
import time
import os
# ---------------------------------------
# KONFIGURATION – FYLL I DINA VÄRDEN!
# ---------------------------------------
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
IG_USER_ID = os.getenv('IG_USER_ID')

print(ACCESS_TOKEN)
print(IG_USER_ID)



IMAGE_PATHS = [
    "bild1.jpg",
    "bild2.jpg",
    "bild3.jpg"
]

CAPTION = "Min caption här! #exempel #produkt"

# ---------------------------------------
# FUNKTIONER
# ---------------------------------------

def upload_image(path):
    """Ladda upp en bild till Instagram som media container."""
    print(f"Laddar upp: {path}")

    url = f"https://graph.facebook.com/v20.0/{IG_USER_ID}/media"

    files = {
        "file": open(path, "rb")
    }

    data = {
        "media_type": "IMAGE",
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(url, files=files, data=data)
    result = response.json()

    print("Upload response:", result)

    if "id" not in result:
        raise Exception(f"Fel vid uppladdning av {path}: {result}")

    return result["id"]


def create_carousel(children_ids):
    """Skapa ett carousel container."""
    print("Skapar carousel...")

    url = f"https://graph.facebook.com/v20.0/{IG_USER_ID}/media"

    data = {
        "media_type": "CAROUSEL",
        "children": ",".join(children_ids),
        "caption": CAPTION,
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(url, data=data)
    result = response.json()

    print("Carousel response:", result)

    if "id" not in result:
        raise Exception(f"Fel vid skapande av carousel: {result}")

    return result["id"]


def publish_container(container_id):
    """Publicera ett media container."""
    print(f"Publicerar container {container_id}...")

    url = f"https://graph.facebook.com/v20.0/{IG_USER_ID}/media_publish"

    data = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(url, data=data)
    result = response.json()

    print("Publish response:", result)
    return result


# ---------------------------------------
# HUVUDFLÖDE
# ---------------------------------------

if __name__ == "__main__":
    print("Startar uppladdning...")

    # 1. Ladda upp alla bilder
    children_ids = []
    for image in IMAGE_PATHS:
        media_id = upload_image(image)
        children_ids.append(media_id)
        time.sleep(1.5)  # Meta rekommenderar en liten paus

    # 2. Skapa carousel container
    carousel_id = create_carousel(children_ids)

    print("Väntar 3 sekunder innan publicering...")
    time.sleep(3)

    # 3. Publicera inlägget
    publish_container(carousel_id)

    print("🚀 Klart! Ditt carousel-inlägg är nu publicerat.")