import os
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(prompt, retries=2):

    for attempt in range(retries + 1):

        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
            )

            text = response.choices[0].message.content

            if not text:
                raise RuntimeError(
                    "Groq returned an empty response."
                )

            return text

        except Exception as error:

            print(f"Groq request failed: {error}")

            if attempt < retries:
                wait_time = 5 * (attempt + 1)

                print(
                    f"Retrying Groq request in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            raise RuntimeError(
                f"Groq request failed: {error}"
            )