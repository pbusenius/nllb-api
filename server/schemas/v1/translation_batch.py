from typing import Annotated

from pydantic import BaseModel, Field

from server.typedefs import Language


class TranslationBatchItem(BaseModel):
    """
    Summary
    -------
    a single translation item in a batch request

    Attributes
    ----------
    text (str)
        source text of a single language

    source (Language)
        source language in the FLORES-200 code format

    target (Language)
        target language in the FLORES-200 code format
    """

    text: Annotated[
        str,
        Field(min_length=1, max_length=4096, description="source text of a single language", examples=["Hello, world!"]),
    ]

    source: Annotated[
        Language,
        Field(description="source language in the FLORES-200 code format", examples=["eng_Latn"]),
    ]

    target: Annotated[
        Language,
        Field(description="target language in the FLORES-200 code format", examples=["spa_Latn"]),
    ]


class TranslationBatch(BaseModel):
    """
    Summary
    -------
    the NLLB batch translation schema

    Attributes
    ----------
    translations (list[TranslationBatchItem])
        list of translation requests to process in batch
    """

    translations: Annotated[
        list[TranslationBatchItem],
        Field(
            min_length=1,
            max_length=128,
            description="list of translation requests to process in batch",
            examples=[
                [
                    {"text": "Hello, world!", "source": "eng_Latn", "target": "spa_Latn"},
                    {"text": "Bonjour le monde!", "source": "fra_Latn", "target": "eng_Latn"},
                ]
            ],
        ),
    ]


class TranslatedBatchItem(BaseModel):
    """
    Summary
    -------
    a single translated result in a batch response

    Attributes
    ----------
    result (str)
        the translated text
    """

    result: Annotated[
        str,
        Field(
            description="translated text in the language specified within the `target` request field",
            examples=["¡Hola, mundo!"],
        ),
    ]


class TranslatedBatch(BaseModel):
    """
    Summary
    -------
    the batch translated schema

    Attributes
    ----------
    results (list[TranslatedBatchItem])
        list of translated texts in the same order as the input requests
    """

    results: Annotated[
        list[TranslatedBatchItem],
        Field(
            description="list of translated texts in the same order as the input requests",
            examples=[{"result": "¡Hola, mundo!"}, {"result": "Hello, world!"}],
        ),
    ]

