from pathlib import Path
from PIL import Image
import imagehash
import os

def scan_duplicates(folder_path):

    hashes = {}

    total_size = 0

    duplicates = []

    folder = Path(folder_path)

    for file in folder.rglob("*"):

        if file.suffix.lower() in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        ]:


            try:

                img = Image.open(file)

                img_hash = imagehash.average_hash(img)

                    
                if img_hash in hashes:

                    duplicates.append({
                        "duplicate": str(file),
                        "original": str(hashes[img_hash])
                    })
                    total_size += os.path.getsize(file)


                else:

                    hashes[img_hash] = file

            except Exception as e:
                print(e)

    return {
        "duplicates": duplicates,
        "size": total_size
    }


