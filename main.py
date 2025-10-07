# # main.py
# from fastapi import FastAPI, Body
# from pipeline import run_pipeline
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="AI Agent Pipeline")

# # Allow frontend to call API
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # in prod, restrict to your UI domain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/generate")
# def generate_pipeline(brd_text: str = Body(..., embed=True)):
#     """
#     Endpoint: /generate
#     Input: {"brd_text": "..."}
#     Output: JSON with PRD, Architecture, Code, Issues, Fixed Code
#     """
#     memory = run_pipeline(brd_text)

#     # Extract results from STM
#     prd = memory.get_stm("PRD")
#     archi = memory.get_stm("Architecture")
#     code = memory.get_stm("Code")
#     validation = memory.get_stm("Validation")
#     fixed_code = memory.get_stm("Fixed_Code")

#     return {
#         "PRD": prd,
#         "Architecture": archi,
#         "Generated_Code": code,
#         "Validation": validation,
#         "Fixed_Code": fixed_code
#     }

# @app.get("/")
# def home():
#     return {"message": "AI Agent Pipeline API is running 🚀"}

#python -m uvicorn main:app  
#python -m uvicorn main:app --reload
#python -m uvicorn main:app --reload --reload-exclude 'generated_ui/*'
#npm install vite --save-dev

#################################################################################################################################(19/9) before updating the QA memory

# from fastapi import FastAPI, Body
# from pipeline import run_pipeline
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="AI Agent Pipeline")

# # Allow frontend to call API
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # in prod, restrict to your UI domain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------- Existing BRD flow --------------------
# @app.post("/generate")
# def generate_pipeline(brd_text: str = Body(..., embed=True)):
#     """
#     Endpoint: /generate
#     Input: {"brd_text": "..."}
#     Output: JSON with PRD, Architecture, Code, Issues, Fixed Code
#     """
#     memory = run_pipeline(brd_text=brd_text)

#     return {
#         "PRD": memory.get_stm("PRD"),
#         "Architecture": memory.get_stm("Architecture"),
#         "Generated_Code": memory.get_stm("Code"),
#         "Validation": memory.get_stm("Validation"),
#         "Fixed_Code": memory.get_stm("Fixed_Code"),
#     }

# # -------------------- New Q/A flow --------------------
# @app.post("/generate_from_qa")
# def generate_from_qa(answers: dict = Body(...)):
#     """
#     Endpoint: /generate_from_qa
#     Input: {"project_name": "...", "objective": "...", "features": "...", ...}
#     Output: JSON with PRD, Architecture, Code, Issues, Fixed Code
#     """
#     # Directly pass dict into pipeline (no need to stringify!)
#     memory = run_pipeline(answers=answers)

#     return {
#         "PRD": memory.get_stm("PRD"),
#         "Architecture": memory.get_stm("Architecture"),
#         "Generated_Code": memory.get_stm("Code"),
#         "Validation": memory.get_stm("Validation"),
#         "Fixed_Code": memory.get_stm("Fixed_Code"),
#     }

# @app.get("/")
# def home():
#     return {"message": "AI Agent Pipeline API is running 🚀"}

####################################################################################################################################### after updating the QA
from fastapi import FastAPI, Body
from pipeline import run_pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Agent Pipeline")

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, restrict to your UI domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Existing BRD flow --------------------
@app.post("/generate")
def generate_pipeline(brd_text: str = Body(..., embed=True)):
    """
    Endpoint: /generate
    Input: {"brd_text": "..."}
    Output: JSON with BRD, PRD, Architecture, Code, Issues, Fixed Code
    """
    memory = run_pipeline(brd_text=brd_text)

    return {
        "QA": memory.get_stm("QA"),   # [ADDED] In case BRD was generated from Q/A
        "BRD": memory.get_stm("BRD"),
        "PRD": memory.get_stm("PRD"),
        "Architecture": memory.get_stm("Architecture"),
        "Generated_Code": memory.get_stm("Code"),
        "Validation": memory.get_stm("Validation"),
        "Fixed_Code": memory.get_stm("Fixed_Code"),
    }

# -------------------- New Q/A flow --------------------
@app.post("/generate_from_qa")
def generate_from_qa(answers: dict = Body(...)):
    """
    Endpoint: /generate_from_qa
    Input: {
        "business": "...",
        "users": "...",
        "screens": [...],
        "features": [...],
        "ui_ux": "...",
        "content": "...",
        "constraints": "..."
    }
    Output: JSON with QA, BRD, PRD, Architecture, Code, Issues, Fixed Code
    """
    # Pass Q/A dict into pipeline
    memory = run_pipeline(answers=answers)

    return {
        "QA": memory.get_stm("QA"),   # [ADDED]
        "BRD": memory.get_stm("BRD"), # [ADDED]
        "PRD": memory.get_stm("PRD"),
        "Architecture": memory.get_stm("Architecture"),
        "Generated_Code": memory.get_stm("Code"),
        "Validation": memory.get_stm("Validation"),
        "Fixed_Code": memory.get_stm("Fixed_Code"),
    }

@app.get("/")
def home():
    return {"message": "AI Agent Pipeline API is running 🚀"}
