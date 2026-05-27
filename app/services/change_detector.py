from sqlmodel import Session, select
from datetime import datetime

from app.core.database import get_session
from app.domain.models.change_event import ChangeEvent
from app.services.documentation_generator import DocumentationGenerator
from app.services.multi_doc_generator import MultiDocGenerator

class ChangeDetector:
    
    def analyze_change(self, change_event_id: int):
        """Analyze change and trigger AI documentation generation"""
        try:
            with next(get_session()) as session:
                event = session.get(ChangeEvent, change_event_id)
                if not event:
                    print(f"❌ Event {change_event_id} not found")
                    return
                
                print(f"🔍 Analyzing changes for Event ID: {change_event_id}")
                
                # Basic change classification
                if event.pr_number:
                    change_type = "pull_request"
                else:
                    change_type = "code_push"
                
                print(f"📊 Change Type Detected: {change_type}")
                
                # Mark as processed
                event.processed = True
                event.processed_at = datetime.utcnow()
                session.add(event)
                session.commit()
                
                print(f"✅ Change analysis completed for Event {change_event_id}")

                # === AI Multi-Document Generation ===
                print(f"🤖 Generating Multiple Documents using AI...")
                
                generator = MultiDocGenerator()
                
                docs = generator.generate_all_docs({
                    "repository": event.changes.get("repository", "Unknown Repository"),
                    "event_type": event.event_type,
                    "changes": event.changes
                })

                print("\n" + "="*80)
                print("📄 AI GENERATED MULTI DOCUMENTS")
                print("="*80)
                for doc_type, content in docs.items():
                    print(f"\n--- {doc_type.upper()} ---")
                    preview = content[:600] + "..." if len(content) > 600 else content
                    print(preview)
                    print("-" * 60)

        except Exception as e:
            print(f"❌ Error in change analysis: {e}")