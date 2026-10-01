"""Download the CC BY raw-URL datasets used by the hierarchical model."""

from pathlib import Path
from urllib.request import Request, urlopen


DATA_DIR = Path(__file__).resolve().parent / "datasets"
SOURCES = {
    "legitphish_v2.csv": "https://data.mendeley.com/public-files/datasets/hx4m73v2sf/files/0ed51e4d-d160-4047-b650-3f0801eea4aa/file_downloaded",
    "url_phish_v2.csv": "https://data.mendeley.com/public-files/datasets/65z9twcx3r/files/0e9c55e4-9adb-43f5-8403-1bbd143ebdb6/file_downloaded",
}


def download_datasets():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename, url in SOURCES.items():
        destination = DATA_DIR / filename
        temporary = destination.with_suffix(destination.suffix + ".part")
        request = Request(url, headers={"User-Agent": "URLShield training data setup/1.0"})
        try:
            with urlopen(request, timeout=120) as response, temporary.open("wb") as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    output.write(chunk)
            if temporary.stat().st_size == 0:
                raise ValueError(f"Downloaded an empty dataset: {filename}")
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
        print(f"Downloaded {filename}: {destination.stat().st_size:,} bytes")


if __name__ == "__main__":
    download_datasets()