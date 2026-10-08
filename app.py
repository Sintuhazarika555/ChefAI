import streamlit as st
from main import ChefAIEngine

# Page Configuration
st.set_page_config(
    page_title="ChefAI — Smart Kitchen Recommender",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Design: Pinkish-Red (#FF3366), Off-White (#FDFDFD), Deep Black (#0E0F12)
st.markdown("""
<style>
    /* Hide the Streamlit sidebar completely */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Primary Container & Background */
    .stApp {
        background-color: #0E0F12;
        color: #F8F9FA;
    }

    /* Headings & Accent Text */
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .accent-pink {
        color: #FF3366 !important;
    }

    /* Top About Card */
    .about-card {
        background: linear-gradient(135deg, rgba(255, 51, 102, 0.12) 0%, rgba(20, 21, 26, 0.8) 100%);
        border: 1px solid rgba(255, 51, 102, 0.35);
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 28px;
    }
    .about-card h3 {
        margin: 0 0 8px 0 !important;
        color: #FF3366 !important;
        font-size: 1.25rem;
    }
    .about-card p {
        color: #D1D5DB;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }

    /* Primary Action Button */
    div.stButton > button:first-child {
        background-color: #FF3366 !important;
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 1.05rem;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        transition: all 0.25s ease-in-out;
        box-shadow: 0 4px 14px rgba(255, 51, 102, 0.35);
    }
    div.stButton > button:first-child:hover {
        background-color: #E02456 !important;
        box-shadow: 0 6px 20px rgba(255, 51, 102, 0.55);
        transform: translateY(-1px);
    }

    /* Prediction Metrics Card */
    .metric-box {
        background-color: #17181F;
        border-left: 4px solid #FF3366;
        border-radius: 10px;
        padding: 18px 22px;
        height: 100%;
    }
    .metric-title {
        color: #9CA3AF;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 4px;
    }

    /* Distribution Badges Container */
    .distribution-panel {
        background-color: #17181F;
        border: 1px solid #282936;
        border-radius: 10px;
        padding: 18px 22px;
    }
    .taste-badge {
        display: inline-block;
        background-color: #21232D;
        border: 1px solid #323544;
        border-radius: 8px;
        padding: 8px 14px;
        margin: 4px;
        font-size: 0.9rem;
    }
    .taste-badge span {
        color: #FF3366;
        font-weight: 600;
    }

    /* Custom Streamlit Expander Cards */
    .streamlit-expanderHeader {
        background-color: #17181F !important;
        border-radius: 8px !important;
        color: #F9FAFB !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load inference engine
@st.cache_resource
def get_engine():
    return ChefAIEngine()

engine = get_engine()

# Header & Hero Title
st.markdown("<h1 style='text-align: center; margin-bottom: 4px;'>👨‍🍳 <span class='accent-pink'>ChefAI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 1.1rem; margin-bottom: 20px;'>Intelligent Flavor Profiling & Constrained Kitchen Recommendation</p>", unsafe_allow_html=True)

# About Section
st.markdown("""
<div class="about-card">
    <h3>About ChefAI</h3>
    <p>
    Wondering what to make with whatever is left in your fridge? Just enter your ingredients, choose your <strong>cookware on hand</strong>, and set your <strong>available time</strong>. ChefAI instantly figures out your ingredients' dominant flavor—whether (<em>Sweet, Savory, Spicy, Tangy, Umami</em>)—and serves up delicious, easy-to-follow recipes tailored specifically to your <strong>available appliances</strong> and <strong>maximum preparation time</strong>. No endless scrolling, no fancy chef gear required—just great meals with what you already own.
</p>
</div>
""", unsafe_allow_html=True)

# Main Input Section: Top Controls
st.markdown("### 🧺 1. Your Pantry & Ingredients")
ingredients_input = st.text_area(
    label="Pantry Ingredients",
    placeholder="e.g., chicken breast, garlic, olive oil, rosemary, lemon, black pepper",
    height=90,
    label_visibility="collapsed"
)

# Kitchen Constraints (Horizontal Layout, No Sidebar)
st.markdown("### ⚙️ 2. Kitchen Constraints & Equipment")
col_time, col_equip, col_taste, col_topk = st.columns([1.2, 1.8, 1.2, 0.8])

with col_time:
    max_time = st.slider(
        "⏱️ Max Time (Minutes)",
        min_value=5,
        max_value=120,
        value=30,
        step=5
    )

with col_equip:
    equipment = st.multiselect(
        "🍳 Available Appliances",
        options=["stovetop", "oven", "microwave", "blender", "slow_cooker"],
        default=["stovetop", "oven"]
    )

with col_taste:
    taste_pref = st.selectbox(
        "👅 Flavor Craving",
        options=["Any", "Savory", "Sweet", "Spicy", "Tangy", "Umami"],
        index=0
    )

with col_topk:
    top_k = st.number_input("📋 Results", min_value=1, max_value=10, value=3)

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# Run Button
if st.button("✨ Discover Matching Recipes", use_container_width=True):
    if not ingredients_input.strip():
        st.warning("Please enter at least one ingredient to begin.")
    elif not equipment:
        st.warning("Please choose at least one kitchen appliance.")
    else:
        with st.spinner("Analyzing ingredient chemistry and querying recipe index..."):
            res = engine.run(
                ingredients=ingredients_input,
                max_time=max_time,
                equipment=equipment,
                taste_pref=taste_pref,
                top_k=top_k
            )

        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

        

        # Result Section: Top Recipe Recommendations
        st.markdown(f"### 🍽️ Matching Recipes ({len(res['matches'])} found)")

        if not res["matches"]:
            st.info("No recipes matched all your exact criteria. Try increasing the time limit or enabling additional cookware.")
        else:
            for idx, r in enumerate(res["matches"], 1):
                header_title = f"#{idx}: {r['title']}  •  {r['match_score']}% Match"
                with st.expander(header_title, expanded=(idx == 1)):
                    # Metadata Badges
                    m1, m2, m3 = st.columns(3)
                    m1.markdown(f"⏱️ **Cook Time:** `{r['cook_time_mins']} mins`")
                    m2.markdown(f"🍳 **Equipment:** `{', '.join(r['equipment'])}`")
                    m3.markdown(f"👅 **Taste Profile:** `{r['taste_profile']}`")

                    st.markdown("---")
                    st.markdown("#### 🛒 Ingredients Required")
                    st.write(r["ingredients"])

                    st.markdown("#### 👨‍🍳 Step-by-Step Directions")
                    st.write(r["directions"])