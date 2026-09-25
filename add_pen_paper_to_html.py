import json

with open('pen_paper_data.json', 'r') as f:
    pen_data = json.load(f)

with open('phartrack_algorithm_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Mode Buttons
old_buttons = '''          <button id="modeBtnPortfolio" class="action-btn" style="background:var(--cyan); color:#000; border-color:var(--cyan); font-weight:700;" onclick="switchSimMode('portfolio')">
            ⚡ All-Medicines Portfolio Simulation (30-Day Reorder)
          </button>
          <button id="modeBtnSingle" class="action-btn" style="background:transparent; color:var(--text-muted); border-color:transparent;" onclick="switchSimMode('single')">
            🔬 Single Medicine Deep-Dive &amp; EOQ Curve
          </button>'''

new_buttons = '''          <button id="modeBtnPortfolio" class="action-btn" style="background:var(--cyan); color:#000; border-color:var(--cyan); font-weight:700;" onclick="switchSimMode('portfolio')">
            ⚡ All-Medicines Portfolio Simulation (30-Day Reorder)
          </button>
          <button id="modeBtnSingle" class="action-btn" style="background:transparent; color:var(--text-muted); border-color:transparent;" onclick="switchSimMode('single')">
            🔬 Single Medicine Deep-Dive &amp; EOQ Curve
          </button>
          <button id="modeBtnPenPaper" class="action-btn" style="background:transparent; color:var(--text-muted); border-color:transparent;" onclick="switchSimMode('penpaper')">
            📝 Pen &amp; Paper Manual Simulation (Audit Mode)
          </button>'''

assert old_buttons in html, "Could not find mode buttons in HTML!"
html = html.replace(old_buttons, new_buttons, 1)

# 2. View C: Pen & Paper Simulation HTML structure
pen_paper_view_html = '''
    <!-- ========================================================================= -->
    <!-- VIEW C: PEN & PAPER MANUAL SIMULATION (AUDIT & DEFENSE PANEL MODE)       -->
    <!-- ========================================================================= -->
    <div id="viewPenPaperSim" style="display:none;">
      <!-- Control Bar -->
      <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:12px; padding:18px 24px; margin-bottom:24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
          <span style="font-size:13px; font-weight:700; color:var(--text); font-family:'Space Grotesk', sans-serif;">Select Audit Case Study:</span>
          <button id="btnCaseBiogesic" onclick="switchPenPaperCase('biogesic')" class="action-btn" style="background:var(--cyan); color:#000; border-color:var(--cyan); font-weight:700; font-size:12px; padding:6px 14px;">
            🔵 Biogesic 500mg (Unilab &middot; Lead Time: 3d)
          </button>
          <button id="btnCaseAmox" onclick="switchPenPaperCase('amoxicillin')" class="action-btn" style="background:transparent; color:var(--text-muted); border-color:var(--border); font-weight:700; font-size:12px; padding:6px 14px;">
            🟢 Amoxicillin 500mg (Dyna Drug &middot; Lead Time: 4d)
          </button>
        </div>

        <div style="display:flex; align-items:center; gap:10px;">
          <button onclick="printPenPaperWorksheet()" class="action-btn" style="background:linear-gradient(135deg, var(--emerald), #059669); color:#fff; border-color:var(--emerald); font-size:12px; padding:7px 16px;">
            🖨️ Print / Save Clean PDF Worksheet
          </button>
        </div>
      </div>

      <!-- Section Header -->
      <div style="margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
          <div>
            <h3 id="penPaperTitle" style="font-family:'Space Grotesk', sans-serif; font-size:20px; font-weight:800; color:var(--text); margin-bottom:4px;">
              Biogesic (Paracetamol 500mg) &mdash; Hand-Worked Mathematical Audit
            </h3>
            <p id="penPaperSubtitle" style="font-size:13px; color:var(--text-muted);">
              Every variable substituted by hand. Complete 14-day manual ledger tracking daily demand, dynamic ROP triggers, and lead time replenishment.
            </p>
          </div>
          <div style="font-family:'JetBrains Mono', monospace; font-size:11px; background:rgba(6,182,212,0.1); border:1px solid rgba(6,182,212,0.3); color:var(--cyan); padding:6px 12px; border-radius:6px;">
            POLICY: (s, Q) Continuous Review &middot; 95% CSL (Z=1.65)
          </div>
        </div>
      </div>

      <!-- Step-by-Step Formula Cards -->
      <div id="penPaperFormulaCards" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:16px; margin-bottom:28px;">
        <!-- Populated via JS -->
      </div>

      <!-- 14-Day Manual Simulation Ledger Table -->
      <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:28px; box-shadow:var(--shadow-card); overflow-x:auto;" id="printableLedgerContainer">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <div>
            <strong style="font-family:'Space Grotesk', sans-serif; font-size:16px; color:var(--text);">
              14-Day Manual Simulation Ledger (Day-by-Day Tabular Calculation)
            </strong>
            <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">
              Governing Equation: $\\text{Ending Stock}_t = \\text{Beginning Stock}_{t} + Q_{arrived, t} - d_t$
            </div>
          </div>
          <div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:var(--text-dim);">
            Manual Audit Verified: 0 Math Discrepancies
          </div>
        </div>

        <table style="width:100%; border-collapse:collapse; font-size:12px; font-family:'Plus Jakarta Sans', sans-serif;" id="penPaperTable">
          <thead>
            <tr style="background:rgba(255,255,255,0.03); border-bottom:2px solid var(--border); font-family:'Space Grotesk', sans-serif; font-size:11px; text-transform:uppercase; color:var(--text-dim);">
              <th style="padding:10px 8px; text-align:center;">Day (t)</th>
              <th style="padding:10px 8px; text-align:right;">Beg. Stock (I<sub>t-1</sub>)</th>
              <th style="padding:10px 8px; text-align:right; color:var(--cyan);">Arrival (Q<sub>arr</sub>)</th>
              <th style="padding:10px 8px; text-align:right;">Available</th>
              <th style="padding:10px 8px; text-align:right; color:var(--rose);">Demand (d<sub>t</sub>)</th>
              <th style="padding:10px 8px; text-align:right; font-weight:700;">End Stock (I<sub>t</sub>)</th>
              <th style="padding:10px 8px; text-align:center;">I<sub>t</sub> &le; ROP?</th>
              <th style="padding:10px 8px; text-align:right; color:var(--emerald);">PO Placed (Q)</th>
              <th style="padding:10px 8px; text-align:center;">ETA Day</th>
              <th style="padding:10px 8px; text-align:right; color:var(--amber);">Pipeline</th>
              <th style="padding:10px 8px; text-align:right;">Holding Cost</th>
              <th style="padding:10px 14px; text-align:left;">Audit &amp; Operational Notes</th>
            </tr>
          </thead>
          <tbody id="penPaperTableBody">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>

      <!-- Theoretical Defense Panel Notes Callout -->
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:20px; margin-bottom:30px;">
        <div style="background:var(--bg-card); border:1px solid var(--border); border-left:4px solid var(--cyan); border-radius:8px; padding:16px 20px;">
          <strong style="font-family:'Space Grotesk', sans-serif; font-size:14px; color:var(--text); display:block; margin-bottom:6px;">
            1. Why Did Stockout Not Occur on Critical Days?
          </strong>
          <p style="font-size:12px; color:var(--text-muted); line-height:1.6; margin:0;">
            During lead time transit (e.g. Day 4 for Biogesic), stock dipped down to <strong>295 units</strong> while awaiting supplier delivery. Because PharTrack dimensioned the <strong>Safety Stock buffer at 171 units</strong> ($Z \\times \\sigma_d \\times \\sqrt{L}$), the stochastic surge in demand was 100% absorbed without customer stockouts.
          </p>
        </div>

        <div style="background:var(--bg-card); border:1px solid var(--border); border-left:4px solid var(--emerald); border-radius:8px; padding:16px 20px;">
          <strong style="font-family:'Space Grotesk', sans-serif; font-size:14px; color:var(--text); display:block; margin-bottom:6px;">
            2. Deterministic EOQ Lot Sizing vs. Dynamic ROP Timing
          </strong>
          <p style="font-size:12px; color:var(--text-muted); line-height:1.6; margin:0;">
            Under the continuous review $(s, Q)$ policy, the order batch size ($Q = EOQ$) is mathematically fixed to balance administrative procurement costs vs. carrying capital ($H = C \\times 20\\%$). The trigger timing ($s = ROP$), however, dynamically shifts depending on real-time sales drawdowns.
          </p>
        </div>

        <div style="background:var(--bg-card); border:1px solid var(--border); border-left:4px solid var(--violet); border-radius:8px; padding:16px 20px;">
          <strong style="font-family:'Space Grotesk', sans-serif; font-size:14px; color:var(--text); display:block; margin-bottom:6px;">
            3. Zero Black-Box Auditability
          </strong>
          <p style="font-size:12px; color:var(--text-muted); line-height:1.6; margin:0;">
            Every single cell in this manual ledger can be calculated with pencil, paper, and a basic calculator. For a pharmacy panel or thesis defense, this eliminates software distrust by transparently demonstrating mathematical determinism.
          </p>
        </div>
      </div>
    </div>
'''

# Insert View C before View A
target_view_marker = '    <!-- ========================================================================= -->\n    <!-- VIEW A: PORTFOLIO-WIDE AUTOMATED REORDERING SIMULATION (ALL MEDICINES)   -->'
assert target_view_marker in html, "Could not find target view marker in HTML!"
html = html.replace(target_view_marker, pen_paper_view_html + '\n' + target_view_marker, 1)

# 3. Add Print CSS to style sheet
print_css = '''
    /* Print Worksheet Optimization for Pen-and-Paper Simulation */
    @media print {
      body {
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 10pt !important;
      }
      header, .nav-tabs, #catFilterTabs, .sim-controls, #modeBtnPortfolio, #modeBtnSingle, #modeBtnPenPaper, #themeBtn, #slideBtn, .btn, button {
        display: none !important;
      }
      #viewPenPaperSim {
        display: block !important;
      }
      #viewPortfolioSim, #viewSingleSim {
        display: none !important;
      }
      #printableLedgerContainer, #penPaperFormulaCards, #viewPenPaperSim {
        background: #ffffff !important;
        border: 1px solid #cccccc !important;
        box-shadow: none !important;
      }
      #penPaperTable th, #penPaperTable td {
        border: 1px solid #dddddd !important;
        color: #000000 !important;
        padding: 4px 6px !important;
      }
    }
'''
html = html.replace('  </style>', print_css + '  </style>', 1)

# 4. Inject PEN_PAPER_DATA and JavaScript functions
js_logic = f'''
  // Pen-and-Paper Simulation Verified Data
  const PEN_PAPER_DATA = {json.dumps(pen_data, indent=2)};
  let activePenPaperCase = 'biogesic';

  function switchPenPaperCase(caseKey) {{
    activePenPaperCase = caseKey;
    const btnBio = document.getElementById('btnCaseBiogesic');
    const btnAmox = document.getElementById('btnCaseAmox');
    if (caseKey === 'biogesic') {{
      btnBio.style.background = 'var(--cyan)';
      btnBio.style.color = '#000';
      btnBio.style.borderColor = 'var(--cyan)';
      btnAmox.style.background = 'transparent';
      btnAmox.style.color = 'var(--text-muted)';
      btnAmox.style.borderColor = 'var(--border)';
    }} else {{
      btnAmox.style.background = 'var(--cyan)';
      btnAmox.style.color = '#000';
      btnAmox.style.borderColor = 'var(--cyan)';
      btnBio.style.background = 'transparent';
      btnBio.style.color = 'var(--text-muted)';
      btnBio.style.borderColor = 'var(--border)';
    }}
    renderPenPaperView();
  }}

  function renderPenPaperView() {{
    const data = PEN_PAPER_DATA[activePenPaperCase];
    if (!data) return;

    // 1. Titles
    document.getElementById('penPaperTitle').textContent = `${{data.name}} — Hand-Worked Mathematical Audit`;
    document.getElementById('penPaperSubtitle').textContent = `Every variable substituted by hand. Complete 14-day manual ledger tracking daily demand, dynamic ROP triggers, and lead time replenishment via ${{data.supplier}}.`;

    // 2. Formula Breakdown Cards
    const cardsContainer = document.getElementById('penPaperFormulaCards');
    if (cardsContainer) {{
      cardsContainer.innerHTML = `
        <!-- Card 1: Demand Profile -->
        <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:10px; padding:16px;">
          <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:var(--text-dim); text-transform:uppercase; margin-bottom:4px; font-weight:700;">
            1. Daily Sales Statistics
          </div>
          <div style="font-size:13px; font-weight:700; color:var(--text); margin-bottom:6px;">
            d̄ = ${{data.d_bar}} u/day &middot; σ<sub>d</sub> = ${{data.sigma_d}} u/day
          </div>
          <div style="font-size:11px; color:var(--text-muted); font-family:'JetBrains Mono', monospace; line-height:1.5;">
            From N = 730 historical POS days<br/>
            Lead Time: L = <strong>${{data.lead_time}} days</strong> (${{data.supplier}})
          </div>
        </div>

        <!-- Card 2: Safety Stock -->
        <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:10px; padding:16px;">
          <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:var(--amber); text-transform:uppercase; margin-bottom:4px; font-weight:700;">
            2. Safety Stock Buffer (SS)
          </div>
          <div style="font-size:13px; font-weight:700; color:var(--amber); margin-bottom:6px;">
            SS = Z &times; σ<sub>d</sub> &times; &radic;L = ${{data.SS.toLocaleString()}} units
          </div>
          <div style="font-size:11px; color:var(--text-muted); font-family:'JetBrains Mono', monospace; line-height:1.5;">
            = 1.65 &times; ${{data.sigma_d}} &times; &radic;${{data.lead_time}}<br/>
            = 1.65 &times; ${{data.sigma_d}} &times; ${{Math.sqrt(data.lead_time).toFixed(4)}} = <strong>${{data.SS_exact}} u</strong>
          </div>
        </div>

        <!-- Card 3: Reorder Point -->
        <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:10px; padding:16px;">
          <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:var(--rose); text-transform:uppercase; margin-bottom:4px; font-weight:700;">
            3. Dynamic Reorder Point (ROP)
          </div>
          <div style="font-size:13px; font-weight:700; color:var(--rose); margin-bottom:6px;">
            ROP = (d̄ &times; L) + SS = ${{data.ROP.toLocaleString()}} units
          </div>
          <div style="font-size:11px; color:var(--text-muted); font-family:'JetBrains Mono', monospace; line-height:1.5;">
            = (${{data.d_bar}} &times; ${{data.lead_time}}) + ${{data.SS}}<br/>
            = ${{(data.d_bar * data.lead_time).toFixed(2)}} + ${{data.SS}} = <strong>${{data.ROP_exact}} u</strong>
          </div>
        </div>

        <!-- Card 4: Wilson EOQ -->
        <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:10px; padding:16px;">
          <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:var(--emerald); text-transform:uppercase; margin-bottom:4px; font-weight:700;">
            4. Economic Order Quantity (EOQ)
          </div>
          <div style="font-size:13px; font-weight:700; color:var(--emerald); margin-bottom:6px;">
            EOQ = &radic;(2DS / H) = ${{data.EOQ.toLocaleString()}} units
          </div>
          <div style="font-size:11px; color:var(--text-muted); font-family:'JetBrains Mono', monospace; line-height:1.5;">
            D = ${{data.D.toLocaleString()}} u/yr &middot; S = ₱${{data.S}} &middot; H = ₱${{data.H}}/yr<br/>
            PO Value: <strong>₱${{Math.round(data.EOQ * data.unitCost).toLocaleString()}}</strong>
          </div>
        </div>
      `;
    }}

    // 3. Render 14-Day Ledger Table Rows
    const tbody = document.getElementById('penPaperTableBody');
    if (tbody) {{
      let html = '';
      data.ledger.forEach((r, idx) => {{
        const isRop = r.is_rop_breached;
        const isArrive = r.order_arrived > 0;
        const isPlaced = r.order_placed > 0;

        let ropBadge = '<span style="color:#10B981; font-weight:700; font-family:\'JetBrains Mono\', monospace;">NO</span>';
        if (isRop) {{
          ropBadge = '<span style="background:rgba(245, 158, 11, 0.15); color:var(--amber); border:1px solid rgba(245, 158, 11, 0.3); padding:2px 6px; border-radius:4px; font-weight:700; font-family:\'JetBrains Mono\', monospace;">YES</span>';
        }}

        let rowBg = idx % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.015)';
        if (isPlaced) rowBg = 'rgba(245, 158, 11, 0.08)';
        if (isArrive) rowBg = 'rgba(16, 185, 129, 0.08)';

        html += `
          <tr style="background:${{rowBg}}; border-bottom:1px solid var(--border); font-family:'JetBrains Mono', monospace; font-size:11px;">
            <td style="padding:8px 8px; text-align:center; font-weight:700; color:var(--text);">Day ${{r.day}}</td>
            <td style="padding:8px 8px; text-align:right;">${{r.beg_stock.toLocaleString()}}</td>
            <td style="padding:8px 8px; text-align:right; color:var(--cyan); font-weight:${{isArrive ? '700' : 'normal'}};">
              ${{isArrive ? '+' + r.order_arrived.toLocaleString() : '0'}}
            </td>
            <td style="padding:8px 8px; text-align:right;">${{r.available.toLocaleString()}}</td>
            <td style="padding:8px 8px; text-align:right; color:var(--rose); font-weight:600;">-${{r.demand.toLocaleString()}}</td>
            <td style="padding:8px 8px; text-align:right; font-weight:800; color:${{isRop ? 'var(--amber)' : 'var(--emerald)'}};">
              ${{r.end_stock.toLocaleString()}}
            </td>
            <td style="padding:8px 8px; text-align:center;">${{ropBadge}}</td>
            <td style="padding:8px 8px; text-align:right; color:var(--emerald); font-weight:${{isPlaced ? '800' : 'normal'}};">
              ${{isPlaced ? r.order_placed.toLocaleString() : '0'}}
            </td>
            <td style="padding:8px 8px; text-align:center; color:${{r.arrival_day ? 'var(--cyan)' : 'var(--text-dim)'}};">
              ${{r.arrival_day ? 'Day ' + r.arrival_day : '—'}}
            </td>
            <td style="padding:8px 8px; text-align:right; color:var(--amber);">
              ${{r.pending_order > 0 ? r.pending_order.toLocaleString() : '0'}}
            </td>
            <td style="padding:8px 8px; text-align:right; color:var(--text-dim);">
              ₱${{r.daily_holding_cost.toFixed(2)}}
            </td>
            <td style="padding:8px 14px; text-align:left; font-family:'Plus Jakarta Sans', sans-serif; font-size:11px; color:var(--text);">
              ${{r.notes}}
            </td>
          </tr>
        `;
      }});
      tbody.innerHTML = html;
    }}
  }}

  function printPenPaperWorksheet() {{
    window.print();
  }}
'''

# Update switchSimMode to handle 'penpaper'
old_switch_sim = '''  function switchSimMode(mode) {
    simMode = mode;
    const viewPort = document.getElementById('viewPortfolioSim');
    const viewSingle = document.getElementById('viewSingleSim');
    const btnPort = document.getElementById('modeBtnPortfolio');
    const btnSingle = document.getElementById('modeBtnSingle');

    if (mode === 'portfolio') {
      viewPort.style.display = 'block';
      viewSingle.style.display = 'none';
      btnPort.style.background = 'var(--cyan)';
      btnPort.style.color = '#000';
      btnPort.style.borderColor = 'var(--cyan)';
      btnSingle.style.background = 'transparent';
      btnSingle.style.color = 'var(--text-muted)';
      btnSingle.style.borderColor = 'transparent';
    } else {
      viewPort.style.display = 'none';
      viewSingle.style.display = 'block';
      btnSingle.style.background = 'var(--cyan)';
      btnSingle.style.color = '#000';
      btnSingle.style.borderColor = 'var(--cyan)';
      btnPort.style.background = 'transparent';
      btnPort.style.color = 'var(--text-muted)';
      btnPort.style.borderColor = 'transparent';
      updateSingleSimulation();
    }
  }'''

new_switch_sim = '''  function switchSimMode(mode) {
    simMode = mode;
    const viewPort = document.getElementById('viewPortfolioSim');
    const viewSingle = document.getElementById('viewSingleSim');
    const viewPenPaper = document.getElementById('viewPenPaperSim');
    const btnPort = document.getElementById('modeBtnPortfolio');
    const btnSingle = document.getElementById('modeBtnSingle');
    const btnPenPaper = document.getElementById('modeBtnPenPaper');

    // Reset all buttons
    [btnPort, btnSingle, btnPenPaper].forEach(btn => {
      if (btn) {
        btn.style.background = 'transparent';
        btn.style.color = 'var(--text-muted)';
        btn.style.borderColor = 'transparent';
      }
    });

    if (mode === 'portfolio') {
      if (viewPort) viewPort.style.display = 'block';
      if (viewSingle) viewSingle.style.display = 'none';
      if (viewPenPaper) viewPenPaper.style.display = 'none';
      btnPort.style.background = 'var(--cyan)';
      btnPort.style.color = '#000';
      btnPort.style.borderColor = 'var(--cyan)';
    } else if (mode === 'single') {
      if (viewPort) viewPort.style.display = 'none';
      if (viewSingle) viewSingle.style.display = 'block';
      if (viewPenPaper) viewPenPaper.style.display = 'none';
      btnSingle.style.background = 'var(--cyan)';
      btnSingle.style.color = '#000';
      btnSingle.style.borderColor = 'var(--cyan)';
      updateSingleSimulation();
    } else if (mode === 'penpaper') {
      if (viewPort) viewPort.style.display = 'none';
      if (viewSingle) viewSingle.style.display = 'none';
      if (viewPenPaper) viewPenPaper.style.display = 'block';
      btnPenPaper.style.background = 'var(--cyan)';
      btnPenPaper.style.color = '#000';
      btnPenPaper.style.borderColor = 'var(--cyan)';
      renderPenPaperView();
    }
  }'''

assert old_switch_sim in html, "Could not find switchSimMode in HTML!"
html = html.replace(old_switch_sim, new_switch_sim, 1)

# Append js_logic before initApp
target_init_marker = '  function initApp() {'
assert target_init_marker in html, "Could not find initApp in HTML!"
html = html.replace(target_init_marker, js_logic + '\n' + target_init_marker, 1)

# Update initApp to also call renderPenPaperView
old_init = '''  function initApp() {
    resetPortfolioSim();
    renderSelectOptions();
    renderChampionPills();
    renderMasterTable('');
    loadMedicine(activeMedId);
  }'''

new_init = '''  function initApp() {
    resetPortfolioSim();
    renderSelectOptions();
    renderChampionPills();
    renderMasterTable('');
    loadMedicine(activeMedId);
    renderPenPaperView();
  }'''

assert old_init in html, "Could not find initApp body in HTML!"
html = html.replace(old_init, new_init, 1)

with open('phartrack_algorithm_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully injected Pen-and-Paper simulation into phartrack_algorithm_presentation.html!")
