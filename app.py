import streamlit as st
import pint
from deep_translator import GoogleTranslator
from fpdf import FPDF
from typing import Tuple, List

# Initialize the unit registry
ureg = pint.UnitRegistry()

# Initialize translator
translator = GoogleTranslator(source="auto", target="es")

# Set page configuration
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS to make the app more beautiful
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
    .stButton {
        margin-top: 1rem;
    }
    .result-container {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-top: 2rem;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Define conversion categories and their units
CONVERSION_CATEGORIES = {
    "Length": ["meters", "kilometers", "miles", "feet", "inches", "centimeters"],
    "Weight": ["kilograms", "grams", "pounds", "ounces"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Volume": ["liters", "milliliters", "gallons", "cups"],
    "Time": ["seconds", "minutes", "hours", "days"],
    "Speed": ["meters_per_second", "kilometers_per_hour", "miles_per_hour"],
}

# Language options
languages = {
    "English": "en",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "German": "de"
}

# Function to translate text
def translate_text(text: str, dest_language: str) -> str:
    try:
        translated = GoogleTranslator(source="auto", target=dest_language).translate(text)
        return translated
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return text  # Fallback to original text if translation fails

# Sidebar for language and theme selection
with st.sidebar:
    st.header("⚙️ Settings")
    # Language selection
    selected_lang = st.selectbox("Select Language", list(languages.keys()))
    lang_code = languages[selected_lang]
    # Theme selection
    theme = st.selectbox("Choose Theme", ["Light", "Dark"])

# Apply theme
if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        .result-container {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        h1 {
            color: white;
        }
        /* Form text color */
        .stNumberInput label, .stSelectbox label, .stButton button, .stMarkdown {
            color: white !important;
        }
        /* Save as PDF button text color */
        .stButton button {
            color: black !important;
        }
        .st.subheader {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }
        .result-container {
            background-color: #f0f2f6;
            color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def convert_units(value: float, from_unit: str, to_unit: str) -> Tuple[float, bool]:
    """Convert value from one unit to another using Pint."""
    try:
        # Handle temperature conversions separately
        if from_unit in ["celsius", "fahrenheit", "kelvin"]:
            from_unit = from_unit.replace("celsius", "degC").replace("fahrenheit", "degF").replace("kelvin", "K")
        if to_unit in ["celsius", "fahrenheit", "kelvin"]:
            to_unit = to_unit.replace("celsius", "degC").replace("fahrenheit", "degF").replace("kelvin", "K")
        
        # Create quantities and convert
        quantity = value * ureg(from_unit)
        result = quantity.to(to_unit)
        return float(result.magnitude), True
    except Exception:
        return 0.0, False

# Main app layout
st.title(translate_text("📏 Smart Unit Converter", lang_code))

# Sidebar for category selection
with st.sidebar:
    category = st.selectbox(
        translate_text("Select Category", lang_code),
        list(CONVERSION_CATEGORIES.keys()),
        key="category"
    )

# Main conversion interface
col1, col2 = st.columns(2)

with col1:
    st.subheader(translate_text("From", lang_code))
    input_value = st.number_input(translate_text("Enter Value", lang_code), value=1.0, format="%f")
    from_unit = st.selectbox(translate_text("From Unit", lang_code), CONVERSION_CATEGORIES[category], key="from_unit")

with col2:
    st.subheader(translate_text("To", lang_code))
    to_unit = st.selectbox(translate_text("To Unit", lang_code), CONVERSION_CATEGORIES[category], key="to_unit")

# Perform conversion
if st.button(translate_text("Convert", lang_code), type="primary"):
    result, success = convert_units(input_value, from_unit, to_unit)
    
    if success:
        result_text = f"{input_value} {from_unit} = {result:.4f} {to_unit}"
        st.markdown("### " + translate_text("Result", lang_code))
        st.markdown(f"""
        <div class="result-container">
            <h3 style="text-align: center; color: #1f77b4;">
                {result_text}
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Save to conversion history
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        st.session_state['history'].append(result_text)
    else:
        st.error(translate_text("Sorry, couldn't perform the conversion. Please check your units.", lang_code))

# Conversion History
if 'history' in st.session_state and st.session_state['history']:
    st.subheader(translate_text("Conversion History", lang_code))
    for entry in st.session_state['history']:
        st.write(entry)

# Save as PDF
if st.button(translate_text("Save as PDF", lang_code)):
    if 'history' in st.session_state and st.session_state['history']:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=translate_text("Conversion History", lang_code), ln=True)
        for entry in st.session_state['history']:
            pdf.cell(200, 10, txt=entry, ln=True)
        pdf.output("conversion_history.pdf")
        st.success(translate_text("PDF saved successfully!", lang_code))
    else:
        st.warning(translate_text("No conversion history to save.", lang_code))

# Add helpful information
with st.expander(translate_text("ℹ️ How to use", lang_code)):
    st.markdown(translate_text("""
    1. Select a conversion category from the sidebar
    2. Enter the value you want to convert
    3. Choose the units you want to convert from and to
    4. Click the Convert button to see the result
    
    The converter supports various units across different categories including length,
    weight, temperature, volume, time, and speed.
    """, lang_code))

# Footer
st.markdown("---")
st.markdown(
    translate_text("Made with ❤️ using Streamlit and Pint", lang_code),
    unsafe_allow_html=True
)