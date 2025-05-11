import streamlit as st

def sentiment_display(emotion):
    """
    Displays the customer's current emotional sentiment with emoji and style.
    
    Args:
    - emotion: String - one of ['happy', 'neutral', 'curious', 'excited', 'reserved']
    """
    emoji_map = {
        "happy": "😊",
        "neutral": "😐",
        "curious": "🤔",
        "excited": "🤩",
        "reserved": "😶",
    }
    colors = {
        "happy": "#7ED957",
        "neutral": "#A9A9A9",
        "curious": "#FFD166",
        "excited": "#FF5733",
        "reserved": "#6C757D",
    }

    emoji = emoji_map.get(emotion.lower(), "❓")
    color = colors.get(emotion.lower(), "#000000")

    st.markdown(
        f"""
        <div style="
            display: flex; 
            align-items: center; 
            font-size: 1.3rem; 
            font-weight: 600; 
            padding: 0.5rem 1rem; 
            background-color: {color}22; 
            border-radius: 12px;
            width: fit-content;
            user-select:none;
            margin-bottom:1rem;
            ">
            <span style="font-size:2rem; margin-right: 0.6rem;">{emoji}</span>
            <span>Current Mood: {emotion.capitalize()}</span>
        </div>
        """, unsafe_allow_html=True
    )
