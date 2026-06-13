def score(response_tokens: list[int], timeout_s: float = 5.0) -> float:
    return 1.0 if response_tokens else 0.0
