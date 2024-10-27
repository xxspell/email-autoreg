import asyncio
import random
from typing import List, Optional

import aiohttp
from aiohttp import ClientSession

from core.captcha import find_ducks
from core.env import SLOWED_MODE
from core.mail.main import get_verification_code
from core.utils.file import save_to_csv
from core.utils.generator.nickname import generate_email
from core.utils.generator.useragent import generate_random_user_agent
from core.utils.log import xlogger
from core.utils.time import generate_afk_seconds

OUTPUT_CSV = "accounts.csv"
SIGNUP_URL = "https://quack.duckduckgo.com/api/auth/signup"
VALIDATE_URL = "https://quack.duckduckgo.com/api/auth/validate-email-address"
VERIFY_URL = "https://quack.duckduckgo.com/api/auth/verify"

HEADERS = {
    'accept': '*/*',
    'origin': 'https://duckduckgo.com',
    'referer': 'https://duckduckgo.com/'
}

PIXEL_URLS = {
    "email-load-start-page": {"url": "https://improving.duckduckgo.com/t/email-load-start-page", "needs_group": False},
    "email-seenlist": {"url": "https://improving.duckduckgo.com/t/email-seenlist", "needs_group": False},
    "email-load-privacy-policy-step": {"url": "https://improving.duckduckgo.com/t/email-load-privacy-policy-step",
                                       "needs_group": True},
    "email-load-signup-page": {"url": "https://improving.duckduckgo.com/t/email-load-signup-page",
                               "needs_group": False},
    "email-load-review-page": {"url": "https://improving.duckduckgo.com/t/email-load-review-page",
                               "needs_group": False},
    "email-load-welcome-page": {"url": "https://improving.duckduckgo.com/t/email-load-welcome-page",
                                "needs_group": False}
}


async def send_pixel(session: aiohttp.ClientSession, action: str, headers: dict, proxy: str) -> bool:
    if action not in PIXEL_URLS:
        xlogger.error(f"Unknown action '{action}'")
        return False

    event_id = f"event_id_{random.randint(1000000, 9999999)}"
    pixel_info = PIXEL_URLS[action]
    url = f"{pixel_info['url']}?{event_id}&isIncontext=false"

    if pixel_info['needs_group']:
        group_value = "unknown"
        url += f"&group={group_value}"

    try:
        async with session.get(url, headers=headers, proxy=proxy) as response:
            if response.status == 200:
                xlogger.debug(f"Pixel sent for action '{action}' - URL: {url}")
                return True
            else:
                xlogger.warning(f"Pixel request failed for action '{action}' with status {response.status}")
                return False
    except aiohttp.ClientError as e:
        xlogger.warning(f"Error sending pixel request for action '{action}': {e}")
        return False


async def validate_email(session: ClientSession, email: str, headers: dict, proxy: str) -> bool:
    async with session.get(f"{VALIDATE_URL}?email={email}", headers=headers, proxy=proxy) as response:
        data = await response.json()
        xlogger.debug(f"Validating email: {email} - Response: {data}")
        return data.get("valid", False)


async def register_account(session: aiohttp.ClientSession, user: str, email: str, headers: dict, proxy: str,
                           secure_reply=0, dry_run=0) -> Optional[dict]:
    form_data = {
        'user': user,
        'email': email,
        'disable_secure_reply': str(secure_reply)
    }
    if dry_run == 1:
        form_data['dry_run'] = '1'

    for attempt in range(1, 4):
        xlogger.debug(f"Attempt {attempt}/3 to register account for {email} using proxy: {form_data}")

        try:
            async with session.post(SIGNUP_URL, data=form_data, headers=headers, proxy=proxy) as response:
                response_text = await response.text()
                if response.status == 200:
                    xlogger.debug(f"Successfully send request for {email} | {response_text}")
                    return await response.json()
                elif response.status == 503:
                    xlogger.warning(f"Service unavailable (503) for proxy {proxy}, retrying...")
                else:
                    if '"error":"rc"' in response_text and '"cp":' in response_text:
                        xlogger.warning(f"Captcha detected! Trying resolve..")
                        data = await response.json()
                        xlogger.debug(data)
                        captcha_string = data.get('c', {}).get('cp')
                        captcha_resolve_string = await find_ducks(captcha_string)
                        form_data["ca"] = captcha_resolve_string
                        form_data["cp"] = captcha_string

                    if '"error":"unavailable_username"' in response_text:
                        xlogger.warning(f"Username is busy")

                    xlogger.debug(f"Attempt {attempt}/3 failed - Status: {response.status}, Response: {response_text}")
        except aiohttp.ClientError as e:
            xlogger.warning(f"Client error during registration for {email}: {e}")

        await asyncio.sleep(2)

    xlogger.warning(f"Failed to register account for email: {email} after 3 attempts")
    return None


async def verify_account(session: ClientSession, user: str, otp: str, headers: dict, proxy: str) -> Optional[dict]:
    params = {'otp': otp, 'user': user}
    xlogger.debug(f"Verifying account for user: {user} with OTP: {otp}")

    for attempt in range(1, 4):
        try:
            async with session.get(VERIFY_URL, params=params, headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    xlogger.debug(f"Account verified for user: {user}")
                    return await response.json()
                else:
                    response_text = await response.text()
                    xlogger.warning(f"Verification failed for {user} - Status: {response.status}, Response: {response_text}")
                    return None
        except aiohttp.ClientError as e:
            xlogger.warning(f"Client error during verfying for user: {user}")

        await asyncio.sleep(2)


async def create_account(session: ClientSession, domain: str, proxy: str, i: int) -> Optional[dict]:
    xlogger.log_prefix_var.set(f"Reg {i} | ")

    if SLOWED_MODE:
        await asyncio.sleep(generate_afk_seconds(45, 200))
    email, user = generate_email(domain)

    headers = HEADERS.copy()
    user_agent = generate_random_user_agent("windows", "chrome")
    headers['user-agent'] = user_agent

    xlogger.info(f"Generated email for registration: {email} | Username: {user} / Proxy: {proxy} / UA: {user_agent}")

    await send_pixel(session, "email-load-start-page", headers, proxy)

    await asyncio.sleep(generate_afk_seconds())
    await send_pixel(session, "email-seenlist", headers, proxy)
    await asyncio.sleep(generate_afk_seconds())
    await send_pixel(session, "email-load-privacy-policy-step", headers, proxy)
    await asyncio.sleep(generate_afk_seconds())
    await send_pixel(session, "email-load-signup-page", headers, proxy)
    await asyncio.sleep(generate_afk_seconds())

    if not await register_account(session, user, email, headers, proxy, secure_reply=1, dry_run=1):
        return None

    if await validate_email(session, email, headers, proxy):
        xlogger.info(f"Email {email} is valid for registration")
        await send_pixel(session, "email-load-review-page", headers, proxy)
        await asyncio.sleep(generate_afk_seconds())

        response = await register_account(session, user, email, headers, proxy, secure_reply=0, dry_run=0)
        if response and response.get("status") == "created":
            while True:
                await asyncio.sleep(15)
                otp = get_verification_code(email)
                if otp:
                    xlogger.info(f"Retrieved OTP for {email}: {otp}")
                    break
                xlogger.debug(f"Waiting for OTP for {email}...")
            auth_response = await verify_account(session, user, otp, headers, proxy)

            await send_pixel(session, "email-load-welcome-page", headers, proxy)
            if auth_response and auth_response.get("status") == "authenticated":
                xlogger.info(f"Successfully registered account for {email}")
                await save_to_csv(OUTPUT_CSV, {"email": email, "user": user})
                return {"email": email, "user": user}
            else:
                xlogger.warning(f"Failed to register account for {email}")
    else:
        xlogger.warning(f"Email {email} is not valid for registration")
    return None


async def main(domain: str, num_accounts: int, max_connections: int, proxies: List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = []
        success_count = 0
        failure_count = 0
        created_accounts = []

        for i in range(num_accounts):
            proxy = random.choice(proxies)
            task = create_account(session, domain, proxy, i + 1)
            tasks.append(task)

            if len(tasks) >= max_connections or i == num_accounts - 1:
                results = await asyncio.gather(*tasks)
                for result in results:
                    if result:
                        created_accounts.append(result)
                        success_count += 1
                    else:
                        failure_count += 1
                tasks.clear()

        xlogger.info(f"Account registration summary: {success_count} created, {failure_count} failed.")
