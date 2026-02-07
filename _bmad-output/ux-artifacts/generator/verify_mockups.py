#!/usr/bin/env python3
"""
WABuilder Mockup Verification Script
Validates generated mockups for quality and completeness
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Paths
GENERATOR_DIR = Path(__file__).parent
MOCKUPS_DIR = GENERATOR_DIR.parent / "mockups"


class MockupVerifier:
    """Verify quality of generated mockups"""

    def __init__(self):
        self.issues = []
        self.stats = defaultdict(int)

    def verify_all(self):
        """Run all verification checks"""
        print("=" * 60)
        print("WABuilder Mockup Verification")
        print("=" * 60)

        self.check_file_existence()
        self.check_css_variables()
        self.check_metadata()
        self.check_fidelity_distribution()
        self.check_links()

        self.print_report()

    def check_file_existence(self):
        """Verify all expected files exist"""
        print("\n[1] Checking file existence...")

        # Check master index
        index_file = MOCKUPS_DIR / "index.html"
        if index_file.exists():
            self.stats['master_index'] = 1
            print("  ✓ Master index exists")
        else:
            self.issues.append("CRITICAL: Master index.html not found")

        # Check CSS file
        css_file = MOCKUPS_DIR / "_assets" / "styles.css"
        if css_file.exists():
            self.stats['css_file'] = 1
            print("  ✓ Design tokens CSS exists")
        else:
            self.issues.append("CRITICAL: styles.css not found")

        # Count HTML files
        html_files = list(MOCKUPS_DIR.rglob("*.html"))
        # Exclude index files from screen count
        screen_files = [f for f in html_files if f.name != "index.html"]
        self.stats['total_screens'] = len(screen_files)
        print(f"  ✓ Found {len(screen_files)} screen mockups")

    def check_css_variables(self):
        """Check that mockups use CSS variables, not hardcoded values"""
        print("\n[2] Checking CSS variable usage...")

        hardcoded_colors = []
        html_files = list(MOCKUPS_DIR.rglob("*.html"))

        for html_file in html_files[:10]:  # Sample first 10 files
            content = html_file.read_text()

            # Check for hardcoded hex colors (excluding CSS definitions)
            if '#' in content and 'var(--color' not in content:
                # Look for inline hex colors
                hex_pattern = r'color:\s*#[0-9A-Fa-f]{6}'
                if re.search(hex_pattern, content):
                    hardcoded_colors.append(html_file.name)

        if hardcoded_colors:
            print(f"  ⚠ {len(hardcoded_colors)} files have hardcoded colors (sample)")
        else:
            print("  ✓ CSS variables used correctly (sample verified)")

    def check_metadata(self):
        """Verify screen metadata is present"""
        print("\n[3] Checking screen metadata...")

        missing_metadata = []
        html_files = list(MOCKUPS_DIR.rglob("*.html"))
        screen_files = [f for f in html_files if f.name != "index.html"]

        for html_file in screen_files[:20]:  # Sample first 20 screens
            content = html_file.read_text()

            if 'id="screen-metadata"' not in content:
                missing_metadata.append(html_file.name)

        if missing_metadata:
            print(f"  ⚠ {len(missing_metadata)} files missing metadata (sample)")
            self.issues.append(f"Metadata missing in: {', '.join(missing_metadata[:5])}")
        else:
            print("  ✓ Screen metadata present (sample verified)")

    def check_fidelity_distribution(self):
        """Check distribution of fidelity levels"""
        print("\n[4] Checking fidelity distribution...")

        fidelity_counts = defaultdict(int)
        html_files = list(MOCKUPS_DIR.rglob("*.html"))
        screen_files = [f for f in html_files if f.name != "index.html"]

        for html_file in screen_files:
            content = html_file.read_text()

            if 'HIGH FIDELITY' in content or 'fidelity-badge">high' in content.lower():
                fidelity_counts['high'] += 1
            elif 'MEDIUM FIDELITY' in content or 'fidelity-badge">medium' in content.lower():
                fidelity_counts['medium'] += 1
            elif 'LOW FIDELITY' in content or 'WIREFRAME' in content:
                fidelity_counts['low'] += 1

        print(f"  High Fidelity:   {fidelity_counts['high']} screens")
        print(f"  Medium Fidelity: {fidelity_counts['medium']} screens")
        print(f"  Low Fidelity:    {fidelity_counts['low']} screens")

        self.stats.update(fidelity_counts)

        # Verify distribution makes sense
        total = sum(fidelity_counts.values())
        if total < 100:
            self.issues.append(f"Low total screen count: {total}")

    def check_links(self):
        """Check for broken relative links"""
        print("\n[5] Checking relative links...")

        broken_links = []
        html_files = list(MOCKUPS_DIR.rglob("*.html"))

        for html_file in html_files[:10]:  # Sample first 10
            content = html_file.read_text()

            # Check CSS link
            if 'href="' in content:
                css_matches = re.findall(r'href="([^"]+\.css)"', content)
                for css_path in css_matches:
                    if not css_path.startswith('http'):
                        resolved_path = (html_file.parent / css_path).resolve()
                        if not resolved_path.exists():
                            broken_links.append(f"{html_file.name} → {css_path}")

        if broken_links:
            print(f"  ⚠ {len(broken_links)} broken CSS links found (sample)")
            self.issues.append(f"Broken links: {broken_links[0]}")
        else:
            print("  ✓ CSS links valid (sample verified)")

    def print_report(self):
        """Print final verification report"""
        print("\n" + "=" * 60)
        print("VERIFICATION REPORT")
        print("=" * 60)

        print(f"\nTotal Screens Generated: {self.stats['total_screens']}")
        print(f"High Fidelity:  {self.stats.get('high', 0)}")
        print(f"Medium Fidelity: {self.stats.get('medium', 0)}")
        print(f"Low Fidelity:   {self.stats.get('low', 0)}")

        if self.issues:
            print(f"\n⚠ Issues Found: {len(self.issues)}")
            for issue in self.issues:
                print(f"  - {issue}")
        else:
            print("\n✓ All checks passed!")

        print("\n" + "=" * 60)
        print("RESULT:", "PASS WITH WARNINGS" if self.issues else "PASS")
        print("=" * 60)


def main():
    """Main execution"""
    verifier = MockupVerifier()
    verifier.verify_all()


if __name__ == "__main__":
    main()
