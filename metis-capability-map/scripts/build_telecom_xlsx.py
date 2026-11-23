"""
Build a Business Capability Map XLSX for a Telecom company (fiber optic cables).
Maturity column is empty with data validation dropdowns and conditional formatting pre-wired.
"""

import sys
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

OUTPUT = os.path.expanduser("~/Downloads/Fiber_Optic_Telecom_Capability_Map.xlsx")

# ── Brand constants ──
HEADER_FONT = Font(name="Calibri", bold=True, size=11, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="20206E")
HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
BODY_FONT = Font(name="Calibri", size=10, color="4A4A4A")
BODY_ALIGN = Alignment(vertical="top", wrap_text=True)
L2_FONT = Font(name="Calibri", bold=True, size=10, color="20206E")
CENTER_ALIGN = Alignment(horizontal="center", vertical="top")
THIN_BORDER = Border(
    left=Side(style="thin", color="CCCCCC"),
    right=Side(style="thin", color="CCCCCC"),
    top=Side(style="thin", color="CCCCCC"),
    bottom=Side(style="thin", color="CCCCCC"),
)

PILLAR_FILLS = {
    "Customer Journey": PatternFill("solid", fgColor="E8F4FD"),
    "Value Chain": PatternFill("solid", fgColor="E8F8E8"),
    "Supporting": PatternFill("solid", fgColor="F5F0FF"),
}

MATURITY_LABELS = {1: "Ad-hoc", 2: "Developing", 3: "Defined", 4: "Managed", 5: "Optimized"}

# ── Capability Map Data ──
# Structure: (Pillar, L1, L2, L3, Shared)
# Maturity left empty for user to fill in

DATA = [
    # ════════════════════════════════════════════════════════════
    # CUSTOMER JOURNEY
    # ════════════════════════════════════════════════════════════
    ("Customer Journey", "Awareness", "Market Presence", "Industry Event & Trade Show Presence"),
    ("Customer Journey", "Awareness", "Market Presence", "Digital Brand & Website Experience"),
    ("Customer Journey", "Awareness", "Market Presence", "Thought Leadership & Technical Publications"),
    ("Customer Journey", "Awareness", "Market Presence", "Analyst & Media Relations"),
    ("Customer Journey", "Awareness", "Demand Generation", "Targeted Account-Based Marketing"),
    ("Customer Journey", "Awareness", "Demand Generation", "Technical Content & White Papers"),
    ("Customer Journey", "Awareness", "Demand Generation", "Referral & Partner Co-Marketing"),

    ("Customer Journey", "Specification & Evaluation", "Technical Consultation", "Fiber Type & Cable Design Advisory"),
    ("Customer Journey", "Specification & Evaluation", "Technical Consultation", "Network Architecture Consultation"),
    ("Customer Journey", "Specification & Evaluation", "Technical Consultation", "Standards & Compliance Guidance (ITU-T, IEC)"),
    ("Customer Journey", "Specification & Evaluation", "Product Demonstration", "Sample & Prototype Provision"),
    ("Customer Journey", "Specification & Evaluation", "Product Demonstration", "Lab Testing & Performance Validation"),
    ("Customer Journey", "Specification & Evaluation", "Product Demonstration", "Reference Site Visits & Case Studies"),
    ("Customer Journey", "Specification & Evaluation", "Competitive Positioning", "Technical Differentiation Communication"),
    ("Customer Journey", "Specification & Evaluation", "Competitive Positioning", "Total Cost of Ownership Modeling"),

    ("Customer Journey", "Quoting & Contracting", "Proposal Management", "Custom Specification & Bill of Materials"),
    ("Customer Journey", "Quoting & Contracting", "Proposal Management", "Pricing & Volume Discount Structuring"),
    ("Customer Journey", "Quoting & Contracting", "Proposal Management", "RFP/RFQ Response Management"),
    ("Customer Journey", "Quoting & Contracting", "Contract Execution", "Master Supply Agreement Negotiation"),
    ("Customer Journey", "Quoting & Contracting", "Contract Execution", "SLA & Warranty Terms Definition"),
    ("Customer Journey", "Quoting & Contracting", "Contract Execution", "Long-Term Volume Commitment Planning"),

    ("Customer Journey", "Order & Fulfillment", "Order Management", "Order Entry & Confirmation"),
    ("Customer Journey", "Order & Fulfillment", "Order Management", "Production Scheduling Visibility"),
    ("Customer Journey", "Order & Fulfillment", "Order Management", "Order Modification & Change Management"),
    ("Customer Journey", "Order & Fulfillment", "Logistics & Delivery", "Cable Reel & Packaging Management"),
    ("Customer Journey", "Order & Fulfillment", "Logistics & Delivery", "Freight & Shipping Coordination"),
    ("Customer Journey", "Order & Fulfillment", "Logistics & Delivery", "Delivery Tracking & Notification"),
    ("Customer Journey", "Order & Fulfillment", "Logistics & Delivery", "Import/Export & Customs Compliance"),

    ("Customer Journey", "Installation & Deployment", "Installation Support", "Field Engineering & Technical Assistance"),
    ("Customer Journey", "Installation & Deployment", "Installation Support", "Splicing & Termination Guidance"),
    ("Customer Journey", "Installation & Deployment", "Installation Support", "Installation Training & Certification"),
    ("Customer Journey", "Installation & Deployment", "Commissioning", "End-to-End Link Testing & Validation"),
    ("Customer Journey", "Installation & Deployment", "Commissioning", "OTDR Testing & Documentation"),
    ("Customer Journey", "Installation & Deployment", "Commissioning", "As-Built Documentation & Handover"),

    ("Customer Journey", "In-Service & Support", "Technical Support", "Tier 1-3 Technical Issue Resolution"),
    ("Customer Journey", "In-Service & Support", "Technical Support", "Failure Analysis & Root Cause Investigation"),
    ("Customer Journey", "In-Service & Support", "Technical Support", "Fiber Performance Monitoring Guidance"),
    ("Customer Journey", "In-Service & Support", "Warranty & Returns", "Warranty Claim Processing"),
    ("Customer Journey", "In-Service & Support", "Warranty & Returns", "Defective Material Return & Replacement"),
    ("Customer Journey", "In-Service & Support", "Proactive Engagement", "Product Update & Upgrade Notifications"),
    ("Customer Journey", "In-Service & Support", "Proactive Engagement", "Preventive Maintenance Recommendations"),

    ("Customer Journey", "Renewal & Expansion", "Account Growth", "Contract Renewal & Renegotiation"),
    ("Customer Journey", "Renewal & Expansion", "Account Growth", "Cross-Sell (Connectivity Solutions, Accessories)"),
    ("Customer Journey", "Renewal & Expansion", "Account Growth", "New Project & Network Expansion Capture"),
    ("Customer Journey", "Renewal & Expansion", "Relationship Management", "Quarterly Business Reviews"),
    ("Customer Journey", "Renewal & Expansion", "Relationship Management", "Executive Sponsor Alignment"),
    ("Customer Journey", "Renewal & Expansion", "Relationship Management", "Customer Satisfaction Measurement"),

    # ════════════════════════════════════════════════════════════
    # VALUE CHAIN
    # ════════════════════════════════════════════════════════════
    ("Value Chain", "Product Strategy & Development", "Product Portfolio Management", "Fiber Product Roadmap & Lifecycle Management"),
    ("Value Chain", "Product Strategy & Development", "Product Portfolio Management", "Market Requirements Definition"),
    ("Value Chain", "Product Strategy & Development", "Product Portfolio Management", "Product Rationalization & Sunset Planning"),
    ("Value Chain", "Product Strategy & Development", "R&D & Innovation", "Fiber Optic Material Science Research"),
    ("Value Chain", "Product Strategy & Development", "R&D & Innovation", "Next-Gen Cable Design (Bend-Insensitive, High-Density)"),
    ("Value Chain", "Product Strategy & Development", "R&D & Innovation", "Manufacturing Process Innovation"),
    ("Value Chain", "Product Strategy & Development", "R&D & Innovation", "Patent & Intellectual Property Management"),
    ("Value Chain", "Product Strategy & Development", "Standards & Certification", "Industry Standards Participation (ITU-T, IEC, TIA)"),
    ("Value Chain", "Product Strategy & Development", "Standards & Certification", "Product Certification & Type Approval"),
    ("Value Chain", "Product Strategy & Development", "Standards & Certification", "Regulatory Compliance Management"),

    ("Value Chain", "Sourcing & Procurement", "Raw Material Sourcing", "Glass Preform & Silica Procurement"),
    ("Value Chain", "Sourcing & Procurement", "Raw Material Sourcing", "Coating & Buffer Material Sourcing"),
    ("Value Chain", "Sourcing & Procurement", "Raw Material Sourcing", "Cable Component Procurement (Kevlar, Sheathing)"),
    ("Value Chain", "Sourcing & Procurement", "Supplier Management", "Supplier Qualification & Audit"),
    ("Value Chain", "Sourcing & Procurement", "Supplier Management", "Supplier Performance Monitoring"),
    ("Value Chain", "Sourcing & Procurement", "Supplier Management", "Strategic Supplier Partnerships"),
    ("Value Chain", "Sourcing & Procurement", "Procurement Operations", "Purchase Order Management"),
    ("Value Chain", "Sourcing & Procurement", "Procurement Operations", "Inventory & Safety Stock Planning"),

    ("Value Chain", "Manufacturing Operations", "Fiber Drawing", "Preform-to-Fiber Draw Tower Operations"),
    ("Value Chain", "Manufacturing Operations", "Fiber Drawing", "Fiber Geometry & Attenuation Control"),
    ("Value Chain", "Manufacturing Operations", "Fiber Drawing", "Coating Application & Cure"),
    ("Value Chain", "Manufacturing Operations", "Cable Production", "Cable Stranding & Assembly"),
    ("Value Chain", "Manufacturing Operations", "Cable Production", "Jacketing & Armoring"),
    ("Value Chain", "Manufacturing Operations", "Cable Production", "Specialty Cable Production (Submarine, Aerial, Micro)"),
    ("Value Chain", "Manufacturing Operations", "Production Management", "Production Planning & Scheduling"),
    ("Value Chain", "Manufacturing Operations", "Production Management", "Capacity Utilization & Throughput Optimization"),
    ("Value Chain", "Manufacturing Operations", "Production Management", "Changeover & Setup Efficiency"),

    ("Value Chain", "Quality Management", "Quality Assurance", "Incoming Material Inspection"),
    ("Value Chain", "Quality Management", "Quality Assurance", "In-Process Quality Monitoring"),
    ("Value Chain", "Quality Management", "Quality Assurance", "Final Product Testing (Optical, Mechanical, Environmental)"),
    ("Value Chain", "Quality Management", "Quality Systems", "ISO 9001 / TL 9000 Compliance"),
    ("Value Chain", "Quality Management", "Quality Systems", "Statistical Process Control (SPC)"),
    ("Value Chain", "Quality Management", "Quality Systems", "Non-Conformance & CAPA Management"),
    ("Value Chain", "Quality Management", "Metrology & Testing", "Optical Test Lab Operations"),
    ("Value Chain", "Quality Management", "Metrology & Testing", "Environmental & Mechanical Test Lab"),
    ("Value Chain", "Quality Management", "Metrology & Testing", "Measurement Traceability & Calibration"),

    ("Value Chain", "Sales & Distribution", "Direct Sales", "Enterprise & Carrier Account Management", ),
    ("Value Chain", "Sales & Distribution", "Direct Sales", "Government & Public Sector Sales"),
    ("Value Chain", "Sales & Distribution", "Direct Sales", "International & Export Sales"),
    ("Value Chain", "Sales & Distribution", "Channel Management", "Distributor & Reseller Network"),
    ("Value Chain", "Sales & Distribution", "Channel Management", "OEM & System Integrator Partnerships"),
    ("Value Chain", "Sales & Distribution", "Sales Operations", "CRM & Pipeline Management"),
    ("Value Chain", "Sales & Distribution", "Sales Operations", "Quoting & Pricing Engine"),
    ("Value Chain", "Sales & Distribution", "Sales Operations", "Sales Forecasting & Territory Planning"),

    ("Value Chain", "Logistics & Distribution", "Warehouse Operations", "Finished Goods Storage & Handling"),
    ("Value Chain", "Logistics & Distribution", "Warehouse Operations", "Reel Management & Tracking"),
    ("Value Chain", "Logistics & Distribution", "Transportation", "Domestic Freight Management"),
    ("Value Chain", "Logistics & Distribution", "Transportation", "International Shipping & Customs"),
    ("Value Chain", "Logistics & Distribution", "Transportation", "Last-Mile Delivery Coordination"),
    ("Value Chain", "Logistics & Distribution", "Order Fulfillment", "Pick-Pack-Ship Operations"),
    ("Value Chain", "Logistics & Distribution", "Order Fulfillment", "Cut-to-Length & Custom Packaging"),

    ("Value Chain", "Customer Success", "Technical Services", "Application Engineering Support"),
    ("Value Chain", "Customer Success", "Technical Services", "Network Design & Optimization Consulting"),
    ("Value Chain", "Customer Success", "Account Management", "Strategic Account Planning"),
    ("Value Chain", "Customer Success", "Account Management", "Customer Health Scoring"),
    ("Value Chain", "Customer Success", "Voice of Customer", "NPS & Satisfaction Program"),
    ("Value Chain", "Customer Success", "Voice of Customer", "Complaint Management & Trend Analysis"),

    # ════════════════════════════════════════════════════════════
    # SUPPORTING DOMAINS
    # ════════════════════════════════════════════════════════════
    ("Supporting", "Finance", "Financial Planning & Analysis", "Budgeting & Forecasting"),
    ("Supporting", "Finance", "Financial Planning & Analysis", "Cost Accounting & Product Costing"),
    ("Supporting", "Finance", "Financial Planning & Analysis", "Capital Expenditure Planning"),
    ("Supporting", "Finance", "Accounting & Controls", "General Ledger & Financial Close"),
    ("Supporting", "Finance", "Accounting & Controls", "Accounts Payable & Receivable"),
    ("Supporting", "Finance", "Accounting & Controls", "Internal Audit & SOX Compliance"),
    ("Supporting", "Finance", "Treasury", "Cash Flow & Working Capital Management"),
    ("Supporting", "Finance", "Treasury", "Foreign Exchange & Hedging"),

    ("Supporting", "Human Resources", "Talent Acquisition", "Recruitment & Employer Branding"),
    ("Supporting", "Human Resources", "Talent Acquisition", "Manufacturing Workforce Recruitment"),
    ("Supporting", "Human Resources", "Talent Development", "Technical Skills Training (Fiber, Manufacturing)"),
    ("Supporting", "Human Resources", "Talent Development", "Leadership Development & Succession"),
    ("Supporting", "Human Resources", "Talent Development", "Performance Management"),
    ("Supporting", "Human Resources", "Workforce Management", "Shift Scheduling & Labor Planning"),
    ("Supporting", "Human Resources", "Workforce Management", "Compensation & Benefits"),
    ("Supporting", "Human Resources", "Workforce Management", "Employee Relations & Engagement"),

    ("Supporting", "Information Technology", "Enterprise Systems", "ERP & MES Integration"),
    ("Supporting", "Information Technology", "Enterprise Systems", "PLM & Engineering Data Management"),
    ("Supporting", "Information Technology", "Enterprise Systems", "CRM & Sales Enablement Platforms"),
    ("Supporting", "Information Technology", "Infrastructure & Operations", "Network & Communications Infrastructure"),
    ("Supporting", "Information Technology", "Infrastructure & Operations", "Cloud & Data Center Management"),
    ("Supporting", "Information Technology", "Infrastructure & Operations", "OT/IT Convergence (Manufacturing Floor)"),
    ("Supporting", "Information Technology", "Cybersecurity", "Industrial Control System Security"),
    ("Supporting", "Information Technology", "Cybersecurity", "Data Protection & Privacy"),

    ("Supporting", "Legal & Compliance", "Regulatory Compliance", "Telecom Industry Regulations"),
    ("Supporting", "Legal & Compliance", "Regulatory Compliance", "Environmental Compliance (RoHS, REACH)"),
    ("Supporting", "Legal & Compliance", "Regulatory Compliance", "Trade Compliance & Export Controls"),
    ("Supporting", "Legal & Compliance", "Contract Management", "Customer Contract Administration"),
    ("Supporting", "Legal & Compliance", "Contract Management", "Supplier & Vendor Agreements"),
    ("Supporting", "Legal & Compliance", "Intellectual Property", "Patent Portfolio Management"),
    ("Supporting", "Legal & Compliance", "Intellectual Property", "Trade Secret Protection"),

    ("Supporting", "Environment, Health & Safety", "Workplace Safety", "Manufacturing Floor Safety Programs"),
    ("Supporting", "Environment, Health & Safety", "Workplace Safety", "Chemical Handling & Hazmat Management"),
    ("Supporting", "Environment, Health & Safety", "Workplace Safety", "Incident Investigation & Reporting"),
    ("Supporting", "Environment, Health & Safety", "Environmental Management", "Emissions & Waste Management"),
    ("Supporting", "Environment, Health & Safety", "Environmental Management", "Energy Efficiency & Sustainability"),
    ("Supporting", "Environment, Health & Safety", "Environmental Management", "ISO 14001 Compliance"),

    ("Supporting", "Data & Analytics", "Business Intelligence", "Sales & Revenue Analytics"),
    ("Supporting", "Data & Analytics", "Business Intelligence", "Manufacturing Performance Dashboards"),
    ("Supporting", "Data & Analytics", "Business Intelligence", "Supply Chain Visibility & Analytics"),
    ("Supporting", "Data & Analytics", "Advanced Analytics", "Demand Forecasting & Predictive Planning"),
    ("Supporting", "Data & Analytics", "Advanced Analytics", "Predictive Quality & Process Optimization"),
    ("Supporting", "Data & Analytics", "Data Governance", "Master Data Management"),
    ("Supporting", "Data & Analytics", "Data Governance", "Data Quality & Stewardship"),
]

# ── Build workbook ──
wb = Workbook()

# ── Sheet 1: Full Capability Map ──
ws = wb.active
ws.title = "Capability Map"

headers = ["Pillar", "L1 Capability", "L2 Capability Group", "L3 Capability", "Maturity (1-5)", "Maturity Label"]
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = HEADER_ALIGN
    cell.border = THIN_BORDER

for i, row_data in enumerate(DATA, 2):
    pillar, l1, l2, l3 = row_data[0], row_data[1], row_data[2], row_data[3]
    vals = [pillar, l1, l2, l3, None, None]
    for col, val in enumerate(vals, 1):
        cell = ws.cell(row=i, column=col, value=val)
        cell.font = BODY_FONT
        cell.alignment = BODY_ALIGN
        cell.border = THIN_BORDER
        cell.fill = PILLAR_FILLS.get(pillar, PatternFill())
    # L2 bold
    ws.cell(row=i, column=3).font = L2_FONT
    # Maturity column centered
    ws.cell(row=i, column=5).alignment = CENTER_ALIGN
    ws.cell(row=i, column=6).alignment = CENTER_ALIGN

max_row = len(DATA) + 1

# Data validation dropdown for maturity (1-5)
dv = DataValidation(type="list", formula1='"1,2,3,4,5"', allow_blank=True)
dv.error = "Please enter a value between 1 and 5"
dv.errorTitle = "Invalid Maturity Score"
dv.prompt = "1=Ad-hoc, 2=Developing, 3=Defined, 4=Managed, 5=Optimized"
dv.promptTitle = "Maturity Score"
ws.add_data_validation(dv)
dv.add(f"E2:E{max_row}")

# Maturity label formula (auto-fills based on score)
for i in range(2, max_row + 1):
    ws.cell(row=i, column=6).value = f'=IF(E{i}="","",CHOOSE(E{i},"Ad-hoc","Developing","Defined","Managed","Optimized"))'
    ws.cell(row=i, column=6).font = Font(name="Calibri", size=10, color="4A4A4A", italic=True)

# Conditional formatting for maturity heat map colors
ws.conditional_formatting.add(f"E2:E{max_row}",
    CellIsRule(operator="equal", formula=["1"], fill=PatternFill("solid", fgColor="E74C3C"),
              font=Font(bold=True, color="FFFFFF")))
ws.conditional_formatting.add(f"E2:E{max_row}",
    CellIsRule(operator="equal", formula=["2"], fill=PatternFill("solid", fgColor="E67E22"),
              font=Font(bold=True, color="FFFFFF")))
ws.conditional_formatting.add(f"E2:E{max_row}",
    CellIsRule(operator="equal", formula=["3"], fill=PatternFill("solid", fgColor="F1C40F"),
              font=Font(bold=True, color="000000")))
ws.conditional_formatting.add(f"E2:E{max_row}",
    CellIsRule(operator="equal", formula=["4"], fill=PatternFill("solid", fgColor="2ECC71"),
              font=Font(bold=True, color="FFFFFF")))
ws.conditional_formatting.add(f"E2:E{max_row}",
    CellIsRule(operator="equal", formula=["5"], fill=PatternFill("solid", fgColor="27AE60"),
              font=Font(bold=True, color="FFFFFF")))

# Column widths
COL_WIDTHS = [18, 28, 32, 45, 14, 16]
for i, w in enumerate(COL_WIDTHS, 1):
    ws.column_dimensions[get_column_letter(i)].width = w

ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:F{max_row}"

# ── Sheet 2: Summary ──
ws2 = wb.create_sheet("Summary")
sum_headers = ["Pillar", "L1", "L2 Count", "L3 Count"]
for col, h in enumerate(sum_headers, 1):
    cell = ws2.cell(row=1, column=col, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = HEADER_ALIGN
    cell.border = THIN_BORDER

from collections import defaultdict
summary = defaultdict(lambda: {"l2s": set(), "l3_count": 0})
for row_data in DATA:
    pillar, l1, l2, l3 = row_data[0], row_data[1], row_data[2], row_data[3]
    key = (pillar, l1)
    summary[key]["l2s"].add(l2)
    summary[key]["l3_count"] += 1

row = 2
for (pillar, l1), stats in summary.items():
    for col, val in enumerate([pillar, l1, len(stats["l2s"]), stats["l3_count"]], 1):
        cell = ws2.cell(row=row, column=col, value=val)
        cell.font = BODY_FONT
        cell.alignment = BODY_ALIGN
        cell.border = THIN_BORDER
        cell.fill = PILLAR_FILLS.get(pillar, PatternFill())
    row += 1

for i, w in enumerate([18, 30, 12, 12], 1):
    ws2.column_dimensions[get_column_letter(i)].width = w
ws2.freeze_panes = "A2"

# ── Sheet 3: Journey ↔ Value Chain Cross-Reference ──
ws3 = wb.create_sheet("Journey ↔ Value Chain")

journey_l1s = []
seen_j = set()
for row_data in DATA:
    if row_data[0] == "Customer Journey" and row_data[1] not in seen_j:
        journey_l1s.append(row_data[1])
        seen_j.add(row_data[1])

vc_l1_l2s = []
seen_vc = set()
for row_data in DATA:
    if row_data[0] == "Value Chain" and row_data[2] not in seen_vc:
        vc_l1_l2s.append((row_data[1], row_data[2]))
        seen_vc.add(row_data[2])

ws3.cell(row=1, column=1, value="Value Chain L1").font = HEADER_FONT
ws3.cell(row=1, column=1).fill = HEADER_FILL
ws3.cell(row=1, column=1).border = THIN_BORDER
ws3.cell(row=1, column=2, value="Value Chain L2").font = HEADER_FONT
ws3.cell(row=1, column=2).fill = HEADER_FILL
ws3.cell(row=1, column=2).border = THIN_BORDER
for j, jl1 in enumerate(journey_l1s):
    cell = ws3.cell(row=1, column=j+3, value=jl1)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", text_rotation=45, wrap_text=True)
    cell.border = THIN_BORDER

# Natural alignment of VC L1s to journey stages
JOURNEY_VC_MAP = {
    "Product Strategy & Development": ["Awareness", "Specification & Evaluation"],
    "Sourcing & Procurement": ["Order & Fulfillment"],
    "Manufacturing Operations": ["Order & Fulfillment"],
    "Quality Management": ["Specification & Evaluation", "Installation & Deployment", "In-Service & Support"],
    "Sales & Distribution": ["Awareness", "Specification & Evaluation", "Quoting & Contracting"],
    "Logistics & Distribution": ["Order & Fulfillment", "Installation & Deployment"],
    "Customer Success": ["In-Service & Support", "Renewal & Expansion"],
}

MINT_FONT = Font(name="Calibri", size=14, color="3BDAC0")
for i, (vc_l1, vc_l2) in enumerate(vc_l1_l2s, 2):
    ws3.cell(row=i, column=1, value=vc_l1).font = L2_FONT
    ws3.cell(row=i, column=1).border = THIN_BORDER
    ws3.cell(row=i, column=2, value=vc_l2).font = BODY_FONT
    ws3.cell(row=i, column=2).border = THIN_BORDER
    mapped_stages = JOURNEY_VC_MAP.get(vc_l1, [])
    for j, jl1 in enumerate(journey_l1s):
        cell = ws3.cell(row=i, column=j+3)
        cell.border = THIN_BORDER
        cell.alignment = Alignment(horizontal="center")
        if jl1 in mapped_stages:
            cell.value = "●"
            cell.font = MINT_FONT

ws3.column_dimensions["A"].width = 28
ws3.column_dimensions["B"].width = 32
for j in range(len(journey_l1s)):
    ws3.column_dimensions[get_column_letter(j+3)].width = 16
ws3.freeze_panes = "C2"

# ── Save ──
wb.save(OUTPUT)
print(f"Saved to: {OUTPUT}")
print(f"Total capabilities: {len(DATA)} L3s")
print(f"L1s: {len(summary)}")
