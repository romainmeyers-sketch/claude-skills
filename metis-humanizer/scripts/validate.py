"""
metis-humanizer validator: finds AI-writing tells and consultant-voice
violations in .md, .txt, .docx, .pptx, and .pdf files, and auto-fixes the
subset that is mechanically safe (curly quotes, em/en dashes, emoji,
predicate-position hyphens, a fixed list of filler phrases).

Everything else (AI vocabulary, cliches, tone, structure) is reported as a
finding for a human or the metis-humanizer skill to rewrite; a regex cannot
safely rephrase a sentence, so this script never tries.

Usage:
    python validate.py check  <path> [<path> ...] [--json]
    python validate.py fix    <path> [<path> ...] [--report]

`check` exits 1 if any finding was found, 0 if clean (CI-friendly).
`fix` rewrites supported files in place, then always exits 0; pass
--report to also print the findings that remain after the mechanical fix.

Requires: python-docx, python-pptx, pypdf for .docx/.pptx/.pdf respectively.
Plain .md/.txt need no extra dependency.
"""

import argparse
import bisect
import json
import re
import sys
from pathlib import Path

PHRASE_CATEGORIES = {
    "significance_inflation": [
        "stands as a testament", "serves as a testament", "pivotal moment",
        "pivotal role", "marking a shift", "marks a shift", "evolving landscape",
        "underscores its importance", "underscores its significance",
        "enduring legacy", "lasting legacy", "indelible mark", "deeply rooted",
        "setting the stage for", "key turning point", "focal point",
    ],
    "notability_padding": [
        "active social media presence", "independent coverage",
        "has been cited in", "widely covered by",
    ],
    "ing_tails": [
        "highlighting", "underscoring", "emphasizing", "reflecting",
        "symbolizing", "cultivating", "fostering", "encompassing", "showcasing",
    ],
    "promotional_language": [
        "groundbreaking", "seamless", "seamlessly", "robust", "vibrant",
        "renowned", "commitment to", "nestled in", "nestled within",
        "must-visit", "breathtaking", "boasts a",
    ],
    "vague_attribution": [
        "experts argue", "experts believe", "industry reports",
        "industry experts", "observers have cited", "some critics argue",
        "several sources suggest",
    ],
    "challenges_boilerplate": [
        "despite these challenges", "challenges and future prospects",
        "future outlook", "faces several challenges",
    ],
    "ai_vocabulary": [
        "delve", "leverage", "unlock", "crucial", "pivotal", "showcase",
        "tapestry", "interplay", "intricate", "intricacies", "testament",
        "garner", "align with", "enhance", "foster", "underscore",
        "valuable insights",
    ],
    "copula_avoidance": [
        "serves as", "functions as", "stands as", "boasts",
        "offers a comprehensive",
    ],
    "negative_parallelism": [
        "it's not just", "it is not just", "not only does it",
        "it's not merely", "it is not merely",
    ],
    "chatbot_artifacts": [
        "i hope this helps", "let me know if", "would you like me to",
        "great question", "of course!", "certainly!", "here is an overview",
    ],
    "knowledge_cutoff": [
        "as of my last update", "while specific details are limited",
        "not publicly available", "it is believed that", "likely grew up",
        "maintains a low profile", "keeps personal details private",
    ],
    "sycophantic_tone": [
        "great question!", "you're absolutely right", "that's an excellent point",
        "excellent question",
    ],
    "generic_positive_conclusion": [
        "the future looks bright", "exciting times ahead",
        "exciting times lie ahead", "major step in the right direction",
    ],
    "persuasive_authority_tropes": [
        "the real question is", "at its core,", "what really matters",
        "the heart of the matter", "fundamentally,",
    ],
    "signposting": [
        "let's dive in", "let's explore", "let's break this down",
        "here's what you need to know", "without further ado",
        "now let's look at",
    ],
    "aphorism_formulas": [
        "is the language of", "is the currency of", "is the architecture of",
        "becomes a trap",
    ],
    "conversational_openers": [
        "honestly?", "here's the thing", "the thing is,", "real talk",
    ],
    "consulting_cliches": [
        "synergies", "synergy", "best-in-class", "world-class", "value-add",
        "win-win", "circle back", "boil the ocean", "low-hanging fruit",
        "move the needle", "north star", "double-click on",
        "socialize the document", "take this offline", "level-set",
        "peel the onion", "holistic", "laser-focused", "paradigm shift",
        "secret sauce", "table stakes", "at the end of the day",
    ],
    "firm_voice_floor": [
        "whether you're", "indeed,", "moreover,", "furthermore,",
    ],
    "brand_placeholder": [
        "the firm", "the consultancy",
    ],
}

EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]+"
)
DASH_PATTERN = re.compile(r"\s*(?:—|–|(?<!-)--(?!-))\s*")
CURLY_QUOTE_MAP = {
    "“": '"', "”": '"', "‘": "'", "’": "'",
}
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
INLINE_HEADER_BULLET = re.compile(r"^\s*[-*]\s+\*\*[^*]+:\*\*", re.MULTILINE)
STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "in", "on", "for", "to", "with",
    "is", "are", "your", "our",
}
PREDICATE_HYPHEN_WORDS = [
    "third-party", "cross-functional", "client-facing", "data-driven",
    "decision-making", "well-known", "high-quality", "real-time",
    "long-term", "end-to-end",
]
PREDICATE_HYPHEN_PATTERN = re.compile(
    r"\b(is|are|was|were|be|being|been)\s+("
    + "|".join(w.replace("-", r"\-") for w in PREDICATE_HYPHEN_WORDS)
    + r")\b",
    re.IGNORECASE,
)
FILLER_FIXES = [
    (re.compile(r"\bin order to\b", re.IGNORECASE), "to"),
    (re.compile(r"\bdue to the fact that\b", re.IGNORECASE), "because"),
    (re.compile(r"\bat this point in time\b", re.IGNORECASE), "now"),
    (re.compile(r"\bin the event that\b", re.IGNORECASE), "if"),
    (re.compile(r"\bit is important to note that\s*", re.IGNORECASE), ""),
    (re.compile(r"\bhas the ability to\b", re.IGNORECASE), "can"),
]


def _preserve_case(original, replacement):
    if original[:1].isupper() and replacement:
        return replacement[0].upper() + replacement[1:]
    return replacement


def find_phrase_findings(text):
    findings = []
    lower = text.lower()
    for category, phrases in PHRASE_CATEGORIES.items():
        for phrase in phrases:
            start = 0
            while True:
                idx = lower.find(phrase, start)
                if idx == -1:
                    break
                findings.append((idx, idx + len(phrase), category, phrase))
                start = idx + len(phrase)
    return findings


def find_regex_findings(text):
    findings = []
    for m in DASH_PATTERN.finditer(text):
        if m.group(0).strip():
            findings.append((m.start(), m.end(), "dash_punctuation", m.group(0).strip()))
    for m in re.finditer("[" + "".join(CURLY_QUOTE_MAP) + "]", text):
        findings.append((m.start(), m.end(), "curly_quotes", m.group(0)))
    for m in EMOJI_PATTERN.finditer(text):
        findings.append((m.start(), m.end(), "emoji", m.group(0)))
    for m in PREDICATE_HYPHEN_PATTERN.finditer(text):
        findings.append((m.start(), m.end(), "predicate_hyphen", m.group(0)))
    for pattern, _ in FILLER_FIXES:
        for m in pattern.finditer(text):
            findings.append((m.start(), m.end(), "filler_phrase", m.group(0)))
    for m in INLINE_HEADER_BULLET.finditer(text):
        findings.append((m.start(), m.end(), "inline_header_bullet", m.group(0)))
    for m in HEADING_PATTERN.finditer(text):
        words = [w for w in re.findall(r"[A-Za-z']+", m.group(2)) if w.lower() not in STOPWORDS]
        if len(words) >= 3:
            capitalized = sum(1 for w in words if w[:1].isupper())
            if capitalized / len(words) >= 0.6:
                findings.append((m.start(2), m.end(2), "title_case_heading", m.group(2)))
    findings.extend(_find_staccato(text))
    findings.extend(_find_fragmented_headers(text))
    findings.extend(_find_brandline_misuse(text))
    return findings


def _find_staccato(text):
    findings = []
    for para_match in re.finditer(r"[^\n]+", text):
        para = para_match.group(0)
        sentences = re.split(r"(?<=[.!?])\s+", para)
        run = 0
        for s in sentences:
            words = s.split()
            if 0 < len(words) <= 6:
                run += 1
            else:
                if run >= 3:
                    findings.append((para_match.start(), para_match.end(), "staccato_drama", para[:80]))
                run = 0
        if run >= 3:
            findings.append((para_match.start(), para_match.end(), "staccato_drama", para[:80]))
    return findings


def _find_fragmented_headers(text):
    findings = []
    for m in HEADING_PATTERN.finditer(text):
        rest = text[m.end():m.end() + 200]
        body_match = re.search(r"\S.*", rest)
        if not body_match:
            continue
        line = body_match.group(0).strip()
        heading_words = set(w.lower() for w in re.findall(r"[A-Za-z']+", m.group(2)))
        line_words = re.findall(r"[A-Za-z']+", line)
        if 0 < len(line_words) <= 6 and heading_words & set(w.lower() for w in line_words):
            findings.append((m.start(), m.end(), "fragmented_header", m.group(2)))
    return findings


def _find_brandline_misuse(text):
    findings = []
    for m in re.finditer(r"Driving change\.\s*Elevating leaders\.", text):
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.end())
        line_end = len(text) if line_end == -1 else line_end
        line = text[line_start:line_end]
        if line.strip() != m.group(0).strip():
            findings.append((m.start(), m.end(), "brandline_misplaced", m.group(0)))
    return findings


def scan_text(text):
    all_findings = find_phrase_findings(text) + find_regex_findings(text)
    all_findings.sort(key=lambda f: f[0])
    return all_findings


def line_number(text, offset):
    return text.count("\n", 0, offset) + 1


def apply_mechanical_fixes(text):
    for char, replacement in CURLY_QUOTE_MAP.items():
        text = text.replace(char, replacement)
    text = EMOJI_PATTERN.sub("", text)
    text = DASH_PATTERN.sub(", ", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\s+,", ",", text)

    def _predicate_sub(m):
        verb, word = m.group(1), m.group(2)
        return f"{verb} {word.replace('-', ' ')}"

    text = PREDICATE_HYPHEN_PATTERN.sub(_predicate_sub, text)
    for pattern, replacement in FILLER_FIXES:
        text = pattern.sub(lambda m: _preserve_case(m.group(0), replacement), text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def format_findings(path, text, findings, as_json):
    if as_json:
        return [
            {
                "file": str(path),
                "line": line_number(text, start),
                "category": category,
                "match": match,
            }
            for start, end, category, match in findings
        ]
    lines = []
    for start, end, category, match in findings:
        snippet = text[max(0, start - 30):end + 30].replace("\n", " ")
        lines.append(f"{path}:{line_number(text, start)}: [{category}] {match!r} ... {snippet.strip()!r}")
    return lines


def load_text_file(path):
    return path.read_text(encoding="utf-8")


def save_text_file(path, text):
    path.write_text(text, encoding="utf-8")


def load_docx_units(path):
    from docx import Document

    doc = Document(str(path))
    paragraphs = list(doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                paragraphs.extend(cell.paragraphs)
    return doc, paragraphs


def load_pptx_units(path):
    from pptx import Presentation

    prs = Presentation(str(path))
    paragraphs = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                paragraphs.extend(shape.text_frame.paragraphs)
    return prs, paragraphs


def paragraphs_corpus(paragraphs):
    texts = [p.text for p in paragraphs]
    return "\n".join(texts)


def fix_paragraph_runs(paragraphs):
    changed = False
    for p in paragraphs:
        for run in p.runs:
            fixed = apply_mechanical_fixes(run.text)
            if fixed != run.text:
                run.text = fixed
                changed = True
    return changed


def load_pdf_text(path):
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def process_file(path, mode, as_json, report_after_fix):
    suffix = path.suffix.lower()
    result = {"file": str(path), "findings": [], "fixed": False, "skipped": None}

    if suffix in (".md", ".txt"):
        text = load_text_file(path)
        if mode == "check":
            result["findings"] = format_findings(path, text, scan_text(text), as_json)
        else:
            fixed_text = apply_mechanical_fixes(text)
            if fixed_text != text:
                save_text_file(path, fixed_text)
                result["fixed"] = True
            if report_after_fix:
                remaining_text = fixed_text if result["fixed"] else text
                result["findings"] = format_findings(path, remaining_text, scan_text(remaining_text), as_json)

    elif suffix == ".docx":
        doc, paragraphs = load_docx_units(path)
        corpus = paragraphs_corpus(paragraphs)
        if mode == "check":
            result["findings"] = format_findings(path, corpus, scan_text(corpus), as_json)
        else:
            result["fixed"] = fix_paragraph_runs(paragraphs)
            if result["fixed"]:
                doc.save(str(path))
            if report_after_fix:
                remaining_corpus = paragraphs_corpus(paragraphs)
                result["findings"] = format_findings(path, remaining_corpus, scan_text(remaining_corpus), as_json)

    elif suffix == ".pptx":
        prs, paragraphs = load_pptx_units(path)
        corpus = paragraphs_corpus(paragraphs)
        if mode == "check":
            result["findings"] = format_findings(path, corpus, scan_text(corpus), as_json)
        else:
            result["fixed"] = fix_paragraph_runs(paragraphs)
            if result["fixed"]:
                prs.save(str(path))
            if report_after_fix:
                remaining_corpus = paragraphs_corpus(paragraphs)
                result["findings"] = format_findings(path, remaining_corpus, scan_text(remaining_corpus), as_json)

    elif suffix == ".pdf":
        text = load_pdf_text(path)
        result["findings"] = format_findings(path, text, scan_text(text), as_json)
        if mode == "fix":
            result["skipped"] = "PDF is read-only for this tool; findings only, no auto-fix."

    else:
        result["skipped"] = f"unsupported extension: {suffix}"

    return result


def expand_paths(raw_paths):
    paths = []
    for raw in raw_paths:
        if any(ch in raw for ch in "*?["):
            paths.extend(Path(p) for p in Path().glob(raw))
        else:
            paths.append(Path(raw))
    return paths


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="mode", required=True)

    check_p = sub.add_parser("check", help="report findings, exit 1 if any found")
    check_p.add_argument("paths", nargs="+")
    check_p.add_argument("--json", action="store_true")

    fix_p = sub.add_parser("fix", help="auto-fix mechanical findings in place")
    fix_p.add_argument("paths", nargs="+")
    fix_p.add_argument("--report", action="store_true", help="also print findings remaining after fix")
    fix_p.add_argument("--json", action="store_true")

    args = parser.parse_args()
    paths = expand_paths(args.paths)
    as_json = args.json
    report_after_fix = args.mode == "fix" and args.report

    all_results = []
    for path in paths:
        if not path.exists():
            print(f"{path}: not found", file=sys.stderr)
            continue
        all_results.append(process_file(path, args.mode, as_json, report_after_fix))

    total_findings = sum(len(r["findings"]) for r in all_results)

    if as_json:
        print(json.dumps(all_results, indent=2))
    else:
        for r in all_results:
            if r["skipped"]:
                print(f"{r['file']}: {r['skipped']}")
            if r["fixed"]:
                print(f"{r['file']}: mechanical fixes applied")
            for line in r["findings"]:
                print(line)
        if args.mode == "check":
            print(f"\n{total_findings} finding(s) across {len(all_results)} file(s)")

    if args.mode == "check":
        sys.exit(1 if total_findings else 0)
    sys.exit(0)


if __name__ == "__main__":
    main()
