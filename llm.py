import os
import io
import json

from openai import OpenAI
from openai.lib._pydantic import to_strict_json_schema
from dotenv import load_dotenv
import pandas as pd

from models.information import Information
from models.swedish_political_party import SwedishPoliticalParty

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER")
MODEL_OPENAI = "gpt-4.1-mini"

if LLM_PROVIDER == "GEMINI":
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    MODEL = "gemini-2.0-flash"
else:
    client = OpenAI()
    MODEL = MODEL_OPENAI

SYSTEM_PROMPT = f"""
    You are a helpful assistant that extracts information about a person's political and business career from a given text.

    Extract the following information:
    - political_roles: A list of the person's political roles, past or present. It could be as minister, MP ('riksdagsledamot'), parliament group leader ('gruppledare'), political secretary ('politisk sekreterare'), etc.
    - other_roles: A list of the person's other roles, past or present. It could be as a non-political government official ('ambassadör', 'departementsråd'), a lobbyist for a pressure group, a member of a company's board ('styrelseledamot' or 'styrelseordförande'), etc.

    Return the information in JSON format.

    Political parties are often named with their initials between parentheses, e.g. {SwedishPoliticalParty.help_text()}.

    It is not uncommon for several roles to be listed separated by commas. For instance:
    - 'statsminister, partiledare means that the person has two political roles ('statsminister' and 'partiledare')
    - 'Styrelseordförande för LKAB och AMF' means that the person has two non-political roles: 'styrelseordförande' for 'LKAB' and 'styrelseordförande' for 'AMF' which are both companies
    - 'Lanshövding i Stockholms län och Västerbottens län' means that the person has had two separate non political roles: 'lanshövding' for the organisation 'Stockholms län' and 'lanshövding' for the organisation 'Västerbottens län'
    - If a person has been ambassador in two different countries, that also counts as two roles. For ambassadors, the role is e.g. 'ambassadör i Frankrike' and the organisation is the corresponding embassy, i.e. 'Sveriges ambassad i Frankrike'.

    Here are examples of organisations: Svenska Fotbollsförbundet, Drivkraft Sverige, LKAB

    Here are examples of job titles with their type:
    - minister: Political role
    - riksdagsledamot: Political role
    - partiledare: Political role
    - ordförande: Non political role
    - styrelseledamot: Non political role
    - lanshövding: Non political role
    - ambassadör: Non political role
    """.strip()


def messages(paragraph):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Text: {paragraph}"},
    ]


def extract_information(paragraph: str | dict) -> dict:
    """
    Extracts political party and role from a paragraph about a person.

    Args:
        paragraph (str): The paragraph to analyze.

    Returns:
        dict: A dictionary with the extracted political party and role(s).
    """

    try:
        response = client.beta.chat.completions.parse(
            model=MODEL,
            messages=messages(paragraph),
            response_format=Information,
        )

        return response.choices[0].message.parsed

    except Exception as e:
        print(f"Error calling the Gemini API: {e}")
        return None


def prepare_request(paragraph: str | dict) -> dict:
    return {
        "model": MODEL_OPENAI,
        "messages": messages(paragraph),
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "information",
                "strict": True,
                "schema": to_strict_json_schema(Information),
            },
        },
    }


def start_batch(paragraphs_with_ids):
    data = []

    for id, paragraph in paragraphs_with_ids:
        data.append(
            {
                "custom_id": str(id),
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": prepare_request(paragraph),
            }
        )

    jsonl_buffer = io.BytesIO()
    pd.DataFrame(data).to_json(
        jsonl_buffer, index=False, orient="records", lines=True, force_ascii=False
    )
    jsonl_buffer.seek(0)

    batch_input_file = client.files.create(file=jsonl_buffer, purpose="batch")

    batch_input_file_id = batch_input_file.id

    batch = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": "nightly eval job"},
    )

    return batch.id


def retrieve_batch(batch_id, delete_files=False):
    batch = client.batches.retrieve(batch_id)
    if batch.status == "completed":
        file_response = client.files.content(batch.output_file_id)
        jsonl_data = file_response.text.splitlines()
        data = [json.loads(line) for line in jsonl_data]
        results = [
            (
                row["custom_id"],
                json.loads(row["response"]["body"]["choices"][0]["message"]["content"]),
            )
            for row in data
        ]

        if delete_files:
            client.files.delete(batch.input_file_id)
            client.files.delete(batch.output_file_id)

        return results
    else:
        print(f"Batch not yet completed. Status: {batch.status}")
        return None
