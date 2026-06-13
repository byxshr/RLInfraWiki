class Trainer:
    def export_checkpoint(self, path: str, policy_id: str, weight_version: int) -> dict:
        return {"path": path, "policy_id": policy_id, "weight_version": weight_version}
