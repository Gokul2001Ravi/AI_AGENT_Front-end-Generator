# # pipeline.py -                                      grok till 5 still testing
# from working import agent, agent1, agent2, agent3, agent4, agent5, clean_json_output
# from working import generate_or_update_prd
# from memory import Memory
# import json
# import re


# def run_pipeline(brd_text: str = None, requirements: dict = None):
#     # Initialize memory
#     memory = Memory()

#     print("🚀 Starting AI Pipeline with Memory...\n")

#     # Step 0: Requirements → BRD
#     if requirements:
#         brd_text = agent(requirements)
#         print("\n=== Generated BRD from Requirements ===\n", brd_text)

#     # Step 1: BRD -> PRD
#     #prd_output = agent1(brd_text)
#     # Check if there’s already a PRD in STM+++++++++++
#     existing_prd = memory.get_stm("PRD")
#     prd_output = generate_or_update_prd(brd_text, existing_prd)
#     memory.add_to_stm("BRD", brd_text)
#     memory.add_to_stm("PRD", prd_output)
#     memory.add_to_ltm("PRD", prd_output)
#     print("\n=== PRD ===\n", prd_output)

#     # Step 2: PRD -> Architecture
#     stm_context = memory.get_stm()
#     arch_input = {
#         "context": stm_context,
#         "focus": "Generate system architecture based on BRD + PRD"
#     }
#     arch_output = agent2(arch_input)
#     memory.add_to_stm("Architecture", arch_output)
#     memory.add_to_ltm("Architecture", arch_output)
#     print("\n=== Architecture ===\n", arch_output)

#     # Step 3: Architecture -> Frontend Code
#     stm_context = memory.get_stm()
#     code_input = {
#         "context": stm_context,
#         "focus": "Generate frontend code based on BRD + PRD + Architecture"
#     }
#     code_output = agent3(code_input)
#     memory.add_to_stm("Code", code_output)
#     memory.add_to_ltm("Code", code_output)
#     print("\n=== Generated Code (React) ===\n", code_output)

#     # Clean and parse Agent3 output
#     try:
#         cleaned_code = clean_json_output(code_output)
#         parsed_code = json.loads(cleaned_code)
#     except json.JSONDecodeError as e:
#         print("❌ Agent 3 produced invalid JSON (after cleaning).")
#         print(f"[DEBUG] Error: {e}")
#         print(f"[DEBUG] Raw output:\n{code_output}")
#         parsed_code = {"raw": cleaned_code}

#     # Step 4: Code -> Validation (Agent 4)
#     validation_result = agent4(parsed_code)
#     memory.add_to_stm("Validation", validation_result)
#     memory.add_to_ltm("Validation", validation_result)
#     # Print logs
#     print("\n=== Agent 4 Logs ===")
#     for log in validation_result.get("logs", []):
#         print(log)
#     # Print issues
#     print("\n=== Agent 4 Validation Issues ===")
#     if validation_result["issues_found"]:
#         for issue in validation_result["issues_found"]:
#             print(issue)
#     else:
#         print("[No issues found ✅]")

#     # Step 5: If issues, run Agent5 to fix code
#     issues = validation_result["issues_found"]
#     arch_text = memory.get_stm("Architecture")  # Use for context
#     if issues:
#         print("\n🚧 Running Agent 5 to fix issues...")
#         fixed_code = agent5(parsed_code, issues, arch_text)
#         memory.add_to_stm("Fixed_Code", fixed_code)
#         memory.add_to_ltm("Fixed_Code", fixed_code)
#         print("\n=== Fixed Code from Agent 5 ===\n", json.dumps(fixed_code, indent=2))

#         # Optional: Re-validate fixed code (up to 2 iterations)
#         max_iters = 2
#         iter_count = 0
#         while issues and iter_count < max_iters:
#             iter_count += 1
#             print(f"\n🔄 Re-validating fixed code (Iteration {iter_count})...")
#             validation_result = agent4(fixed_code)
#             issues = validation_result["issues_found"]
#             if issues:
#                 print("\nRemaining Issues:")
#                 for issue in issues:
#                     print(issue)
#                 fixed_code = agent5(fixed_code, issues, arch_text)
#                 memory.update_stm("Fixed_Code", fixed_code)
#                 memory.add_to_ltm("Fixed_Code", fixed_code)
#                 print("\n=== Updated Fixed Code ===\n", json.dumps(fixed_code, indent=2))
#             else:
#                 print("\n[All issues fixed ✅]")

#     # Final: return memory (STM + LTM) for inspection
#     return memory


# # if __name__ == "__main__":
# #     brd_text = """We want to build a personal portfolio website for showcasing an individual's projects and skills. The website should have the following sections: Home, About, Projects, Skills, and Contact. Users should be able to click through navigation links at the top of the page to move between sections smoothly (single-page scrolling). 
# #     The Projects section should display project cards with images, titles, short descriptions, and buttons to view more details or visit external links (e.g., GitHub, Live Demo). 
# #     The Contact section should include a simple form with fields for name, email, and message (no backend processing required, just UI). 
# #     The design should be modern, responsive (desktop, tablet, mobile), and lightweight, with a visually appealing color scheme. 
# #     Animations and transitions should be used for smooth user experience. 
# #     There is no need for backend or database; this is a frontend-only project."""

# #     memory = run_pipeline(brd_text)

# #     # Show what STM and LTM look like
# #     print("\n📌 STM State:", memory.get_stm())
# #     print("\n📌 LTM DB:", memory.get_ltm())

# if __name__ == "__main__":
#     # -------------------------------
#     # Toggle between modes here
#     # -------------------------------
#     MODE = "dict"   # options: "dict" or "brd"
 
#     if MODE == "dict":
#         user_requirements = {
#             "Business": "Online Bookstore",
#             "Users": "Readers and Authors",
#             "Pages": "Home, Catalog, Book Details, Cart, Checkout, Profile",
#             "Features": "Search, Filters, Add to Cart, Reviews, Ratings",
#             "UI/UX": "Responsive, modern, easy navigation",
#             "Content": "Book listings, images, metadata",
#             "Other": "No backend, frontend only"
#         }
#         memory = run_pipeline(user_requirements=user_requirements)
 
#     elif MODE == "brd":
#         brd_text = """We want to build a personal portfolio website 
#         showcasing projects, skills, resume, and a contact form. 
#         Target users are recruiters and collaborators. 
#         Pages: Home, About, Projects, Resume, Contact. 
#         Features: Clean UI, responsive design, downloadable resume."""
#         memory = run_pipeline(brd_text=brd_text)
 
#     else:
#         raise ValueError("Invalid MODE. Choose 'dict' or 'brd'.")


#########################################################################################################working comment out coz of memory updated in memory.py(19/9)

# from working import agent, agent1, agent2, agent3, agent4, agent5, clean_json_output
# from working import generate_or_update_prd
# from memory import Memory
# import json
# import re


# def run_pipeline(brd_text: str = None, user_requirements: dict = None, answers: dict = None):
#     """
#     Run the multi-agent pipeline.
#     - If brd_text provided → use directly.
#     - If user_requirements or answers dict provided → generate BRD first.
#     """
#     # Initialize memory
#     memory = Memory()
#     print("🚀 Starting AI Pipeline with Memory...\n")

#     # Step 0: Dict (requirements/answers) → BRD
#     if user_requirements or answers:
#         reqs = user_requirements if user_requirements else answers
#         brd_text = agent(reqs)  # Agent0: turn dict into BRD text
#         print("\n=== Generated BRD from Requirements ===\n", brd_text)

#     if not brd_text:
#         raise ValueError("❌ run_pipeline requires either brd_text or requirements/answers dict")

#     # Step 1: BRD -> PRD
#     existing_prd = memory.get_stm("PRD")
#     prd_output = generate_or_update_prd(brd_text, existing_prd)
#     memory.add_to_stm("BRD", brd_text)
#     memory.add_to_stm("PRD", prd_output)
#     memory.add_to_ltm("PRD", prd_output)
#     print("\n=== PRD ===\n", prd_output)

#     # Step 2: PRD -> Architecture
#     stm_context = memory.get_stm()
#     arch_input = {
#         "context": stm_context,
#         "focus": "Generate system architecture based on BRD + PRD"
#     }
#     arch_output = agent2(arch_input)
#     memory.add_to_stm("Architecture", arch_output)
#     memory.add_to_ltm("Architecture", arch_output)
#     print("\n=== Architecture ===\n", arch_output)

#     # Step 3: Architecture -> Frontend Code
#     stm_context = memory.get_stm()
#     code_input = {
#         "context": stm_context,
#         "focus": "Generate frontend code based on BRD + PRD + Architecture"
#     }
#     code_output = agent3(code_input)
#     memory.add_to_stm("Code", code_output)
#     memory.add_to_ltm("Code", code_output)
#     print("\n=== Generated Code (React) ===\n", code_output)

#     # Clean and parse Agent3 output
#     try:
#         cleaned_code = clean_json_output(code_output)
#         parsed_code = json.loads(cleaned_code)
#     except json.JSONDecodeError as e:
#         print("❌ Agent 3 produced invalid JSON (after cleaning).")
#         print(f"[DEBUG] Error: {e}")
#         print(f"[DEBUG] Raw output:\n{code_output}")
#         parsed_code = {"raw": cleaned_code}

#     # Step 4: Code -> Validation (Agent 4)
#     validation_result = agent4(parsed_code)
#     memory.add_to_stm("Validation", validation_result)
#     memory.add_to_ltm("Validation", validation_result)

#     print("\n=== Agent 4 Logs ===")
#     for log in validation_result.get("logs", []):
#         print(log)

#     print("\n=== Agent 4 Validation Issues ===")
#     if validation_result["issues_found"]:
#         for issue in validation_result["issues_found"]:
#             print(issue)
#     else:
#         print("[No issues found ✅]")

#     # Step 5: If issues, run Agent5 to fix code
#     issues = validation_result["issues_found"]
#     arch_text = memory.get_stm("Architecture")
#     if issues:
#         print("\n🚧 Running Agent 5 to fix issues...")
#         fixed_code = agent5(parsed_code, issues, arch_text)
#         memory.add_to_stm("Fixed_Code", fixed_code)
#         memory.add_to_ltm("Fixed_Code", fixed_code)
#         print("\n=== Fixed Code from Agent 5 ===\n", json.dumps(fixed_code, indent=2))

#         # Optional: Re-validate fixed code
#         max_iters = 2
#         iter_count = 0
#         while issues and iter_count < max_iters:
#             iter_count += 1
#             print(f"\n🔄 Re-validating fixed code (Iteration {iter_count})...")
#             validation_result = agent4(fixed_code)
#             issues = validation_result["issues_found"]
#             if issues:
#                 print("\nRemaining Issues:")
#                 for issue in issues:
#                     print(issue)
#                 fixed_code = agent5(fixed_code, issues, arch_text)
#                 memory.update_stm("Fixed_Code", fixed_code)
#                 memory.add_to_ltm("Fixed_Code", fixed_code)
#                 print("\n=== Updated Fixed Code ===\n", json.dumps(fixed_code, indent=2))
#             else:
#                 print("\n[All issues fixed ✅]")

#     return memory


# if __name__ == "__main__":
#     # Toggle between modes here
#     MODE = "dict"   # options: "dict" | "answers" | "brd"

#     if MODE == "dict":
#         user_requirements = {
#             "Business": "Online Bookstore",
#             "Users": "Readers and Authors",
#             "Pages": "Home, Catalog, Book Details, Cart, Checkout, Profile",
#             "Features": "Search, Filters, Add to Cart, Reviews, Ratings",
#             "UI/UX": "Responsive, modern, easy navigation",
#             "Content": "Book listings, images, metadata",
#             "Other": "No backend, frontend only"
#         }
#         memory = run_pipeline(user_requirements=user_requirements)

#     elif MODE == "answers":
#         answers = {
#             "business_type": "E-commerce website for sports products",
#             "target_users": "General customers",
#             "screens": ["Home", "Product Listing", "Cart", "Checkout"],
#             "features": ["Search", "Filters", "User login", "Payment integration"]
#         }
#         memory = run_pipeline(answers=answers)

#     elif MODE == "brd":
#         brd_text = """We want to build a personal portfolio website 
#         showcasing projects, skills, resume, and a contact form. 
#         Target users are recruiters and collaborators. 
#         Pages: Home, About, Projects, Resume, Contact. 
#         Features: Clean UI, responsive design, downloadable resume."""
#         memory = run_pipeline(brd_text=brd_text)

#     else:
#         raise ValueError("Invalid MODE. Choose 'dict', 'answers', or 'brd'.")


########################################################################################################################## this is new with QA memory and BRD (19/9)
from working import agent, agent1, agent2, agent3, agent4, agent5, clean_json_output
from working import generate_or_update_prd
from memory import Memory
import json
import re
import subprocess, os, sys
import os
import shutil
import psutil
import os, sys, shutil, subprocess, psutil, re, pathlib

def kill_existing_vite():
    """Kill any running vite dev server (port 5173 by default)."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and "vite" in " ".join(proc.info['cmdline']).lower():
                print(f"[Agent6] 🔪 Killing existing vite process PID={proc.info['pid']}")
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def ensure_tailwind(base_dir):
    """Install Tailwind + Vite plugin and patch configs safely."""
    # Step 1: Install tailwind + vite plugin
    subprocess.run(
        ["npm", "install", "-D", "tailwindcss", "@tailwindcss/vite"],
        cwd=base_dir, shell=True, check=True
    )
    print("[Agent6] 📦 Tailwind + @tailwindcss/vite installed")

    # Step 2: Patch vite.config.js
    vite_path = os.path.join(base_dir, "vite.config.js")
    if os.path.exists(vite_path):
        vite_text = pathlib.Path(vite_path).read_text()

        # Guarantee correct imports
        if "from '@vitejs/plugin-react'" not in vite_text:
            vite_text = "import react from '@vitejs/plugin-react'\n" + vite_text
        if "from '@tailwindcss/vite'" not in vite_text:
            vite_text = "import tailwindcss from '@tailwindcss/vite'\n" + vite_text

        # Ensure defineConfig import exists
        if "from 'vite'" not in vite_text:
            vite_text = "import { defineConfig } from 'vite'\n" + vite_text

        # Patch plugins array cleanly
        vite_text = re.sub(
            r"plugins:\s*\[[^\]]*\]",
            "plugins: [react(), tailwindcss()]",
            vite_text
        )

        pathlib.Path(vite_path).write_text(vite_text)
        print("[Agent6] ⚡ vite.config.js patched with Tailwind")

    # Step 3: Patch index.css
    css_path = os.path.join(base_dir, "src", "index.css")
    if os.path.exists(css_path):
        css_text = pathlib.Path(css_path).read_text()
        if '@import "tailwindcss"' not in css_text:
            css_text = '@import "tailwindcss";\n' + css_text
            pathlib.Path(css_path).write_text(css_text)
            print("[Agent6] 🎨 index.css updated with Tailwind import")

    # Step 4: Init tailwind.config.js if missing
    if not os.path.exists(os.path.join(base_dir, "tailwind.config.js")):
        subprocess.run(
            ["npx", "tailwindcss", "init", "-p"],
            cwd=base_dir, shell=True, check=True
        )
        print("[Agent6] 🛠 tailwind.config.js created")



def agent6(fixed_code: dict, base_dir="generated_ui"):
    """Safely write frontend code and launch Vite dev server with Tailwind."""

    # 1️⃣ Clean old generated folders
    for folder in ["generated_ui", "validated_code"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
            print(f"[Agent6] 🧹 Cleaned {folder}")

    # 2️⃣ Extract frontend if nested
    if "frontend" in fixed_code:
        fixed_code = fixed_code["frontend"]

    fixed_code = dict(fixed_code)  # fresh copy
    print(f"[Agent6] 📝 Preparing {len(fixed_code)} files to write")

    # 3️⃣ Write files
    for filename, content in fixed_code.items():
        file_path = os.path.join(base_dir, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"[Agent6] ✅ Files written to {base_dir}")

    # 4️⃣ Ensure index.html exists in project root
    root_index = os.path.join(base_dir, "index.html")
    public_index = os.path.join(base_dir, "public", "index.html")

    if os.path.exists(public_index) and not os.path.exists(root_index):
        shutil.move(public_index, root_index)
        print("[Agent6] 🔀 Moved index.html from /public → /")
    elif not os.path.exists(root_index):
        with open(root_index, "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Auto-Generated App</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>""")
        print("[Agent6] 🛠️ Created fallback index.html in project root")

    # 5️⃣ Run npm install only if node_modules missing
    node_modules_path = os.path.join(base_dir, "node_modules")
    if not os.path.exists(node_modules_path):
        print("[Agent6] 📦 node_modules not found → running npm install...")
        subprocess.run(["npm", "install"], cwd=base_dir, shell=True, check=True)
        print("[Agent6] 📦 npm install completed")
    else:
        print("[Agent6] ⚡ Skipping npm install (node_modules already exists)")

    # 6️⃣ Ensure Tailwind setup
    ensure_tailwind(base_dir)

    # 7️⃣ Kill any existing vite dev server
    kill_existing_vite()

    # 8️⃣ Run npm run dev (detached, new terminal)
    if sys.platform == "win32":
        subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=base_dir,
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=base_dir,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setpgrp
        )

    print("[Agent6] 🚀 Vite dev server launched in new terminal at http://localhost:5173")


# def kill_existing_vite():
#     """Kill any running vite dev server (port 5173 by default)."""
#     for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
#         try:
#             if proc.info['cmdline'] and "vite" in " ".join(proc.info['cmdline']).lower():
#                 print(f"[Agent6] 🔪 Killing existing vite process PID={proc.info['pid']}")
#                 proc.terminate()
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue


# def agent6(fixed_code: dict, base_dir="generated_ui"):
#     """Safely write frontend code and launch Vite dev server without crashing FastAPI."""

#     # 1️⃣ Clean old generated folders
#     for folder in ["generated_ui", "validated_code"]:
#         if os.path.exists(folder):
#             shutil.rmtree(folder, ignore_errors=True)
#             print(f"[Agent6] 🧹 Cleaned {folder}")

#     # 2️⃣ Extract frontend if nested
#     if "frontend" in fixed_code:
#         fixed_code = fixed_code["frontend"]

#     fixed_code = dict(fixed_code)  # fresh copy
#     print(f"[Agent6] 📝 Preparing {len(fixed_code)} files to write")

#     # 3️⃣ Write files
#     for filename, content in fixed_code.items():
#         file_path = os.path.join(base_dir, filename)
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(content)

#     print(f"[Agent6] ✅ Files written to {base_dir}")

#     # 4️⃣ Ensure index.html exists in project root
#     root_index = os.path.join(base_dir, "index.html")
#     public_index = os.path.join(base_dir, "public", "index.html")

#     if os.path.exists(public_index) and not os.path.exists(root_index):
#         shutil.move(public_index, root_index)
#         print("[Agent6] 🔀 Moved index.html from /public → /")
#     elif not os.path.exists(root_index):
#         with open(root_index, "w", encoding="utf-8") as f:
#             f.write("""<!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8" />
#   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#   <title>Auto-Generated App</title>
# </head>
# <body>
#   <div id="root"></div>
#   <script type="module" src="/src/main.jsx"></script>
# </body>
# </html>""")
#         print("[Agent6] 🛠️ Created fallback index.html in project root")

#     # 5️⃣ Run npm install only if node_modules missing
#     node_modules_path = os.path.join(base_dir, "node_modules")
#     if not os.path.exists(node_modules_path):
#         print("[Agent6] 📦 node_modules not found → running npm install...")
#         subprocess.run(["npm", "install"], cwd=base_dir, shell=True, check=True)
#         print("[Agent6] 📦 npm install completed")
#     else:
#         print("[Agent6] ⚡ Skipping npm install (node_modules already exists)")

#     # 6️⃣ Kill any existing vite dev server
#     kill_existing_vite()

#     # 7️⃣ Run npm run dev (detached, new terminal)
#     if sys.platform == "win32":
#         subprocess.Popen(
#             ["npm", "run", "dev"],
#             cwd=base_dir,
#             shell = True,
#             creationflags=subprocess.CREATE_NEW_CONSOLE
#         )
#     else:
#         subprocess.Popen(
#             ["npm", "run", "dev"],
#             cwd=base_dir,
#             shell = True,
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.STDOUT,
#             preexec_fn=os.setpgrp
#         )

#     print("[Agent6] 🚀 Vite dev server launched in new terminal at http://localhost:5173")


# # Agent 6 → Serve UI                                     - works fine but, session mismatch btwn fastapi and vite
# def agent6(fixed_code: dict, base_dir="generated_ui"):
#     """Take Fixed_Code JSON, clean old dirs, write files, run npm install + npm run dev"""
    
#     # 1. Always clean old generated_ui and validated_code
#     for folder in ["generated_ui", "validated_code"]:
#         if os.path.exists(folder):
#             shutil.rmtree(folder, ignore_errors=True)
#             print(f"[Agent6] 🧹 Cleaned {folder}")

#     # 2. Extract frontend part if nested
#     if "frontend" in fixed_code:
#         fixed_code = fixed_code["frontend"]

#     # 🚨 Ensure we only work with a clean dict
#     fixed_code = dict(fixed_code)  # copy fresh
#     print(f"[Agent6] 📝 Preparing {len(fixed_code)} files to write")

#     # 3. Write all files to disk
#     for filename, content in fixed_code.items():
#         file_path = os.path.join(base_dir, filename)
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(content)

#     print(f"[Agent6] ✅ Files written to {base_dir}")

#     # 4. Run npm install
#     subprocess.run(["npm", "install"], cwd=base_dir, shell=True)
#     print("[Agent6] 📦 npm install completed")

#     # 5. Start dev server
#     subprocess.Popen(["npm", "run", "dev"], cwd=base_dir, shell=True)
#     print("[Agent6] 🚀 Vite dev server running on http://localhost:5173")

def run_pipeline(brd_text: str = None, user_requirements: dict = None, answers: dict = None):
    """
    Run the multi-agent pipeline.
    - If brd_text provided → use directly.
    - If user_requirements or answers dict provided → generate BRD first.
    """
    # Initialize memory
    memory = Memory()
    print("🚀 Starting AI Pipeline with Memory...\n")

    # =========================
    # Step 0: QA/Requirements → BRD
    # =========================
    if user_requirements or answers:
        reqs = user_requirements if user_requirements else answers

        # [ADDED] Save QA/Requirements into STM + LTM
        memory.add_to_stm("QA", reqs)
        memory.add_to_ltm("QA", reqs)

        brd_text = agent(reqs)  # Agent0: turn dict into BRD text
        print("\n=== Generated BRD from Requirements ===\n", brd_text)

    if not brd_text:
        raise ValueError("❌ run_pipeline requires either brd_text or requirements/answers dict")

    # =========================
    # Step 1: BRD -> PRD
    # =========================
    existing_prd = memory.get_stm("PRD")
    prd_output = generate_or_update_prd(brd_text, existing_prd)

    memory.add_to_stm("BRD", brd_text)
    memory.add_to_ltm("BRD", brd_text)   # [ADDED] Save BRD into LTM
    memory.add_to_stm("PRD", prd_output)
    memory.add_to_ltm("PRD", prd_output)
    print("\n=== PRD ===\n", prd_output)

    # =========================
    # Step 2: PRD -> Architecture
    # =========================
    stm_context = memory.get_stm()
    arch_input = {
        "context": stm_context,
        "focus": "Generate system architecture based on BRD + PRD"
    }
    arch_output = agent2(arch_input)
    memory.add_to_stm("Architecture", arch_output)
    memory.add_to_ltm("Architecture", arch_output)
    print("\n=== Architecture ===\n", arch_output)

    # =========================
    # Step 3: Architecture -> Frontend Code
    # =========================
    stm_context = memory.get_stm()
    code_input = {
        "context": stm_context,
        "focus": "Generate frontend code based on BRD + PRD + Architecture"
    }
    code_output = agent3(code_input)
    memory.add_to_stm("Code", code_output)
    memory.add_to_ltm("Code", code_output)
    print("\n=== Generated Code (React) ===\n", code_output)

    # Clean and parse Agent3 output
    try:
        cleaned_code = clean_json_output(code_output)
        parsed_code = json.loads(cleaned_code)
    except json.JSONDecodeError as e:
        print("❌ Agent 3 produced invalid JSON (after cleaning).")
        print(f"[DEBUG] Error: {e}")
        print(f"[DEBUG] Raw output:\n{code_output}")
        parsed_code = {"raw": cleaned_code}

    # =========================
    # Step 4: Code -> Validation
    # =========================
    validation_result = agent4(parsed_code)
    memory.add_to_stm("Validation", validation_result)
    memory.add_to_ltm("Validation", validation_result)

    print("\n=== Agent 4 Logs ===")
    for log in validation_result.get("logs", []):
        print(log)

    print("\n=== Agent 4 Validation Issues ===")
    if validation_result["issues_found"]:
        for issue in validation_result["issues_found"]:
            print(issue)
    else:
        print("[No issues found ✅]")

    # =========================
    # Step 5: Fix Code (if issues)
    # =========================
    issues = validation_result["issues_found"]
    arch_text = memory.get_stm("Architecture")

    # Default: if no issues, use the parsed_code as fixed_code
    fixed_code = parsed_code

    if issues:
        print("\n🚧 Running Agent 5 to fix issues...")
        fixed_code = agent5(parsed_code, issues, arch_text)
        memory.add_to_stm("Fixed_Code", fixed_code)
        memory.add_to_ltm("Fixed_Code", fixed_code)
        print("\n=== Fixed Code from Agent 5 ===\n", json.dumps(fixed_code, indent=2))

        # Optional: Re-validate fixed code
        max_iters = 1
        iter_count = 0
        while issues and iter_count < max_iters:
            iter_count += 1
            print(f"\n🔄 Re-validating fixed code (Iteration {iter_count})...")
            validation_result = agent4(fixed_code)
            issues = validation_result["issues_found"]
            if issues:
                print("\nRemaining Issues:")
                for issue in issues:
                    print(issue)
                fixed_code = agent5(fixed_code, issues, arch_text)
                memory.update_stm("Fixed_Code", fixed_code)
                memory.add_to_ltm("Fixed_Code", fixed_code)
                print("\n=== Updated Fixed Code ===\n", json.dumps(fixed_code, indent=2))
            else:
                print("\n[All issues fixed ✅]")

     # =========================
    # Step 6: Serve UI
    # =========================
    agent6(fixed_code)

    return memory



if __name__ == "__main__":
    # Toggle between modes here
    MODE = "dict"   # options: "dict" | "answers" | "brd"

    if MODE == "dict":
        user_requirements = {
            "Business": "Online Bookstore",
            "Users": "Readers and Authors",
            "Pages": "Home, Catalog, Book Details, Cart, Checkout, Profile",
            "Features": "Search, Filters, Add to Cart, Reviews, Ratings",
            "UI/UX": "Responsive, modern, easy navigation",
            "Content": "Book listings, images, metadata",
            "Other": "No backend, frontend only"
        }
        memory = run_pipeline(user_requirements=user_requirements)

    elif MODE == "answers":
        answers = {
            "business_type": "E-commerce website for sports products",
            "target_users": "General customers",
            "screens": ["Home", "Product Listing", "Cart", "Checkout"],
            "features": ["Search", "Filters", "User login", "Payment integration"]
        }
        memory = run_pipeline(answers=answers)

    elif MODE == "brd":
        brd_text = """We want to build a personal portfolio website 
        showcasing projects, skills, resume, and a contact form. 
        Target users are recruiters and collaborators. 
        Pages: Home, About, Projects, Resume, Contact. 
        Features: Clean UI, responsive design, downloadable resume."""
        memory = run_pipeline(brd_text=brd_text)

    else:
        raise ValueError("Invalid MODE. Choose 'dict', 'answers', or 'brd'.")
