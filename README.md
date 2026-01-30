# 🤖 Website RAG Chatbot

Hi! 👋 This is my submission for the **AI/ML Engineer Assignment**. 

I have built a Website-Based Chatbot that can "read" any website you give it and answer questions based **only** on that website's content. It uses RAG (Retrieval-Augmented Generation) to make sure it doesn't make things up!

## 🚀 Project Overview
The goal was to create a chatbot that:
1. Takes a website URL from the user.
2. Scrapes and cleans the text data.
3. Turns that text into "embeddings" (number vectors).
4. Stores them in a database.
5. Uses a Large Language Model (LLM) to answer user questions using that data.

**Key Feature:** If the answer isn't on the website, the bot honestly says: *"The answer is not available on the provided website."* (No hallucinations allowed! 🚫)

## 🛠️ Tech Stack & Decisions

Here is what I used and why I chose them:

### 1. The Brain (LLM): **Google Gemini 1.5 Flash** 🧠
* **Model Name:** `gemini-flash-latest`
* **Why I chose it:** * It's extremely fast and efficient.
    * It has a generous free tier for developers like me.
    * It supports a large context window, which is great for understanding website content.

### 2. The Memory (Vector Database): **ChromaDB** 💾
* **Why I chose it:**
    * It is open-source and runs locally (no complex cloud setup needed).
    * It integrates really well with Python and LangChain concepts.
    * Perfect for a lightweight project like this.

### 3. The Translator (Embeddings): **Sentence-Transformers** 🗣️
* **Model:** `all-MiniLM-L6-v2`
* **Why I chose it:**
    * It's small and runs fast on a standard laptop CPU.
    * It creates high-quality embeddings specifically for semantic search.
    * It's free and local (doesn't eat up API quotas).

### 4. The Interface: **Streamlit** 🎨
* **Why I chose it:** It allowed me to build a clean, interactive UI in pure Python without needing to learn HTML/CSS/React.

---

## 🏗️ Architecture (How it works)

Here is the flow of data in my app:

1.  **Crawl:** The app uses `requests` and `BeautifulSoup` to fetch the HTML and strip out "junk" (like ads, scripts, and navbars).
2.  **Chunk:** The clean text is split into smaller chunks (1000 characters) so the AI doesn't get overwhelmed.
3.  **Embed:** Each chunk is converted into numbers (vectors) using `all-MiniLM-L6-v2`.
4.  **Store:** These vectors are saved in `ChromaDB`.
5.  **Retrieve:** When you ask a question, the system looks for the most similar text chunks in the database.
6.  **Answer:** The relevant chunks + your question are sent to **Gemini**, which writes the final answer.

---

## ⚙️ Setup & How to Run

Follow these steps to run the chatbot on your machine:

**Prerequisites:** You need Python 3.11 installed.

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-link-here>
    cd humanli-rag-chatbot
    ```

2.  **Install Dependencies**
    I included a `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Key**
    * Get a free API Key from [Google AI Studio](https://aistudio.google.com/).
    * Create a file named `.env` in the main folder.
    * Add your key inside it like this:
        ```
        GOOGLE_API_KEY=your_paste_key_here
        ```

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```

---

## 🔮 Limitations & Future Improvements

Since this is a fresher project, there are a few things I'd like to improve later:

* **JavaScript Support:** Currently, the crawler uses `requests`, so it can't read websites that require JavaScript to load (like React apps). I would add Selenium or Playwright later.
* **Chat History:** Right now, the memory is short-term (session only). I would like to add a database to save chat history permanently.
* **Multi-URL Support:** Currently, it handles one link. I'd love to make it crawl a whole domain (sub-pages).

---

**Thank you for checking out my project!** I learned a lot about RAG pipelines and Vector DBs while building this. 🚀