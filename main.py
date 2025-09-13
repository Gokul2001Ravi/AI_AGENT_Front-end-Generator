# main.py
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

@app.post("/generate")
def generate_pipeline(brd_text: str = Body(..., embed=True)):
    """
    Endpoint: /generate
    Input: {"brd_text": "..."}
    Output: JSON with PRD, Architecture, Code, Issues, Fixed Code
    """
    memory = run_pipeline(brd_text)

    # Extract results from STM
    prd = memory.get_stm("PRD")
    archi = memory.get_stm("Architecture")
    code = memory.get_stm("Code")
    validation = memory.get_stm("Validation")
    fixed_code = memory.get_stm("Fixed_Code")

    return {
        "PRD": prd,
        "Architecture": archi,
        "Generated_Code": code,
        "Validation": validation,
        "Fixed_Code": fixed_code
    }

@app.get("/")
def home():
    return {"message": "AI Agent Pipeline API is running 🚀"}


#python -m uvicorn main:app --reload



# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8" />
#   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#   <title>BRD Generator</title>
#   <style>
#     body {
#       font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#       background: #f0fdf4;
#       margin: 0;
#       padding: 0;
#       display: flex;
#       justify-content: center;
#       align-items: flex-start;
#       min-height: 100vh;
#     }

#     .container {
#       background: #ffffff;
#       margin-top: 40px;
#       padding: 30px;
#       border-radius: 16px;
#       box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
#       width: 80%;
#       max-width: 900px;
#     }

#     h1 {
#       color: #15803d;
#       text-align: center;
#       margin-bottom: 20px;
#     }

#     textarea {
#       width: 100%;
#       height: 200px;
#       padding: 12px;
#       border: 2px solid #22c55e;
#       border-radius: 10px;
#       resize: vertical;
#       font-size: 16px;
#     }

#     button {
#       margin-top: 15px;
#       background: #22c55e;
#       color: white;
#       border: none;
#       padding: 12px 24px;
#       border-radius: 10px;
#       font-size: 16px;
#       cursor: pointer;
#       transition: background 0.3s ease;
#       display: block;
#       width: 100%;
#     }

#     button:hover {
#       background: #16a34a;
#     }

#     .output {
#       margin-top: 20px;
#       padding: 20px;
#       border-radius: 10px;
#       background: #ecfdf5;
#       border: 1px solid #22c55e;
#       white-space: pre-wrap;
#       max-height: 400px;
#       overflow-y: auto;
#       font-size: 15px;
#     }
#   </style>
# </head>
# <body>
#   <div class="container">
#     <h1>BRD → UI Code Generator</h1>
#     <textarea id="brdInput" placeholder="Paste your BRD here..."></textarea>
#     <button onclick="generate()">Generate</button>
#     <div id="output" class="output"></div>
#   </div>

#   <script>
#     async function generate() {
#       const brdText = document.getElementById("brdInput").value;
#       const outputDiv = document.getElementById("output");
#       outputDiv.innerText = "⏳ Processing... please wait...";

#       try {
#         const response = await fetch("http://127.0.0.1:8000/generate", {
#           method: "POST",
#           headers: {
#             "Content-Type": "application/json",
#           },
#           body: JSON.stringify({ brd_text: brdText }),
#         });

#         if (!response.ok) {
#           throw new Error("Server error: " + response.status);
#         }

#         const data = await response.json();
#         outputDiv.innerText = JSON.stringify(data, null, 2);
#       } catch (err) {
#         outputDiv.innerText = "❌ Error: " + err.message;
#       }
#     }
#   </script>
# </body>
# </html>

   