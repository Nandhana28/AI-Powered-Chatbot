# AI-Powered Chatbot for Structured Data Analysis

## Overview
This project is an AI-powered chatbot that enables users to **query, summarize, and analyze structured data** (Excel, PDF, CSV). Built using **Python, Streamlit, LangChain, FAISS, and Google Gemini API**, it provides an intuitive interface for seamless data interaction.

## Features
 **Upload multiple files** (PDF, TXT, CSV, XLS, XLSX)  
 **Conversational AI** for answering queries  
 **Summarization of key insights**  
 **Accuracy validation for reliable responses**  
 **Dark & Light mode support**  
 **Real-time deployment with Streamlit**  
 **Easy-to-use UI with clear history option**  

---

## Installation Guide
### 1) Clone the Repository
```bash
git clone https://github.com/Nandhana28/AI-Powered-Chatbot.git
cd AI-Powered-Chatbot
```

### 2️) Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️) Install Required Libraries
```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```bash
pip install streamlit pandas PyPDF2 langchain langchain-google-genai google-generativeai faiss-cpu python-dotenv
```

### 4️) Set Up API Keys
Create a `.env` file in the project root and add your **Google API Key**:
```ini
GOOGLE_API_KEY=your_google_api_key
```

---

## How to Use
### 1️) Run the Chatbot
```bash
streamlit run app.py
```
or
```bash
python -m streamlit run app.py
```

### 2️) Uploading Files
- Click **"Upload Files"** button in the sidebar.
- Select multiple files **(PDF, CSV, TXT, XLS, XLSX)**.
- Click **"Submit & Process"** to extract and process text.
- Wait for the success message: "Files processed successfully!"

### 3️) Querying the Chatbot
- Type a question in the chat input.
- Press **Enter** or click the **"Send"** button.
- The chatbot will process your query and respond with insights.

### 4️) Clearing Chat History
- Click the **"Clear Chat History"** button in the sidebar.
- This will remove all past chat messages and reset the session.

### 5️) Switching Between Dark & Light Mode
- Streamlit automatically detects system preferences.
- To manually change it, use **"Settings" → "Theme"**.

---

## Deployment Guide
### 1️) Deploy on Streamlit Cloud
- Push your project to **GitHub**.
- Go to [Streamlit Cloud](https://streamlit.io/cloud).
- Click **"Deploy an app"**.
- Select your **GitHub repo** & branch.
- Set up environment variables (**GOOGLE_API_KEY**).
- Click **"Deploy"**.

### 2️) Deploy on Heroku (Optional)
```bash
heroku login
heroku create your-app-name
heroku config:set GOOGLE_API_KEY=your_google_api_key
heroku buildpacks:add heroku/python
git push heroku main
heroku open
```

---

## Contributing
- Fork the repository.
- Create a feature branch (`git checkout -b feature-name`).
- Commit changes (`git commit -m "Added feature"`).
- Push to your fork (`git push origin feature-name`).
- Open a **Pull Request**.

---

## License
This project is licensed under the **MIT License**.

---

## Contact
**Nandhana S**  
Email: nandhana.cbe@gmail.com  
GitHub: [Nandhana28](https://github.com/Nandhana28)  

