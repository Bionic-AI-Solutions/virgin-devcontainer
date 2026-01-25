# GenImage UI Mockup Generation Workflow

This workflow defines how BMAD agents use GenImage MCP for **creating UI mockups and wireframes** as part of the SDLC.

## Core Principle: Design-First Development

**RULE:** UI-focused Features and Stories must have visual mockups before implementation.

```
┌─────────────────────────────────────────────────────────────────┐
│                    UI MOCKUP GENERATION WORKFLOW                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. RECEIVE REQUEST                                              │
│     └── PM/SM requests UI mockup for Feature/Story              │
│                                                                  │
│  2. ANALYZE REQUIREMENTS                                         │
│     └── Review acceptance criteria, user flows, constraints      │
│                                                                  │
│  3. GENERATE MOCKUP                                              │
│     └── mcp_genimage_create_mockup(prompt, style, resolution)   │
│                                                                  │
│  4. REVIEW AND ITERATE                                           │
│     └── Refine based on feedback from PM/Dev                    │
│                                                                  │
│  5. ATTACH TO OPENPROJECT                                        │
│     └── mcp_openproject_add_work_package_attachment(...)        │
│                                                                  │
│  6. UPDATE WORK PACKAGE STATUS                                   │
│     └── Notify SM that UI artifacts are ready for verification  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## RACI Matrix

| Activity | PM | UX Designer | SM | Dev | Architect | TEA |
|----------|-------|-------------|-------|-----|-----------|-----|
| Request UI Mockup | R | I | C | C | C | I |
| Create Mockup | C | R/A | I | C | C | I |
| Review Mockup | A | R | C | C | C | I |
| Iterate on Feedback | C | R | I | C | I | I |
| Attach to OpenProject | I | R | A | I | I | I |
| Verify Artifacts | I | C | R/A | I | I | I |
| Approve for Development | A | C | R | C | C | I |

**Legend:** R = Responsible, A = Accountable, C = Consulted, I = Informed

## When to Generate UI Mockups

### Feature Level (Required)

Generate UI mockups when:
- Feature includes user-facing UI components
- Feature description mentions "interface", "screen", "page", "view"
- Feature has user interaction requirements

**Quality Gate:** Features with UI components cannot transition to "Specified" without attached UI mockups.

### Story Level (Recommended)

Generate UI mockups when:
- Story modifies existing UI
- Story adds new UI components
- Story has specific visual acceptance criteria

## Mockup Generation Workflow

### Step 1: Analyze Requirements

Before generating mockups, UX Designer must:

1. **Read the Feature/Story description** in OpenProject
2. **Identify UI components** mentioned in acceptance criteria
3. **Review user flows** and interactions required
4. **Check existing designs** for consistency (prior mockups, style guide)
5. **Clarify ambiguities** with PM if requirements are unclear

```python
# Get work package details
work_package = mcp_openproject_get_work_package(work_package_id=feature_id)
description = work_package["work_package"]["description"]["raw"]

# Extract UI requirements from description
# Look for: screens, components, interactions, states
```

### Step 2: Generate Initial Mockup

Create mockup with detailed prompt:

```python
# Construct detailed prompt from requirements
prompt = """
Modern web application dashboard with:
- Left sidebar navigation with icons for Home, Analytics, Settings, Profile
- Top header with search bar, notification bell, user avatar dropdown
- Main content area with:
  - Welcome message with user name
  - 4 metric cards showing key statistics
  - Data table with pagination
  - Line chart showing trends
- Color scheme: Blue primary (#3B82F6), white background, gray text
- Responsive layout optimized for desktop
"""

mockup = mcp_genimage_create_mockup(
    prompt=prompt,
    style="modern",
    resolution="1920x1080"
)
```

### Step 3: Review with Stakeholders

Present mockup to PM and relevant stakeholders:

```python
# Add comment to work package with mockup for review
mcp_openproject_add_work_package_comment(
    work_package_id=feature_id,
    comment=f"""
    **UI Mockup Ready for Review**
    
    Generated mockup for {feature_name}. Please review and provide feedback.
    
    **Next Steps:**
    1. PM: Review and approve or request changes
    2. Dev: Comment on technical feasibility
    3. UX Designer: Iterate based on feedback
    """,
    notify=True
)
```

### Step 4: Iterate Based on Feedback

Refine mockup using iteration tool:

```python
# Iterate based on PM/Dev feedback
refined = mcp_genimage_iterate(
    image_id=mockup["image_id"],
    feedback="""
    Changes requested:
    1. Make the sidebar collapsible
    2. Add a "Create New" button in the header
    3. Include empty state design for the data table
    4. Adjust chart to show weekly instead of daily data
    """
)
```

### Step 5: Attach Final Mockup to OpenProject

Once approved, attach to work package:

```python
# Export final version
final_image = mcp_genimage_export(
    image_id=refined["image_id"],
    format="png"
)

# Attach to Feature work package
mcp_openproject_add_work_package_attachment(
    work_package_id=feature_id,
    file_data=final_image["base64"],
    filename=f"feature-{feature_id}-ui-mockup-v1.png",
    content_type="image/png",
    description=f"Approved UI mockup for {feature_name}"
)

# Add approval comment
mcp_openproject_add_work_package_comment(
    work_package_id=feature_id,
    comment="✅ UI Mockup approved and attached. Ready for SM verification.",
    notify=True
)
```

### Step 6: SM Verification

SM verifies mockup is attached before allowing status transition:

```python
# SM verification function
def verify_ui_mockups_attached(feature_id: int) -> tuple[bool, str]:
    """
    Verify UI mockups are attached to Feature.
    Called by SM before allowing "In specification" → "Specified" transition.
    """
    attachments = mcp_openproject_list_work_package_attachments(
        work_package_id=feature_id
    )
    
    # Check for image attachments
    image_extensions = ['.png', '.jpg', '.jpeg', '.svg', '.fig', '.sketch']
    has_mockups = any(
        any(a["fileName"].lower().endswith(ext) for ext in image_extensions)
        or "mock" in a["fileName"].lower()
        or "design" in a["fileName"].lower()
        for a in attachments.get("attachments", [])
    )
    
    if has_mockups:
        return True, "UI mockups verified"
    else:
        return False, "Missing: UI mockups (Feature includes UI components)"
```

## Integration with Specification Quality Gates

### Feature Specification Requirements

For Features with UI components, the following must be attached before "Specified" status:

| Artifact | Generator | Responsible | Accountable |
|----------|-----------|-------------|-------------|
| Feature Architecture | Architect | Architect | PM |
| API Documentation | Dev/Architect | Architect | PM |
| **UI Mockups** | GenImage MCP | UX Designer | PM |
| Feature Scope | PM | PM | SM |

### Story Specification Requirements

For Stories with UI components:

| Artifact | Generator | Responsible | Accountable |
|----------|-----------|-------------|-------------|
| Acceptance Criteria | PM | PM | SM |
| **UI Mocks** | GenImage MCP | UX Designer | PM |
| Technical Specs | Dev/Architect | Dev | SM |

## Mockup Types and When to Use

| Type | Tool | Use Case | Resolution |
|------|------|----------|------------|
| Full Page Mockup | `create_mockup` | Feature-level design | 1920x1080 |
| Component Mockup | `create_mockup` | Specific UI component | 800x600 |
| Wireframe | `create_wireframe` | Early concept, layout | 1920x1080 |
| Mobile Mockup | `create_mockup` | Mobile app screens | 375x812 |
| State Variations | `create_mockup` | Loading, error, empty states | 800x600 |

## Error Handling

### Generation Fails

```python
try:
    mockup = mcp_genimage_create_mockup(prompt=prompt, style="modern")
except Exception as e:
    # Notify PM/UX Designer
    mcp_openproject_add_work_package_comment(
        work_package_id=feature_id,
        comment=f"⚠️ UI Mockup generation failed: {str(e)}. UX Designer to retry or create manually.",
        notify=True
    )
```

### Quality Not Acceptable

```python
# If generated mockup doesn't meet requirements
mcp_openproject_add_work_package_comment(
    work_package_id=feature_id,
    comment="""
    ⚠️ Generated mockup requires significant revision.
    
    **Issues:**
    - Layout doesn't match requirements
    - Missing key components
    
    **Action:** UX Designer to iterate or create manually in Figma/Sketch
    """,
    notify=True
)
```

## Best Practices

1. **Always include context** in prompts (app type, target users, brand guidelines)
2. **Generate multiple variations** for important screens
3. **Create state variations** (loading, error, empty, success)
4. **Use consistent style** across all mockups in a Feature
5. **Document design decisions** in work package comments
6. **Iterate based on feedback** before finalizing
7. **Always attach to OpenProject** - never store only locally
8. **Reference mockups in acceptance criteria** for Stories

## Agent Responsibilities Summary

| Agent | Responsibility | Accountability |
|-------|----------------|----------------|
| **PM** | Request mockups, approve designs | Final design approval |
| **UX Designer** | Generate mockups, iterate on feedback | Mockup quality |
| **SM** | Verify artifacts attached | Process compliance |
| **Dev** | Provide technical feedback | Implementation feasibility |
| **Architect** | System design constraints | Technical architecture alignment |
