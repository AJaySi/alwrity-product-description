import os
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential
import google.generativeai as genai
import json

def main():
    set_page_config()
    custom_css()
    hide_elements()
    write_ai_prod_desc()


def set_page_config():
    st.set_page_config(
        page_title="Alwrity - AI Product Description Writer",
        layout="wide",
    )


def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
                    ::-webkit-scrollbar-track {
        background: #e1ebf9;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }

        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)


def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


def generate_product_description(title, details, audience, tone, length, keywords):
    """
    Generates a product description using OpenAI's API.

    Args:
        title (str): The title of the product.
        details (list): A list of product details (features, benefits, etc.).
        audience (list): A list of target audience segments.
        tone (str): The desired tone of the description (e.g., "Formal", "Informal").
        length (str): The desired length of the description (e.g., "short", "medium", "long").
        keywords (str): Keywords related to the product (comma-separated).

    Returns:
        str: The generated product description.
    """
    if not all([title, details, audience, tone, length, keywords]):
        st.error("Please fill in all the required fields.")
        return None

    prompt = f"""
        Write a compelling product description for {title}.

        Highlight these key features: {', '.join(details)} 

        Emphasize the benefits of these features for the target audience ({audience}). 
        Maintain a {tone} tone and aim for a length of approximately {length} words.

        Use these keywords naturally throughout the description: {', '.join(keywords)}.

        Remember to be persuasive and focus on the value proposition.
    """

    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)    



def display_inputs():
    st.title("🧕 ALwrity | AI Product Description Writer 🚀")
    st.markdown("**Generate compelling and accurate product descriptions with AI.**")

    col1, col2 = st.columns(2)

    with col1:
        product_title = st.text_input("🏷️ **Product Title**", placeholder="Enter the product title (e.g., Wireless Bluetooth Headphones)", help="Enter the title of your product.")
    with col2:
        product_details = st.text_area("📄 **Product Details**", placeholder="Enter features, benefits, specifications, materials, etc. (e.g., Noise Cancellation, Long Battery Life, Water Resistant, Comfortable Design)", help="List the key features and benefits of your product.")

    col3, col4 = st.columns(2)

    with col3:
        keywords = st.text_input("🔑 **Keywords**", placeholder="Enter keywords, comma-separated (e.g., wireless headphones, noise cancelling, Bluetooth 5.0)", help="Enter relevant keywords for your product, separated by commas.")
    with col4:
        target_audience = st.multiselect(
            "🎯 **Target Audience**",
            ["Teens", "Adults", "Seniors", "Music Lovers", "Fitness Enthusiasts", "Tech Savvy", "Busy Professionals", "Travelers", "Casual Users"],
            placeholder="Select target audience (optional)",
            help="Choose the audience your product is intended for."
        )

    col5, col6 = st.columns(2)

    with col5:
        description_length = st.selectbox(
            "📏 **Desired Description Length**",
            ["Short (1-2 sentences)", "Medium (3-5 sentences)", "Long (6+ sentences)"],
            help="Select the desired length of the product description"
        )
    with col6:
        brand_tone = st.selectbox(
            "🎨 **Brand Tone**",
            ["Formal", "Informal", "Fun & Energetic"],
            help="Select the desired tone for the description"
        )

    return product_title, product_details, target_audience, brand_tone, description_length, keywords


def write_ai_prod_desc():
    product_title, product_details, target_audience, brand_tone, description_length, keywords = display_inputs()

    if st.button("Generate Product Description 🚀"):
        with st.spinner("Generating description..."):
            progress_bar = st.progress(0)
            description = generate_product_description(
                product_title,
                product_details.split(", "),  # Split details into a list
                target_audience,
                brand_tone,
                description_length.split(" ")[0].lower(),  # Extract length from selectbox
                keywords
            )
            if description:
                st.subheader("✨ Generated Product Description:")
                st.markdown(description)
            progress_bar.progress(100)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 0.7,
            "top_k": 0,
            "max_output_tokens": 4096,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()
