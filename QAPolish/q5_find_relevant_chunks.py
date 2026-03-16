from typing import List, Dict


def find_relevant_chunks(query_embedding: List[float], text_chunks: List[Dict], k: int) -> List[str]:
    """Return the text of the k most similar chunks by cosine similarity.

    Assumes embeddings are already normalized so cosine similarity reduces to dot product.

    Args:
        query_embedding: Normalized query embedding (list of floats).
        text_chunks: List of dicts with keys 'text' (str) and 'embedding' (list[float]).
        k: Number of top chunks to return.

    Returns:
        List of chunk['text'] for the top-k most similar chunks (highest dot product).
    """
    if not text_chunks:
        return []
    # Compute scores
    scores = []
    q = query_embedding
    for chunk in text_chunks:
        emb = chunk.get('embedding')
        if not emb:
            score = -1.0
        else:
            # dot product
            score = sum(a * b for a, b in zip(q, emb))
        scores.append((score, chunk.get('text', '')))

    # Get top-k by score
    scores.sort(key=lambda x: x[0], reverse=True)
    topk = scores[:max(0, k)]
    return [t for _, t in topk]


if __name__ == '__main__':
    q_emb = [0.0, 1.0, 0.0]
    chunks = [
        {'text': 'A', 'embedding': [0.0, 1.0, 0.0]},
        {'text': 'B', 'embedding': [1.0, 0.0, 0.0]},
        {'text': 'C', 'embedding': [0.0, 0.7, 0.7]},
    ]
    print(find_relevant_chunks(q_emb, chunks, 2))
