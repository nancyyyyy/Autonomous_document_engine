from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings

class MultiDocGenerator:
    
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.3,
            api_key=settings.GROQ_API_KEY,
            max_tokens=1000
        )

    def generate_all_docs(self, change_data: dict) -> dict:
        """Generate multiple types of documentation for a code change"""
        
        repo_name = change_data.get("repository", "Unknown Repository")
        event_type = change_data.get("event_type", "code change")
        raw_changes = str(change_data.get("changes", "No details provided"))

        results = {}

        # 1. Changelog
        prompt = ChatPromptTemplate.from_template("""
        You are a senior technical writer.
        Write a clean, professional changelog entry.

        Repository: {repo_name}
        Event Type: {event_type}
        Details: {raw_changes}

        Use markdown formatting with appropriate emojis.
        Keep it concise but informative.
        """)
        chain = prompt | self.llm
        results["changelog"] = chain.invoke({
            "repo_name": repo_name,
            "event_type": event_type,
            "raw_changes": raw_changes
        }).content.strip()

        # 2. README Update Suggestion
        prompt = ChatPromptTemplate.from_template("""
        Suggest how to update the README.md file for this change.

        Project: {repo_name}
        Recent Change: {raw_changes}

        Provide:
        1. Which sections should be updated
        2. Sample content for those sections
        """)
        chain = prompt | self.llm
        results["readme"] = chain.invoke({
            "repo_name": repo_name,
            "raw_changes": raw_changes
        }).content.strip()

        # 3. Architecture Impact
        prompt = ChatPromptTemplate.from_template("""
        Analyze the architecture impact of this change.

        Repository: {repo_name}
        Change Details: {raw_changes}

        Focus on:
        - Affected components
        - Possible design implications
        - Any breaking changes
        Keep it technical and short.
        """)
        chain = prompt | self.llm
        results["architecture"] = chain.invoke({
            "repo_name": repo_name,
            "raw_changes": raw_changes
        }).content.strip()

        # 4. PR Summary
        prompt = ChatPromptTemplate.from_template("""
        Write a clear and professional Pull Request description.

        Repository: {repo_name}
        Change Type: {event_type}
        Details: {raw_changes}

        Make it suitable for developers to understand the change quickly.
        """)
        chain = prompt | self.llm
        results["pr_summary"] = chain.invoke({
            "repo_name": repo_name,
            "event_type": event_type,
            "raw_changes": raw_changes
        }).content.strip()

        return results