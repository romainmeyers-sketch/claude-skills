#!/usr/bin/env node
/**
 * render-whitepaper.js
 * Converts a Metis Strategy whitepaper HTML file to a print-ready PDF via Playwright.
 *
 * Usage:
 *   node scripts/render-whitepaper.js <html-file> [output.pdf] [landscape|portrait]
 *
 * Examples:
 *   node scripts/render-whitepaper.js whitepaper.html
 *   node scripts/render-whitepaper.js whitepaper.html output/ai-smart.pdf landscape
 *   node scripts/render-whitepaper.js whitepaper.html playbook.pdf portrait
 *
 * Prerequisites (one-time setup):
 *   npm install playwright
 *   npx playwright install chromium
 */

const { chromium } = require('playwright');
const path = require('path');
const fs   = require('fs');

// ── Configuration ────────────────────────────────────────────────────────────

const PAGE_SIZES = {
  landscape: { width: '1280px', height: '720px'  },
  portrait:  { width: '816px',  height: '1056px' },
};

// ── Argument parsing ─────────────────────────────────────────────────────────

const [,, htmlArg, pdfArg, orientArg] = process.argv;

if (!htmlArg) {
  console.error('\nUsage: node render-whitepaper.js <html-file> [output.pdf] [landscape|portrait]\n');
  process.exit(1);
}

const htmlPath   = path.resolve(htmlArg);
const orientation = (orientArg || 'landscape').toLowerCase();

if (!fs.existsSync(htmlPath)) {
  console.error(`\nError: HTML file not found: ${htmlPath}\n`);
  process.exit(1);
}

if (!PAGE_SIZES[orientation]) {
  console.error(`\nError: orientation must be "landscape" or "portrait", got: "${orientation}"\n`);
  process.exit(1);
}

// Default output path: same directory as the HTML file, named whitepaper.pdf
const defaultPdf = path.join(path.dirname(htmlPath), 'whitepaper.pdf');
const pdfPath    = path.resolve(pdfArg || defaultPdf);

// Ensure output directory exists
const outDir = path.dirname(pdfPath);
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

// ── Rendering ────────────────────────────────────────────────────────────────

async function render() {
  const { width, height } = PAGE_SIZES[orientation];
  const isLandscape        = (orientation === 'landscape');

  console.log(`\nMetis Whitepaper Renderer`);
  console.log(`  HTML:        ${htmlPath}`);
  console.log(`  Output:      ${pdfPath}`);
  console.log(`  Orientation: ${orientation} (${width} × ${height})`);
  console.log('');

  const browser = await chromium.launch();

  try {
    const page = await browser.newPage();

    // Set viewport to match page size so relative units resolve correctly
    await page.setViewportSize({
      width:  parseInt(width,  10),
      height: parseInt(height, 10),
    });

    // Load the HTML file — waitUntil: 'networkidle' ensures Google Fonts CDN loads
    const fileUrl = `file://${htmlPath.replace(/\\/g, '/')}`;
    console.log(`  Loading:     ${fileUrl}`);
    await page.goto(fileUrl, { waitUntil: 'networkidle', timeout: 30000 });

    // Brief pause to allow any deferred font rendering to complete
    await page.waitForTimeout(800);

    // Export PDF
    console.log('  Rendering PDF...');
    // IMPORTANT: Do NOT combine landscape:true with explicit landscape dimensions.
    // Playwright interprets landscape:true as "swap width and height," so passing
    // width:1280 + height:720 + landscape:true produces a 720×1280 portrait page.
    // Since PAGE_SIZES already encodes the correct dimensions for each orientation,
    // we omit the landscape flag entirely and let width/height control the page size.
    await page.pdf({
      path:            pdfPath,
      width,
      height,
      printBackground: true,   // REQUIRED — dark navies and photo fills depend on this
      margin:          { top: '0px', right: '0px', bottom: '0px', left: '0px' },
    });

    // Report file size
    const stats   = fs.statSync(pdfPath);
    const sizeMB  = (stats.size / 1024 / 1024).toFixed(2);
    console.log(`\n✓ PDF saved: ${pdfPath} (${sizeMB} MB)\n`);

  } finally {
    await browser.close();
  }
}

render().catch(err => {
  console.error('\nRendering failed:', err.message || err);
  process.exit(1);
});
