def validate_content(content: str, topic: str, content_length: str):
    if not content or not content.strip():
        return False, "Generated content is empty."

    minimum_lengths = {
        "Short": 50,
        "Medium": 100,
        "Long": 200,
    }

    minimum = minimum_lengths.get(content_length, 50)

    if len(content.strip()) < minimum:
        return False, "Generated content is shorter than requested."

    return True, "Content validation successful."
