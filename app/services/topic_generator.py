# app/services/topic_generator.py

import re
from transformers import pipeline, set_seed
from app.config import MODEL_NAMES

generator = pipeline("text-generation", model=MODEL_NAMES["text_generator"])
set_seed(42)

def generate_topics(event_themes, user_interests, facts=None, bio=None):
    facts = facts or []
    valid_facts = [f for f in facts if f and "failed" not in f.lower() and "no summary" not in f.lower()]
    fact_snippet = valid_facts[0][:200] if valid_facts else ""
    bio_snippet = f"About me: {bio}. " if bio else ""

    prompt = (
        f"I'm at a networking event about {', '.join(event_themes)}. "
        f"I'm interested in {', '.join(user_interests)}. "
        f"{bio_snippet}"
        f"Fact: {fact_snippet} "
        f"A good conversation starter I could say is:"
    )

    outputs = generator(
        prompt,
        max_new_tokens=40,
        num_return_sequences=3,
        do_sample=True,
        temperature=0.9,
        top_p=0.92,
        repetition_penalty=1.3,
        no_repeat_ngram_size=3,
        return_full_text=False,
        pad_token_id=generator.tokenizer.eos_token_id,
    )

    suggestions = []
    for out in outputs:
        text = out["generated_text"].strip()
        match = re.search(r"^(.*?[.!?])", text)  # cut at first full sentence
        cleaned = match.group(1) if match else text
        if cleaned:
            suggestions.append(cleaned)

    return suggestions if suggestions else ["Could not generate a starter this time — try again."]