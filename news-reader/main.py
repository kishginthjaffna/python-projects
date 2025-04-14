import requests
import re
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Setup Groq LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key='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',
    model_name="llama3-70b-8192"
)

# Structured Prompt Template
full_prompt = PromptTemplate.from_template("""
You are a DevOps-savvy AI assistant. Summarize the following news article for developers and tech enthusiasts in the following format (use markdown):

**Title:** <title of article>

**Summary:** <3-4 lines summary>

**Key Takeaways:**
- <point 1>
- <point 2>
- <point 3>

**Technologies Involved:** <comma-separated list or N/A>

Article:
{content}
""")

# News API Config
API_KEY = '2d94b2f42ff32e2bbf8b6a14358ee3ca'
BASE_URL = 'https://gnews.io/api/v4/search'

def fetch_tech_news(topic):
    params = {
        'q': topic,
        'lang': 'en',
        'token': API_KEY,
        'max': 6,
        'sort': 'relevance',
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"Error fetching news: {response.status_code} - {response.text}")

    data = response.json()
    articles = data.get('articles', [])
    if not articles:
        return None

    summaries = []
    for article in articles:
        try:
            doc = WebBaseLoader(article['url']).load()
            content = doc[0].page_content

            prompt = full_prompt.format(content=content)
            llm_response = llm.invoke(prompt)
            response_text = llm_response.content

            # Extract data using regex
            summary_match = re.search(r"\*\*Summary:\*\*\s*(.+?)(?:\n\n|\Z)", response_text, re.DOTALL)
            takeaways = re.findall(r"- (.+)", response_text)
            tech_match = re.search(r"\*\*Technologies Involved:\*\*\s*(.+)", response_text)

            summaries.append({
                "title": article['title'],
                "summary": summary_match.group(1).strip() if summary_match else "Summary not found.",
                "keyTakeaways": takeaways[:3] if takeaways else [],
                "technologies": tech_match.group(1).strip().split(", ") if tech_match else []
            })

        except Exception as e:
            summaries.append({
                "title": "Error processing article",
                "summary": str(e),
                "keyTakeaways": [],
                "technologies": []
            })

    return summaries
