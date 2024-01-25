import numpy as np
import torch

torchfy = lambda x: torch.as_tensor(x, dtype=torch.float32)


class Recommender:
    def __init__(self, co, model_name):
        self.co = co
        self.model_name = model_name

    def get_similarity(self, input_text: str, candidates, top_k: int):
        vectors_to_search = np.array(
            self.co.embed(model=self.model_name, texts=[input_text], truncate="RIGHT").embeddings,
            dtype=np.float32,
        )
        torched_candidates = torchfy(candidates).transpose(0, 1)
        target = torchfy(vectors_to_search)
        cos_scores = torch.mm(target, torched_candidates)

        scores, indices = torch.topk(cos_scores, k=top_k)
        similarity_hits = [{'id': idx, 'score': score} for idx, score in zip(indices[0].tolist(), scores[0].tolist())]

        return similarity_hits
