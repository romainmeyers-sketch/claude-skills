"""
Build a Business Capability Map XLSX for a Luxury Resort Chain.
Includes maturity heat mapping. No tech enablers.
"""

import sys
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ── Output path ──
OUTPUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Downloads")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT = os.path.join(OUTPUT_DIR, "Luxury_Resort_Capability_Map.xlsx")

# ── Brand constants ──
HEADER_FONT = Font(name="Calibri", bold=True, size=11, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="20206E")
HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
BODY_FONT = Font(name="Calibri", size=10, color="4A4A4A")
BODY_ALIGN = Alignment(vertical="top", wrap_text=True)
L2_FONT = Font(name="Calibri", bold=True, size=10, color="20206E")
THIN_BORDER = Border(
    left=Side(style="thin", color="CCCCCC"),
    right=Side(style="thin", color="CCCCCC"),
    top=Side(style="thin", color="CCCCCC"),
    bottom=Side(style="thin", color="CCCCCC"),
)

PILLAR_FILLS = {
    "Guest Journey": PatternFill("solid", fgColor="E8F4FD"),
    "Value Chain": PatternFill("solid", fgColor="E8F8E8"),
    "Supporting": PatternFill("solid", fgColor="F5F0FF"),
}

MATURITY_FILLS = {
    1: PatternFill("solid", fgColor="E74C3C"),
    2: PatternFill("solid", fgColor="E67E22"),
    3: PatternFill("solid", fgColor="F1C40F"),
    4: PatternFill("solid", fgColor="2ECC71"),
    5: PatternFill("solid", fgColor="27AE60"),
}
MATURITY_FONT = {
    1: Font(name="Calibri", bold=True, size=10, color="FFFFFF"),
    2: Font(name="Calibri", bold=True, size=10, color="FFFFFF"),
    3: Font(name="Calibri", bold=True, size=10, color="000000"),
    4: Font(name="Calibri", bold=True, size=10, color="FFFFFF"),
    5: Font(name="Calibri", bold=True, size=10, color="FFFFFF"),
}
MATURITY_LABELS = {1: "Ad-hoc", 2: "Developing", 3: "Defined", 4: "Managed", 5: "Optimized"}

# ── Capability Map Data ──
# Structure: (Pillar, L1, L2, L3, Shared, Maturity)

DATA = [
    # ════════════════════════════════════════════════════════════
    # GUEST JOURNEY
    # ════════════════════════════════════════════════════════════
    ("Guest Journey", "Discovery", "Brand Awareness", "Social Media Presence & Content", "", 3),
    ("Guest Journey", "Discovery", "Brand Awareness", "Search Engine Visibility (SEO/SEM)", "", 3),
    ("Guest Journey", "Discovery", "Brand Awareness", "Public Relations & Media Coverage", "", 4),
    ("Guest Journey", "Discovery", "Brand Awareness", "Influencer & Partnership Marketing", "", 2),
    ("Guest Journey", "Discovery", "Destination Appeal", "Destination Storytelling & Imagery", "", 4),
    ("Guest Journey", "Discovery", "Destination Appeal", "Virtual Property Tours", "", 2),
    ("Guest Journey", "Discovery", "Destination Appeal", "Local Experience Curation", "", 3),

    ("Guest Journey", "Booking", "Reservation Experience", "Direct Booking (Web & App)", "", 3),
    ("Guest Journey", "Booking", "Reservation Experience", "Third-Party Channel Management (OTAs)", "", 4),
    ("Guest Journey", "Booking", "Reservation Experience", "Group & Event Booking", "", 3),
    ("Guest Journey", "Booking", "Pricing & Availability", "Dynamic Pricing Display", "", 3),
    ("Guest Journey", "Booking", "Pricing & Availability", "Package & Promotion Presentation", "", 3),
    ("Guest Journey", "Booking", "Pricing & Availability", "Rate Transparency & Comparison", "", 2),
    ("Guest Journey", "Booking", "Booking Confidence", "Guest Reviews & Social Proof", "", 3),
    ("Guest Journey", "Booking", "Booking Confidence", "Cancellation & Flexibility Policies", "", 4),

    ("Guest Journey", "Pre-Arrival", "Guest Communication", "Confirmation & Itinerary Delivery", "", 4),
    ("Guest Journey", "Pre-Arrival", "Guest Communication", "Pre-Arrival Preference Collection", "", 3),
    ("Guest Journey", "Pre-Arrival", "Guest Communication", "Concierge Pre-Planning", "", 3),
    ("Guest Journey", "Pre-Arrival", "Anticipation Building", "Welcome Journey Messaging", "", 2),
    ("Guest Journey", "Pre-Arrival", "Anticipation Building", "Upsell & Experience Pre-Booking", "", 2),
    ("Guest Journey", "Pre-Arrival", "Travel Facilitation", "Transportation Coordination", "", 3),
    ("Guest Journey", "Pre-Arrival", "Travel Facilitation", "Digital Check-In & Key Issuance", "", 2),

    ("Guest Journey", "Arrival & Check-In", "Welcome Experience", "Personalized Greeting & Recognition", "", 4),
    ("Guest Journey", "Arrival & Check-In", "Welcome Experience", "Efficient Check-In Process", "", 3),
    ("Guest Journey", "Arrival & Check-In", "Welcome Experience", "Room Readiness & Assignment", "", 3),
    ("Guest Journey", "Arrival & Check-In", "First Impressions", "Property Orientation", "", 4),
    ("Guest Journey", "Arrival & Check-In", "First Impressions", "Welcome Amenity & Gift Delivery", "", 4),

    ("Guest Journey", "Stay & Experience", "In-Stay Services", "Housekeeping & Room Maintenance", "", 4),
    ("Guest Journey", "Stay & Experience", "In-Stay Services", "Concierge & Guest Requests", "", 4),
    ("Guest Journey", "Stay & Experience", "In-Stay Services", "In-Room Technology & Connectivity", "", 3),
    ("Guest Journey", "Stay & Experience", "Dining Experience", "Restaurant Reservation & Seating", "", 4),
    ("Guest Journey", "Stay & Experience", "Dining Experience", "Menu Personalization & Dietary Needs", "", 3),
    ("Guest Journey", "Stay & Experience", "Dining Experience", "In-Room Dining & Minibar", "", 4),
    ("Guest Journey", "Stay & Experience", "Activities & Wellness", "Spa & Wellness Booking", "", 4),
    ("Guest Journey", "Stay & Experience", "Activities & Wellness", "Recreational Activities & Excursions", "", 3),
    ("Guest Journey", "Stay & Experience", "Activities & Wellness", "Kids & Family Programming", "", 3),
    ("Guest Journey", "Stay & Experience", "Service Recovery", "Real-Time Issue Detection", "", 2),
    ("Guest Journey", "Stay & Experience", "Service Recovery", "Complaint Resolution & Follow-Up", "", 3),

    ("Guest Journey", "Departure", "Checkout Experience", "Express & Digital Checkout", "", 3),
    ("Guest Journey", "Departure", "Checkout Experience", "Folio Accuracy & Transparency", "", 3),
    ("Guest Journey", "Departure", "Checkout Experience", "Departure Transportation", "", 3),
    ("Guest Journey", "Departure", "Farewell", "Personalized Farewell & Thank You", "", 4),
    ("Guest Journey", "Departure", "Farewell", "Post-Stay Feedback Invitation", "", 3),

    ("Guest Journey", "Post-Stay & Loyalty", "Relationship Nurture", "Post-Stay Follow-Up Communication", "", 3),
    ("Guest Journey", "Post-Stay & Loyalty", "Relationship Nurture", "Guest Feedback Analysis & Response", "", 3),
    ("Guest Journey", "Post-Stay & Loyalty", "Relationship Nurture", "Personalized Re-Engagement Campaigns", "", 2),
    ("Guest Journey", "Post-Stay & Loyalty", "Loyalty Program", "Loyalty Enrollment & Tier Management", "", 3),
    ("Guest Journey", "Post-Stay & Loyalty", "Loyalty Program", "Rewards Redemption & Recognition", "", 3),
    ("Guest Journey", "Post-Stay & Loyalty", "Loyalty Program", "Lifetime Value Cultivation", "", 2),

    # ════════════════════════════════════════════════════════════
    # VALUE CHAIN
    # ════════════════════════════════════════════════════════════
    ("Value Chain", "Brand Strategy", "Brand Positioning", "Brand Architecture & Portfolio Management", "", 4),
    ("Value Chain", "Brand Strategy", "Brand Positioning", "Competitive Differentiation", "", 3),
    ("Value Chain", "Brand Strategy", "Brand Positioning", "Brand Standards & Guidelines", "", 4),
    ("Value Chain", "Brand Strategy", "Market Intelligence", "Market Research & Trend Analysis", "", 3),
    ("Value Chain", "Brand Strategy", "Market Intelligence", "Competitive Benchmarking", "", 3),
    ("Value Chain", "Brand Strategy", "Market Intelligence", "Guest Segmentation & Personas", "", 2),

    ("Value Chain", "Revenue Management", "Pricing Strategy", "Dynamic Rate Optimization", "[shared]", 3),
    ("Value Chain", "Revenue Management", "Pricing Strategy", "Demand Forecasting", "", 3),
    ("Value Chain", "Revenue Management", "Pricing Strategy", "Yield Management", "", 3),
    ("Value Chain", "Revenue Management", "Distribution", "Channel Strategy & Mix Optimization", "[shared]", 3),
    ("Value Chain", "Revenue Management", "Distribution", "Direct Booking Conversion", "[shared]", 3),
    ("Value Chain", "Revenue Management", "Distribution", "OTA Relationship Management", "[shared]", 4),

    ("Value Chain", "Sales & Marketing", "Digital Marketing", "Content Marketing & Storytelling", "[shared]", 3),
    ("Value Chain", "Sales & Marketing", "Digital Marketing", "Paid Media & Performance Marketing", "", 3),
    ("Value Chain", "Sales & Marketing", "Digital Marketing", "Email & CRM Marketing", "", 3),
    ("Value Chain", "Sales & Marketing", "Direct Sales", "Group & Corporate Sales", "", 3),
    ("Value Chain", "Sales & Marketing", "Direct Sales", "Wedding & Events Sales", "", 4),
    ("Value Chain", "Sales & Marketing", "Direct Sales", "Travel Advisor & Trade Relations", "", 3),

    ("Value Chain", "Guest Services Operations", "Front Office Operations", "Reception & Guest Relations", "[shared]", 4),
    ("Value Chain", "Guest Services Operations", "Front Office Operations", "Guest Profile & Preference Management", "[shared]", 3),
    ("Value Chain", "Guest Services Operations", "Front Office Operations", "VIP & Special Occasion Management", "", 4),
    ("Value Chain", "Guest Services Operations", "Concierge Operations", "Local Experience Coordination", "[shared]", 3),
    ("Value Chain", "Guest Services Operations", "Concierge Operations", "Transportation & Logistics", "[shared]", 3),
    ("Value Chain", "Guest Services Operations", "Service Delivery", "Service Standard Execution", "", 4),
    ("Value Chain", "Guest Services Operations", "Service Delivery", "Quality Assurance & Mystery Shopping", "", 3),

    ("Value Chain", "Food & Beverage", "Culinary Operations", "Menu Development & Innovation", "", 4),
    ("Value Chain", "Food & Beverage", "Culinary Operations", "Kitchen Operations & Production", "", 4),
    ("Value Chain", "Food & Beverage", "Culinary Operations", "Food Safety & Compliance", "", 4),
    ("Value Chain", "Food & Beverage", "Restaurant Operations", "Service Standards & Training", "[shared]", 4),
    ("Value Chain", "Food & Beverage", "Restaurant Operations", "Inventory & Cost Control", "", 3),
    ("Value Chain", "Food & Beverage", "Beverage & Bar", "Beverage Program Development", "", 3),
    ("Value Chain", "Food & Beverage", "Beverage & Bar", "Wine & Spirits Curation", "", 4),

    ("Value Chain", "Property & Facilities", "Property Maintenance", "Preventive Maintenance Programs", "", 3),
    ("Value Chain", "Property & Facilities", "Property Maintenance", "Capital Planning & Renovation", "", 3),
    ("Value Chain", "Property & Facilities", "Property Maintenance", "Energy & Utilities Management", "", 3),
    ("Value Chain", "Property & Facilities", "Housekeeping Operations", "Room Cleaning Standards & Scheduling", "[shared]", 4),
    ("Value Chain", "Property & Facilities", "Housekeeping Operations", "Laundry & Linen Management", "", 3),
    ("Value Chain", "Property & Facilities", "Grounds & Amenities", "Landscaping & Exterior Maintenance", "", 4),
    ("Value Chain", "Property & Facilities", "Grounds & Amenities", "Pool, Spa & Recreation Facilities", "[shared]", 4),

    ("Value Chain", "Loyalty & CRM", "Guest Data Management", "360° Guest Profile Development", "[shared]", 2),
    ("Value Chain", "Loyalty & CRM", "Guest Data Management", "Preference Tracking & Personalization Engine", "[shared]", 2),
    ("Value Chain", "Loyalty & CRM", "Loyalty Program Management", "Program Design & Tier Structure", "[shared]", 3),
    ("Value Chain", "Loyalty & CRM", "Loyalty Program Management", "Partner & Coalition Management", "", 2),
    ("Value Chain", "Loyalty & CRM", "Guest Analytics", "Satisfaction Measurement (NPS/CSAT)", "[shared]", 3),
    ("Value Chain", "Loyalty & CRM", "Guest Analytics", "Behavioral & Spend Analysis", "", 2),

    # ════════════════════════════════════════════════════════════
    # SUPPORTING DOMAINS
    # ════════════════════════════════════════════════════════════
    ("Supporting", "Finance", "Financial Planning & Analysis", "Budgeting & Forecasting", "", 3),
    ("Supporting", "Finance", "Financial Planning & Analysis", "Management Reporting & Dashboards", "", 3),
    ("Supporting", "Finance", "Financial Planning & Analysis", "Investment Appraisal & ROI Analysis", "", 3),
    ("Supporting", "Finance", "Accounting & Controls", "General Ledger & Close", "", 4),
    ("Supporting", "Finance", "Accounting & Controls", "Accounts Payable & Receivable", "", 4),
    ("Supporting", "Finance", "Accounting & Controls", "Internal Audit & Compliance", "", 3),
    ("Supporting", "Finance", "Treasury & Risk", "Cash Flow Management", "", 3),
    ("Supporting", "Finance", "Treasury & Risk", "Insurance & Risk Mitigation", "", 3),

    ("Supporting", "Human Resources", "Talent Acquisition", "Recruitment & Employer Branding", "", 3),
    ("Supporting", "Human Resources", "Talent Acquisition", "Onboarding & Orientation", "", 3),
    ("Supporting", "Human Resources", "Talent Development", "Learning & Development Programs", "", 3),
    ("Supporting", "Human Resources", "Talent Development", "Performance Management & Reviews", "", 3),
    ("Supporting", "Human Resources", "Talent Development", "Leadership & Succession Planning", "", 2),
    ("Supporting", "Human Resources", "Workforce Management", "Scheduling & Labor Optimization", "", 3),
    ("Supporting", "Human Resources", "Workforce Management", "Compensation & Benefits", "", 3),
    ("Supporting", "Human Resources", "Workforce Management", "Employee Engagement & Retention", "", 3),

    ("Supporting", "Information Technology", "Infrastructure", "Network & Connectivity", "", 3),
    ("Supporting", "Information Technology", "Infrastructure", "Property Management System (PMS)", "", 3),
    ("Supporting", "Information Technology", "Infrastructure", "Cloud & Data Center Management", "", 3),
    ("Supporting", "Information Technology", "Digital Platforms", "Website & Mobile App", "", 3),
    ("Supporting", "Information Technology", "Digital Platforms", "Guest-Facing IoT & Smart Room Tech", "", 2),
    ("Supporting", "Information Technology", "Cybersecurity", "Data Privacy & PCI Compliance", "", 3),
    ("Supporting", "Information Technology", "Cybersecurity", "Incident Response & Threat Management", "", 2),

    ("Supporting", "Legal & Compliance", "Regulatory Compliance", "Health & Safety Regulations", "", 4),
    ("Supporting", "Legal & Compliance", "Regulatory Compliance", "Licensing & Permits", "", 4),
    ("Supporting", "Legal & Compliance", "Regulatory Compliance", "Data Protection (GDPR/CCPA)", "", 3),
    ("Supporting", "Legal & Compliance", "Contract Management", "Vendor & Supplier Agreements", "", 3),
    ("Supporting", "Legal & Compliance", "Contract Management", "Franchise & Management Agreements", "", 3),

    ("Supporting", "Procurement & Supply Chain", "Strategic Sourcing", "Vendor Selection & Negotiation", "", 3),
    ("Supporting", "Procurement & Supply Chain", "Strategic Sourcing", "Contract & Spend Management", "", 3),
    ("Supporting", "Procurement & Supply Chain", "Operational Purchasing", "FF&E Procurement", "", 3),
    ("Supporting", "Procurement & Supply Chain", "Operational Purchasing", "OS&E & Consumables Ordering", "", 3),
    ("Supporting", "Procurement & Supply Chain", "Operational Purchasing", "Food & Beverage Sourcing", "", 3),

    ("Supporting", "Sustainability", "Environmental Management", "Energy Efficiency & Carbon Reduction", "", 2),
    ("Supporting", "Sustainability", "Environmental Management", "Waste Management & Circular Economy", "", 2),
    ("Supporting", "Sustainability", "Environmental Management", "Water Conservation", "", 2),
    ("Supporting", "Sustainability", "Social Responsibility", "Community Engagement & Local Impact", "", 3),
    ("Supporting", "Sustainability", "Social Responsibility", "DEI Programs & Reporting", "", 2),
    ("Supporting", "Sustainability", "ESG Reporting", "Sustainability Metrics & Disclosure", "", 2),
]

# ── Build workbook ──
wb = Workbook()

# ── Sheet 1: Full Capability Map ──
ws = wb.active
ws.title = "Capability Map"

headers = ["Pillar", "L1 Capability", "L2 Capability Group", "L3 Capability", "Shared", "Maturity (1-5)", "Maturity Label"]
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = HEADER_ALIGN
    cell.border = THIN_BORDER

for i, (pillar, l1, l2, l3, shared, maturity) in enumerate(DATA, 2):
    row_data = [pillar, l1, l2, l3, shared, maturity, MATURITY_LABELS[maturity]]
    for col, val in enumerate(row_data, 1):
        cell = ws.cell(row=i, column=col, value=val)
        cell.font = BODY_FONT
        cell.alignment = BODY_ALIGN
        cell.border = THIN_BORDER
        # Pillar background
        cell.fill = PILLAR_FILLS.get(pillar, PatternFill())
    # Maturity cell coloring
    mat_cell = ws.cell(row=i, column=6)
    mat_cell.fill = MATURITY_FILLS[maturity]
    mat_cell.font = MATURITY_FONT[maturity]
    mat_cell.alignment = Alignment(horizontal="center", vertical="top")
    # L2 bold
    ws.cell(row=i, column=3).font = L2_FONT

# Column widths
COL_WIDTHS = [16, 22, 28, 38, 8, 14, 16]
for i, w in enumerate(COL_WIDTHS, 1):
    ws.column_dimensions[get_column_letter(i)].width = w

# Freeze panes
ws.freeze_panes = "A2"

# Auto-filter
ws.auto_filter.ref = f"A1:G{len(DATA)+1}"

# ── Sheet 2: Summary ──
ws2 = wb.create_sheet("Summary")
sum_headers = ["Pillar", "L1", "L2 Count", "L3 Count", "Avg Maturity"]
for col, h in enumerate(sum_headers, 1):
    cell = ws2.cell(row=1, column=col, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = HEADER_ALIGN
    cell.border = THIN_BORDER

# Aggregate
from collections import defaultdict
summary = defaultdict(lambda: {"l2s": set(), "l3_count": 0, "maturity_sum": 0})
for pillar, l1, l2, l3, shared, maturity in DATA:
    key = (pillar, l1)
    summary[key]["l2s"].add(l2)
    summary[key]["l3_count"] += 1
    summary[key]["maturity_sum"] += maturity

row = 2
for (pillar, l1), stats in summary.items():
    avg_mat = round(stats["maturity_sum"] / stats["l3_count"], 1)
    for col, val in enumerate([pillar, l1, len(stats["l2s"]), stats["l3_count"], avg_mat], 1):
        cell = ws2.cell(row=row, column=col, value=val)
        cell.font = BODY_FONT
        cell.alignment = BODY_ALIGN
        cell.border = THIN_BORDER
        cell.fill = PILLAR_FILLS.get(pillar, PatternFill())
    row += 1

for i, w in enumerate([16, 24, 12, 12, 14], 1):
    ws2.column_dimensions[get_column_letter(i)].width = w
ws2.freeze_panes = "A2"

# ── Sheet 3: Journey ↔ Value Chain Cross-Reference ──
ws3 = wb.create_sheet("Journey ↔ Value Chain")
# Get unique Journey L1s and Value Chain L2s that are shared
journey_l1s = []
seen_j = set()
for pillar, l1, *_ in DATA:
    if pillar == "Guest Journey" and l1 not in seen_j:
        journey_l1s.append(l1)
        seen_j.add(l1)

vc_l2s = []
seen_vc = set()
for pillar, l1, l2, l3, shared, _ in DATA:
    if pillar == "Value Chain" and l2 not in seen_vc:
        vc_l2s.append((l1, l2))
        seen_vc.add(l2)

# Header row
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

# Simple mapping based on natural alignment
JOURNEY_VC_MAP = {
    "Brand Strategy": ["Discovery"],
    "Revenue Management": ["Booking"],
    "Sales & Marketing": ["Discovery", "Booking"],
    "Guest Services Operations": ["Arrival & Check-In", "Stay & Experience"],
    "Food & Beverage": ["Stay & Experience"],
    "Property & Facilities": ["Stay & Experience", "Arrival & Check-In"],
    "Loyalty & CRM": ["Post-Stay & Loyalty", "Pre-Arrival"],
}

for i, (vc_l1, vc_l2) in enumerate(vc_l2s, 2):
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
            cell.font = Font(name="Calibri", size=14, color="3BDAC0")
        else:
            cell.value = ""

ws3.column_dimensions["A"].width = 22
ws3.column_dimensions["B"].width = 28
for j in range(len(journey_l1s)):
    ws3.column_dimensions[get_column_letter(j+3)].width = 14
ws3.freeze_panes = "C2"

# ── Save ──
wb.save(OUTPUT)
print(f"Saved to: {OUTPUT}")
print(f"Total capabilities: {len(DATA)} L3s across {len(summary)} L1s")
