# # # # # pipeline.py -                                                        gpt till 4 worked
# # # # from working import agent1, agent2, agent3, agent4
# # # # from memory import Memory
# # # # import json
# # # # import re

# # # # def run_pipeline(brd_text: str):
# # # #     # Initialize memory
# # # #     memory = Memory()

# # # #     print("🚀 Starting AI Pipeline with Memory...\n")

# # # #     # Step 1: BRD -> PRD
# # # #     prd_output = agent1(brd_text)
# # # #     memory.add_to_stm("BRD", brd_text)
# # # #     memory.add_to_stm("PRD", prd_output)
# # # #     memory.add_to_ltm("PRD", prd_output)
# # # #     print("\n=== PRD ===\n", prd_output)

# # # #     # Step 2: PRD -> Architecture
# # # #     stm_context = memory.get_stm()
# # # #     arch_input = {
# # # #         "context": stm_context,
# # # #         "focus": "Generate system architecture based on BRD + PRD"
# # # #     }
# # # #     arch_output = agent2(arch_input)
# # # #     memory.add_to_stm("Architecture", arch_output)
# # # #     memory.add_to_ltm("Architecture", arch_output)
# # # #     print("\n=== Architecture ===\n", arch_output)

# # # #     # Step 3: Architecture -> Frontend Code
# # # #     stm_context = memory.get_stm()
# # # #     code_input = {
# # # #         "context": stm_context,
# # # #         "focus": "Generate frontend code based on BRD + PRD + Architecture"
# # # #     }
# # # #     code_output = agent3(code_input)
# # # #     memory.add_to_stm("Code", code_output)
# # # #     memory.add_to_ltm("Code", code_output)
# # # #     print("\n=== Generated Code (React) ===\n", code_output)

# # # #     # Step 4: Code -> Validation (Agent 4)
# # # #     # try:
# # # #     #     parsed_code = json.loads(code_output)  # JSON from Agent 3
# # # #     # except json.JSONDecodeError:
# # # #     #     print("❌ Agent 3 produced invalid JSON.")
# # # #     #     parsed_code = {}

# # # #     def clean_json_output(raw: str) -> str:
# # # #         """
# # # #         Cleans Agent 3's raw output so it can be parsed as JSON.
# # # #         - Removes ```json / ``` fences
# # # #         - Removes trailing commas
# # # #         - Strips whitespace
# # # #         """
# # # #         if not raw:
# # # #             return "{}"

# # # #         # Remove code fences
# # # #         cleaned = re.sub(r"```(?:json)?", "", raw, flags=re.IGNORECASE).strip()
# # # #         cleaned = cleaned.replace("```", "").strip()

# # # #         # Remove trailing commas before closing } or ]
# # # #         cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)

# # # #         return cleaned

# # # #     # === Step 4: Code -> Validation (Agent 4) ===
# # # #     try:
# # # #         cleaned_code = clean_json_output(code_output)
# # # #         parsed_code = json.loads(cleaned_code)
# # # #     except json.JSONDecodeError as e:
# # # #         print("❌ Agent 3 produced invalid JSON (after cleaning).")
# # # #         print(f"[DEBUG] Error: {e}")
# # # #         print(f"[DEBUG] Raw output:\n{code_output}")
# # # #         # fallback: keep raw inside dict so Agent 4 still gets something
# # # #         parsed_code = {"raw": cleaned_code}


# # # #     validation_result = agent4(parsed_code)
# # # #     # Store validation results in memory (includes logs + issues + code)
# # # #     memory.add_to_stm("Validation", validation_result)
# # # #     memory.add_to_ltm("Validation", validation_result)
# # # #     # Print logs
# # # #     print("\n=== Agent 4 Logs ===")
# # # #     for log in validation_result.get("logs", []):
# # # #         print(log)
# # # #     # Print issues
# # # #     print("\n=== Agent 4 Validation Issues ===")
# # # #     if validation_result["issues_found"]:
# # # #         for issue in validation_result["issues_found"]:
# # # #             print(issue)
# # # #     else:
# # # #         print("[No issues found ✅]")

# # # #     # Final: return memory (STM + LTM) for inspection
# # # #     return memory


# # # # if __name__ == "__main__":
# # # #     brd_text = """We want to build a personal portfolio website for showcasing an individual's projects and skills. The website should have the following sections: Home, About, Projects, Skills, and Contact. Users should be able to click through navigation links at the top of the page to move between sections smoothly (single-page scrolling). 
# # # #     The Projects section should display project cards with images, titles, short descriptions, and buttons to view more details or visit external links (e.g., GitHub, Live Demo). 
# # # #     The Contact section should include a simple form with fields for name, email, and message (no backend processing required, just UI). 
# # # #     The design should be modern, responsive (desktop, tablet, mobile), and lightweight, with a visually appealing color scheme. 
# # # #     Animations and transitions should be used for smooth user experience. 
# # # #     There is no need for backend or database; this is a frontend-only project."""

# # # #     memory = run_pipeline(brd_text)

# # # #     # Show what STM and LTM look like
# # # #     print("\n📌 STM State:", memory.get_stm())
# # # #     print("\n📌 LTM DB:", memory.get_ltm())



# pipeline.py -                                      grok till 5 still testing
from working import agent1, agent2, agent3, agent4, agent5, clean_json_output
from memory import Memory
import json
import re

def run_pipeline(brd_text: str):
    # Initialize memory
    memory = Memory()

    print("🚀 Starting AI Pipeline with Memory...\n")

    # Step 1: BRD -> PRD
    prd_output = agent1(brd_text)
    memory.add_to_stm("BRD", brd_text)
    memory.add_to_stm("PRD", prd_output)
    memory.add_to_ltm("PRD", prd_output)
    print("\n=== PRD ===\n", prd_output)

    # Step 2: PRD -> Architecture
    stm_context = memory.get_stm()
    arch_input = {
        "context": stm_context,
        "focus": "Generate system architecture based on BRD + PRD"
    }
    arch_output = agent2(arch_input)
    memory.add_to_stm("Architecture", arch_output)
    memory.add_to_ltm("Architecture", arch_output)
    print("\n=== Architecture ===\n", arch_output)

    # Step 3: Architecture -> Frontend Code
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

    # Step 4: Code -> Validation (Agent 4)
    validation_result = agent4(parsed_code)
    memory.add_to_stm("Validation", validation_result)
    memory.add_to_ltm("Validation", validation_result)
    # Print logs
    print("\n=== Agent 4 Logs ===")
    for log in validation_result.get("logs", []):
        print(log)
    # Print issues
    print("\n=== Agent 4 Validation Issues ===")
    if validation_result["issues_found"]:
        for issue in validation_result["issues_found"]:
            print(issue)
    else:
        print("[No issues found ✅]")

    # Step 5: If issues, run Agent5 to fix code
    issues = validation_result["issues_found"]
    arch_text = memory.get_stm("Architecture")  # Use for context
    if issues:
        print("\n🚧 Running Agent 5 to fix issues...")
        fixed_code = agent5(parsed_code, issues, arch_text)
        memory.add_to_stm("Fixed_Code", fixed_code)
        memory.add_to_ltm("Fixed_Code", fixed_code)
        print("\n=== Fixed Code from Agent 5 ===\n", json.dumps(fixed_code, indent=2))

        # Optional: Re-validate fixed code (up to 2 iterations)
        max_iters = 2
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

    # Final: return memory (STM + LTM) for inspection
    return memory


if __name__ == "__main__":
    brd_text = """We want to build a personal portfolio website for showcasing an individual's projects and skills. The website should have the following sections: Home, About, Projects, Skills, and Contact. Users should be able to click through navigation links at the top of the page to move between sections smoothly (single-page scrolling). 
    The Projects section should display project cards with images, titles, short descriptions, and buttons to view more details or visit external links (e.g., GitHub, Live Demo). 
    The Contact section should include a simple form with fields for name, email, and message (no backend processing required, just UI). 
    The design should be modern, responsive (desktop, tablet, mobile), and lightweight, with a visually appealing color scheme. 
    Animations and transitions should be used for smooth user experience. 
    There is no need for backend or database; this is a frontend-only project."""

    memory = run_pipeline(brd_text)

    # Show what STM and LTM look like
    print("\n📌 STM State:", memory.get_stm())
    print("\n📌 LTM DB:", memory.get_ltm())

