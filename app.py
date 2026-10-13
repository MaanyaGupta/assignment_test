"""
Local Web UI Server for Policy QA Assistant
Zero external dependencies (uses standard library http.server).
Runs a modern, responsive web application at http://localhost:8000
"""

import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from assistant import ask

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Policy QA Assistant — The Policy That Changed</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: rgba(22, 30, 49, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --primary-hover: #0ea5e9;
      --accent: #818cf8;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: radial-gradient(circle at 50% 0%, #1e293b 0%, var(--bg) 70%);
      color: var(--text);
      font-family: 'Inter', -apple-system, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding: 2rem 1rem;
    }

    .container {
      max-width: 900px;
      margin: 0 auto;
      width: 100%;
    }

    header {
      text-align: center;
      margin-bottom: 2rem;
    }

    .badge-sub {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--primary);
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 9999px;
      margin-bottom: 0.75rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    h1 {
      font-size: 2.2rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #ffffff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }

    p.subtitle {
      color: var(--text-muted);
      font-size: 0.95rem;
    }

    .card {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }

    .form-grid {
      display: grid;
      grid-template-columns: 1fr 220px;
      gap: 1rem;
      margin-bottom: 1rem;
    }
    @media (max-width: 640px) {
      .form-grid { grid-template-columns: 1fr; }
    }

    label {
      display: block;
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.5rem;
    }

    input[type="text"], input[type="date"] {
      width: 100%;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--card-border);
      color: var(--text);
      padding: 0.75rem 1rem;
      border-radius: 10px;
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    input[type="text"]:focus, input[type="date"]:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
    }

    .btn-submit {
      width: 100%;
      background: linear-gradient(135deg, var(--primary) 0%, #2563eb 100%);
      color: #fff;
      font-weight: 600;
      padding: 0.85rem 1.5rem;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      font-size: 1rem;
      transition: transform 0.15s, opacity 0.2s;
    }
    .btn-submit:hover {
      opacity: 0.92;
      transform: translateY(-1px);
    }

    .chips-title {
      font-size: 0.8rem;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      margin-bottom: 0.6rem;
    }

    .chips-container {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 0.4rem 0.75rem;
      font-size: 0.8rem;
      color: #cbd5e1;
      cursor: pointer;
      transition: all 0.2s;
    }
    .chip:hover {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--primary);
      color: #fff;
    }
    .chip.adv {
      border-color: rgba(245, 158, 11, 0.3);
      color: #fbbf24;
    }
    .chip.adv:hover {
      background: rgba(245, 158, 11, 0.15);
      border-color: var(--warning);
    }

    /* Result Card */
    #resultBox {
      display: none;
      animation: fadeIn 0.3s ease-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      margin-bottom: 1rem;
    }
    .status-ANSWERED { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .status-CONFLICT_RESOLVED { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .status-CANNOT_ANSWER { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

    .citations-list {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1.25rem;
    }
    .citation-tag {
      background: rgba(129, 140, 248, 0.1);
      border: 1px solid rgba(129, 140, 248, 0.25);
      color: #c7d2fe;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
    }

    .answer-text {
      white-space: pre-wrap;
      line-height: 1.65;
      font-size: 0.95rem;
      color: #e2e8f0;
      background: rgba(15, 23, 42, 0.6);
      padding: 1.25rem;
      border-radius: 12px;
      border: 1px solid var(--card-border);
      margin-bottom: 1rem;
    }

    .resolution-callout {
      background: rgba(56, 189, 248, 0.08);
      border-left: 3px solid var(--primary);
      padding: 0.75rem 1rem;
      border-radius: 4px;
      font-size: 0.85rem;
      color: #bae6fd;
      line-height: 1.5;
    }

    footer {
      text-align: center;
      margin-top: auto;
      padding-top: 2rem;
      color: #64748b;
      font-size: 0.8rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge-sub">Grounded Temporal Q&A Assistant</div>
      <h1>The Policy That Changed</h1>
      <p class="subtitle">Answering merchant fee, refund & limit questions across conflicting policy documents.</p>
    </header>

    <div class="card">
      <form id="qaForm" onsubmit="handleAsk(event)">
        <div class="form-grid">
          <div>
            <label for="questionInput">Merchant Question</label>
            <input type="text" id="questionInput" placeholder="e.g. When does a small merchant receive UPI money?" required />
          </div>
          <div>
            <label for="dateInput">As of Date</label>
            <input type="text" id="dateInput" value="15 August 2026" placeholder="15 August 2026" required />
          </div>
        </div>
        <button type="submit" class="btn-submit" id="submitBtn">Ask Assistant</button>
      </form>

      <div style="margin-top: 1.5rem;">
        <div class="chips-title">Preset Benchmark Questions (Click to Ask)</div>
        <div class="chips-container">
          <div class="chip" onclick="setQuestion('When does a small merchant receive UPI money?', '15 August 2026')">Q1. Small Merchant Settlement</div>
          <div class="chip" onclick="setQuestion('A large merchant (above Rs.10 lakh monthly) receives a Rs.4,000 UPI payment. What MDR and GST do they pay?', '15 August 2026')">Q2. Large Merchant Fee (₹4,000)</div>
          <div class="chip adv" onclick="setQuestion('Same merchant, a Rs.1,50,000 payment. What do they pay?', '15 August 2026')">Q3. Limit Trap (₹1,50,000)</div>
          <div class="chip" onclick="setQuestion('A merchant refunds a customer 3 hours after the sale. Do they get the MDR back?', '20 Aug 2026')">Q4a. Refund on 20 Aug 2026</div>
          <div class="chip adv" onclick="setQuestion('A merchant refunds a customer 3 hours after the sale. Do they get the MDR back?', '5 Sep 2026')">Q4b. Refund on 5 Sep 2026 (Deleted Clause)</div>
          <div class="chip adv" onclick="setQuestion('What does the FAQ say about the MDR cap, and is the FAQ right?', '15 August 2026')">Q5. Stale FAQ Cap Conflict</div>
          <div class="chip" onclick="setQuestion('Can a customer pay Rs.1,00,000 twice in one day to a merchant?', '15 August 2026')">Q6. Customer Daily Limit</div>
          <div class="chip" onclick="setQuestion('I closed my account yesterday. When will I get my money?', '15 August 2026')">Q7. Account Closure Money</div>
          <div class="chip" onclick="setQuestion('Does the policy allow me to settle card payments same day?', '15 August 2026')">Q8. Card Same Day?</div>
          <div class="chip adv" onclick="setQuestion('What is the MDR fee for RuPay credit cards processed over UPI?', '15 August 2026')">Adversarial: RuPay on UPI</div>
          <div class="chip adv" onclick="setQuestion('How much does the Instant Settlement add-on cost per month?', '15 August 2026')">Adversarial: Add-on Cost</div>
        </div>
      </div>
    </div>

    <!-- Result Display -->
    <div class="card" id="resultBox">
      <div id="statusBadge" class="status-badge"></div>
      
      <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.4rem;">
        Grounded Citations
      </div>
      <div id="citationsList" class="citations-list"></div>

      <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.4rem;">
        Assistant Answer
      </div>
      <div id="answerText" class="answer-text"></div>

      <div id="conflictCallout" class="resolution-callout" style="display: none;"></div>
    </div>

    <footer>
      Evaluation & QA Assistant &bull; Offline Deterministic Engine &bull; Version 1.0
    </footer>
  </div>

  <script>
    function setQuestion(q, d) {
      document.getElementById('questionInput').value = q;
      document.getElementById('dateInput').value = d;
      handleAsk();
    }

    async function handleAsk(e) {
      if (e) e.preventDefault();
      const question = document.getElementById('questionInput').value.trim();
      const date = document.getElementById('dateInput').value.trim();
      if (!question) return;

      const submitBtn = document.getElementById('submitBtn');
      submitBtn.innerText = 'Analyzing Policy...';
      submitBtn.disabled = true;

      try {
        const resp = await fetch('/api/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: question, as_of_date: date })
        });
        const data = await resp.json();
        renderResult(data);
      } catch (err) {
        alert('Error connecting to backend: ' + err);
      } finally {
        submitBtn.innerText = 'Ask Assistant';
        submitBtn.disabled = false;
      }
    }

    function renderResult(data) {
      const box = document.getElementById('resultBox');
      const badge = document.getElementById('statusBadge');
      const citList = document.getElementById('citationsList');
      const ansText = document.getElementById('answerText');
      const callout = document.getElementById('conflictCallout');

      badge.className = 'status-badge status-' + data.status;
      badge.innerText = data.status.replace('_', ' ');

      citList.innerHTML = '';
      if (data.citations && data.citations.length > 0) {
        data.citations.forEach(c => {
          const span = document.createElement('span');
          span.className = 'citation-tag';
          span.innerText = c;
          citList.appendChild(span);
        });
      } else {
        const span = document.createElement('span');
        span.className = 'citation-tag';
        span.innerText = 'No citations (Information omitted / out-of-scope)';
        citList.appendChild(span);
      }

      ansText.innerText = data.answer;

      if (data.conflict_resolution) {
        callout.style.display = 'block';
        callout.innerHTML = '<strong>Conflict Resolution:</strong> ' + data.conflict_resolution;
      } else {
        callout.style.display = 'none';
      }

      box.style.display = 'block';
      box.scrollIntoView({ behavior: 'smooth' });
    }
  </script>
</body>
</html>
"""


class QAHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/ask":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                payload = json.loads(body)
                q = payload.get("question", "")
                dt = payload.get("as_of_date", "15 August 2026")
                res = ask(q, dt)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(res).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Concise logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")


def run_server(port: int = 8000):
    server = HTTPServer(("127.0.0.1", port), QAHandler)
    print("=" * 70)
    print(f"  POLICY QA ASSISTANT LOCAL WEB SERVER STARTED")
    print(f"  URL: http://localhost:{port}")
    print("  Zero external dependencies. Press Ctrl+C to terminate.")
    print("=" * 70)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
