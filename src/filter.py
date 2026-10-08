# apply filter to the data values and generate the data values which are in our need.

def filter_recipes(df, max_time: int, user_equipment: list, taste_pref: str = "Any"):
    user_eq = set(e.strip().lower() for e in user_equipment)
    
    def can_cook(recipe_eq):
        if recipe_eq is None or len(recipe_eq) == 0:
            return True
        return set(recipe_eq).issubset(user_eq)
    
    mask = (df["cook_time_mins"] <= max_time) & (df["equipment"].apply(can_cook))
    
    if taste_pref != "Any":
        mask = mask & (df["taste_profile"] == taste_pref)
        
    return df[mask]
    