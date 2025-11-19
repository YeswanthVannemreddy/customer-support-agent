# main.py - Customer Support Agent demo (single-file)
import json
from datetime import datetime

# ---- Memory ----
class Memory:
    def __init__(self):
        self.history = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content, "time": datetime.now().isoformat()})

    def get_context(self):
        out = ""
        for m in self.history:
            out += f"{m['role']}: {m['content']}\n"
        return out

    def get(self):
        return self.history

# ---- Intent Agent ----
class IntentAgent:
    def classify(self, message):
        text = message.lower()
        if "refund" in text or "money back" in text:
            return "refund", "high"
        if "cancel" in text or "subscription" in text:
            return "cancellation", "high"
        if "invoice" in text or "bill" in text or "charged" in text:
            return "billing", "medium"
        if "help" in text or "support" in text or "issue" in text:
            return "general_help", "low"
        return "general", "low"

# ---- Reply Agent ----
class ReplyAgent:
    def create_reply(self, message, intent, urgency):
        if intent == "refund":
            return "I understand you want a refund. Please share your order ID so I can assist you further."
        if intent == "cancellation":
            return "I can help you cancel your subscription. Kindly provide your registered email."
        if intent == "billing":
            return "It seems you have a billing concern. Please send your invoice number for verification."
        if intent == "general_help" or intent == "general":
            return "Thank you for your message. How can I assist you today?"
        return "Sorry, I could not understand. Please provide more details."

# ---- Coordinator ----
class Coordinator:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.reply_agent = ReplyAgent()
        self.memory = Memory()

    def ask(self, message):
        self.memory.add("user", message)
        intent, urgency = self.intent_agent.classify(message)
        reply = self.reply_agent.create_reply(message, intent, urgency)
        self.memory.add("agent", reply)
        return {"intent": intent, "urgency": urgency, "reply": reply}

# ---- Demo runner ----
def demo():
    agent = Coordinator()
    messages = [
        "I want to cancel my subscription.",
        "My invoice amount is wrong.",
        "I need a refund please.",
        "Hello, I need help."
    ]
    for m in messages:
        out = agent.ask(m)
        print("USER:", m)
        print(json.dumps(out, indent=2))
        print("-" * 40)

    print("\nConversation memory:")
    print(agent.memory.get_context())

if __name__ == "__main__":
    demo()
