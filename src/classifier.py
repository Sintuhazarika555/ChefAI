# for taste prediction according to the ingredients

def predict_taste(ingredients_text: str, tfidf, mlp, label_encoder):
    
    vec = tfidf.transform([ingredients_text])
    pred_idx = mlp.predict(vec)[0]
    taste = label_encoder.inverse_transform([pred_idx])[0]
    
    probs = mlp.predict_proba(vec)[0]
    confidence = float(probs[pred_idx] * 100)
    
    breakdown = {
        cls: round(float(prob * 100), 1)
        for cls, prob in zip(label_encoder.classes_, probs)
    }
    return taste, confidence, breakdown