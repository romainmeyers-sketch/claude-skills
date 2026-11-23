# Metis Framework Diagram Builders — SVG Code

All diagrams are built as **inline SVG** and dropped directly into the HTML page. Every diagram must include a `<text>` caption: `Source: Metis Strategy` (9px, var(--gray), centered below the diagram).

Use these generators as starting templates. Adjust labels, colors, and counts to match the specific framework being illustrated.

---

## Table of Contents

1. [Horizontal Maturity Ladder (5-level)](#1-horizontal-maturity-ladder-5-level)
2. [S-Curve / Growth Phase Flow](#2-s-curve--growth-phase-flow)
3. [2×2 Strategic Matrix](#3-22-strategic-matrix)
4. [Phase Flow / Roadmap (Horizontal)](#4-phase-flow--roadmap-horizontal)
5. [Layered Framework Table](#5-layered-framework-table)
6. [Cycle / Wheel Diagram](#6-cycle--wheel-diagram)
7. [Comparison Table (Side-by-Side)](#7-comparison-table-side-by-side)
8. [Stacked Bar / Investment Mix](#8-stacked-bar--investment-mix)
9. [Swimlane / Responsibility Matrix](#9-swimlane--responsibility-matrix)
10. [Design Guidelines](#10-design-guidelines)

---

## 1. Horizontal Maturity Ladder (5-level)

Classic left-to-right progression ladder. Numbers in dark-blue circles, connected by a line with an upward-arcing axis on the left. "Most Companies" label marks the typical position.

```svg
<svg width="1100" height="280" viewBox="0 0 1100 280" font-family="Open Sans, sans-serif">

  <!-- Value-Add axis arrow (left side, vertical) -->
  <line x1="40" y1="240" x2="40" y2="60" stroke="#20216f" stroke-width="2"/>
  <polygon points="40,52 35,66 45,66" fill="#20216f"/>
  <text x="36" y="155" text-anchor="middle" font-size="11" fill="#20216f" font-weight="600"
        transform="rotate(-90 36 155)">Value-Add</text>

  <!-- Baseline connector line -->
  <line x1="80" y1="200" x2="1060" y2="140" stroke="#c8cdd6" stroke-width="1.5" stroke-dasharray="6,4"/>

  <!-- Level data: cx, cy, number, title, bullets -->
  <!-- Level 1: Student -->
  <circle cx="160" cy="210" r="22" fill="#20216f"/>
  <text x="160" y="216" text-anchor="middle" font-size="16" font-weight="700" fill="white">1</text>
  <text x="160" y="248" text-anchor="middle" font-size="12" font-weight="700" fill="#20216f">Student</text>
  <text x="160" y="262" text-anchor="middle" font-size="9" fill="#7b8692">Awareness &amp; exploration</text>
  <text x="160" y="273" text-anchor="middle" font-size="9" fill="#7b8692">Ad hoc experiments</text>

  <!-- Level 2: Explorer -->
  <circle cx="330" cy="193" r="22" fill="#20216f"/>
  <text x="330" y="199" text-anchor="middle" font-size="16" font-weight="700" fill="white">2</text>
  <text x="330" y="231" text-anchor="middle" font-size="12" font-weight="700" fill="#20216f">Explorer</text>
  <text x="330" y="245" text-anchor="middle" font-size="9" fill="#7b8692">Targeted pilots</text>
  <text x="330" y="256" text-anchor="middle" font-size="9" fill="#7b8692">Limited governance</text>

  <!-- Level 3: Builder — "Most Companies" marker -->
  <circle cx="550" cy="173" r="22" fill="#20216f"/>
  <text x="550" y="179" text-anchor="middle" font-size="16" font-weight="700" fill="white">3</text>
  <text x="550" y="211" text-anchor="middle" font-size="12" font-weight="700" fill="#20216f">Builder</text>
  <text x="550" y="225" text-anchor="middle" font-size="9" fill="#7b8692">Platform foundations</text>
  <text x="550" y="236" text-anchor="middle" font-size="9" fill="#7b8692">Emerging operating model</text>
  <!-- "Most Companies" indicator -->
  <line x1="550" y1="148" x2="550" y2="100" stroke="#3cdbc0" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="550" y="94" text-anchor="middle" font-size="10" font-weight="600" fill="#3cdbc0">Most Companies</text>

  <!-- Level 4: Scaler -->
  <circle cx="770" cy="155" r="22" fill="#20216f"/>
  <text x="770" y="161" text-anchor="middle" font-size="16" font-weight="700" fill="white">4</text>
  <text x="770" y="193" text-anchor="middle" font-size="12" font-weight="700" fill="#20216f">Scaler</text>
  <text x="770" y="207" text-anchor="middle" font-size="9" fill="#7b8692">AI at scale across domains</text>
  <text x="770" y="218" text-anchor="middle" font-size="9" fill="#7b8692">Mature governance</text>

  <!-- Level 5: Commander -->
  <circle cx="990" cy="138" r="22" fill="#3cdbc0"/>
  <text x="990" y="144" text-anchor="middle" font-size="16" font-weight="700" fill="#20216f">5</text>
  <text x="990" y="176" text-anchor="middle" font-size="12" font-weight="700" fill="#20216f">Commander</text>
  <text x="990" y="190" text-anchor="middle" font-size="9" fill="#7b8692">AI-native operations</text>
  <text x="990" y="201" text-anchor="middle" font-size="9" fill="#7b8692">Continuous reinvention</text>

  <!-- Source caption -->
  <text x="550" y="278" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>

</svg>
```

---

## 2. S-Curve / Growth Phase Flow

Shows three phases of AI adoption along an S-curve: Explore, Build, Scale. Useful for investment thesis or maturity narrative pages.

```svg
<svg width="900" height="320" viewBox="0 0 900 320" font-family="Open Sans, sans-serif">

  <!-- Axes -->
  <line x1="60" y1="270" x2="860" y2="270" stroke="#c8cdd6" stroke-width="1.5"/>
  <line x1="60" y1="270" x2="60" y2="30"  stroke="#c8cdd6" stroke-width="1.5"/>
  <!-- Axis arrows -->
  <polygon points="860,270 848,264 848,276" fill="#c8cdd6"/>
  <polygon points="60,30 54,42 66,42"       fill="#c8cdd6"/>
  <!-- Axis labels -->
  <text x="460" y="295" text-anchor="middle" font-size="11" fill="#7b8692">Time / Investment</text>
  <text x="30"  y="155" text-anchor="middle" font-size="11" fill="#7b8692" transform="rotate(-90 30 155)">Business Value</text>

  <!-- S-curve path -->
  <path d="M80,258 C150,255 200,240 260,210 C320,178 350,140 420,100 C490,60 560,45 660,38 C760,32 820,32 860,30"
        fill="none" stroke="#20216f" stroke-width="3"/>

  <!-- Phase bands (vertical shaded regions) -->
  <rect x="60"  y="30" width="220" height="240" fill="#3cdbc0" opacity="0.08"/>
  <rect x="280" y="30" width="240" height="240" fill="#20216f" opacity="0.06"/>
  <rect x="520" y="30" width="340" height="240" fill="#3cdbc0" opacity="0.08"/>

  <!-- Phase labels -->
  <text x="170"  y="56" text-anchor="middle" font-size="13" font-weight="700" fill="#20216f">I. Explore</text>
  <text x="400"  y="56" text-anchor="middle" font-size="13" font-weight="700" fill="#20216f">II. Build</text>
  <text x="690"  y="56" text-anchor="middle" font-size="13" font-weight="700" fill="#20216f">III. Scale</text>

  <!-- Phase dividers -->
  <line x1="280" y1="30" x2="280" y2="270" stroke="#c8cdd6" stroke-width="1" stroke-dasharray="5,4"/>
  <line x1="520" y1="30" x2="520" y2="270" stroke="#c8cdd6" stroke-width="1" stroke-dasharray="5,4"/>

  <!-- Phase descriptors -->
  <text x="170" y="200" text-anchor="middle" font-size="9" fill="#7b8692">Pilot &amp; learn</text>
  <text x="170" y="213" text-anchor="middle" font-size="9" fill="#7b8692">Low cost, high optionality</text>
  <text x="400" y="170" text-anchor="middle" font-size="9" fill="#7b8692">Platform investment</text>
  <text x="400" y="183" text-anchor="middle" font-size="9" fill="#7b8692">Growing returns</text>
  <text x="690" y="130" text-anchor="middle" font-size="9" fill="#7b8692">Compounding value</text>
  <text x="690" y="143" text-anchor="middle" font-size="9" fill="#7b8692">AI-native operations</text>

  <!-- Source caption -->
  <text x="450" y="314" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>

</svg>
```

---

## 3. 2×2 Strategic Matrix

Classic quadrant matrix. Adjust axis labels and quadrant names for the specific framework. Dots can be added to position initiatives.

```svg
<svg width="680" height="600" viewBox="0 0 680 600" font-family="Open Sans, sans-serif">

  <!-- Quadrant fills -->
  <rect x="80"  y="40"  width="250" height="240" fill="#f4f6fa" rx="4"/>
  <rect x="350" y="40"  width="250" height="240" fill="#e8f8f5" rx="4"/>
  <rect x="80"  y="300" width="250" height="240" fill="#f4f6fa" rx="4"/>
  <rect x="350" y="300" width="250" height="240" fill="#20216f" rx="4"/>

  <!-- Grid lines -->
  <line x1="80"  y1="280" x2="600" y2="280" stroke="#c8cdd6" stroke-width="1.5"/>
  <line x1="340" y1="40"  x2="340" y2="540" stroke="#c8cdd6" stroke-width="1.5"/>

  <!-- Y-axis arrow + label -->
  <line x1="60" y1="540" x2="60" y2="30" stroke="#20216f" stroke-width="2"/>
  <polygon points="60,24 55,38 65,38" fill="#20216f"/>
  <text x="56" y="295" text-anchor="middle" font-size="12" font-weight="600" fill="#20216f"
        transform="rotate(-90 56 295)">Strategic Value →</text>

  <!-- X-axis arrow + label -->
  <line x1="80" y1="560" x2="610" y2="560" stroke="#20216f" stroke-width="2"/>
  <polygon points="616,560 602,554 602,566" fill="#20216f"/>
  <text x="345" y="585" text-anchor="middle" font-size="12" font-weight="600" fill="#20216f">Implementation Complexity →</text>

  <!-- Quadrant labels -->
  <!-- Top-left: Quick Wins -->
  <text x="205" y="130" text-anchor="middle" font-size="14" font-weight="700" fill="#20216f">Quick Wins</text>
  <text x="205" y="150" text-anchor="middle" font-size="10" fill="#7b8692">High value, low complexity</text>
  <text x="205" y="163" text-anchor="middle" font-size="10" fill="#7b8692">Pursue immediately</text>

  <!-- Top-right: Strategic Bets -->
  <text x="475" y="130" text-anchor="middle" font-size="14" font-weight="700" fill="#20216f">Strategic Bets</text>
  <text x="475" y="150" text-anchor="middle" font-size="10" fill="#20216f">High value, high complexity</text>
  <text x="475" y="163" text-anchor="middle" font-size="10" fill="#20216f">Invest &amp; plan carefully</text>

  <!-- Bottom-left: Low Priorities -->
  <text x="205" y="395" text-anchor="middle" font-size="14" font-weight="700" fill="#20216f">Low Priorities</text>
  <text x="205" y="415" text-anchor="middle" font-size="10" fill="#7b8692">Low value, low complexity</text>
  <text x="205" y="428" text-anchor="middle" font-size="10" fill="#7b8692">Automate or defer</text>

  <!-- Bottom-right: Hard Problems (dark navy) -->
  <text x="475" y="395" text-anchor="middle" font-size="14" font-weight="700" fill="#3cdbc0">Hard Problems</text>
  <text x="475" y="415" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.75)">Low value, high complexity</text>
  <text x="475" y="428" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.75)">Avoid or sunset</text>

  <!-- Example initiative dots (customize or remove) -->
  <circle cx="220" cy="180" r="8" fill="#20216f" opacity="0.7"/>
  <text x="234" y="184" font-size="9" fill="#20216f">Initiative A</text>
  <circle cx="430" cy="120" r="8" fill="#3cdbc0"/>
  <text x="444" y="124" font-size="9" fill="#20216f">Initiative B</text>

  <!-- Source caption -->
  <text x="340" y="598" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>

</svg>
```

---

## 4. Phase Flow / Roadmap (Horizontal)

Three to five phases in connected rounded boxes, with arrows between them. Good for operating model phases, transformation roadmaps.

```svg
<svg width="1100" height="200" viewBox="0 0 1100 200" font-family="Open Sans, sans-serif">

  <!-- Phase boxes (5 phases) -->
  <!-- Phase 1 -->
  <rect x="30"  y="50" width="180" height="100" rx="8" fill="#20216f"/>
  <text x="120" y="90"  text-anchor="middle" font-size="11" font-weight="700" fill="#3cdbc0">Phase 1</text>
  <text x="120" y="108" text-anchor="middle" font-size="13" font-weight="700" fill="white">Assess</text>
  <text x="120" y="125" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.7)">Baseline &amp; gap analysis</text>
  <text x="120" y="138" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.7)">6–8 weeks</text>

  <!-- Arrow 1→2 -->
  <polygon points="218,100 208,94 208,106" fill="#3cdbc0"/>
  <line x1="210" y1="100" x2="248" y2="100" stroke="#3cdbc0" stroke-width="2"/>

  <!-- Phase 2 -->
  <rect x="250" y="50" width="180" height="100" rx="8" fill="#20216f"/>
  <text x="340" y="90"  text-anchor="middle" font-size="11" font-weight="700" fill="#3cdbc0">Phase 2</text>
  <text x="340" y="108" text-anchor="middle" font-size="13" font-weight="700" fill="white">Design</text>
  <text x="340" y="125" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.7)">Architecture &amp; roadmap</text>
  <text x="340" y="138" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.7)">4–6 weeks</text>

  <!-- Arrow 2→3 -->
  <polygon points="438,100 428,94 428,106" fill="#3cdbc0"/>
  <line x1="430" y1="100" x2="468" y2="100" stroke="#3cdbc0" stroke-width="2"/>

  <!-- Phase 3 -->
  <rect x="470" y="50" width="180" height="100" rx="8" fill="#256ba2"/>
  <text x="560" y="90"  text-anchor="middle" font-size="11" font-weight="700" fill="#3cdbc0">Phase 3</text>
  <text x="560" y="108" text-anchor="middle" font-size="13" font-weight="700" fill="white">Build</text>
  <text x="560" y="125" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.7)">Platform &amp; MVP delivery</text>
  <text x="560" y="138" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.7)">12–16 weeks</text>

  <!-- Arrow 3→4 -->
  <polygon points="658,100 648,94 648,106" fill="#3cdbc0"/>
  <line x1="650" y1="100" x2="688" y2="100" stroke="#3cdbc0" stroke-width="2"/>

  <!-- Phase 4 -->
  <rect x="690" y="50" width="180" height="100" rx="8" fill="#256ba2"/>
  <text x="780" y="90"  text-anchor="middle" font-size="11" font-weight="700" fill="#3cdbc0">Phase 4</text>
  <text x="780" y="108" text-anchor="middle" font-size="13" font-weight="700" fill="white">Scale</text>
  <text x="780" y="125" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.7)">Expand across domains</text>
  <text x="780" y="138" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.7)">Ongoing</text>

  <!-- Arrow 4→5 -->
  <polygon points="878,100 868,94 868,106" fill="#3cdbc0"/>
  <line x1="870" y1="100" x2="908" y2="100" stroke="#3cdbc0" stroke-width="2"/>

  <!-- Phase 5 -->
  <rect x="910" y="50" width="180" height="100" rx="8" fill="#3cdbc0"/>
  <text x="1000" y="90"  text-anchor="middle" font-size="11" font-weight="700" fill="#20216f">Phase 5</text>
  <text x="1000" y="108" text-anchor="middle" font-size="13" font-weight="700" fill="#20216f">Optimize</text>
  <text x="1000" y="125" text-anchor="middle" font-size="9"  fill="#20216f">Continuous improvement</text>
  <text x="1000" y="138" text-anchor="middle" font-size="9"  fill="#20216f">AI-native operations</text>

  <!-- Source caption -->
  <text x="550" y="185" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>

</svg>
```

---

## 5. Layered Framework Table

Stacked horizontal bands, each representing a layer of a framework. Good for technology stack views, operating model layers, or capability maps.

```svg
<svg width="1000" height="340" viewBox="0 0 1000 340" font-family="Open Sans, sans-serif">

  <!-- Layer rows (5 layers) — adjust labels and counts as needed -->

  <!-- Layer 1: Strategy (dark blue) -->
  <rect x="0" y="0" width="1000" height="58" rx="0" fill="#20216f"/>
  <text x="20" y="23" font-size="10" font-weight="700" fill="#3cdbc0" letter-spacing="0.1em">LAYER 1</text>
  <text x="20" y="41" font-size="15" font-weight="700" fill="white">AI Strategy &amp; Vision</text>
  <text x="300" y="36" font-size="10" fill="rgba(255,255,255,0.7)">Business case  ·  Use case prioritization  ·  Investment thesis  ·  Executive alignment</text>

  <!-- Layer 2: Governance (medium blue) -->
  <rect x="0" y="62" width="1000" height="58" rx="0" fill="#256ba2"/>
  <text x="20" y="85" font-size="10" font-weight="700" fill="#3cdbc0" letter-spacing="0.1em">LAYER 2</text>
  <text x="20" y="103" font-size="15" font-weight="700" fill="white">Governance &amp; Risk</text>
  <text x="300" y="98" font-size="10" fill="rgba(255,255,255,0.7)">AI council  ·  Policy framework  ·  Ethics review  ·  Regulatory compliance  ·  Risk tiering</text>

  <!-- Layer 3: Operating Model (light blue / teal-light) -->
  <rect x="0" y="124" width="1000" height="58" rx="0" fill="#e8f8f5"/>
  <text x="20" y="147" font-size="10" font-weight="700" fill="#20216f" letter-spacing="0.1em">LAYER 3</text>
  <text x="20" y="165" font-size="15" font-weight="700" fill="#20216f">Operating Model</text>
  <text x="300" y="160" font-size="10" fill="#256ba2">Platform team  ·  Funding model  ·  Talent strategy  ·  Change management</text>

  <!-- Layer 4: Data (light bg) -->
  <rect x="0" y="186" width="1000" height="58" rx="0" fill="#f4f6fa"/>
  <text x="20" y="209" font-size="10" font-weight="700" fill="#20216f" letter-spacing="0.1em">LAYER 4</text>
  <text x="20" y="227" font-size="15" font-weight="700" fill="#20216f">Data Foundation</text>
  <text x="300" y="222" font-size="10" fill="#7b8692">Data quality  ·  Accessibility  ·  Lineage  ·  Feature stores  ·  Governance policies</text>

  <!-- Layer 5: Technology (white) -->
  <rect x="0" y="248" width="1000" height="58" rx="0" fill="white" stroke="#dde2ea" stroke-width="1"/>
  <text x="20" y="271" font-size="10" font-weight="700" fill="#20216f" letter-spacing="0.1em">LAYER 5</text>
  <text x="20" y="289" font-size="15" font-weight="700" fill="#20216f">Technology &amp; Infrastructure</text>
  <text x="300" y="284" font-size="10" fill="#7b8692">Model registry  ·  MLOps  ·  Compute  ·  API gateway  ·  Monitoring &amp; observability</text>

  <!-- Source caption -->
  <text x="500" y="330" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>

</svg>
```

---

## 6. Cycle / Wheel Diagram

Four-phase circular cycle. Useful for iterative processes: Build–Measure–Learn, Plan–Do–Check–Act, etc.

```svg
<svg width="560" height="560" viewBox="0 0 560 560" font-family="Open Sans, sans-serif">

  <!-- Center circle -->
  <circle cx="280" cy="280" r="60" fill="#20216f"/>
  <text x="280" y="273" text-anchor="middle" font-size="12" font-weight="700" fill="white">AI</text>
  <text x="280" y="290" text-anchor="middle" font-size="12" font-weight="700" fill="#3cdbc0">Cycle</text>

  <!-- Quarter arcs (donut segments) using paths -->
  <!-- Top-right: Phase 1 -->
  <path d="M280,280 L280,90 A190,190 0 0,1 470,280 Z" fill="#20216f" opacity="0.9"/>
  <text x="390" y="195" text-anchor="middle" font-size="13" font-weight="700" fill="white">1. Define</text>
  <text x="390" y="213" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.75)">Goals &amp; scope</text>

  <!-- Bottom-right: Phase 2 -->
  <path d="M280,280 L470,280 A190,190 0 0,1 280,470 Z" fill="#256ba2"/>
  <text x="390" y="375" text-anchor="middle" font-size="13" font-weight="700" fill="white">2. Build</text>
  <text x="390" y="393" text-anchor="middle" font-size="9"  fill="rgba(255,255,255,0.75)">Develop &amp; test</text>

  <!-- Bottom-left: Phase 3 -->
  <path d="M280,280 L280,470 A190,190 0 0,1 90,280 Z" fill="#3cdbc0"/>
  <text x="170" y="375" text-anchor="middle" font-size="13" font-weight="700" fill="#20216f">3. Deploy</text>
  <text x="170" y="393" text-anchor="middle" font-size="9"  fill="#20216f">Release &amp; monitor</text>

  <!-- Top-left: Phase 4 -->
  <path d="M280,280 L90,280 A190,190 0 0,1 280,90 Z" fill="#e8f8f5"/>
  <text x="170" y="195" text-anchor="middle" font-size="13" font-weight="700" fill="#20216f">4. Optimize</text>
  <text x="170" y="213" text-anchor="middle" font-size="9"  fill="#7b8692">Learn &amp; improve</text>

  <!-- Dividing lines -->
  <line x1="280" y1="90"  x2="280" y2="470" stroke="white" stroke-width="2"/>
  <line x1="90"  y1="280" x2="470" y2="280" stroke="white" stroke-width="2"/>

  <!-- Cycle arrows (curved, outside ring) — simplified as arc indicators -->
  <path d="M330,96 A190,190 0 0,1 464,230" fill="none" stroke="#3cdbc0" stroke-width="2.5" stroke-dasharray="6,4"/>
  <polygon points="464,230 458,218 470,222" fill="#3cdbc0"/>

  <!-- Source caption -->
  <text x="280" y="548" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>

</svg>
```

---

## 7. Comparison Table (Side-by-Side)

Two-column comparison: "Traditional Approach" vs "AI-Enabled Approach" (or any two states). Dark navy header row, alternating light rows.

```svg
<svg width="900" height="380" viewBox="0 0 900 380" font-family="Open Sans, sans-serif">

  <!-- Header row -->
  <rect x="0" y="0" width="900" height="48" fill="#20216f" rx="4 4 0 0"/>
  <text x="220" y="30" text-anchor="middle" font-size="13" font-weight="700" fill="white">Traditional Approach</text>
  <text x="680" y="30" text-anchor="middle" font-size="13" font-weight="700" fill="#3cdbc0">AI-Enabled Approach</text>
  <!-- Vertical divider -->
  <line x1="450" y1="0" x2="450" y2="380" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>

  <!-- Row data — alternate white / light-bg -->
  <!-- Row 1 (white) -->
  <rect x="0" y="48" width="900" height="52" fill="white"/>
  <text x="20" y="70" font-size="10" font-weight="700" fill="#20216f">Demand Forecasting</text>
  <text x="20" y="86" font-size="10" fill="#7b8692">Manual analysis, weekly cycles, 20–30% error rates</text>
  <text x="470" y="70" font-size="10" font-weight="700" fill="#20216f">Demand Forecasting</text>
  <text x="470" y="86" font-size="10" fill="#256ba2">Continuous ML models, &lt;5% error, real-time adjustment</text>
  <line x1="0" y1="100" x2="900" y2="100" stroke="#dde2ea" stroke-width="1"/>

  <!-- Row 2 (light bg) -->
  <rect x="0" y="100" width="900" height="52" fill="#f4f6fa"/>
  <text x="20" y="122" font-size="10" font-weight="700" fill="#20216f">Customer Service</text>
  <text x="20" y="138" font-size="10" fill="#7b8692">Tiered call centers, 48h resolution SLAs, high cost-per-contact</text>
  <text x="470" y="122" font-size="10" font-weight="700" fill="#20216f">Customer Service</text>
  <text x="470" y="138" font-size="10" fill="#256ba2">AI triage + human escalation, 80% deflection, same-day resolution</text>
  <line x1="0" y1="152" x2="900" y2="152" stroke="#dde2ea" stroke-width="1"/>

  <!-- Row 3 (white) -->
  <rect x="0" y="152" width="900" height="52" fill="white"/>
  <text x="20" y="174" font-size="10" font-weight="700" fill="#20216f">Software Development</text>
  <text x="20" y="190" font-size="10" fill="#7b8692">Manual code review, 2-week sprint cycles, individual productivity</text>
  <text x="470" y="174" font-size="10" font-weight="700" fill="#20216f">Software Development</text>
  <text x="470" y="190" font-size="10" fill="#256ba2">AI-assisted coding, 30–40% velocity increase, automated review</text>
  <line x1="0" y1="204" x2="900" y2="204" stroke="#dde2ea" stroke-width="1"/>

  <!-- Row 4 (light bg) -->
  <rect x="0" y="204" width="900" height="52" fill="#f4f6fa"/>
  <text x="20" y="226" font-size="10" font-weight="700" fill="#20216f">Risk &amp; Compliance</text>
  <text x="20" y="242" font-size="10" fill="#7b8692">Rule-based monitoring, batch reviews, reactive posture</text>
  <text x="470" y="226" font-size="10" font-weight="700" fill="#20216f">Risk &amp; Compliance</text>
  <text x="470" y="242" font-size="10" fill="#256ba2">Real-time anomaly detection, predictive flags, proactive response</text>
  <line x1="0" y1="256" x2="900" y2="256" stroke="#dde2ea" stroke-width="1"/>

  <!-- Row 5 (white) -->
  <rect x="0" y="256" width="900" height="52" fill="white"/>
  <text x="20" y="278" font-size="10" font-weight="700" fill="#20216f">Decision Making</text>
  <text x="20" y="294" font-size="10" fill="#7b8692">Quarterly reporting cycles, intuition-heavy executive decisions</text>
  <text x="470" y="278" font-size="10" font-weight="700" fill="#20216f">Decision Making</text>
  <text x="470" y="294" font-size="10" fill="#256ba2">Continuous data-driven insights, scenario modeling at speed</text>
  <line x1="0" y1="308" x2="900" y2="308" stroke="#dde2ea" stroke-width="1"/>

  <!-- Bottom border -->
  <rect x="0" y="308" width="900" height="4" fill="#20216f" rx="0 0 4 4"/>

  <!-- Source caption -->
  <text x="450" y="334" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>

</svg>
```

---

## 8. Stacked Bar / Investment Mix

Horizontal stacked bars showing portfolio allocation across investment tiers. Good for funding model or budget allocation pages.

```svg
<svg width="900" height="280" viewBox="0 0 900 280" font-family="Open Sans, sans-serif">

  <!-- Title -->
  <text x="450" y="24" text-anchor="middle" font-size="13" font-weight="700" fill="#20216f">Recommended AI Investment Mix by Maturity Stage</text>

  <!-- Row labels -->
  <text x="130" y="72"  text-anchor="end" font-size="11" fill="#20216f" font-weight="600">Explore</text>
  <text x="130" y="122" text-anchor="end" font-size="11" fill="#20216f" font-weight="600">Build</text>
  <text x="130" y="172" text-anchor="end" font-size="11" fill="#20216f" font-weight="600">Scale</text>

  <!-- Bar: Explore (60% run / 30% grow / 10% transform) -->
  <rect x="140" y="52" width="420" height="34" fill="#20216f" rx="2"/>
  <rect x="560" y="52" width="210" height="34" fill="#256ba2" rx="2"/>
  <rect x="770" y="52" width="70"  height="34" fill="#3cdbc0" rx="2"/>
  <text x="350" y="73" text-anchor="middle" font-size="10" fill="white">60% Run</text>
  <text x="665" y="73" text-anchor="middle" font-size="10" fill="white">30% Grow</text>
  <text x="805" y="73" text-anchor="middle" font-size="10" fill="#20216f" font-weight="700">10%</text>

  <!-- Bar: Build (45% run / 35% grow / 20% transform) -->
  <rect x="140" y="102" width="315" height="34" fill="#20216f" rx="2"/>
  <rect x="455" y="102" width="245" height="34" fill="#256ba2" rx="2"/>
  <rect x="700" y="102" width="140" height="34" fill="#3cdbc0" rx="2"/>
  <text x="297" y="123" text-anchor="middle" font-size="10" fill="white">45% Run</text>
  <text x="577" y="123" text-anchor="middle" font-size="10" fill="white">35% Grow</text>
  <text x="770" y="123" text-anchor="middle" font-size="10" fill="#20216f" font-weight="700">20%</text>

  <!-- Bar: Scale (30% run / 35% grow / 35% transform) -->
  <rect x="140" y="152" width="210" height="34" fill="#20216f" rx="2"/>
  <rect x="350" y="152" width="245" height="34" fill="#256ba2" rx="2"/>
  <rect x="595" y="152" width="245" height="34" fill="#3cdbc0" rx="2"/>
  <text x="245" y="173" text-anchor="middle" font-size="10" fill="white">30% Run</text>
  <text x="472" y="173" text-anchor="middle" font-size="10" fill="white">35% Grow</text>
  <text x="717" y="173" text-anchor="middle" font-size="10" fill="#20216f" font-weight="700">35% Transform</text>

  <!-- Legend -->
  <rect x="250" y="216" width="14" height="14" fill="#20216f"/>
  <text x="270" y="227" font-size="10" fill="#20216f">Run (keep lights on)</text>
  <rect x="430" y="216" width="14" height="14" fill="#256ba2"/>
  <text x="450" y="227" font-size="10" fill="#20216f">Grow (enhance &amp; extend)</text>
  <rect x="640" y="216" width="14" height="14" fill="#3cdbc0"/>
  <text x="660" y="227" font-size="10" fill="#20216f">Transform (net-new)</text>

  <!-- Source caption -->
  <text x="450" y="258" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>

</svg>
```

---

## 9. Swimlane / Responsibility Matrix

Shows which group (rows) owns which activities (columns) in a process. Use for operating model, RACI, or phase-by-role views.

```svg
<svg width="1000" height="360" viewBox="0 0 1000 360" font-family="Open Sans, sans-serif">

  <!-- Header row -->
  <rect x="0" y="0" width="1000" height="44" fill="#20216f"/>
  <text x="110" y="26" text-anchor="middle" font-size="10" font-weight="700" fill="rgba(255,255,255,0.5)">ROLE</text>
  <!-- Column headers -->
  <text x="290"  y="26" text-anchor="middle" font-size="11" font-weight="700" fill="white">Strategy &amp; Funding</text>
  <text x="470"  y="26" text-anchor="middle" font-size="11" font-weight="700" fill="white">Build &amp; Deliver</text>
  <text x="650"  y="26" text-anchor="middle" font-size="11" font-weight="700" fill="white">Govern &amp; Risk</text>
  <text x="860"  y="26" text-anchor="middle" font-size="11" font-weight="700" fill="white">Measure &amp; Optimize</text>
  <!-- Column lines -->
  <line x1="220" y1="0" x2="220" y2="360" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
  <line x1="400" y1="0" x2="400" y2="360" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
  <line x1="580" y1="0" x2="580" y2="360" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
  <line x1="760" y1="0" x2="760" y2="360" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>

  <!-- Swimlane rows -->
  <!-- CIO/CTO row -->
  <rect x="0" y="44" width="1000" height="52" fill="#f4f6fa"/>
  <text x="110" y="66" text-anchor="middle" font-size="11" font-weight="700" fill="#20216f">CIO / CTO</text>
  <text x="290"  y="66" text-anchor="middle" font-size="9" fill="#20216f">●● Approves AI investment portfolio</text>
  <text x="290"  y="80" text-anchor="middle" font-size="9" fill="#7b8692">Sets AI vision &amp; priorities</text>
  <text x="470"  y="70" text-anchor="middle" font-size="9" fill="#7b8692">Sponsors platform team</text>
  <text x="650"  y="70" text-anchor="middle" font-size="9" fill="#20216f">●● Chairs AI governance council</text>
  <text x="860"  y="70" text-anchor="middle" font-size="9" fill="#7b8692">Reviews OKRs quarterly</text>
  <line x1="0" y1="96" x2="1000" y2="96" stroke="#dde2ea" stroke-width="1"/>

  <!-- Platform Team row -->
  <rect x="0" y="96" width="1000" height="52" fill="white"/>
  <text x="110" y="118" text-anchor="middle" font-size="11" font-weight="700" fill="#20216f">Platform Team</text>
  <text x="290"  y="118" text-anchor="middle" font-size="9" fill="#7b8692">Provides cost transparency</text>
  <text x="470"  y="118" text-anchor="middle" font-size="9" fill="#20216f">●● Builds &amp; operates AI platform</text>
  <text x="470"  y="132" text-anchor="middle" font-size="9" fill="#7b8692">Owns MLOps &amp; model registry</text>
  <text x="650"  y="118" text-anchor="middle" font-size="9" fill="#7b8692">Enforces data &amp; model policies</text>
  <text x="860"  y="118" text-anchor="middle" font-size="9" fill="#20216f">●● Monitors model performance</text>
  <line x1="0" y1="148" x2="1000" y2="148" stroke="#dde2ea" stroke-width="1"/>

  <!-- Product Teams row -->
  <rect x="0" y="148" width="1000" height="52" fill="#f4f6fa"/>
  <text x="110" y="170" text-anchor="middle" font-size="11" font-weight="700" fill="#20216f">Product Teams</text>
  <text x="290"  y="170" text-anchor="middle" font-size="9" fill="#20216f">●● Submits use cases for funding</text>
  <text x="470"  y="170" text-anchor="middle" font-size="9" fill="#20216f">●● Builds AI features on platform</text>
  <text x="650"  y="170" text-anchor="middle" font-size="9" fill="#7b8692">Participates in risk reviews</text>
  <text x="860"  y="170" text-anchor="middle" font-size="9" fill="#20216f">●● Defines &amp; tracks KPIs</text>
  <line x1="0" y1="200" x2="1000" y2="200" stroke="#dde2ea" stroke-width="1"/>

  <!-- Data &amp; Analytics row -->
  <rect x="0" y="200" width="1000" height="52" fill="white"/>
  <text x="110" y="222" text-anchor="middle" font-size="11" font-weight="700" fill="#20216f">Data &amp; Analytics</text>
  <text x="290"  y="222" text-anchor="middle" font-size="9" fill="#7b8692">Advises on data feasibility</text>
  <text x="470"  y="222" text-anchor="middle" font-size="9" fill="#20216f">●● Owns data pipelines &amp; quality</text>
  <text x="650"  y="222" text-anchor="middle" font-size="9" fill="#20216f">●● Manages data governance</text>
  <text x="860"  y="222" text-anchor="middle" font-size="9" fill="#7b8692">Supplies reporting data</text>
  <line x1="0" y1="252" x2="1000" y2="252" stroke="#dde2ea" stroke-width="1"/>

  <!-- Legal / Risk row -->
  <rect x="0" y="252" width="1000" height="52" fill="#f4f6fa"/>
  <text x="110" y="274" text-anchor="middle" font-size="11" font-weight="700" fill="#20216f">Legal / Risk</text>
  <text x="290"  y="274" text-anchor="middle" font-size="9" fill="#7b8692">Reviews funding structures</text>
  <text x="470"  y="274" text-anchor="middle" font-size="9" fill="#7b8692">Reviews model contracts</text>
  <text x="650"  y="274" text-anchor="middle" font-size="9" fill="#20216f">●● Owns compliance &amp; ethics policy</text>
  <text x="860"  y="274" text-anchor="middle" font-size="9" fill="#7b8692">Reviews audit reports</text>
  <line x1="0" y1="304" x2="1000" y2="304" stroke="#dde2ea" stroke-width="1"/>

  <!-- Legend -->
  <text x="20" y="326" font-size="9" font-weight="700" fill="#20216f">●●</text>
  <text x="36" y="326" font-size="9" fill="#7b8692">= Primary owner</text>

  <!-- Source caption -->
  <text x="500" y="350" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>

</svg>
```

---

## 10. Design Guidelines

### Color usage in diagrams
- **Dark blue `#20216f`** — primary bars, dominant shapes, axis lines
- **Teal `#3cdbc0`** — highlights, top-level achievements, accent shapes
- **Medium blue `#256ba2`** — secondary bars, mid-tier items
- **Gray `#7b8692`** — labels, captions, supporting text
- **Light bg `#f4f6fa`** — alternating row fills, background fields
- **Teal light `#e8f8f5`** — callout fills, selected state

### Sizing guidelines (landscape whitepaper)
- **Full-page diagram**: 1100px wide × 320–380px tall — fits below a 6-line header with room for the footer
- **Half-page diagram** (beside text): 480–520px wide × 260–320px tall
- **Inline diagram** (within text column): 420px wide × 200px tall

### Required caption
Every diagram must include exactly this line immediately below:
```
<text x="[center-x]" y="[bottom+14]" text-anchor="middle" font-size="9" fill="#7b8692">Source: Metis Strategy</text>
```

### Accessibility note
All SVG text must be actual `<text>` elements (not paths), so the PDF renderer can use the Open Sans font loaded via Google Fonts in the HTML `<head>`. Never convert diagram text to outlines.
