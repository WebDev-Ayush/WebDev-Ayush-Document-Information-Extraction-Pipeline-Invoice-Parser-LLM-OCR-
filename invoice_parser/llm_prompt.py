from __future__ import annotations

from typing import Any

from .models import InvoiceData


SYSTEM_PROMPT = (
    "You are an invoice extraction assistant. "
    "Extract all available invoice fields and return only valid JSON "
    "that matches the provided schema."
)


def build_invoice_prompt(document_text: str) -> str:
    schema = InvoiceData.model_json_schema()
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"JSON Schema:\n{schema}\n\n"
        f"Document text:\n{document_text}"
    )


def parse_with_openai_instructor(client: Any, model: str, document_text: str) -> InvoiceData:
    """
    Requires an Instructor-patched OpenAI client:
    `client = instructor.from_openai(OpenAI())`
    """

    prompt = build_invoice_prompt(document_text)
    return client.chat.completions.create(
        model=model,
        response_model=InvoiceData,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )


def parse_with_langchain(llm: Any, document_text: str) -> InvoiceData:
    """
    Parse invoice data with LangChain using PydanticOutputParser.
    """
    from langchain.output_parsers import PydanticOutputParser
    from langchain.prompts import PromptTemplate

    parser = PydanticOutputParser(pydantic_object=InvoiceData)
    template = PromptTemplate(
        template=(
            "{system_prompt}\n\n"
            "Extract invoice data from the text below.\n"
            "{format_instructions}\n\n"
            "Text:\n{text}"
        ),
        input_variables=["text"],
        partial_variables={
            "system_prompt": SYSTEM_PROMPT,
            "format_instructions": parser.get_format_instructions(),
        },
    )
    response = llm.invoke(template.format(text=document_text))
    return parser.parse(response if isinstance(response, str) else response.content)
