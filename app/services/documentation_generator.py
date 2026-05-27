from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings

class DocumentationGenerator:
    
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",      # Fast + Free tier friendly
            temperature=0.3,
            api_key=settings.GROQ_API_KEY
        )

    def generate_changelog(self, change_event: dict) -> str:
        prompt = ChatPromptTemplate.from_template("""
        You are a senior technical writer.
        Write a clean, professional changelog entry:

        Repository: {repo_name}
        Change Type: {event_type}
        Details: {change_summary}

        Use markdown with proper formatting and emojis.
        Keep it short and useful.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({
            "repo_name": change_event.get("repository", "Unknown"),
            "event_type": change_event.get("event_type", "change"),
            "change_summary": str(change_event.get("changes", ""))
        })
        return response.content