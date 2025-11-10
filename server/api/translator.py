from typing import Annotated, get_args

from fastapi import APIRouter, Depends, Query, Request, Response, status
from sse_starlette.sse import EventSourceResponse

from server.guards import requires_secret
from server.schemas.v1 import Tokens, Translated, Translation, TranslationBatch, TranslatedBatch
from server.typedefs import Language, get_app_state

router = APIRouter()


@router.delete("/translator", dependencies=[Depends(requires_secret)], status_code=status.HTTP_204_NO_CONTENT)
def unload_model(
    request: Request,
    to_cpu: Annotated[bool, Query(description="whether to unload the model to CPU")] = False,
    state=Depends(get_app_state),
) -> Response:
    """
    Summary
    -------
    unload the model from the current device
    """
    if state.translator.unload_model(to_cpu=to_cpu):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_304_NOT_MODIFIED)


@router.put("/translator", dependencies=[Depends(requires_secret)], status_code=status.HTTP_204_NO_CONTENT)
def load_model(
    request: Request,
    keep_cache: Annotated[bool, Query(description="whether to keep the model cache in RAM")] = False,
    state=Depends(get_app_state),
) -> Response:
    """
    Summary
    -------
    load the model back to the initial device
    """
    if state.translator.load_model(keep_cache=keep_cache):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_304_NOT_MODIFIED)


@router.get("/translator/tokens", tags=["API"], response_model=Tokens)
def token_count(
    text: Annotated[str, Query(min_length=1, description="source text of a single language")],
    state=Depends(get_app_state),
) -> Tokens:
    """
    Summary
    -------
    count the number of tokens in the input text
    """
    return Tokens(length=state.translator.count_tokens(text))


@router.get("/translator", tags=["API"], response_model=Translated)
def translator_get(
    text: Annotated[
        str,
        Query(
            min_length=1,
            description="source text of a single language",
            examples=["Hello, world!", "¡Hola, mundo!"],
        ),
    ],
    source: Annotated[
        Language,
        Query(
            description="source language in the FLORES-200 code format",
            examples=[code for code in get_args(Language.__value__)],
        ),
    ] = "eng_Latn",
    target: Annotated[
        Language,
        Query(
            description="target language in the FLORES-200 code format",
            examples=[code for code in get_args(Language.__value__)],
        ),
    ] = "spa_Latn",
    state=Depends(get_app_state),
) -> Translated:
    """
    Summary
    -------
    the GET variant of the `/translator` route
    """
    return Translated(result=state.translator.translate(text, source, target))


@router.post("/translator/batch", tags=["API"], response_model=TranslatedBatch, status_code=status.HTTP_200_OK)
def translator_batch(
    data: TranslationBatch,
    state=Depends(get_app_state),
) -> TranslatedBatch:
    """
    Summary
    -------
    translate multiple texts in batch for improved GPU utilization

    Parameters
    ----------
    data (TranslationBatch)
        batch translation request containing list of translation items

    Returns
    -------
    TranslatedBatch
        batch translation response containing list of translated texts in the same order as input
    """
    texts = [item.text for item in data.translations]
    source_languages = [item.source for item in data.translations]
    target_languages = [item.target for item in data.translations]

    translated_texts = state.translator.translate_batch(texts, source_languages, target_languages)

    return TranslatedBatch(
        results=[{"result": text} for text in translated_texts],
    )


@router.post("/translator", tags=["API"], response_model=Translated, status_code=status.HTTP_200_OK, deprecated=True)
def translator_post(
    data: Translation,
    state=Depends(get_app_state),
) -> Translated:
    """
    Summary
    -------
    the POST variant of the `/translator` route
    """
    return Translated(result=state.translator.translate(data.text, data.source, data.target))


@router.get("/translator/stream", tags=["API"])
def translator_stream(
    request: Request,
    text: Annotated[
        str,
        Query(
            min_length=1,
            description="source text of a single language",
            examples=["Hello, world!", "¡Hola, mundo!"],
        ),
    ],
    source: Annotated[
        Language,
        Query(
            description="source language in the FLORES-200 code format",
            examples=[code for code in get_args(Language.__value__)],
        ),
    ] = "eng_Latn",
    target: Annotated[
        Language,
        Query(
            description="target language in the FLORES-200 code format",
            examples=[code for code in get_args(Language.__value__)],
        ),
    ] = "spa_Latn",
    event_type: Annotated[str | None, Query(description="the event that an event listener will listen for")] = None,
    state=Depends(get_app_state),
) -> EventSourceResponse:
    """
    Summary
    -------
    the `/translator/stream` returns a Server-Sent Event stream of the translation
    """
    async def generate():
        for chunk in state.translator.translate_stream(text, source, target):
            yield {"event": event_type, "data": chunk} if event_type else {"data": chunk}

    return EventSourceResponse(generate())

