# Timesaver Visual Library — Index

The Metis Timesaver deck is the **canonical library of slide structures** — 260 pre-designed layouts that span every chart type, framework, and narrative arc Metis Strategy uses. This is one of the two co-equal design paths in `metis-pptx` (see SKILL.md §0.6).

**Source pptx:** `G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\Metis_Timesaver Slides.pptx`

**Rendered PNG previews:**

`${CLAUDE_PLUGIN_ROOT}/brand-assets/timesaver_pngs/slide-{N}.png` when installed inside the `metis-skills` plugin, else `G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\timesaver_pngs\slide-{N}.png` on a Metis machine. Resolve programmatically via `scripts/resolve_assets.py` (key `timesaver_pngs`) rather than hardcoding either path.

Every Metis machine has the G:\ drive mapped, so the path resolves identically for everyone — no per-user setup, rendering, or caching required.

---

## How to use this index

When designing a content slide via Path B (see SKILL.md §0.6 for routing rules):

1. **Scan this index.** Find the row whose **"Use when..."** matches the thought you want to express.
2. **Load 2-4 candidate previews** from the shared-drive path above using the multimodal Read tool.
3. **Pick the winner.** Reproduce the layout in python-pptx using brand tokens from `metis-brand.md`.

Do NOT default to "title + bullets in boxes" when the thought has a structural metaphor. Pick the **shape that expresses the thought** first; the text comes second.

---

## Categories at a glance

| Slide range | Category |
|---|---|
| 2-9 | Structural — covers, dividers, content layouts |
| 10-45 | Text-based — exec summaries, statements, quotes, lists |
| 46-52 | Bar charts |
| 53-70 | Column charts |
| 71-81 | Line charts |
| 82-91 | Pie / Doughnut / Harvey Ball / Wheel |
| 92-95 | Area charts |
| 96-102 | Scatter / Radar / Bubble |
| 103-143 | Workplan & process — flows, timelines, journeys, decision trees, gantt |
| 144-154 | Organization & relationships — org charts, networks, matrices |
| 155-188 | Concept slides — metaphors (house, hex, pyramid, triangle, funnel, gears, venn, ladder, etc.) |
| 189-193 | Map slides — geographic + heat |
| 194-214 | Consulting frameworks — Porter, McKinsey, BCG, PESTEL, etc. |
| 215-217 | Additional / data charts |
| 218-260 | Executive Summary structures — narrative arcs (SBAR, vision-strategy-action, etc.) |

---

## Structural — covers, dividers, content layouts

| # | Title | Use when... | Preview |
|---|---|---|---|
| 2 | Section Divider | You need a visual divider between major sections of the deck | `slide-2.png` |
| 3 | Table of Contents | You need a table of contents — 4-6 major topics with page references | `slide-3.png` |
| 4 | Elements | You need: Elements | `slide-4.png` |
| 5 | Elements | You need: Elements | `slide-5.png` |
| 7 | Reference page for theme accent colors | You need: Reference page for theme accent colors | `slide-7.png` |
| 8 | Content slide | You need: Content slide | `slide-8.png` |

## Text-based — exec summaries, statements, quotes, lists

| # | Title | Use when... | Preview |
|---|---|---|---|
| 10 | Executive Summary 1 | You need an executive summary with a single-image hero + 3 takeaways | `slide-10.png` |
| 11 | Executive Summary 2 | You need an executive summary with multiple highlight callouts | `slide-11.png` |
| 12 | Executive Summary 3 | You need an executive summary with 3 horizontal bands of takeaways | `slide-12.png` |
| 13 | Executive Summary 4 | You need an executive summary with 4 quadrant takeaways | `slide-13.png` |
| 14 | Executive Summary 5 | You need an executive summary structured as left-narrative + right-supporting cards | `slide-14.png` |
| 15 | Executive Summary 6 | You need: Executive Summary 6 | `slide-15.png` |
| 16 | Executive Summary 7 | You need: Executive Summary 7 | `slide-16.png` |
| 17 | Description slide | You need a description slide — long-form narrative w/ supporting visual | `slide-17.png` |
| 18 | Description slide | You need: Description slide | `slide-18.png` |
| 19 | Description slide | You need: Description slide | `slide-19.png` |
| 20 | Description slide | You need: Description slide | `slide-20.png` |
| 21 | Description Slide | You need: Description Slide | `slide-21.png` |
| 22 | Statements | You need to make 3-5 bold statements with supporting one-liners | `slide-22.png` |
| 23 | Four categories | You need to lay out 4 categories side-by-side with equal weight | `slide-23.png` |
| 24 | Table of words | You need a table of words/concepts (no numbers) | `slide-24.png` |
| 25 | Table | You need a structured data table | `slide-25.png` |
| 26 | Table | You need: Table | `slide-26.png` |
| 27 | Features List | You need a features list — bulleted catalog of capabilities | `slide-27.png` |
| 28 | A - Quote | You want to feature a single executive quote with attribution | `slide-28.png` |
| 29 | B - Quote | You want to feature a paired quote (two speakers) | `slide-29.png` |
| 30 | C- Quote | You want to feature 3 quotes side-by-side (3 speakers / 3 perspectives) | `slide-30.png` |
| 31 | D- Quote | You want to feature 4 stacked quotes | `slide-31.png` |
| 32 | E- Quote | You want to feature a quote with extended commentary | `slide-32.png` |
| 33 | Key points diagram | You need to show a key-points diagram with linked items | `slide-33.png` |
| 34 | A - SWOT Analysis | You need a SWOT analysis (Strengths/Weaknesses/Opportunities/Threats) | `slide-34.png` |
| 35 | B- SWOT Analysis | You need a SWOT variant with a different visual emphasis | `slide-35.png` |
| 36 | Checklist | You need a checklist of action items or criteria | `slide-36.png` |
| 37 | Problem-Solving Process Checklist | You need: Problem-Solving Process Checklist | `slide-37.png` |
| 38 | Problem Definition Worksheet | You need to define a problem clearly — structured worksheet | `slide-38.png` |
| 39 | Problem Statement | You need: Problem Statement | `slide-39.png` |
| 40 | A - Stakeholder Analysis | You need to map stakeholders by interest/influence | `slide-40.png` |
| 41 | B - Stakeholder Analysis | You need: B - Stakeholder Analysis | `slide-41.png` |
| 42 | A - Statistics table | You need: A - Statistics table | `slide-42.png` |
| 43 | B - Statistics table | You need: B - Statistics table | `slide-43.png` |
| 44 | Word cloud | You need a word cloud — frequency-weighted text visualization | `slide-44.png` |

## Bar charts

| # | Title | Use when... | Preview |
|---|---|---|---|
| 46 | Simple bar chart | You need a simple horizontal bar chart | `slide-46.png` |
| 47 | Stacked bar chart | You need: Stacked bar chart | `slide-47.png` |
| 48 | 100% Stacked bar chart | You need: 100% Stacked bar chart | `slide-48.png` |
| 49 | Clustered bar chart | You need: Clustered bar chart | `slide-49.png` |
| 50 | Waterfall bar chart | You need a waterfall chart — incremental contributions to a total | `slide-50.png` |
| 51 | Bar chart with words | You need to show categorical magnitudes with descriptive labels (no axes) | `slide-51.png` |

## Column charts

| # | Title | Use when... | Preview |
|---|---|---|---|
| 53 | Simple column chart | You need a simple vertical column chart | `slide-53.png` |
| 54 | Stacked column chart | You need to show parts of a whole over time (stacked columns) | `slide-54.png` |
| 55 | 100% stacked column chart | You need: 100% stacked column chart | `slide-55.png` |
| 56 | Clustered column chart | You need: Clustered column chart | `slide-56.png` |
| 57 | Waterfall column chart | You need: Waterfall column chart | `slide-57.png` |
| 58 | Vertical dot chart | You need: Vertical dot chart | `slide-58.png` |
| 59 | Grouped column chart | You need: Grouped column chart | `slide-59.png` |
| 60 | Multiple column chart | You need: Multiple column chart | `slide-60.png` |
| 61 | Pyramid column chart | You need: Pyramid column chart | `slide-61.png` |
| 62 | Combination chart | You need: Combination chart | `slide-62.png` |
| 63 | Mekko chart | You need a Marimekko chart — 2D area showing share + magnitude | `slide-63.png` |
| 64 | Histogram | You need a histogram — distribution of values across bins | `slide-64.png` |
| 65 | Density chart | You need: Density chart | `slide-65.png` |
| 66 | Population pyramid | You need a population pyramid — two-sided horizontal bars | `slide-66.png` |
| 67 | Percentage breakdown | You need: Percentage breakdown | `slide-67.png` |
| 68 | Heat map | You need a heat map — color-coded grid of values | `slide-68.png` |
| 69 | Heat map (with numbers) | You need: Heat map (with numbers) | `slide-69.png` |

## Line charts

| # | Title | Use when... | Preview |
|---|---|---|---|
| 71 | Line chart | You need a simple line chart over time | `slide-71.png` |
| 72 | Vertical Line chart | You need: Vertical Line chart | `slide-72.png` |
| 73 | Multiple Line chart | You need: Multiple Line chart | `slide-73.png` |
| 74 | Data over time line chart | You need to show data evolution over a long time horizon | `slide-74.png` |
| 75 | Growth curve line chart Line chart | You need a growth curve — typical S-curve adoption shape | `slide-75.png` |
| 76 | Product Life Cycle | You need: Product Life Cycle | `slide-76.png` |
| 77 | Peak line chart | You need a peak chart — single spike or peak event | `slide-77.png` |
| 78 | Arrow line chart | You need: Arrow line chart | `slide-78.png` |
| 79 | Evolution Chart | You need: Evolution Chart | `slide-79.png` |
| 80 | Radial chart | You need: Radial chart | `slide-80.png` |

## Pie / Doughnut / Harvey Ball / Wheel

| # | Title | Use when... | Preview |
|---|---|---|---|
| 82 | Pie chart | You need a pie chart for a simple part-to-whole breakdown | `slide-82.png` |
| 83 | Doughnut chart | You need a doughnut chart with a center number callout | `slide-83.png` |
| 84 | Multiple Doughnuts | You need: Multiple Doughnuts | `slide-84.png` |
| 85 | Multiple Doughnuts | You need: Multiple Doughnuts | `slide-85.png` |
| 86 | Harvey Ball Slide | You need Harvey Balls — capability or maturity ratings (empty/quarter/half/etc.) | `slide-86.png` |
| 87 | Harvey Ball Slide | You need: Harvey Ball Slide | `slide-87.png` |
| 88 | Harvey Ball Slide | You need: Harvey Ball Slide | `slide-88.png` |
| 89 | Harvey Ball Map Slide | You need: Harvey Ball Map Slide | `slide-89.png` |
| 90 | Wheel chart | You need a wheel chart — radial proportion visualization | `slide-90.png` |

## Area charts

| # | Title | Use when... | Preview |
|---|---|---|---|
| 92 | Simple area chart | You need: Simple area chart | `slide-92.png` |
| 93 | Proportional area chart | You need: Proportional area chart | `slide-93.png` |
| 94 | Rectangle area chart | You need: Rectangle area chart | `slide-94.png` |

## Scatter / Radar / Bubble

| # | Title | Use when... | Preview |
|---|---|---|---|
| 96 | Dot Matrix chart | You need: Dot Matrix chart | `slide-96.png` |
| 97 | Radar chart | You need: Radar chart | `slide-97.png` |
| 98 | Scatter chart | You need: Scatter chart | `slide-98.png` |
| 99 | Scatter chart with four quadrants | You need: Scatter chart with four quadrants | `slide-99.png` |
| 100 | Scatter chart with segmentation | You need: Scatter chart with segmentation | `slide-100.png` |
| 101 | XY Bubble chart | You need: XY Bubble chart | `slide-101.png` |

## Workplan & process — flows, timelines, journeys, decision trees, gantt

| # | Title | Use when... | Preview |
|---|---|---|---|
| 103 | Flow chart | You need a flow chart with decision diamonds | `slide-103.png` |
| 104 | Repeating process | You need a repeating loop process | `slide-104.png` |
| 105 | Timeline | You need a horizontal timeline with milestones | `slide-105.png` |
| 106 | Timeline | You need: Timeline | `slide-106.png` |
| 107 | Boat chart | You need: Boat chart | `slide-107.png` |
| 108 | Boat chart | You need: Boat chart | `slide-108.png` |
| 109 | Boat chart vertical | You need: Boat chart vertical | `slide-109.png` |
| 110 | From-to chart | You need: From-to chart | `slide-110.png` |
| 111 | Circular process | You need a circular process — continuous loop | `slide-111.png` |
| 112 | Circular process | You need: Circular process | `slide-112.png` |
| 113 | Journey Slide | You need a customer journey across stages | `slide-113.png` |
| 114 | Linear Process | You need a linear process (3-7 steps) | `slide-114.png` |
| 115 | Linear Process | You need: Linear Process | `slide-115.png` |
| 116 | Snake process | You need a snake/zigzag process for many steps | `slide-116.png` |
| 117 | Go-To-Market Slide | You need a go-to-market multi-stage plan | `slide-117.png` |
| 118 | Project timeline | You need a project timeline with deliverables | `slide-118.png` |
| 119 | Customer Touchpoints | You need to show customer touchpoints across journey | `slide-119.png` |
| 120 | Customer Phases | You need to show customer phases / lifecycle | `slide-120.png` |
| 121 | Hype Cycle | You need to show a hype cycle (Gartner-style) | `slide-121.png` |
| 122 | Business workflow | You need to show a business workflow with multiple lanes | `slide-122.png` |
| 123 | Circular process | You need: Circular process | `slide-123.png` |
| 124 | Road flow chart | You need: Road flow chart | `slide-124.png` |
| 125 | Plans vs. actual chart | You need: Plans vs. actual chart | `slide-125.png` |
| 126 | Forecast chart | You need: Forecast chart | `slide-126.png` |
| 127 | Steps chart | You need to show ascending steps to a goal | `slide-127.png` |
| 128 | Phases chart | You need to show distinct phases of a transformation | `slide-128.png` |
| 129 | Strategy chart | You need: Strategy chart | `slide-129.png` |
| 130 | Decision tree | You need a decision tree — branching logic with terminal outcomes | `slide-130.png` |
| 131 | Decision Tree | You need: Decision Tree | `slide-131.png` |
| 132 | Decision Tree | You need: Decision Tree | `slide-132.png` |
| 133 | Hypothesis Tree | You need a hypothesis tree — root question splitting into sub-hypotheses | `slide-133.png` |
| 134 | Issue Tree | You need an issue tree — top-down problem decomposition | `slide-134.png` |
| 135 | Gantt chart | You need a Gantt chart — tasks across time with bars | `slide-135.png` |
| 136 | Plan Analyses | You need: Plan Analyses | `slide-136.png` |
| 137 | Analysis Plan | You need: Analysis Plan | `slide-137.png` |
| 138 | High-level Workplan | You need a high-level workplan with phases and deliverables | `slide-138.png` |
| 139 | 5-Week Workplan | You need a 5-week / multi-week workplan | `slide-139.png` |
| 140 | One-Week Workplan | You need a one-week sprint workplan | `slide-140.png` |
| 141 | Image timeline | You need: Image timeline | `slide-141.png` |
| 142 | Inflow and outflow | You need to show flows in and out of a system (Sankey-lite) | `slide-142.png` |

## Organization & relationships — org charts, networks, matrices

| # | Title | Use when... | Preview |
|---|---|---|---|
| 144 | Organizational chart | You need an organizational chart | `slide-144.png` |
| 145 | Hierarchy Infographic | You need a hierarchy infographic (icon-driven) | `slide-145.png` |
| 146 | Business systems/hierarchy | You need: Business systems/hierarchy | `slide-146.png` |
| 147 | Many-to-one chart | You need to show many sources flowing to one destination | `slide-147.png` |
| 148 | Rank chart | You need to rank items by score / importance | `slide-148.png` |
| 149 | Comparative table | You need a comparative table across 3+ options | `slide-149.png` |
| 150 | Network analysis | You need to show two networks/clusters side-by-side | `slide-150.png` |
| 151 | 2x2 Matrix | You need a 2x2 matrix (e.g., importance/urgency) | `slide-151.png` |
| 152 | 3x2 Matrix | You need a 3x2 matrix | `slide-152.png` |
| 153 | 3x3 Matrix | You need a 3x3 matrix | `slide-153.png` |

## Concept slides — metaphors (house, hex, pyramid, triangle, funnel, gears, venn, ladder, etc.)

| # | Title | Use when... | Preview |
|---|---|---|---|
| 155 | Honeycomb chart | You have 6 reinforcing capabilities/items + descriptions on each side — HEXAGON FLYWHEEL | `slide-155.png` |
| 156 | Hexagon concept | You have 6 capabilities radiating from a center — HEXAGON CONCEPT | `slide-156.png` |
| 157 | Pentagon concept | You have 5 connected concepts — PENTAGON | `slide-157.png` |
| 158 | Four categories | You have 4 categories with equal visual weight | `slide-158.png` |
| 159 | Pyramid concept | You have a hierarchy with broad base narrowing to a peak — PYRAMID | `slide-159.png` |
| 160 | A - Triangle concept | You have 3 elements forming a unified whole — TRIANGLE CONCEPT (A) | `slide-160.png` |
| 161 | B - Triangle concept | You have 3 elements with one nested inside — TRIANGLE CONCEPT (B) | `slide-161.png` |
| 162 | Challenges Slide | You need to show challenges only (no solutions yet) | `slide-162.png` |
| 163 | Challenges and solutions | You need to pair challenges with solutions side-by-side | `slide-163.png` |
| 164 | Decision Diagram | You need: Decision Diagram | `slide-164.png` |
| 165 | Decision Diagram | You need: Decision Diagram | `slide-165.png` |
| 166 | Tree diagram | You need: Tree diagram | `slide-166.png` |
| 167 | Funnel chart | You need a funnel — narrowing stages from broad input to narrow output | `slide-167.png` |
| 168 | Funnel chart | You need: Funnel chart | `slide-168.png` |
| 169 | Open book slide | You need an "open book" metaphor — two-page spread for paired content | `slide-169.png` |
| 170 | Mind map | You need a mind map radiating from a central concept | `slide-170.png` |
| 171 | Sankey diagram | You need a Sankey diagram — flow magnitudes between categories | `slide-171.png` |
| 172 | Kagi chart | You need: Kagi chart | `slide-172.png` |
| 173 | Ladder chart | You need a ladder — sequential climbing steps (e.g., maturity) | `slide-173.png` |
| 174 | Questions chart | You need to pose a series of questions for the audience | `slide-174.png` |
| 175 | Comparison chart #1 | You need a side-by-side comparison (variant 1) | `slide-175.png` |
| 176 | Comparison chart #2 | You need a side-by-side comparison (variant 2) | `slide-176.png` |
| 177 | Gears chart | You need a "gears" metaphor — interlocking moving parts | `slide-177.png` |
| 178 | Semicircle chart | You need a semicircle progression (half-pie / dial) | `slide-178.png` |
| 179 | House chart | You have layered architecture (foundation -> body -> roof) + 4 pillar items + sidebar — HOUSE CHART | `slide-179.png` |
| 180 | Venn Diagram | You need a Venn diagram — overlap of 2-3 sets | `slide-180.png` |
| 181 | Circle diagram | You need: Circle diagram | `slide-181.png` |
| 182 | Circle diagram with segmentation | You need: Circle diagram with segmentation | `slide-182.png` |
| 183 | Bull-s eye diagram | You need a bullseye — concentric rings of priority/scope | `slide-183.png` |
| 184 | Balance Scale Diagram | You need a balance scale — trade-off between two options | `slide-184.png` |
| 185 | Level diagram | You need a level / tier diagram — discrete graduated levels | `slide-185.png` |
| 186 | Two axis diagram | You need: Two axis diagram | `slide-186.png` |
| 187 | Three axis diagram | You need: Three axis diagram | `slide-187.png` |

## Map slides — geographic + heat

| # | Title | Use when... | Preview |
|---|---|---|---|
| 189 | Maps showing data | You need a geographic map with data overlays | `slide-189.png` |
| 190 | Flow map | You need a flow map — directional arrows between locations | `slide-190.png` |
| 191 | Bubble map | You need a bubble map — sized markers on locations | `slide-191.png` |
| 192 | Choropleth map | You need a choropleth map — color-coded regions | `slide-192.png` |

## Consulting frameworks — Porter, McKinsey, BCG, PESTEL, etc.

| # | Title | Use when... | Preview |
|---|---|---|---|
| 194 | Porter-s Five Forces | Porter's Five Forces — industry structure analysis | `slide-194.png` |
| 195 | Porter's Value Chain | Porter's Value Chain — primary + support activities | `slide-195.png` |
| 196 | Porter's Generic Strategies | Porter's Generic Strategies — cost / differentiation / focus | `slide-196.png` |
| 197 | BCG Growth Share Matrix | BCG Growth-Share Matrix — Stars / Cash Cows / Question Marks / Dogs | `slide-197.png` |
| 198 | GE McKinsey Matrix | GE-McKinsey 9-box Matrix — industry attractiveness vs. business strength | `slide-198.png` |
| 199 | Ansoff Matrix | Ansoff Matrix — product/market growth options | `slide-199.png` |
| 200 | McKinsey 7-S Framework | McKinsey 7-S Framework — 7 organizational dimensions around shared values | `slide-200.png` |
| 201 | The 3 C-s | The 3 Cs — Customer / Company / Competitor | `slide-201.png` |
| 202 | The 4 Ps | The 4 Ps — Product / Price / Place / Promotion | `slide-202.png` |
| 203 | Force Field Analysis | You need: Force Field Analysis | `slide-203.png` |
| 204 | Profitability Framework | Profitability Framework — revenue/cost decomposition | `slide-204.png` |
| 205 | Blue Ocean Strategy | Blue Ocean Strategy — value innovation framework | `slide-205.png` |
| 206 | Value Disciplines Model | You need: Value Disciplines Model | `slide-206.png` |
| 207 | Roger-s Five Factors | You need: Roger-s Five Factors | `slide-207.png` |
| 208 | SIPOC model | SIPOC — Suppliers / Inputs / Process / Outputs / Customers | `slide-208.png` |
| 209 | PESTEL Analysis | PESTEL — Political/Economic/Social/Technological/Environmental/Legal | `slide-209.png` |
| 210 | Lafley Strategy -Strategy Cascade- | You need: Lafley Strategy -Strategy Cascade- | `slide-210.png` |
| 211 | Three Horizons | Three Horizons — H1/H2/H3 growth waves | `slide-211.png` |
| 212 | Seven Degrees of Freedom for Growth | You need: Seven Degrees of Freedom for Growth | `slide-212.png` |
| 213 | Galbraith Star Model | You need: Galbraith Star Model | `slide-213.png` |

## Additional / data charts

| # | Title | Use when... | Preview |
|---|---|---|---|
| 215 | Skills And Self-id Top Factors | You need: Skills And Self-id Top Factors | `slide-215.png` |
| 216 | Percentage breakdown (circles) | You need: Percentage breakdown (circles) | `slide-216.png` |

## Executive Summary structures — narrative arcs (SBAR, vision-strategy-action, etc.)

| # | Title | Use when... | Preview |
|---|---|---|---|
| 218 | 1. PROJECT KICKOFF | You need: 1. PROJECT KICKOFF | `slide-218.png` |
| 219 | Overview 1 | Executive overview — variant 1 | `slide-219.png` |
| 220 | Overview 2 | Executive overview — variant 2 | `slide-220.png` |
| 221 | Overview 3 | Executive overview — variant 3 | `slide-221.png` |
| 222 | Three-Part Structure | Three-part structure — opening / middle / close | `slide-222.png` |
| 223 | Vision > Strategy > Action | Vision -> Strategy -> Action narrative | `slide-223.png` |
| 224 | 2. STRATEGIC PLANNING | You need: 2. STRATEGIC PLANNING | `slide-224.png` |
| 225 | Strategic Recommendations | Strategic Recommendations summary | `slide-225.png` |
| 226 | Goal > Obstacle > Strategy > Action | Goal -> Obstacle -> Strategy -> Action | `slide-226.png` |
| 227 | CLEAR Method | CLEAR Method narrative | `slide-227.png` |
| 228 | 3. MARKET ANALYSIS AND COMPETITIVE LANDSCAPE | You need: 3. MARKET ANALYSIS AND COMPETITIVE LANDSCAPE | `slide-228.png` |
| 229 | The 4 P-s | You need: The 4 P-s | `slide-229.png` |
| 230 | The 5 C-s | You need: The 5 C-s | `slide-230.png` |
| 231 | Trends > Implications > Opportunities | Trends -> Implications -> Opportunities | `slide-231.png` |
| 232 | 4. BUDGET AND FINANCIAL REVIEW | You need: 4. BUDGET AND FINANCIAL REVIEW | `slide-232.png` |
| 233 | Financial Summary | You need: Financial Summary | `slide-233.png` |
| 234 | Objective > Criteria > Metrics | Objective -> Criteria -> Metrics | `slide-234.png` |
| 235 | Problem > Solution > Benefit | Problem -> Solution -> Benefit | `slide-235.png` |
| 236 | 5. OPERATIONAL REVIEW | You need: 5. OPERATIONAL REVIEW | `slide-236.png` |
| 237 | Logical Flow | Logical flow — premise to conclusion | `slide-237.png` |
| 238 | Situation > Complication > Resolution | Situation -> Complication -> Resolution (SCR) | `slide-238.png` |
| 239 | Roadmap/Action Plan | Roadmap / Action Plan | `slide-239.png` |
| 240 | 6. RISK MANAGEMENT | You need: 6. RISK MANAGEMENT | `slide-240.png` |
| 241 | Problem > Process > Payoff | Problem -> Process -> Payoff | `slide-241.png` |
| 242 | Opportunity > Challenges > Solutions | Opportunity -> Challenges -> Solutions | `slide-242.png` |
| 243 | Challenge > Options > Decision | Challenge -> Options -> Decision | `slide-243.png` |
| 244 | 7. INNOVATION AND PRODUCT DEVELOPMENT | You need: 7. INNOVATION AND PRODUCT DEVELOPMENT | `slide-244.png` |
| 245 | Highlights 1 | You need: Highlights 1 | `slide-245.png` |
| 246 | Highlights 2 | You need: Highlights 2 | `slide-246.png` |
| 247 | DIVE Framework | You need: DIVE Framework | `slide-247.png` |
| 248 | Needs > Features > Advantages > Benefits | Needs -> Features -> Advantages -> Benefits (NFAB) | `slide-248.png` |
| 249 | 8. DECISION BRIEFING | You need: 8. DECISION BRIEFING | `slide-249.png` |
| 250 | Key Findings | Key Findings summary | `slide-250.png` |
| 251 | Insight > Action > Outcome | Insight -> Action -> Outcome | `slide-251.png` |
| 252 | Motivation > Opportunity > Ability | Motivation -> Opportunity -> Ability | `slide-252.png` |
| 253 | 9. STATUS UPDATE | You need: 9. STATUS UPDATE | `slide-253.png` |
| 254 | Status > Action > Impact | Status -> Action -> Impact | `slide-254.png` |
| 255 | Context > Challenges > Strategies | Context -> Challenges -> Strategies | `slide-255.png` |
| 256 | What > So What > Now What | What -> So What -> Now What | `slide-256.png` |
| 257 | 10. RESULTS REPORTING | You need: 10. RESULTS REPORTING | `slide-257.png` |
| 258 | Priority > Action > Impact | Priority -> Action -> Impact | `slide-258.png` |
| 259 | SUCCESS Method | SUCCESS Method narrative | `slide-259.png` |
| 260 | Summary > Background > Analysis > Recommendation | Summary -> Background -> Analysis -> Recommendation (SBAR) | `slide-260.png` |

---

## Bespoke metaphor — when none of the above fit

If your thought maps to a real-world object that isn't in the catalog above (e.g., bridge, river, scaffold, telescope), build it as a bespoke metaphor diagram from primitives — see `metis-brand.md` "Universal Closers & Metaphor Primitives" section.
