
from flask import Flask, request, jsonify
from agents import AIModel, ContentAnalysisAgent, RewriteAgent, SummaryAgent, VerificationAgent
import os

class MultiAgentSystem:
    def __init__(self):
        self.model = AIModel()
        self.analysis_agent = ContentAnalysisAgent(self.model)
        self.rewrite_agent = RewriteAgent(self.model)
        self.summary_agent = SummaryAgent(self.model)
        self.verification_agent = VerificationAgent()

    def process_document(self, doc: str):
        issues = self.analysis_agent.analyze(doc)
        rewritten = self.rewrite_agent.rewrite(doc)
        summary = self.summary_agent.summarize(rewritten)
        verified = self.verification_agent.verify(doc, rewritten)

        with open("suggestions.txt", "a", encoding="utf-8") as f:
            f.write(f"原文: {doc}\n重写: {rewritten}\n问题: {issues}\n验证: {verified}\n{'-'*50}\n")

        return {
            "original": doc,
            "issues": issues,
            "rewritten": rewritten,
            "summary": summary,
            "verified": verified,
            "tokens_used": self.model.total_tokens
        }

    def batch_process(self, docs: list):
        return [self.process_document(doc) for doc in docs]

app = Flask(__name__)
system = MultiAgentSystem()

@app.route("/process", methods=['POST'])
def process():
    data = request.json
    docs = data.get("documents", [])
    results = system.batch_process(docs)
    return jsonify(results)

if __name__ == "__main__":
    if os.path.exists("suggestions.txt"):
        os.remove("suggestions.txt")

    test_docs = [
        "i am writing a test document that may contain grammar mistakes.",
        "this is a very long sentence that should ideally be broken down into smaller sentences for readability."
    ]
    results = system.batch_process(test_docs)
    for r in results:
        print(r)
    app.run(host="0.0.0.0", port=5000)
