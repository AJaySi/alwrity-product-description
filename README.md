## Alwrity AI Product Description Writer - Streamlit App

**A powerful AI-powered tool for generating compelling product descriptions that boost sales and drive conversions.**

This Streamlit app leverages the power of AI(Google Gemini) to help you craft engaging product descriptions that captivate customers and optimize your e-commerce presence. 

**Features:**

* **AI-Powered Description Generation:** Quickly generate high-quality product descriptions using advanced AI models.
* **Customizable Settings:**  Control the tone, length, target audience, and keywords for tailored descriptions.
* **SEO Optimization:**  Create descriptions that are optimized for search engines, improving your website's visibility.
* **User-Friendly Interface:**  A simple and intuitive Streamlit app makes it easy to use.

**Getting Started:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/alwrity-product-description-writer.git
   ```
2. **Install Dependencies:**
   ```bash
   cd alwrity-product-description-writer
   pip install -r requirements.txt
   ```
3. **Create a `.env` File:**
   - Create a file named `.env` in the project directory.
   - Add your API keys for the chosen AI model (OpenAI, Google Gemini, etc.):
     ```
     OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
     # Or  GEMINI_API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY" 
     ```
4. **Run the App:**
   ```bash
   streamlit run main.py
   ```

**Usage:**

*  Launch the app in your web browser.
*  Provide the required product details, including title, features, benefits, target audience, tone, length, and keywords.
*  Click the "Generate Product Description" button.
*  Review and edit the AI-generated description as needed.

**Additional Notes:**

* This app requires an API key for the chosen AI model (OpenAI, Google Gemini, etc.). 
*  You can customize the app's behavior and features by modifying the code in the `lib` directory.
*  The `prompt_llm.txt` file in the `lib/workspace/alwrity_prompts` directory contains prompts for the AI models. You can adjust these prompts to refine the output.

**Contributions:**

Contributions to this project are welcome! Feel free to open an issue or submit a pull request.


**Let's get writing!**


