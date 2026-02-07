#!/usr/bin/env python3
"""
WABuilder Mockup Generator
Generates HTML mockups from YAML screen definitions using Jinja2 templates
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Paths
GENERATOR_DIR = Path(__file__).parent
TEMPLATES_DIR = GENERATOR_DIR / "templates"
MOCKUPS_DIR = GENERATOR_DIR.parent / "mockups"
DESIGN_TOKENS_FILE = GENERATOR_DIR / "design_tokens.json"
SCREEN_DEFINITIONS_FILE = GENERATOR_DIR / "screen_definitions.yaml"


class MockupGenerator:
    """Generate HTML mockups from screen definitions"""

    def __init__(self):
        self.design_tokens = self._load_design_tokens()
        self.screen_definitions = self._load_screen_definitions()
        self.env = self._setup_jinja_env()
        self.generated_files = []

    def _load_design_tokens(self) -> Dict:
        """Load design tokens from JSON"""
        with open(DESIGN_TOKENS_FILE, 'r') as f:
            return json.load(f)

    def _load_screen_definitions(self) -> Dict:
        """Load screen definitions from YAML"""
        if not SCREEN_DEFINITIONS_FILE.exists():
            print(f"Warning: {SCREEN_DEFINITIONS_FILE} not found. Creating empty structure.")
            return {"screens": {}}

        with open(SCREEN_DEFINITIONS_FILE, 'r') as f:
            return yaml.safe_load(f)

    def _setup_jinja_env(self) -> Environment:
        """Set up Jinja2 environment"""
        env = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Add custom filters
        env.filters['tojson'] = json.dumps

        # Add global variables
        env.globals['design_tokens'] = self.design_tokens

        return env

    def generate_screen(self, screen: Dict, portal: str, category: str) -> str:
        """Generate a single screen HTML file"""
        screen_id = screen.get('id', 'unknown')
        screen_name = screen.get('name', 'Untitled Screen')
        fidelity = screen.get('fidelity', 'medium')

        print(f"  Generating: {screen_name} ({fidelity} fidelity)...")

        # Check for screen-specific template first
        screen_template = f'screens/{screen_id}.html'
        template_exists = (TEMPLATES_DIR / screen_template).exists()

        if template_exists:
            template_name = screen_template
            print(f"    Using dedicated template: {screen_template}")
        else:
            # Fall back to fidelity-based template
            template_map = {
                'high': 'screen-templates/high-fidelity.html',
                'medium': 'screen-templates/medium-fidelity.html',
                'low': 'screen-templates/low-fidelity.html'
            }
            template_name = template_map.get(fidelity, 'screen-templates/medium-fidelity.html')

        try:
            template = self.env.get_template(template_name)

            # Prepare context
            context = {
                'screen_id': screen_id,
                'screen_name': screen_name,
                'portal': portal,
                'category': category,
                'fidelity': fidelity,
                'components_used': screen.get('components_used', []),
                'user_journey': screen.get('user_journey', ''),
                'critical_path': screen.get('critical_path', False),
                **screen  # Include all screen data
            }

            # Render HTML
            html_content = template.render(context)

            # Determine output path
            output_dir = MOCKUPS_DIR / f"{portal}-portal" / category
            output_dir.mkdir(parents=True, exist_ok=True)

            output_file = output_dir / f"{screen_id}.html"

            # Write file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.generated_files.append({
                'file': str(output_file.relative_to(MOCKUPS_DIR)),
                'screen_id': screen_id,
                'screen_name': screen_name,
                'portal': portal,
                'category': category,
                'fidelity': fidelity
            })

            return str(output_file.relative_to(MOCKUPS_DIR))

        except Exception as e:
            print(f"    ERROR: Failed to generate {screen_name}: {e}")
            return None

    def generate_all_screens(self):
        """Generate all screens from definitions"""
        screens_data = self.screen_definitions.get('screens', {})

        total_screens = 0
        for portal, categories in screens_data.items():
            print(f"\n{portal.upper()} PORTAL:")
            for category, screens in categories.items():
                print(f"  Category: {category}")
                for screen in screens:
                    self.generate_screen(screen, portal, category)
                    total_screens += 1

        print(f"\n✓ Generated {total_screens} screens")
        return total_screens

    def generate_master_index(self):
        """Generate master navigation index"""
        print("\nGenerating master index...")

        # Group screens by portal
        portals = {}
        for file_info in self.generated_files:
            portal = file_info['portal']
            if portal not in portals:
                portals[portal] = {
                    'name': portal.replace('-', ' ').title(),
                    'screens': []
                }
            portals[portal]['screens'].append(file_info)

        # Create master index HTML
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WABuilder Mockups - Master Index</title>
  <link rel="stylesheet" href="_assets/styles.css">
  <style>
    body {{
      background: var(--color-bg-gray);
      padding: var(--space-6);
    }}
    .master-header {{
      max-width: 1280px;
      margin: 0 auto var(--space-6);
      background: var(--color-bg-white);
      padding: var(--space-6);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-md);
    }}
    .portal-grid {{
      max-width: 1280px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: var(--space-6);
    }}
    .portal-card {{
      background: var(--color-bg-white);
      border-radius: var(--radius-lg);
      padding: var(--space-6);
      box-shadow: var(--shadow-md);
    }}
    .screen-list {{
      display: flex;
      flex-direction: column;
      gap: var(--space-2);
      margin-top: var(--space-4);
    }}
    .screen-link {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: var(--space-3);
      background: var(--color-neutral-50);
      border-radius: var(--radius-md);
      text-decoration: none;
      color: var(--color-neutral-900);
      transition: background 0.2s;
    }}
    .screen-link:hover {{
      background: var(--color-primary-light);
    }}
    .search-box {{
      width: 100%;
      padding: var(--space-3);
      border: 1px solid var(--color-neutral-300);
      border-radius: var(--radius-md);
      font-family: var(--font-family);
      font-size: 16px;
      margin-top: var(--space-4);
    }}
    .stats {{
      display: flex;
      gap: var(--space-6);
      margin-top: var(--space-4);
    }}
    .stat {{
      display: flex;
      flex-direction: column;
      gap: var(--space-1);
    }}
  </style>
</head>
<body>
  <div class="master-header">
    <h1 class="heading-h1" style="color: var(--color-primary-main);">WABuilder UI Mockups</h1>
    <p class="body-large" style="color: var(--color-neutral-700); margin-top: var(--space-2);">
      Comprehensive screen mockups for all 122+ screens across three portals
    </p>
    <div class="stats">
      <div class="stat">
        <div class="metric-medium">{len(self.generated_files)}</div>
        <div class="body-small">Total Screens</div>
      </div>
      <div class="stat">
        <div class="metric-medium">{len([f for f in self.generated_files if f['fidelity'] == 'high'])}</div>
        <div class="body-small">High Fidelity</div>
      </div>
      <div class="stat">
        <div class="metric-medium">{len([f for f in self.generated_files if f['fidelity'] == 'medium'])}</div>
        <div class="body-small">Medium Fidelity</div>
      </div>
      <div class="stat">
        <div class="metric-medium">{len([f for f in self.generated_files if f['fidelity'] == 'low'])}</div>
        <div class="body-small">Low Fidelity</div>
      </div>
    </div>
    <input type="text" id="searchBox" class="search-box" placeholder="Search screens...">
  </div>

  <div class="portal-grid" id="portalGrid">
"""

        for portal_id, portal_data in portals.items():
            index_html += f"""
    <div class="portal-card">
      <h2 class="heading-h2">{portal_data['name']} Portal</h2>
      <p class="body-base" style="color: var(--color-neutral-500);">{len(portal_data['screens'])} screens</p>
      <div class="screen-list">
"""
            for screen in sorted(portal_data['screens'], key=lambda x: x['screen_name']):
                fidelity_badge = {
                    'high': '<span class="badge badge-success">High</span>',
                    'medium': '<span class="badge badge-neutral">Medium</span>',
                    'low': '<span class="badge badge-warning">Low</span>'
                }.get(screen['fidelity'], '')

                index_html += f"""
        <a href="{screen['file']}" class="screen-link" data-screen-name="{screen['screen_name'].lower()}">
          <span class="label-base">{screen['screen_name']}</span>
          {fidelity_badge}
        </a>
"""

            index_html += """
      </div>
    </div>
"""

        index_html += """
  </div>

  <script>
    // Search functionality
    const searchBox = document.getElementById('searchBox');
    const screenLinks = document.querySelectorAll('.screen-link');

    searchBox.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      screenLinks.forEach(link => {
        const screenName = link.getAttribute('data-screen-name');
        if (screenName.includes(query)) {
          link.style.display = 'flex';
        } else {
          link.style.display = 'none';
        }
      });
    });
  </script>
</body>
</html>
"""

        # Write index file
        index_file = MOCKUPS_DIR / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)

        print(f"✓ Master index created at: {index_file}")


def main():
    """Main execution"""
    print("=" * 60)
    print("WABuilder Mockup Generator")
    print("=" * 60)

    generator = MockupGenerator()

    # Generate all screens
    total = generator.generate_all_screens()

    # Generate master index
    if total > 0:
        generator.generate_master_index()

    print("\n" + "=" * 60)
    print(f"✓ Generation complete! {total} screens created.")
    print(f"✓ View mockups: {MOCKUPS_DIR}/index.html")
    print("=" * 60)


if __name__ == "__main__":
    main()
