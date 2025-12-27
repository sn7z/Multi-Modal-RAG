
# utils/confidence.py

class ConfidenceScorer:

    def __init__(self, max_distance: float = 1.0, min_confidence: float = 0.2):
        self.max_distance = max_distance
        self.min_confidence = min_confidence

    def _distance_to_confidence(self, distance: float) -> float:

        # Convert distance to confidence score (0 to 1).
        if distance is None:
            return 0.0

        confidence = 1.0 - (distance / self.max_distance)
        return max(0.0, min(confidence, 1.0))

    def compute_confidence(self, retrieved_chunks: list) -> dict:

        if not retrieved_chunks:
            return {
                "confidence": 0.0,
                "confidence_percent": "0%",
                "status": "No relevant context found"
            }

        chunk_confidences = []

        for chunk in retrieved_chunks:
            distance = chunk.get("score")
            conf = self._distance_to_confidence(distance)
            chunk_confidences.append(conf)

        # Weighted average (top chunks matter more)
        weights = list(range(len(chunk_confidences), 0, -1))
        weighted_sum = sum(c * w for c, w in zip(chunk_confidences, weights))
        confidence = weighted_sum / sum(weights)

        status = (
            "High confidence"
            if confidence >= self.min_confidence
            else "Low confidence – answer may be incomplete"
        )

        return {
            "confidence": round(confidence, 3),
            "confidence_percent": f"{round(confidence * 100)}%",
            "status": status
        }