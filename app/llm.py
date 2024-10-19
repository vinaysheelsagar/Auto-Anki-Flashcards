import os
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from icecream import ic


class FlashCard(BaseModel):
    deck: str = Field(..., description="The address of the deck")
    question: str = Field(..., description="The question for the flashcard.")
    answer: str = Field(..., description="The answer for the flashcard.")
    tags: list[str] = Field(..., description="Tags for the flashcard.")


def main():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    parser = JsonOutputParser(pydantic_object=FlashCard)

    prompt = PromptTemplate(
        template="""Create flashcards based on the informaton.
Keep the question detailed independent of the information of the answer.

{format_instructions}
{input_text}
""",
        input_variables=["input_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | llm | parser
    result = chain.invoke({
        "input_text": "The earth will be completely populated with a society of enightened people"
    })

    ic(result)


if __name__ == "__main__":
    main()
