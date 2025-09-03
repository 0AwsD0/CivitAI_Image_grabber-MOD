from typing import List
import aiohttp
import asyncio
import os

MODELS_API_URL = "https://civitai.com/api/v1/models"
API_TOKEN = ""  #put API KEY if needed

async def _get_client():
    return aiohttp.ClientSession()  #you can add headers if needed

async def download_file(url: str, save_path: str):

    #Make sure folder exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(save_path, "wb") as f:
                    f.write(await resp.read())
                print(f"Downloaded {save_path}")
            else:
                print(f"Failed to download {url}, status: {resp.status}")

async def _model_download_all_versions(model_id: str, download_dir: str = ".") -> List[int]:
    """Fetch all model version IDs from Civitai API and download their primary files with token."""
    version_ids = []
    try:
        client = await _get_client()
        async with client.get(f"{MODELS_API_URL}/{model_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                model_versions = data.get("modelVersions", [])
                for version in model_versions:
                    version_id = version.get("id")
                    version_ids.append(version_id)

                    #Download primary file
                    files = version.get("files", [])
                    for file in files:
                        if file.get("primary", False):
                            #Add API KEY (if needed) to download URL //uncomment/comment line below and comment/uncomment line under that
                            file_url = f"{file['downloadUrl']}?token={API_TOKEN}"
                            #file_url = f"{file.get('downloadUrl')}"
                            file_name = file.get("name")
                            save_path = os.path.join(download_dir, file_name)
                            await download_file(file_url, save_path)
            else:
                print(f"Failed to fetch model data for ID {model_id}, status: {resp.status}")
    except Exception as e:
        print(f"Error fetching model versions for ID {model_id}: {e}")
    finally:
        await client.close()
    return version_ids

#Example usage
async def main():
    model_id = "149904"
    versions = await _model_download_all_versions(model_id, download_dir="downloads")
    print("Downloaded version IDs:", versions)

asyncio.run(main())