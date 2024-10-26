import aiohttp
import asyncio
import json

from core.env import OPENROUTER_API_KEY
from core.utils.log import xlogger


SITE_URL = "https://github.com/xxspell/email-autoreg"
APP_NAME = "Auto register duck.com email"


async def send_image_for_duck_check(session, image_id):
    """
    Sends an image to the OpenRouter API to check if it's a duck.
    Returns 'yes' if it's a duck, 'no' otherwise.
    """
    url = f'https://duckduckgo.com/assets/anomaly/images/challenge/{image_id}.jpg'
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Is this image a duck? Answer only 'yes' or 'no'"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url
                    }
                }
            ]
        },
    ]
    try:
        async with session.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": f"{SITE_URL}",
                    "X-Title": f"{APP_NAME}",
                },
                json={
                    "model": "google/gemini-flash-1.5",
                    "messages": messages
                }
        ) as response:
            response.raise_for_status()  # Check for HTTP errors
            response_data = await response.json()
            answer = response_data.get("choices")[0].get("message").get("content", "").strip().lower()
            xlogger.debug(f"Response for image {image_id}: {answer}")
            return answer
    except aiohttp.ClientError as e:
        xlogger.error(f"API request error for image {image_id}: {e}")
        return None


async def find_ducks(input_string):
    """
    Takes a string of image IDs, sends each image to the OpenRouter API to check if it's a duck,
    and returns a string with IDs of images identified as ducks.
    """
    image_ids = input_string.split("-")
    duck_id_list = []

    async with aiohttp.ClientSession() as session:
        tasks = [send_image_for_duck_check(session, image_id) for image_id in image_ids]
        results = await asyncio.gather(*tasks)

        for image_id, answer in zip(image_ids, results):
            if answer == "yes":
                duck_id_list.append(image_id)
                xlogger.debug(f"Image {image_id} identified as a duck.")
            elif answer == "no":
                xlogger.debug(f"Image {image_id} identified as not a duck.")
            else:
                xlogger.warning(f"Could not determine if image {image_id} is a duck.")

    output = "-".join(duck_id_list)
    xlogger.info(f"Captcha resolve: {output}")
    return output


# input_string = "070f99e64ec34233a0428b0c6f91a564-c9dec22f36904d8c831835cf4c76f899-2e5c720ff34345d9b3b685b3436bad3d-c6e75320917346aeb1a1ca1d2276da47-e6f9bd901da7421085b26924010190b9-ed254e2b0abf4744b648d1f2046bbfdb-ded06afd2c4444e286ac18162dd4af1f-278581a8660d49dc9193a715c6a17cc0-bba533ee6f214de5913ef897380987bd"
# duck_image_ids = asyncio.run(find_ducks(input_string))
# print(f"List of duck image IDs: {duck_image_ids}")
