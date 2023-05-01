from typing import Dict, List, Literal, Union

from .models import TSNEHParams, UMAPHParams

preset_k = [5, 7, 9, 11, 13, 15]
preset_min_support = [6, 7, 8, 9, 10]



preset_params = {
    "tsne": {
        "perplexity": [15, 30, 45],
        "learning_rate": ["auto", 200, 500, 800],
    },
    
    "umap": {
        "n_neighbors": [20, 80],
        "min_dist": [0.2, 0.5, 0.8],
        "init": ["spectral", "random"],
    },
}


PresetMethodNames = Literal["tsne10", "tsne20", "umap10", "umap20"]
preset_methods: Dict[PresetMethodNames, Union[List[TSNEHParams], List[UMAPHParams]]] = {
    "tsne10": [
        TSNEHParams(initialization="random", perplexity=45, learning_rate="auto")
        for _ in range(10)
    ],
    "tsne20":[
        TSNEHParams(initialization="random", perplexity=45, learning_rate="auto")
        for _ in range(20)
    ],
    "umap10": [UMAPHParams(n_neighbors=30, min_dist=0.15, init="spectral") for _ in range(10)],
    
    "umap20": [UMAPHParams(n_neighbors=15, min_dist=0.1, init="spectral") for _ in range(20)],
}
    