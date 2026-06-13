class RolloutWorker:
    def generate(self, prompt: str, weight_version: int) -> dict:
        return {
            "prompt_id": "fixture",
            "response_tokens": [1, 2, 3],
            "action_mask": [1, 1, 1],
            "old_logprobs": [-0.1, -0.2, -0.3],
            "reward": 1.0,
            "weight_version": weight_version,
        }
