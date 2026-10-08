from src.loader import load_all_artifacts # for all artifacts loading in main
from src.classifier import predict_taste # for taste classification 
from src.filter import filter_recipes # filtering required set
from src.recommender import rank_recipes # main model


class ChefAIEngine:
    def __init__(self):
        self.tfidf, self.mlp, self.label_encoder, self.df, self.catalog_matrix = load_all_artifacts()

    def run(self, ingredients: str, max_time: int, equipment: list, taste_pref: str = "Any", top_k: int = 3):
        if not ingredients.strip():
            return {"error": "No ingredients provided"}
            
        taste, conf, breakdown = predict_taste(ingredients, self.tfidf, self.mlp, self.label_encoder)
        candidate_df = filter_recipes(self.df, max_time, equipment, taste_pref)
        matches = rank_recipes(ingredients, candidate_df, self.tfidf, self.catalog_matrix, top_k)
        
        return {
            "taste": taste,
            "confidence": conf,
            "breakdown": breakdown,
            "matches": matches
        }

if __name__ == "__main__":
    engine = ChefAIEngine()
    # Note: 'equipment' matches the parameter name in engine.run()
    res = engine.run("eggs butter cheese", max_time=30, equipment=["stovetop"])
    print("Predicted Taste:", res["taste"])
    print("Confidence:", f"{res['confidence']:.1f}%")
    print("Top Match:", res["matches"][0]["title"] if res["matches"] else "None")