# RAG Multi-PDF Chat App 📚💬

### App Link - [Live](https://super-chat-pdf.streamlit.app/)

This repository contains a project focused on building a conversational AI application that can interact with and answer questions from multiple PDF documents using Retrieval-Augmented Generation (RAG).

## Project Overview 🌟

The **RAG Multi-PDF Chat App** enables users to upload multiple PDF documents and query them for specific information. It uses a combination of natural language processing (NLP) and advanced machine learning models to retrieve relevant content and generate precise answers.

## Screenshots

![App Screenshot](https://raw.githubusercontent.com/Prathmeshpawar21/Resources/refs/heads/main/SS/ragpdf1-modified.png)

## Features 🎯

- Upload and process multiple PDFs.
- Ask natural language questions about the content.
- Retrieve precise and context-aware responses.
- Intuitive web-based interface for easy interaction.

## Technologies Used 🛠️

- **Python**
- **Libraries:** PyPDF2, OpenAI API, Hugging Face Transformers, Streamlit
- **Frontend:** HTML, CSS, JavaScript
- **Frameworks:** Flask, Langchain
- **Database:** Vector databases (FAISS)
- **Model Pipeline:**  
  - **Embedding Model:** `all-MiniLM-L6-v2` – A lightweight and efficient embedding model for semantic text representation.  
  - **Conversation Chain Model:** `Mistral-7B-Instruct-v0.2` – A powerful instruction-tuned language model optimized for conversational AI.  


## Project Structure 🗂️

```
├── assets
│   ├── bot_image.png
│   └── user_image.png
├── pdf
│   ├── 1...
│   ├── 2...
│   └── 3...
├── .evn
├── .gitignore
├── app.py
├── conversationChain.json
├── htmlTemplates.py
├── requirements.txt
└── README.md
```

## Setup Instructions ⚙️

1. Clone the repository:
   ```bash
   git clone https://github.com/Prathmeshpawar21/GPT-RAG-FineTune-Custom-Model.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
    **OR**

3. Create and activate a virtual environment using Anaconda:
   ```bash
   conda create -n venv python=3.12.0 -y
   conda activate venv 
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000`.

## How It Works 🧠

1. **Document Upload:** Users upload one or more PDF documents to the application.
2. **Preprocessing:** PDFs are processed to extract text.
3. **Embedding:** The text is embedded using a transformer model and stored in a vector database.
4. **Query Handling:** User questions are matched against stored embeddings, and relevant context is retrieved.
5. **Answer Generation:** The context is passed to a language model to generate accurate answers.

## Results 🏆

- **Performance:** High accuracy and relevance in response generation.
- **Efficiency:** Handles multiple PDFs with ease.

## Future Improvements 🚀

- Add support for other document formats (e.g., Word, Excel).
- Implement user authentication for document privacy.
- Optimize embedding generation for larger document sets.
- Extend support to cloud-based vector databases.

## Contributing 🤝

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Open a Pull Request.

## 🔗 Links

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](#)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](#)

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
