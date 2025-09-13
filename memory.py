################## Whole stuffs will be saved in json(LTD) 
# # memory.py
# import json
# import os

# class Memory:
#     def __init__(self, ltm_file="ltm_2.json"):
#         # Short-Term Memory (per session, resets if you restart script)
#         self.stm = {}

#         # Long-Term Memory (persists across runs, saved to JSON file)
#         self.ltm_file = ltm_file
#         if os.path.exists(self.ltm_file):
#             try:
#                 with open(self.ltm_file, "r") as f:
#                     self.ltm = json.load(f)
#             except json.JSONDecodeError:
#                 self.ltm = []
#         else:
#             self.ltm = []

#     # ====== STM (short-term memory) ======
#     def add_to_stm(self, key, value):
#         """Alias for update_stm — matches pipeline.py."""
#         self.stm[key] = value

#     def update_stm(self, key, value):
#         """Add or update key in short-term memory."""
#         self.stm[key] = value

#     def get_stm(self, key=None):
#         """Fetch STM by key, or return all if key=None."""
#         if key:
#             return self.stm.get(key, None)
#         return self.stm

#     def clear_stm(self):
#         """Wipe short-term memory."""
#         self.stm = {}

#     # ====== LTM (long-term memory) ======
#     def add_to_ltm(self, key, value):
#         """Alias for save_ltm — stores key/value style for pipeline."""
#         entry = {"type": key, "value": value}
#         self.save_ltm(entry)

#     def save_ltm(self, entry: dict):
#         """Append an entry (dict) to LTM and persist to disk."""
#         self.ltm.append(entry)
#         with open(self.ltm_file, "w") as f:
#             json.dump(self.ltm, f, indent=2)

#     def get_ltm(self, filter_type=None):
#         """Get all LTM entries, optionally filtered by type."""
#         if filter_type:
#             return [e for e in self.ltm if e.get("type") == filter_type]
#         return self.ltm

#     def clear_ltm(self):
#         """Erase LTM (careful! wipes file)."""
#         self.ltm = []
#         with open(self.ltm_file, "w") as f:
#             json.dump([], f)


############ Tried with placeholder for LTM(Slicing the some sort of info from prd, arch..)
# import json
# import os

# # === Simple LLM-based summarizer (stub for now) ===
# def summarizer_llm(text: str, context_type: str) -> str:
#     """
#     Summarize text to keep only key facts for future use.
#     Replace this stub with your LLM API call.
#     """
#     # Example: heuristic short version
#     if context_type == "PRD":
#         return f"[PRD Summary] {text[:500]}..."
#     elif context_type == "Architecture":
#         return f"[Arch Summary] {text[:500]}..."
#     elif context_type == "Validation":
#         return f"[Validation Summary] {text[:1000]}..."
#     else:
#         return f"[Summary] {text[:200]}..."


# class Memory:
#     def __init__(self, ltm_file="ltm_Summarized.json"):
#         # Short-Term Memory
#         self.stm = {}

#         # Long-Term Memory
#         self.ltm_file = ltm_file
#         if os.path.exists(self.ltm_file):
#             try:
#                 with open(self.ltm_file, "r") as f:
#                     self.ltm = json.load(f)
#             except json.JSONDecodeError:
#                 self.ltm = []
#         else:
#             self.ltm = []

#     # ====== STM (short-term memory) ======
#     def add_to_stm(self, key, value):
#         self.stm[key] = value

#     def update_stm(self, key, value):
#         self.stm[key] = value

#     def get_stm(self, key=None):
#         if key:
#             return self.stm.get(key, None)
#         return self.stm

#     def clear_stm(self):
#         self.stm = {}

#     # ====== LTM (long-term memory) ======
#     def add_to_ltm(self, key, value):
#         """
#         Store into LTM.
#         - Summarize long text (PRD, Arch, Validation, etc.)
#         - Store raw code fully (since summaries won’t help for execution).
#         """
#         if key.lower() in ["code", "frontend_code", "generated_code"]:
#             # For code → store raw
#             entry = {"type": key, "raw": value}
#         else:
#             # For textual outputs → store summary + raw (optional)
#             summary = summarizer_llm(value, key)
#             entry = {"type": key, "summary": summary}

#         self.save_ltm(entry)

#     def save_ltm(self, entry: dict):
#         self.ltm.append(entry)
#         with open(self.ltm_file, "w") as f:
#             json.dump(self.ltm, f, indent=2)

#     def get_ltm(self, filter_type=None):
#         if filter_type:
#             return [e for e in self.ltm if e.get("type") == filter_type]
#         return self.ltm

#     def clear_ltm(self):
#         self.ltm = []
#         with open(self.ltm_file, "w") as f:
#             json.dump([], f)

# # # # # ########### Tried a llm model to summarize the raw outputs and storing the relevant info and future needed info alone in LTM   -  gpt till 4 worked
# # # # # import json
# # # # # import os
# # # # # import requests

# # # # # # =========================
# # # # # # Summarizer (semantic, LLM-based via Ollama)
# # # # # # =========================
# # # # # def summarizer_llm(text: str, context_type: str) -> str:
# # # # #     if not isinstance(text, str):
# # # # #         try:
# # # # #             text = json.dumps(text, indent=2)
# # # # #         except Exception:
# # # # #             text = str(text)

# # # # #     prompt = f"""
# # # # #     You are a memory compression assistant.
# # # # #     Summarize the following {context_type} into a concise form,
# # # # #     keeping only the key facts needed for future agents.
# # # # #     - Use bullet points if helpful
# # # # #     - Max length: ~500 characters
# # # # #     - Do NOT include filler text.

# # # # #     Text:
# # # # #     {text}
# # # # #     """

# # # # #     try:
# # # # #         with requests.post(
# # # # #             "http://localhost:11434/api/generate",
# # # # #             json={"model": "mistral:instruct", "prompt": prompt, "stream": True},
# # # # #             stream=True,
# # # # #             timeout=180
# # # # #         ) as resp:
# # # # #             resp.raise_for_status()
# # # # #             output = ""
# # # # #             for line in resp.iter_lines():
# # # # #                 if line:
# # # # #                     chunk = json.loads(line.decode("utf-8"))
# # # # #                     output += chunk.get("response", "")
# # # # #             return output.strip()
# # # # #     except Exception as e:
# # # # #         print(f"[WARN] Ollama summarizer failed: {e}")
# # # # #         return f"[{context_type} Summary] {text[:300]}..."


# # # # # # =========================
# # # # # # Memory Class
# # # # # # =========================
# # # # # class Memory:
# # # # #     def __init__(self, ltm_file="ltm_Summarized.json"):
# # # # #         # Short-Term Memory (per session, resets if you restart script)
# # # # #         self.stm = {}

# # # # #         # Long-Term Memory (persists across runs, saved to JSON file)
# # # # #         self.ltm_file = ltm_file
# # # # #         if os.path.exists(self.ltm_file):
# # # # #             try:
# # # # #                 with open(self.ltm_file, "r") as f:
# # # # #                     self.ltm = json.load(f)
# # # # #             except json.JSONDecodeError:
# # # # #                 self.ltm = []
# # # # #         else:
# # # # #             self.ltm = []

# # # # #     # ====== STM (short-term memory) ======
# # # # #     def add_to_stm(self, key, value):
# # # # #         self.stm[key] = value

# # # # #     def update_stm(self, key, value):
# # # # #         self.stm[key] = value

# # # # #     def get_stm(self, key=None):
# # # # #         if key:
# # # # #             return self.stm.get(key, None)
# # # # #         return self.stm

# # # # #     def clear_stm(self):
# # # # #         self.stm = {}

# # # # #     # ====== LTM (long-term memory) ======
# # # # #     def add_to_ltm(self, key, value):
# # # # #         """
# # # # #         Store into LTM.
# # # # #         - Summarize long text (PRD, Arch, Validation, etc.)
# # # # #         - Store raw code fully (since summaries won’t help for execution).
# # # # #         """
# # # # #         if key.lower() in ["code", "frontend_code", "generated_code"]:
# # # # #             entry = {"type": key, "raw": value}
# # # # #         else:
# # # # #             summary = summarizer_llm(value, key)
# # # # #             entry = {"type": key, "summary": summary}

# # # # #         self.save_ltm(entry)

# # # # #     def save_ltm(self, entry: dict):
# # # # #         self.ltm.append(entry)
# # # # #         with open(self.ltm_file, "w") as f:
# # # # #             json.dump(self.ltm, f, indent=2)

# # # # #     def get_ltm(self, filter_type=None):
# # # # #         if filter_type:
# # # # #             return [e for e in self.ltm if e.get("type") == filter_type]
# # # # #         return self.ltm

# # # # #     def clear_ltm(self):
# # # # #         self.ltm = []
# # # # #         with open(self.ltm_file, "w") as f:
# # # # #             json.dump([], f)

########### Tried a llm model to summarize the raw outputs and storing the relevant info and future needed info alone in LTM   - grok till 5 still testing
import json
import os
import requests

# =========================
# Summarizer (semantic, LLM-based via Ollama)
# =========================
def summarizer_llm(text: str, context_type: str) -> str:
    if not isinstance(text, str):
        try:
            text = json.dumps(text, indent=2)
        except Exception:
            text = str(text)

    prompt = f"""
    You are a memory compression assistant.
    Summarize the following {context_type} into a concise form,
    keeping only the key facts needed for future agents.
    - Use bullet points if helpful
    - Max length: ~500 characters
    - Do NOT include filler text.

    Text:
    {text}
    """

    try:
        with requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral:instruct", "prompt": prompt, "stream": True},
            stream=True,
            timeout=180
        ) as resp:
            resp.raise_for_status()
            output = ""
            for line in resp.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    output += chunk.get("response", "")
            return output.strip()
    except Exception as e:
        print(f"[WARN] Ollama summarizer failed: {e}")
        return f"[{context_type} Summary] {text[:300]}..."


# =========================
# Memory Class
# =========================
class Memory:
    def __init__(self, ltm_file="ltm_Summarized-Medical.json"):
        # Short-Term Memory (per session, resets if you restart script)
        self.stm = {}

        # Long-Term Memory (persists across runs, saved to JSON file)
        self.ltm_file = ltm_file
        if os.path.exists(self.ltm_file):
            try:
                with open(self.ltm_file, "r") as f:
                    self.ltm = json.load(f)
            except json.JSONDecodeError:
                self.ltm = []
        else:
            self.ltm = []

    # ====== STM (short-term memory) ======
    def add_to_stm(self, key, value):
        self.stm[key] = value

    def update_stm(self, key, value):
        self.stm[key] = value

    def get_stm(self, key=None):
        if key:
            return self.stm.get(key, None)
        return self.stm

    def clear_stm(self):
        self.stm = {}

    # ====== LTM (long-term memory) ======
    def add_to_ltm(self, key, value):
        """
        Store into LTM.
        - Summarize long text (PRD, Arch, Validation, etc.)
        - Store raw code fully (since summaries won’t help for execution).
        """
        if key.lower() in ["code", "frontend_code", "generated_code", "fixed_code"]:
            entry = {"type": key, "raw": value}
        else:
            summary = summarizer_llm(value, key)
            entry = {"type": key, "summary": summary}

        self.save_ltm(entry)

    def save_ltm(self, entry: dict):
        self.ltm.append(entry)
        with open(self.ltm_file, "w") as f:
            json.dump(self.ltm, f, indent=2)

    def get_ltm(self, filter_type=None):
        if filter_type:
            return [e for e in self.ltm if e.get("type") == filter_type]
        return self.ltm

    def clear_ltm(self):
        self.ltm = []
        with open(self.ltm_file, "w") as f:
            json.dump([], f)


