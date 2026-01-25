# GenImage MCP Integration for BMAD

This module provides integration with GenImage MCP server for **AI-powered UI mockup and wireframe generation**.

## Overview

GenImage is used by the **UX Designer agent** to create visual design artifacts:

- **UI Mockups**: Visual representations of user interface screens
- **Wireframes**: Low-fidelity structural layouts
- **Design Assets**: Icons, illustrations, and UI components
- **Feature Visualizations**: Visual representations of proposed features

## RACI for GenImage Usage

| Activity | Responsible | Accountable | Consulted | Informed |
|----------|-------------|-------------|-----------|----------|
| UI Mockup Creation | UX Designer | PM | Dev, Architect | SM |
| Wireframe Generation | UX Designer | PM | Dev | SM |
| Design Review | UX Designer | SM | PM, Dev | TEA |
| Artifact Attachment | UX Designer | SM | PM | Dev |

## Quick Setup

### 1. Verify GenImage MCP Server

```python
# Test connection to GenImage MCP server
mcp_genimage_test_connection()
```

### 2. Update Configuration

Edit `_bmad/_config/project-config.yaml`:

```yaml
genimage:
  enabled: true
  
  defaults:
    style: "modern"           # UI style (modern, minimal, corporate)
    resolution: "1920x1080"   # Default resolution
    format: "png"             # Output format (png, jpg, svg)
```

## Files in This Module

| File | Purpose |
|------|---------|
| `tools.md` | Complete MCP tool reference for image generation |
| `workflow.md` | UX design workflow for mockup creation |
| `README.md` | This setup guide |

## Integration with BMAD Agents

| Agent | GenImage Usage | RACI |
|-------|----------------|------|
| **UX Designer** | Create UI mockups, wireframes, design assets | **R** (Responsible) |
| **PM** | Request designs, approve mockups | **A** (Accountable) |
| **Dev** | Consult on technical feasibility | **C** (Consulted) |
| **Architect** | Consult on system constraints | **C** (Consulted) |
| **SM** | Verify artifacts attached to work packages | **A** (Accountable for process) |

## Core Workflow

```
1. RECEIVE REQUEST  → PM/SM requests UI mockup for Feature/Story
2. ANALYZE          → UX Designer reviews requirements and acceptance criteria
3. GENERATE         → mcp_genimage_create_mockup(prompt, style, resolution)
4. REVIEW           → UX Designer reviews and iterates on generated designs
5. ATTACH           → Attach to OpenProject work package (Feature or Story level)
6. NOTIFY           → Inform PM/SM that design artifacts are ready
```

## Document Storage

**All generated design artifacts must be stored as OpenProject attachments:**

| Design Type | Storage Level | Example |
|-------------|---------------|---------|
| Feature UI Mockups | Feature work package | `feature-X-ui-mockups.png` |
| Story UI Mockups | Story work package | `story-X-Y-ui-mocks.png` |
| Wireframes | Feature work package | `feature-X-wireframe.png` |
| System Diagrams | Epic/Project level | `system-ui-overview.png` |

**CRITICAL:** Do NOT store designs only locally. Always attach to OpenProject for traceability.

## Integration with Specification Quality Gates

UI mockups are **required artifacts** for work packages that include UI components:

### Feature "Specified" Status Requirements

For Features with UI components, SM must verify:
- [ ] UI Mockups attached (generated via GenImage or uploaded)
- [ ] Mockups cover all key user interactions
- [ ] Design approved by PM

### Story "Specified" Status Requirements

For Stories with UI components, SM must verify:
- [ ] UI Mocks attached showing the specific UI for this story
- [ ] Acceptance criteria reference the mockups

## Troubleshooting

### Image Generation Fails

- Check GenImage MCP server is running
- Verify prompt is clear and specific
- Try different style parameters

### Poor Quality Results

- Use more specific prompts describing UI elements
- Specify the application type (web, mobile, dashboard)
- Include color scheme or brand guidelines in prompt

### Cannot Attach to OpenProject

- Verify work package ID is correct
- Check file size limits
- Ensure proper file format (PNG, JPG recommended)

## Related Documentation

- See `workflow.md` for detailed mockup generation workflow
- See `tools.md` for complete GenImage MCP tool reference
- See `_bmad/integrations/openproject/` for work package attachment workflow
