import os
from typing import List

from langchain.chains import LLMChain
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser

from .schemas import ShipmentEntitySchema
from ..config import settings

# Define few‑shot examples
EXAMPLES = [
    {
        "input": "Shipment BOL-8832 is delayed at Port of LA due to customs strike. Expected release is Friday. Temp dropped to 4C.",
        "output": {
            "bill_of_lading_id": "BOL-8832",
            "delay_reason": "customs strike",
            "estimated_delay_days": 2,
            "critical_status": true
        },
    },
    {
        "input": "The cargo with BOL-1245 encountered a storm causing a 3‑day delay. No critical impact.",
        "output": {
            "bill_of_lading_id": "BOL-1245",
            "delay_reason": "storm",
            "estimated_delay_days": 3,
            "critical_status": false
        },
    },
    {
        "input": "BOL-3321 arrived at warehouse early, no delay.",
        "output": {
            "bill_of_lading_id": "BOL-3321",
            "delay_reason": "none",
            "estimated_delay_days": 0,
            "critical_status": false
        },
    },
]

example_prompt = PromptTemplate(
    input_variables=["input"],
    template="Input: {input}\nOutput:"  # Output will be filled by the model
)

few_shot_prompt = FewShotPromptTemplate(
    examples=EXAMPLES,
    example_prompt=example_prompt,
    prefix="Extract shipment delay information from the following unstructured text. Return a JSON object matching the schema.",
    suffix="Input: {text}\nOutput:",
    input_variables=["text"],
    example_separator="\n---\n",
)

# Output parser using Pydantic schema
parser = PydanticOutputParser(pydantic_object=ShipmentEntitySchema)

def _get_llm():
    if settings.openai_api_key:
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key
        return OpenAI(model_name="gpt-3.5-turbo", temperature=0)
    else:
        return None

def _mock_extractor(text: str) -> ShipmentEntitySchema:
    """Very naive mock that extracts BOL id and guesses values.
    This runs when no OpenAI key is present.
    """
    import re
    bol_match = re.search(r"BOL[-\s]?\d+", text, re.IGNORECASE)
    bol = bol_match.group(0).replace(" ", "-") if bol_match else "UNKNOWN"
    # Simple heuristics for delay reason and days
    if "delay" in text.lower():
        if "customs" in text.lower():
            reason = "customs"
            days = 2
        elif "storm" in text.lower():
            reason = "storm"
            days = 3
        else:
            reason = "unknown"
            days = 1
        critical = True
    else:
        reason = "none"
        days = 0
        critical = False
    return ShipmentEntitySchema(
        bill_of_lading_id=bol,
        delay_reason=reason,
        estimated_delay_days=days,
        critical_status=critical,
    )

def extract_shipment_entities(text: str) -> ShipmentEntitySchema:
    """Extract structured shipment entity information from raw text.

    If an OpenAI API key is configured, the function will call the LLM with a few‑shot
    prompt and enforce the JSON schema via Pydantic. When the key is missing, a deterministic
    mock implementation runs instead, guaranteeing the function always returns a valid
    ``ShipmentEntitySchema`` instance.
    """
    llm = _get_llm()
    if llm is None:
        return _mock_extractor(text)
    chain = LLMChain(llm=llm, prompt=few_shot_prompt)
    raw_output = chain.run({"text": text})
    # The LLM may return surrounding whitespace or explanations – attempt to parse JSON part
    try:
        return parser.parse(raw_output)
    except Exception:
        # Fallback to mock on parsing errors
        return _mock_extractor(text)
