def chunk_text(text, chunk_size=750, overlap=150):
    """
    Splits text into chunks of specified character length with overlap.
    Returns list of dicts with 'index', 'text', 'char_length'.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_len = len(text)
    idx = 0

    while start < text_len:
        end = min(start + chunk_size, text_len)
        
        # Avoid breaking words in the middle if possible
        if end < text_len and text[end] not in [' ', '\n', '.', ',']:
            last_space = text.rfind(' ', start, end)
            if last_space > start:
                end = last_space

        chunk_snippet = text[start:end].strip()
        if chunk_snippet:
            chunks.append({
                'index': idx,
                'text': chunk_snippet,
                'char_length': len(chunk_snippet)
            })
            idx += 1

        start += (chunk_size - overlap)

    return chunks
