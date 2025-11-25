#!/usr/bin/env node
/**
 * Automated QA Diagnostic Script for Portfolio Site
 * Validates HTML, CSS, JS and checks critical functionality
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 Running Portfolio QA Diagnostics...\n');

const errors = [];
const warnings = [];

// 1. Check CSS Syntax
function validateCSS() {
    console.log('📝 Validating CSS...');
    try {
        const cssPath = path.join(__dirname, 'src/style.css');
        const css = fs.readFileSync(cssPath, 'utf8');

        // Count braces
        const opens = (css.match(/{/g) || []).length;
        const closes = (css.match(/}/g) || []).length;

        if (opens !== closes) {
            errors.push(`CSS: Mismatched braces (${opens} opens, ${closes} closes)`);
        } else {
            console.log(`  ✅ Braces balanced (${opens} pairs)`);
        }

        // Check for common errors
        if (css.includes('}}}}')) {
            warnings.push('CSS: Found suspicious multiple closing braces');
        }

        // Check file size
        const sizeKB = (css.length / 1024).toFixed(2);
        console.log(`  📊 File size: ${sizeKB} KB`);

    } catch (err) {
        errors.push(`CSS: Failed to read file - ${err.message}`);
    }
}

// 2. Check HTML Files
function validateHTML() {
    console.log('\n📝 Validating HTML...');
    const htmlFiles = ['index.html', 'project.html', 'projects/studio-pierrot-bi/dashboard/index.html'];

    htmlFiles.forEach(file => {
        try {
            const htmlPath = path.join(__dirname, file);
            if (!fs.existsSync(htmlPath)) {
                warnings.push(`HTML: ${file} not found`);
                return;
            }

            const html = fs.readFileSync(htmlPath, 'utf8');

            // Basic checks
            if (!html.includes('<!DOCTYPE html>')) {
                errors.push(`HTML ${file}: Missing DOCTYPE`);
            }
            if (!html.includes('</html>')) {
                errors.push(`HTML ${file}: Missing closing </html>`);
            }
            if (!html.includes('</head>')) {
                errors.push(`HTML ${file}: Missing closing </head>`);
            }
            if (!html.includes('</body>')) {
                errors.push(`HTML ${file}: Missing closing </body>`);
            }

            console.log(`  ✅ ${file}`);
        } catch (err) {
            errors.push(`HTML ${file}: ${err.message}`);
        }
    });
}

// 3. Check Dashboard JS
function validateDashboardJS() {
    console.log('\n📝 Validating Dashboard JS...');
    try {
        const jsPath = path.join(__dirname, 'projects/studio-pierrot-bi/dashboard/dashboard.js');
        const js = fs.readFileSync(jsPath, 'utf8');

        // Check for critical functions
        const requiredFunctions = [
            'initPhase1Dashboard',
            'renderPhase1ScoreChart',
            'renderPhase1PopularityChart',
            'switchTab'
        ];

        requiredFunctions.forEach(fn => {
            if (!js.includes(`function ${fn}`) && !js.includes(`const ${fn}`)) {
                errors.push(`Dashboard JS: Missing function ${fn}()`);
            } else {
                console.log(`  ✅ Found ${fn}()`);
            }
        });

    } catch (err) {
        errors.push(`Dashboard JS: ${err.message}`);
    }
}

// 4. Check File Paths
function validateFilePaths() {
    console.log('\n📝 Validating File Paths...');
    const criticalFiles = [
        'src/style.css',
        'src/main.js',
        'projects/studio-pierrot-bi/dashboard/data.js',
        'projects/studio-pierrot-bi/dashboard/dashboard.js'
    ];

    criticalFiles.forEach(file => {
        const filePath = path.join(__dirname, file);
        if (!fs.existsSync(filePath)) {
            errors.push(`Missing critical file: ${file}`);
        } else {
            console.log(`  ✅ ${file}`);
        }
    });
}

// Run all validations
validateCSS();
validateHTML();
validateDashboardJS();
validateFilePaths();

// Report
console.log('\n' + '='.repeat(60));
console.log('📊 QA Report Summary');
console.log('='.repeat(60));

if (errors.length === 0 && warnings.length === 0) {
    console.log('✅ All checks passed!');
} else {
    if (errors.length > 0) {
        console.log(`\n❌ ${errors.length} Error(s):`);
        errors.forEach((err, i) => console.log(`  ${i + 1}. ${err}`));
    }

    if (warnings.length > 0) {
        console.log(`\n⚠️  ${warnings.length} Warning(s):`);
        warnings.forEach((warn, i) => console.log(`  ${i + 1}. ${warn}`));
    }

    process.exit(1);
}
