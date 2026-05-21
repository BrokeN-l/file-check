
import re
from typing import List

class AIModel:
    def __init__(self):
        self.total_tokens = 0

    def analyze_text(self, text: str) -> List[str]:
        self.total_tokens += len(text)//2
        issues = []
        if re.search(r'\bi\b', text):
            issues.append("小写 'i' 应该大写")
        if len(text) > 100:
            issues.append("句子过长，建议拆分")
        return issues

    def rewrite_text(self, text: str) -> str:
        self.total_tokens += len(text)//3
        text = re.sub(r'\bi\b', 'I', text)
        if len(text) > 100:
            text = text[:100] + "…"
        return text

    def generate_summary(self, text: str) -> str:
        self.total_tokens += len(text)//4
        return text[:50] + '...' if len(text) > 50 else text

class ContentAnalysisAgent:
    def __init__(self, model: AIModel):
        self.model = model

    def analyze(self, doc: str) -> List[str]:
        return self.model.analyze_text(doc)

class RewriteAgent:
    def __init__(self, model: AIModel):
        self.model = model

    def rewrite(self, doc: str) -> str:
        return self.model.rewrite_text(doc)

class SummaryAgent:
    def __init__(self, model: AIModel):
        self.model = model

    def summarize(self, doc: str) -> str:
        return self.model.generate_summary(doc)

class VerificationAgent:
    def verify(self, original: str, rewritten: str) -> bool:
        original_keywords = original.split()[:5]
        return all(word in rewritten or word.lower() in rewritten.lower() for word in original_keywords)
