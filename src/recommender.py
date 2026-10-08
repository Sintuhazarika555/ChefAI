# here the recommendation work will done 

from sklearn.metrics.pairwise import cosine_similarity

def rank_recipes(user_text: str, candidate_df, tfidf, full_catalog_matrix, top_k: int = 3):
    if candidate_df.empty:
        return []
        
    user_vec = tfidf.transform([user_text])
    candidate_matrix = full_catalog_matrix[candidate_df.index]
    
    scores = cosine_similarity(user_vec, candidate_matrix).flatten()
    top_indices = scores.argsort()[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        score = scores[idx]
        if score <= 0.0:
            continue
        # Use .iloc here (integer location)
        row = candidate_df.iloc[idx]
        results.append({
            "title": row["title"],
            "match_score": round(float(score) * 100, 1),
            "cook_time_mins": int(row["cook_time_mins"]),
            "equipment": list(row["equipment"]),
            "taste_profile": row["taste_profile"],
            "ingredients": row["clean_ingredients"],
            "directions": row["clean_directions"]
        })
    return results