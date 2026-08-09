import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_ai(prompt, retries=2):

    for attempt in range(retries + 1):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text

        except Exception as error:

            error_text = str(error)

            # Gemini quota/rate-limit error
            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                print("Gemini quota/rate limit reached.")

                if attempt < retries:
                    wait_time = 10 * (attempt + 1)

                    print(
                        f"Retrying Gemini request in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                    continue

                raise RuntimeError(
                    "Gemini quota is currently exhausted."
                )

            # Other temporary/API errors
            if attempt < retries:

                wait_time = 5 * (attempt + 1)

                print(
                    f"Gemini request failed. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            raise