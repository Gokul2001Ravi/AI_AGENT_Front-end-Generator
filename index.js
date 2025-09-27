 
    // ---------------- Q/A Chatbot ----------------
    const qaQuestions = [
      "What is your business or product?",
      "Who are the target users?",
      "What screens/pages do you need?",
      "What features should it include?",
      "Any specific UI/UX preferences?",
      "What type of content will it have?",
      "Any constraints or other notes?"
    ];
    const qaKeys = ["Business", "Users", "Pages", "Features", "UI/UX", "Content", "Other"];
    let qaAnswers = {};
    let qaIndex = 0;

    function addMessage(text, sender="bot") {
      const container = document.getElementById("chatContainer");
      const msg = document.createElement("div");
      msg.style.margin = "6px 0";
      msg.style.padding = "8px 12px";
      msg.style.borderRadius = "10px";
      msg.style.maxWidth = "75%";
      msg.style.whiteSpace = "pre-wrap";
      msg.style.background = sender === "bot" ? "#dcfce7" : "#bbf7d0";
      msg.style.alignSelf = sender === "bot" ? "flex-start" : "flex-end";
      msg.innerText = text;
      container.appendChild(msg);
      container.scrollTop = container.scrollHeight;
    }

    function startQA() {
      qaAnswers = {};
      qaIndex = 0;
      document.getElementById("chatContainer").innerHTML = "";
      document.getElementById("chatSection").style.display = "block";
      document.getElementById("manualSection").style.display = "none"; // hide manual form
      addMessage("Let's gather your requirements! 🚀");
      addMessage(qaQuestions[qaIndex]);
    }

    function sendAnswer() {
      const input = document.getElementById("chatInput");
      const answer = input.value.trim();
      if (!answer) return;
      addMessage(answer, "user");
      qaAnswers[qaKeys[qaIndex]] = answer;
      input.value = "";
      qaIndex++;
      if (qaIndex < qaQuestions.length) {
        addMessage(qaQuestions[qaIndex]);
      } else {
        addMessage("✅ Thanks! Generating your BRD...");
        generateFromQA(qaAnswers); // directly call pipeline
      }
    }

    async function generateFromQA(answers) {
      const outputDiv = document.getElementById("output");
      outputDiv.innerText = "⏳ Generating BRD & PRD from your answers...";
      try {
        const response = await fetch("http://127.0.0.1:8000/generate_from_qa", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ answers })
        });
        if (!response.ok) throw new Error("Server error: " + response.status);
        const data = await response.json();
        const runId = `qa-${Date.now()}`;
        const run = {
          id: runId,
          projectName: answers.Business || "Untitled Project",
          timestamp: new Date().toISOString(),
          brd: JSON.stringify(answers, null, 2), // save the raw answers as BRD
          results: data
        };

        saveRun(run);
        displayResults(data);
      } catch (err) {
        outputDiv.innerText = "❌ Error: " + err.message;
      }
    }

    // ---------------- IndexedDB ----------------
    let db;
    const request = indexedDB.open("PipelineDB", 1);
    request.onupgradeneeded = (event) => {
      db = event.target.result;
      if (!db.objectStoreNames.contains("runs")) {
        const store = db.createObjectStore("runs", { keyPath: "id" });
        store.createIndex("projectName", "projectName", { unique: false });
      }
    };
    request.onsuccess = (event) => {
      db = event.target.result;
      loadHistoryDropdown();
    };

    function saveRun(run) {
      const tx = db.transaction("runs", "readwrite");
      tx.objectStore("runs").put(run);
      tx.oncomplete = () => loadHistoryDropdown();
    }

    function getAllRuns(callback) {
      const tx = db.transaction("runs", "readonly");
      const request = tx.objectStore("runs").getAll();
      request.onsuccess = () => callback(request.result);
    }

    function getRun(id, callback) {
      const tx = db.transaction("runs", "readonly");
      const request = tx.objectStore("runs").get(id);
      request.onsuccess = () => callback(request.result);
    }

    function loadHistoryDropdown() {
      getAllRuns((runs) => {
        const dropdown = document.getElementById("historyDropdown");
        dropdown.innerHTML = `<option value="">-- Select Previous Project --</option>`;
        runs.forEach(run => {
          dropdown.innerHTML += `<option value="${run.id}">${run.projectName} (${new Date(run.timestamp).toLocaleString()})</option>`;
        });
      });
    }

    function onHistorySelect() {
      const dropdown = document.getElementById("historyDropdown");
      const projectInput = document.getElementById("projectName");
      projectInput.disabled = !!dropdown.value;
    }

    // ---------------- Pipeline (Manual BRD form) ----------------
    async function generate() {
      const projectNameInput = document.getElementById("projectName");
      const dropdown = document.getElementById("historyDropdown");
      const brdText = document.getElementById("brdInput").value.trim();
      const outputDiv = document.getElementById("output");

      if (!brdText) {
        alert("Please enter a BRD or modification.");
        return;
      }

      let runId, projectName, baseRun = null, mergedBRD = brdText;

      if (dropdown.value) {
        await new Promise(resolve => getRun(dropdown.value, (run) => {
          baseRun = run;
          projectName = run.projectName;
          runId = run.id;
          resolve();
        }));
      } else if (projectNameInput.value.trim()) {
        const allRuns = await new Promise(resolve => getAllRuns(resolve));
        const matches = allRuns.filter(r => r.projectName.toLowerCase() === projectNameInput.value.trim().toLowerCase());
        if (matches.length) {
          baseRun = matches[matches.length - 1];
          projectName = baseRun.projectName;
          runId = baseRun.id;
        } else {
          projectName = projectNameInput.value.trim();
          runId = `${projectName.toLowerCase().replace(/\s+/g, "-")}-${Date.now()}`;
        }
      } else {
        const allRuns = await new Promise(resolve => getAllRuns(resolve));
        baseRun = await semanticSearch(brdText, allRuns);
        if (baseRun) {
          projectName = baseRun.projectName;
          runId = baseRun.id;
        } else {
          projectName = "Untitled Project";
          runId = `untitled-${Date.now()}`;
        }
      }

      if (baseRun) {
        mergedBRD = baseRun.brd + "\n\n--- UPDATE ---\n\n" + brdText;
      }

      outputDiv.innerText = "⏳ Generating...";
      try {
        const response = await fetch("http://127.0.0.1:8000/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ brd_text: mergedBRD })
        });
        if (!response.ok) throw new Error("Server error: " + response.status);
        const data = await response.json();
        const run = {
          id: runId,
          projectName,
          timestamp: new Date().toISOString(),
          brd: mergedBRD,
          results: data
        };

        saveRun(run);
        displayResults(data);
      } catch (err) {
        outputDiv.innerText = "❌ Error: " + err.message;
      }
    }

    // ---------------- esbuild init + preview ----------------
    let esbuildInitialized = false;
    async function initEsbuild() {
      if (!esbuildInitialized) {
        await esbuild.initialize({
          wasmURL: "https://unpkg.com/esbuild-wasm@0.17.19/esbuild.wasm"
        });
        esbuildInitialized = true;
      }
    }

    async function showPreview(frontendFiles) {
      await initEsbuild();
      const entry = frontendFiles["src/main.jsx"] || frontendFiles["src/App.jsx"];
      if (!entry) {
        console.warn("No entry file found in frontend files");
        return;
      }

      const result = await esbuild.build({
        entryPoints: ["entry.jsx"],
        bundle: true,
        write: false,
        format: "iife",
        platform: "browser",
        stdin: {
          contents: entry,
          resolveDir: "/",
          sourcefile: "entry.jsx",
          loader: "jsx"
        }
      });

      const jsOutput = result.outputFiles[0].text;
      const cssOutput = frontendFiles["src/index.css"] || "";

      const iframe = document.getElementById("previewFrame");
      const doc = iframe.contentDocument || iframe.contentWindow.document;
      doc.open();
      doc.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <style>${cssOutput}</style>
          <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
          <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
        </head>
        <body>
          <div id="root"></div>
          <script>${jsOutput}</script>
        </body>
        </html>
      `);
      doc.close();
    }

    // ---------------- displayResults ----------------
    function displayResults(data) {
      const outputDiv = document.getElementById("output");
      outputDiv.innerHTML = "";
      for (const [key, value] of Object.entries(data)) {
        if (value === null || value === undefined || value === "") continue;
        const section = document.createElement("div");
        section.className = "section";
        const btn = document.createElement("button");
        btn.className = "section-btn";
        btn.innerText = key;
        const content = document.createElement("div");
        content.className = "section-content";
        let displayText = typeof value === "string" ? value : JSON.stringify(value, null, 2);
        let charIndex = 0;
        const typingInterval = setInterval(() => {
          content.innerText += displayText.charAt(charIndex);
          charIndex++;
          if (charIndex >= displayText.length) clearInterval(typingInterval);
        }, 10);
        btn.addEventListener("click", () => {
          content.style.display = content.style.display === "block" ? "none" : "block";
        });
        section.appendChild(btn);
        section.appendChild(content);
        outputDiv.appendChild(section);
      }

      // Auto-preview if frontend exists
      if (data.frontend) {
        showPreview(data.frontend);
      }
    }

    // ---------------- Embeddings ----------------
    async function embedText(text) {
      try {
        const resp = await fetch("http://localhost:11434/api/embeddings", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ model: "nomic-embed-text", input: text })
        });
        const data = await resp.json();
        return data.embedding;
      } catch (err) {
        console.error("Embedding error:", err);
        return null;
      }
    }

    function cosineSim(a, b) {
      const dot = a.reduce((sum, v, i) => sum + v * b[i], 0);
      const normA = Math.sqrt(a.reduce((sum, v) => sum + v * v, 0));
      const normB = Math.sqrt(b.reduce((sum, v) => sum + v * v, 0));
      return dot / (normA * normB);
    }

    async function semanticSearch(query, runs) {
      const queryEmbed = await embedText(query);
      if (!queryEmbed) return null;
      let best = null, bestScore = -1;
      for (const run of runs) {
        if (!run.embedding) continue;
        const score = cosineSim(queryEmbed, run.embedding);
        if (score > bestScore) {
          best = run;
          bestScore = score;
        }
      }
      return best;
    }
  