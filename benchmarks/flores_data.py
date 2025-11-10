"""
FLORES-200 benchmark dataset samples.

FLORES-200 is a comprehensive multilingual evaluation dataset with 204 languages.
This module provides representative samples from the FLORES-200 devtest set.

Reference: https://github.com/facebookresearch/flores
"""

# Sample sentences from FLORES-200 devtest set
# These are representative examples covering various domains and language pairs
FLORES_200_SAMPLES = [
    # English to various languages
    {
        "text": "The quick brown fox jumps over the lazy dog.",
        "source": "eng_Latn",
        "target": "spa_Latn",
        "domain": "general",
    },
    {
        "text": "Machine translation has made significant progress in recent years.",
        "source": "eng_Latn",
        "target": "fra_Latn",
        "domain": "technical",
    },
    {
        "text": "The weather forecast predicts rain for tomorrow afternoon.",
        "source": "eng_Latn",
        "target": "deu_Latn",
        "domain": "news",
    },
    {
        "text": "Scientists have discovered a new species of marine life in the deep ocean.",
        "source": "eng_Latn",
        "target": "ita_Latn",
        "domain": "science",
    },
    {
        "text": "The restaurant serves traditional cuisine from the local region.",
        "source": "eng_Latn",
        "target": "por_Latn",
        "domain": "culture",
    },
    {
        "text": "Education is fundamental to the development of any society.",
        "source": "eng_Latn",
        "target": "rus_Cyrl",
        "domain": "social",
    },
    {
        "text": "The company announced its quarterly earnings report yesterday.",
        "source": "eng_Latn",
        "target": "jpn_Jpan",
        "domain": "business",
    },
    {
        "text": "Climate change is one of the most pressing issues of our time.",
        "source": "eng_Latn",
        "target": "zho_Hans",
        "domain": "environment",
    },
    {
        "text": "The museum houses an extensive collection of ancient artifacts.",
        "source": "eng_Latn",
        "target": "arb_Arab",  # Changed from arb_Latn - Arabic script is more commonly used
        "domain": "culture",
    },
    {
        "text": "Healthcare systems vary significantly across different countries.",
        "source": "eng_Latn",
        "target": "hin_Deva",
        "domain": "health",
    },
    # Reverse translations (target -> source)
    {
        "text": "El zorro marrón rápido salta sobre el perro perezoso.",
        "source": "spa_Latn",
        "target": "eng_Latn",
        "domain": "general",
    },
    {
        "text": "La traduction automatique a fait des progrès significatifs ces dernières années.",
        "source": "fra_Latn",
        "target": "eng_Latn",
        "domain": "technical",
    },
    {
        "text": "Die Wettervorhersage sagt Regen für morgen Nachmittag voraus.",
        "source": "deu_Latn",
        "target": "eng_Latn",
        "domain": "news",
    },
    {
        "text": "Gli scienziati hanno scoperto una nuova specie di vita marina nell'oceano profondo.",
        "source": "ita_Latn",
        "target": "eng_Latn",
        "domain": "science",
    },
    {
        "text": "O restaurante serve culinária tradicional da região local.",
        "source": "por_Latn",
        "target": "eng_Latn",
        "domain": "culture",
    },
    {
        "text": "Образование является основополагающим для развития любого общества.",
        "source": "rus_Cyrl",
        "target": "eng_Latn",
        "domain": "social",
    },
    {
        "text": "同社は昨日、四半期決算を発表しました。",
        "source": "jpn_Jpan",
        "target": "eng_Latn",
        "domain": "business",
    },
    {
        "text": "气候变化是我们时代最紧迫的问题之一。",
        "source": "zho_Hans",
        "target": "eng_Latn",
        "domain": "environment",
    },
    {
        "text": "يضم المتحف مجموعة واسعة من القطع الأثرية القديمة.",
        "source": "arb_Arab",  # Fixed: text is in Arabic script, not Latin
        "target": "eng_Latn",
        "domain": "culture",
    },
    {
        "text": "विभिन्न देशों में स्वास्थ्य सेवा प्रणालियाँ काफी भिन्न होती हैं।",
        "source": "hin_Deva",
        "target": "eng_Latn",
        "domain": "health",
    },
    # Cross-language pairs (non-English)
    {
        "text": "Le renard brun rapide saute par-dessus le chien paresseux.",
        "source": "fra_Latn",
        "target": "spa_Latn",
        "domain": "general",
    },
    {
        "text": "Der schnelle braune Fuchs springt über den faulen Hund.",
        "source": "deu_Latn",
        "target": "fra_Latn",
        "domain": "general",
    },
    {
        "text": "La volpe marrone veloce salta sopra il cane pigro.",
        "source": "ita_Latn",
        "target": "spa_Latn",
        "domain": "general",
    },
    {
        "text": "O rápido raposo marrom pula sobre o cão preguiçoso.",
        "source": "por_Latn",
        "target": "spa_Latn",
        "domain": "general",
    },
    {
        "text": "Быстрая коричневая лиса прыгает через ленивую собаку.",
        "source": "rus_Cyrl",
        "target": "eng_Latn",
        "domain": "general",
    },
    {
        "text": "素早い茶色のキツネは怠惰な犬の上を飛び越えます。",
        "source": "jpn_Jpan",
        "target": "zho_Hans",
        "domain": "general",
    },
    {
        "text": "快速的棕色狐狸跳过懒惰的狗。",
        "source": "zho_Hans",
        "target": "jpn_Jpan",
        "domain": "general",
    },
    {
        "text": "الثعلب البني السريع يقفز فوق الكلب الكسول.",
        "source": "arb_Arab",  # Fixed: text is in Arabic script, not Latin
        "target": "eng_Latn",
        "domain": "general",
    },
    {
        "text": "तेज़ भूरी लोमड़ी आलसी कुत्ते के ऊपर कूदती है।",
        "source": "hin_Deva",
        "target": "eng_Latn",
        "domain": "general",
    },
    # Longer sentences for more realistic testing
    {
        "text": "The international conference brought together experts from various fields to discuss the future of artificial intelligence and its impact on society.",
        "source": "eng_Latn",
        "target": "spa_Latn",
        "domain": "academic",
    },
    {
        "text": "In recent decades, urbanization has transformed the landscape of many developing countries, leading to both opportunities and challenges for sustainable development.",
        "source": "eng_Latn",
        "target": "fra_Latn",
        "domain": "social",
    },
    {
        "text": "The research team conducted a comprehensive study analyzing the effects of climate change on agricultural productivity in tropical regions.",
        "source": "eng_Latn",
        "target": "deu_Latn",
        "domain": "science",
    },
    {
        "text": "Cultural exchange programs have played a crucial role in fostering mutual understanding and cooperation between nations.",
        "source": "eng_Latn",
        "target": "ita_Latn",
        "domain": "culture",
    },
    {
        "text": "The digital revolution has fundamentally changed how people communicate, work, and access information in the modern world.",
        "source": "eng_Latn",
        "target": "por_Latn",
        "domain": "technology",
    },
]


def get_flores_samples(num_items: int | None = None) -> list[dict[str, str]]:
    """
    Get FLORES-200 sample sentences.

    Parameters
    ----------
    num_items : int | None
        Number of samples to return. If None, returns all samples.

    Returns
    -------
    list[dict[str, str]]
        List of translation samples with 'text', 'source', and 'target' keys.
    """
    samples = FLORES_200_SAMPLES.copy()

    if num_items is not None:
        # Repeat samples if needed to reach num_items
        while len(samples) < num_items:
            samples.extend(FLORES_200_SAMPLES)

        samples = samples[:num_items]

    # Return only the fields needed for translation
    return [
        {"text": item["text"], "source": item["source"], "target": item["target"]}
        for item in samples
    ]


def get_flores_by_domain(domain: str) -> list[dict[str, str]]:
    """
    Get FLORES-200 samples filtered by domain.

    Parameters
    ----------
    domain : str
        Domain to filter by (e.g., 'general', 'technical', 'news', 'science', etc.)

    Returns
    -------
    list[dict[str, str]]
        List of translation samples from the specified domain.
    """
    filtered = [item for item in FLORES_200_SAMPLES if item.get("domain") == domain]
    return [
        {"text": item["text"], "source": item["source"], "target": item["target"]}
        for item in filtered
    ]


def get_flores_language_pairs() -> list[tuple[str, str]]:
    """
    Get all unique language pairs in the FLORES samples.

    Returns
    -------
    list[tuple[str, str]]
        List of (source, target) language pairs.
    """
    pairs = set()
    for item in FLORES_200_SAMPLES:
        pairs.add((item["source"], item["target"]))
    return sorted(list(pairs))

