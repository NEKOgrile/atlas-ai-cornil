from datetime import datetime
import chromadb


client = chromadb.PersistentClient(path="./data/memory")
collection = client.get_or_create_collection("conversations")


class ShortTermMemory:

    def __init__(self, max_messages=50):
        self.messages = []
        self.max = max_messages

    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": content,
            "time": datetime.now().isoformat()
        })

        # garde que les derniers
        if len(self.messages) > self.max:
            self.messages = self.messages[-self.max:]

    def get(self):
        # format pour le LLM
        return [{"role": m["role"], "content": m["content"]} for m in self.messages]

    def clear(self):
        self.messages = []


class LongTermMemory:

    def __init__(self):
        self.col = collection 

    def store(self, text, metadata=None):
        try:
            self.col.add(
                documents=[text],
                metadatas=[metadata or {"type": "chat"}],
                ids=[str(datetime.now().timestamp())]
            )
        except Exception as e:
            print("erreur store:", e)

    def search(self, query, k=5):
        try:
            res = self.col.query(
                query_texts=[query],
                n_results=k
            )

            if not res or "documents" not in res:
                return []

            return res["documents"][0]

        except Exception as e:
            print("erreur search:", e)
            return []