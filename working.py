# working.py
import requests
import os
import json
import re
#from google import genai - for gloabal ebv
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()
# -------------------------------
# Config
# -------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"

# ------------------------------------------  GEM  1
# Example: get Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Gemini key loaded?", bool(GEMINI_API_KEY))  # Debug



# if GEMINI_API_KEY: ---------------------------------------------------------------- FOR GLOBAL ENV
#     gemini_client = genai.Client(api_key=GEMINI_API_KEY)
# else:
#     gemini_client = None

if GEMINI_API_KEY:                                                                  # - For venv
    genai.configure(api_key=GEMINI_API_KEY)
else:
    genai = None  # Optional: handle no-key situation


# -------------------------------
# Generic Model Wrapper (OLLAMA)
# -------------------------------
def model_chat_completion(model: str, prompt: str) -> str:
    """Call Ollama with a given model + prompt and return clean text response."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload).json()
        return resp.get("response", "").strip()
    except Exception as e:
        return f"[Error contacting Ollama: {e}]"
    

# Generic Model Wrapper (Gemini)                                                                            - GEM 1
# -------------------------------
# def gemini_completion(model: str, prompt: str) -> str:                                                    ---- for gloabal env
#     """Call Gemini with prompt and return clean response text."""
#     if not gemini_client:
#         raise ValueError("❌ GEMINI_API_KEY not set, but Gemini was requested")
#     try:
#         resp = gemini_client.models.generate_content(model=model, contents=prompt)
#         if resp.candidates:
#             return resp.candidates[0].content.parts[0].text.strip()
#         return "[No response from Gemini]"
#     except Exception as e:
#         return f"[Error contacting Gemini: {e}]"


def gemini_completion(model: str, prompt: str) -> str:                              # - for venv
    """Call Gemini with prompt and return clean response text (old SDK)."""
    if not genai:
        raise ValueError("❌ GEMINI_API_KEY not set, but Gemini was requested")
    
    try:
        # create the model object
        gm = genai.GenerativeModel(model)
        
        # generate content
        resp = gm.generate_content(prompt)
        
        # get text safely
        if resp and resp.text:
            return resp.text.strip()
        return "[No response from Gemini]"
    
    except Exception as e:
        return f"[Error contacting Gemini: {e}]"


# -------------------------------
# Agent 0 → Requirements → BRD
# -------------------------------
def agent(requirements: dict) -> str:
    """
    Takes structured user requirements (dict) and generates a clean BRD.
    """
    brd_instruction = """You are an expert Business Analyst.
Generate a clear and professional **Business Requirement Document (BRD)** based on the provided requirements.

Rules:
- Be structured and concise
- Do not add extra assumptions
- Organize under standard BRD sections:
  1. Overview
  2. Objectives
  3. In-Scope
  4. Out-of-Scope
  5. UI/UX Requirements
  6. Functional Requirements
  7. Non-Functional Requirements
  8. Acceptance Criteria
"""

    # Convert dict into plain text for LLM
    req_text = "\n".join([f"{k}: {v}" for k, v in requirements.items() if v])
    prompt = brd_instruction + "\n\nUser Requirements:\n" + req_text

    return model_chat_completion("llama3", prompt)




# -------------------------------
# Agent 1 → BRD → PRD
# -------------------------------
def agent1(brd_text: str) -> str:
    prd_instruction = """You are a Product Manager, but keep your output minimal and developer-focused. 
Convert the following Business Requirement Document (BRD) into a concise Frontend Product Requirement Document (PRD)

Rules:
- Be short and direct. 
- No long explanations or repeated sentences. 
- Only include details needed for developers to build the frontend. 
- Focus on structure, not prose. 

Your PRD must have these exact sections:
1. Objectives (1-3 bullet points max)
2. UI Screens & Components (list of screens and key UI components only)
3. State Management (list the slices/states required)
4. Data Persistence (only if applicable)
5. User Roles (if any, otherwise say 'None')
6. Acceptance Criteria (just the checklist of frontend behaviors)

Output should be structured and minimal.
BRD:
"""
    prompt = prd_instruction + brd_text
    return model_chat_completion("llama3", prompt)


# -------------------------------
# Generate or Update PRD (Smart Merge Wrapper)
# -------------------------------
def generate_or_update_prd(new_brd_text: str, existing_prd: str = None) -> str:
    """
    Checks if there is an existing PRD and updates it with new BRD text.
    If no existing PRD, generates a new one.
    """
    if existing_prd:
        update_prompt = f"""
Existing PRD:
{existing_prd}

New BRD Update:
{new_brd_text}

Update the PRD to include the new requirements while keeping previous features intact.
- Maintain all existing sections (Objectives, UI Screens & Components, State Management, Data Persistence, User Roles, Acceptance Criteria)
- Be minimal, structured, and developer-focused
"""
        return agent1(update_prompt)
    else:
        return agent1(new_brd_text)



# -------------------------------
# Agent 2 → PRD → Architecture
# -------------------------------
def agent2(input_data):
    """Takes PRD (and optional STM context) and generates Architecture"""
    if isinstance(input_data, dict):
        context = input_data.get("context", {})
        focus = input_data.get("focus", "")
        prd_text = context.get("PRD", "")
        brd_text = context.get("BRD", "")
        input_text = f"BRD:\n{brd_text}\n\nPRD:\n{prd_text}\n\nInstruction:\n{focus}"
    else:
        input_text = str(input_data)

    arch_instruction = """You are a Solutions Architect. Convert the following Product Requirement Document (PRD)
into a developer-focused **Frontend Architecture Specification** that explicitly maps features to file paths.

Rules:
- The frontend must always be implemented in **React**, regardless of what the PRD says.
- Styling must use **Tailwind CSS**.
- Build tool must be **Vite**.
- State management should default to **Redux Toolkit** (or Context API if very simple).
- Client-side storage should be **localStorage/sessionStorage** if data persistence is needed.
- All screens and components must be explicitly mapped to file paths (e.g., src/screens/Home.jsx, src/components/Navbar.jsx).
- Mandatory base files must always be listed under "Mandatory Files".

Your architecture document must contain ONLY the following sections:
1. Tech Stack (React, Tailwind, Vite, state management, other required libs)
2. Mandatory Files (always present: src/App.jsx, src/main.jsx, src/index.css, tailwind.config.js, vite.config.js, package.json)
3. Screens (each screen listed in PRD → mapped to src/screens/*.jsx)
4. Components (each reusable component → mapped to src/components/*.jsx)
5. State Management (Redux store and slices if needed, with file paths)
6. Data Storage (localStorage/sessionStorage if applicable, otherwise None)
7. UI Features (responsive design, animations, forms, role-based access if mentioned)

Output must be a clean markdown document with file mappings.
"""
    prompt = arch_instruction + input_text
    return model_chat_completion("qwen2.5:7b", prompt)


# # -------------------------------
# # Agent 3 → Architecture → Code      - OLLAMA
# # -------------------------------
# def agent3(input_data):
#     """Takes Architecture (and optional STM context) and generates React code"""
#     if isinstance(input_data, dict):
#         context = input_data.get("context", {})
#         focus = input_data.get("focus", "")
#         prd_text = context.get("PRD", "")
#         arch_text = context.get("Architecture", "")
#         input_text = f"PRD:\n{prd_text}\n\nArchitecture:\n{arch_text}\n\nInstruction:\n{focus}"
#     else:
#         input_text = str(input_data)

#     code_instruction = """You are a Frontend Developer. Output a single VALID JSON object.
#     Top-level key MUST be "frontend". Each key is a file path, each value is the full file content as a string.
#     Absolutely NO markdown, NO code fences, NO comments, NO prose. Just JSON.
    
#     Use ONLY: React, Redux Toolkit (if state management needed), Tailwind CSS, Vite, PapaParse, uuid.
#     Always use React + Tailwind for UI. No other frontend frameworks allowed.
#     Do NOT include axios, react-toastify, or any other libraries.
    
#     Rules:
#     - Mandatory files (must always be present): 
#       index.html (in project root, must include <div id="root"></div> and <script type="module" src="/src/main.jsx"></script>),
#       src/App.jsx,
#       src/main.jsx,
#       src/index.css,
#       tailwind.config.js,
#       vite.config.js,
#       package.json
#     - Also mandatory if PRD/Architecture specifies them (NOT optional): 
#       src/store/store.js (if state management is mentioned),
#       src/screens/* (for each screen listed in architecture),
#       src/components/* (for each component listed in architecture)
#     - The structure of components, screens, and Redux slices MUST be based on the entities, features, and navigation described in the PRD/arch_text.
#     - If state persistence is needed, use localStorage (load on init, save on changes).
#     - For navigation:
#       - If PRD says "single-page scroll", use section IDs + anchor links in Navbar (no react-router-dom).
#       - If PRD says "multi-page routing", then use react-router-dom v6.
#     - All components must be implemented as React functional components with JSX.
#     - Every file value MUST contain actual valid source code (imports, functions, JSX, etc.). 
#     - Do NOT output summaries, placeholders, or meta descriptions.

#     Strict Coding Rules (MUST follow):
#     - Never use "=>" inside import/export statements. Use only valid ES6 import/export syntax.
#     - All JSX must be valid React 18 syntax. Close every tag properly.
#     - Never mix lowercase and uppercase component names. Components must always start with uppercase.
#     - Every component must explicitly export (default or named) at the end of the file.
#     - Do not include unused imports or variables.
#     - Code must compile successfully under Vite + React + Tailwind with no syntax errors.
#     - Before returning, self-check that the code passes ESLint React rules (no syntax/lint violations).

#     - package.json requirements:
#       - MUST include ONLY the allowed dependencies: react, react-dom, vite, tailwindcss, @reduxjs/toolkit, react-redux, react-router-dom (if needed), papaparse, uuid.
#       - All dependency names MUST be spelled exactly as in npm registry (e.g., "papaparse" NOT "papa-parse").
#       - Versions MUST be the latest stable releases at generation time (e.g., "latest").
#       - No deprecated, old, or extra packages.

#     - Use double quotes in JSON. Escape all newlines inside strings as \\n. 
#     - No trailing commas anywhere in JSON or code strings.
    
#     The output must strictly follow the architecture specifications provided in arch_text.
# """
#     prompt = code_instruction + input_text
#     return model_chat_completion("llama3:latest", prompt)



# -------------------------------
# Agent 3 → Architecture → Code (Gemini 2.5 Flash)
# -------------------------------
def agent3(input_data):
    """Takes Architecture (and optional STM context) and generates React code"""
    if isinstance(input_data, dict):
        context = input_data.get("context", {})
        focus = input_data.get("focus", "")
        prd_text = context.get("PRD", "")
        arch_text = context.get("Architecture", "")
        input_text = f"PRD:\n{prd_text}\n\nArchitecture:\n{arch_text}\n\nInstruction:\n{focus}"
    else:
        input_text = str(input_data)

    code_instruction = """You are a Frontend Developer. Output a single VALID JSON object.
    Top-level key MUST be "frontend". Each key is a file path, each value is the full file content as a string.
    Absolutely NO markdown, NO code fences, NO comments, NO prose. Just JSON.
    
    Use ONLY: React, Redux Toolkit (if state management needed), Tailwind CSS, Vite, PapaParse, uuid.
    Always use React + Tailwind for UI. No other frontend frameworks allowed.
    Do NOT include axios, react-toastify, or any other libraries.
    
    Rules:
    - Mandatory files (must always be present): 
      index.html (in project root, must include <div id="root"></div> and <script type="module" src="/src/main.jsx"></script>),
      src/App.jsx,
      src/main.jsx,
      src/index.css,
      tailwind.config.js,
      vite.config.js,
      package.json
    - Also mandatory if PRD/Architecture specifies them (NOT optional): 
      src/store/store.js (if state management is mentioned),
      src/screens/* (for each screen listed in architecture),
      src/components/* (for each component listed in architecture)
    - The structure of components, screens, and Redux slices MUST be based on the entities, features, and navigation described in the PRD/arch_text.
    - If state persistence is needed, use localStorage (load on init, save on changes).
    - For navigation:
      - If PRD says "single-page scroll", use section IDs + anchor links in Navbar (no react-router-dom).
      - If PRD says "multi-page routing", then use react-router-dom v6.
    - All components must be implemented as React functional components with JSX.
    - Every file value MUST contain actual valid source code (imports, functions, JSX, etc.). 
    - Do NOT output summaries, placeholders, or meta descriptions.

    Strict Coding Rules (MUST follow):
    - Never use "=>" inside import/export statements. Use only valid ES6 import/export syntax.
    - All JSX must be valid React 18 syntax. Close every tag properly.
    - Never mix lowercase and uppercase component names. Components must always start with uppercase.
    - Every component must explicitly export (default or named) at the end of the file.
    - Do not include unused imports or variables.
    - Code must compile successfully under Vite + React + Tailwind with no syntax errors.
    - Before returning, self-check that the code passes ESLint React rules (no syntax/lint violations).

    - package.json requirements:
      - MUST include ONLY the allowed dependencies: react, react-dom, vite, tailwindcss, @reduxjs/toolkit, react-redux, react-router-dom (if needed), papaparse, uuid.
      - All dependency names MUST be spelled exactly as in npm registry (e.g., "papaparse" NOT "papa-parse").
      - Versions MUST be the latest stable releases at generation time (e.g., "latest").
      - No deprecated, old, or extra packages.

    - Use double quotes in JSON. Escape all newlines inside strings as \\n. 
    - No trailing commas anywhere in JSON or code strings.
    
    The output must strictly follow the architecture specifications provided in arch_text.
"""

    prompt = code_instruction + input_text
    return gemini_completion("gemini-2.5-flash", prompt)



# Agent 4 → Validation + Cleaning
# -------------------------------
def agent4(generated_code: dict, base_dir="validated_code"):

    os.makedirs(base_dir, exist_ok=True)

    # Handle nested "frontend" key
    if "frontend" in generated_code:
        generated_code = generated_code["frontend"]

    # Save files to disk
    for filename, content in generated_code.items():
        file_path = os.path.join(base_dir, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    issues = []
    logs = ["[INFO] Running Agent 4 Validation..."]

    # --- Mandatory files (Vite only) ---
    mandatory = [
        "package.json",
        "index.html",
        "src/App.jsx",
        "src/main.jsx",
        "src/index.css",
        "tailwind.config.js",
        "vite.config.js"
    ]
    for f in mandatory:
        if not os.path.exists(os.path.join(base_dir, f)):
            issues.append(f"❌ Missing required file: {f}")
        else:
            logs.append(f"[✅] Found {f}")

    # --- package.json checks ---
    pkg_file = os.path.join(base_dir, "package.json")
    if os.path.exists(pkg_file):
        try:
            with open(pkg_file, "r", encoding="utf-8") as f:
                package_json = json.load(f)

            deps = package_json.get("dependencies", {})
            dev_deps = package_json.get("devDependencies", {})

            # Required deps
            required_deps = ["react", "react-dom"]
            required_dev = ["vite", "tailwindcss"]

            for d in required_deps:
                if d not in deps:
                    issues.append(f"❌ '{d}' missing in dependencies")
                else:
                    logs.append(f"[✅] {d} found in dependencies")

            for d in required_dev:
                if d not in deps and d not in dev_deps:
                    issues.append(f"❌ '{d}' missing in devDependencies/dependencies")
                else:
                    logs.append(f"[✅] {d} found in devDependencies/dependencies")

        except json.JSONDecodeError:
            issues.append("❌ package.json is invalid JSON")

    # --- index.html checks ---
    index_file = os.path.join(base_dir, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            html = f.read()
        if '<div id="root">' not in html:
            issues.append("❌ index.html missing <div id='root'>")
        if 'src="/src/main.jsx"' not in html and 'src=\'/src/main.jsx\'' not in html:
            issues.append("❌ index.html missing <script type='module' src='/src/main.jsx'>")

    # --- App.jsx sanity check ---
    app_file = os.path.join(base_dir, "src", "App.jsx")
    if os.path.exists(app_file):
        with open(app_file, "r", encoding="utf-8") as f:
            app_code = f.read()
        if "export default" not in app_code:
            issues.append("❌ App.jsx missing default export")

    # --- main.jsx sanity check ---
    main_file = os.path.join(base_dir, "src", "main.jsx")
    if os.path.exists(main_file):
        with open(main_file, "r", encoding="utf-8") as f:
            main_code = f.read()
        if "ReactDOM.createRoot" not in main_code:
            issues.append("❌ main.jsx missing ReactDOM.createRoot")
        if "App" not in main_code:
            issues.append("❌ main.jsx does not render <App />")

    # --- Broken import check ---
    broken_imports = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith((".jsx", ".js")):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    code = f.read()
                imports = re.findall(r'import .* from ["\'](.*)["\']', code)
                for imp in imports:
                    if imp.startswith("."):  # relative import
                        target = os.path.normpath(os.path.join(root, imp))
                        if not any(os.path.exists(target + ext) for ext in [".js", ".jsx", ".ts", ".tsx"]):
                            broken_imports.append(f"{imp} in {file}")

    for bi in broken_imports:
        issues.append(f"❌ Broken import: {bi}")

    # --- Clean code ---
    validated_code = {}
    for filename, content in generated_code.items():
        clean_lines = []
        for line in content.splitlines():
            if "console.log" in line:
                continue
            clean_lines.append(line.rstrip())
        validated_code[filename] = "\n".join(clean_lines)

    logs.append("[INFO] Validation complete.")

    return {
        "issues_found": issues,
        "logs": logs,
        "validated_code": validated_code
    }

# # -------------------------------
# # Agent 5 → Code + Issues → Fixed Code -                                  - OLLAMA
# # -------------------------------
# # # def agent5(generated_code: dict, issues: list, arch_text: str) -> dict:
# # #     """Takes Agent3's generated code and Agent4's issues, generates fixed JSON code. Fix issues without losing files."""
# # #     # Clean and parse if needed
# # #     if isinstance(generated_code, str):
# # #         try:
# # #             generated_code = json.loads(clean_json_output(generated_code))
# # #         except json.JSONDecodeError:
# # #             generated_code = {}

# # #     if "frontend" in generated_code:
# # #         generated_code = generated_code["frontend"]

# # #     all_files = list(generated_code.keys())

# # #     # Prompt for Agent5
# # #     system_prompt = f"""
# # # You are a React Code Debugger. Output ONLY a single VALID JSON object: 
# # # {{"frontend": {{"file/path": "full fixed code string", ...}}}}.

# # # Your tasks:
# # # - Fix ONLY the listed issues.
# # # - Preserve ALL original files (from Agent3). If a file has no issue, copy it verbatim.
# # # - Do NOT delete or omit files. Return at least the same number of files as input.
# # # - Architecture Specs (must follow): {arch_text}

# # # Original Files (preserve structure, only patch what’s broken):
# # # {json.dumps(generated_code, indent=2)}

# # # Issues to Fix:
# # # {chr(10).join([f"- {issue}" for issue in issues])}

# # # Rules:
# # # - Missing file → generate minimal valid code.
# # # - Broken import → correct relative path.
# # # - Missing export → add `export default`.
# # # - package.json → must stay valid JSON, allowed deps only.
# # # - Escape newlines as \\n. Double quotes only. No trailing commas.
# # # - JSX must be valid React 18.
# # # """

# # #     payload = {
# # #         "model": "jcdickinson/wizardcoder:15b",
# # #         "prompt": system_prompt,
# # #         "stream": False,
# # #         "options": {"temperature": 0.1, "num_ctx": 16384}
# # #     }
# # #     try:
# # #         resp = requests.post(OLLAMA_URL, json=payload).json()
# # #         raw_output = resp.get("response", "").strip()
# # #         cleaned = clean_json_output(raw_output)
# # #         fixed = json.loads(cleaned)
# # #         if "frontend" not in fixed:
# # #             fixed = {"frontend": fixed}
# # #         return fixed
# # #     except Exception as e:
# # #         print(f"❌ Agent5 error: {e}")
# # #         return generated_code  # Fallback to original


# -------------------------------
# Agent 5 → Code + Issues → Fixed Code  (GEMINI)
# -------------------------------
def agent5(generated_code: dict, issues: list, arch_text: str) -> dict: #----------------------------------------- for agent 5 , if again that incomplete issue arise we need to inject this code
    """Takes Agent3's generated code and Agent4's issues, generates fixed JSON code. Fix issues without losing files."""

    # Parse incoming JSON
    if isinstance(generated_code, str):
        try:
            generated_code = json.loads(clean_json_output(generated_code))
        except json.JSONDecodeError:
            generated_code = {}

    # Always unwrap only once
    if "frontend" in generated_code:
        generated_code = generated_code["frontend"]

    all_files = list(generated_code.keys())  # ✅ Keep full file list

    system_prompt = f"""
You are a React Code Debugger. Output ONLY a single VALID JSON object: 
{{"frontend": {{"file/path": "full fixed code string", ...}}}}.

Your tasks:
- Fix ONLY the listed issues.
- Preserve ALL original files (from Agent3). If a file has no issue, copy it verbatim.
- Do NOT delete or omit files. Return at least the same number of files as input.
- Architecture Specs (must follow): {arch_text}

Original Files (preserve structure, only patch what’s broken):
{json.dumps(generated_code, indent=2)}

Issues to Fix:
{chr(10).join([f"- {issue}" for issue in issues])}

Rules:
- Missing file → generate minimal valid code.
- Broken import → correct relative path.
- Missing export → add `export default`.
- package.json → must stay valid JSON, allowed deps only.
- Escape newlines as \\n. Double quotes only. No trailing commas.
- JSX must be valid React 18.
"""

    try:
        raw_output = gemini_completion("gemini-2.5-flash", system_prompt)
        cleaned = clean_json_output(raw_output)
        fixed = json.loads(cleaned)

        if "frontend" not in fixed:
            fixed = {"frontend": fixed}

        return fixed
    except Exception as e:
        print(f"❌ Agent5 error (Gemini): {e}")
        return {"frontend": generated_code}  # Fallback



def clean_json_output(raw: str) -> str:
    """Utility to clean raw JSON output."""
    if not raw:
        return "{}"
    cleaned = re.sub(r"```(?:json)?", "", raw, flags=re.IGNORECASE).strip()
    cleaned = cleaned.replace("```", "").strip()
    cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)
    return cleaned

# -------------------------------
# Test Run
# -------------------------------


# # # If you want a quick demo of the 3 agents alone -

# if __name__ == "__main__":
#     brd_text = """We want to build a personal portfolio website for showcasing an individual's projects and skills. 
# The website should have the following sections: Home, About, Projects, Skills, and Contact. 
# Users should be able to click through navigation links at the top of the page to move between sections smoothly (single-page scrolling). 
# The Projects section should display project cards with images, titles, short descriptions, and buttons to view more details or visit external links (e.g., GitHub, Live Demo). 
# The Contact section should include a simple form with fields for name, email, and message (no backend processing required, just UI). 
# The design should be modern, responsive (desktop, tablet, mobile), and lightweight, with a visually appealing color scheme. 
# Animations and transitions should be used for smooth user experience. 
# There is no need for backend or database; this is a frontend-only project."""

#     prd_output = agent1(brd_text)
#     print("\n=== PRD ===\n", prd_output)

#     arch_output = agent2({"context": {"BRD": brd_text, "PRD": prd_output}, "focus": ""})
#     print("\n=== Architecture ===\n", arch_output)

#     code_output = agent3({"context": {"PRD": prd_output, "Architecture": arch_output}, "focus": ""})
#     print("\n=== Generated Code (JSON) ===\n", code_output)
