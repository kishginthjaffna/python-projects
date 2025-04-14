import requests
import json
import os
import re
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

# Configuration
RESPONSE_FILE = "last_response.txt"
DEBUG = True  # Set to False in production

# Clean up previous response file if it exists
if os.path.exists(RESPONSE_FILE):
    os.remove(RESPONSE_FILE)

llm = ChatGroq(
    temperature=0, 
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama3-70b-8192"
)

api_key = os.getenv("DEV_API_KEY")
if not api_key:
    print("❌ Please set the DEV_API_KEY environment variable.")
    exit()

# Strict JSON-only prompt template
full_article_prompt = PromptTemplate.from_template("""
Generate a DEV.to blog post about {input} and return ONLY a JSON object with these requirements:

1. Structure must be exactly:
{{
    "article": {{
        "title": "Your title here",
        "published": true,
        "body_markdown": "Markdown content with escaped newlines (\\n) and quotes (\\")",
        "tags": ["list", "of", "tags"],
        "series": ""
    }}
}}

2. Rules:
- Only return the JSON object, no other text
- Tags must be an array, not a string
- No markdown code blocks (```)
- No trailing commas
- All property names in double quotes
- No special characters(avoid space between words) and number of tags should not be exceed 3
""")

headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

def save_response(content):
    """Save raw response for debugging."""
    with open(RESPONSE_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    if DEBUG:
        print(f"Debug: Response saved to {RESPONSE_FILE}")

def extract_json_from_response(response_content):
    """Extract and parse JSON from LLM response with multiple fallback methods."""
    # Method 1: Try parsing as pure JSON first
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        pass
    
    # Method 2: Try extracting from code blocks
    try:
        json_match = re.search(r'```(?:json)?\n({.*?})\n```', response_content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
    except:
        pass
    
    # Method 3: Try finding any JSON structure
    try:
        json_match = re.search(r'{\s*"article".*?}', response_content, re.DOTALL)
        if json_match:
            # Clean the JSON string
            json_str = json_match.group(0)
            json_str = json_str.replace('\n', '\\n').replace('\t', '\\t')
            json_str = re.sub(r'(?<!\\)"', r'\"', json_str)  # Escape unescaped quotes
            return json.loads(json_str)
    except:
        pass
    
    # Method 4: Manual construction as last resort
    try:
        title = re.search(r'"title"\s*:\s*"(.*?)"', response_content)
        body = re.search(r'"body_markdown"\s*:\s*"(.*?)"', response_content, re.DOTALL)
        tags = re.search(r'"tags"\s*:\s*\[(.*?)\]', response_content) or \
               re.search(r'"tags"\s*:\s*"(.*?)"', response_content)
        
        if title and body:
            article_data = {
                "article": {
                    "title": title.group(1),
                    "published": True,
                    "body_markdown": body.group(1).replace('\n', '\\n').replace('"', '\\"'),
                    "tags": [],
                    "series": ""
                }
            }
            
            if tags:
                if tags.group(1).startswith('"'):
                    # Tags are in string format "tag1, tag2"
                    article_data["article"]["tags"] = [
                        t.strip().strip('"') for t in tags.group(1).split(',')
                    ]
                else:
                    # Tags are in array format [tag1, tag2]
                    article_data["article"]["tags"] = [
                        t.strip().strip('"\'') for t in tags.group(1).split(',')
                    ]
            
            return article_data
    except Exception as e:
        print(f"Debug: Manual construction failed - {str(e)}")
    
    return None

def validate_article_data(article_data):
    """Validate the article data structure."""
    if not article_data or not isinstance(article_data, dict):
        return False
    if "article" not in article_data:
        return False
    required_fields = ["title", "published", "body_markdown", "tags"]
    return all(field in article_data["article"] for field in required_fields)

print("🚀 Welcome to the DEV.to Blog Post Automation!")
choice = input("Do you already have markdown content? (yes/no): ").strip().lower()

if choice == "yes":
    print("Please paste your markdown content when prompted for the topic.")
    print("For now, please use 'no' and we'll generate everything for you.")
    exit()
elif choice == "no":
    topic = input("Enter your topic: ").strip()
    print("\nGenerating your article... Please wait...")
    
    try:
        response = llm.invoke(full_article_prompt.format(input=topic))
        response_content = response.content if hasattr(response, 'content') else str(response)
        save_response(response_content)
        
        article_data = extract_json_from_response(response_content)
        
        if not validate_article_data(article_data):
            print("\n❌ Failed to generate valid article data.")
            print("The raw response has been saved to last_response.txt")
            print("Please check the file and consider adjusting your prompt.")
            exit()
            
        # Final validation and cleaning
        if isinstance(article_data["article"]["tags"], str):
            article_data["article"]["tags"] = [
                t.strip() for t in article_data["article"]["tags"].split(',')
            ]
        
        print("\n✅ Article generated successfully!")
        print(f"Title: {article_data['article']['title']}")
        print(f"Tags: {', '.join(article_data['article']['tags'])}")
        
        # Post to DEV.to
        post = input("\nWould you like to post this to DEV.to now? (yes/no): ").strip().lower()
        if post == "yes":
            print("\nPosting to DEV.to...")
            response = requests.post("https://dev.to/api/articles", headers=headers, json=article_data)
            
            if response.status_code == 201:
                print("✅ Blog posted successfully!")
                print(f"🔗 URL: {response.json().get('url', 'URL not available')}")
            else:
                print(f"❌ Failed to post blog (Status {response.status_code}):")
                print(response.text)
        else:
            print("\nArticle data ready but not posted. You can find it in last_response.txt")
            
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        if os.path.exists(RESPONSE_FILE):
            print("The raw response has been saved to last_response.txt for debugging")
else:
    print("❌ Invalid input. Please enter 'yes' or 'no'.")