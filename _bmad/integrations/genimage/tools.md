# GenImage MCP Tools Reference

This document provides the reference for GenImage MCP tools used for **UI mockup and wireframe generation** in BMAD workflows.

## CRITICAL: GenImage Scope

**USE GenImage For:**

- UI mockups for Features and Stories
- Wireframes for application screens
- Design assets (icons, illustrations)
- Visual representations of user flows

**Storage Requirement:**

All generated images must be attached to OpenProject work packages at the appropriate level.

## Configuration

GenImage settings in `_bmad/_config/project-config.yaml`:

```yaml
genimage:
  enabled: true
  defaults:
    style: "modern"
    resolution: "1920x1080"
    format: "png"
```

## Tool Categories

### Connection & Health

| Tool | Description | Parameters |
|------|-------------|------------|
| `mcp_genimage_test_connection()` | Test MCP server connectivity | None |
| `mcp_genimage_health_check()` | Check server health status | None |

### Image Generation

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `mcp_genimage_create_mockup(prompt, ...)` | Generate UI mockup | `prompt` (required), `style`, `resolution` |
| `mcp_genimage_create_wireframe(prompt, ...)` | Generate wireframe | `prompt` (required), `fidelity` |
| `mcp_genimage_create_icon(prompt, ...)` | Generate icon/asset | `prompt` (required), `size`, `style` |
| `mcp_genimage_iterate(image_id, feedback)` | Refine existing image | `image_id`, `feedback` (required) |

### Image Management

| Tool | Description | Parameters |
|------|-------------|------------|
| `mcp_genimage_get_image(image_id)` | Retrieve generated image | `image_id` (required) |
| `mcp_genimage_list_images(session_id)` | List session images | `session_id` (optional) |
| `mcp_genimage_export(image_id, format)` | Export in specific format | `image_id`, `format` |

## UI Mockup Generation

### Basic Mockup Creation

```python
# Generate a UI mockup for a login screen
mockup = mcp_genimage_create_mockup(
    prompt="Modern web application login page with email and password fields, 'Sign In' button, 'Forgot Password' link, and social login options for Google and GitHub. Clean, minimal design with blue accent colors.",
    style="modern",
    resolution="1920x1080"
)

# Get the generated image
image_data = mcp_genimage_get_image(image_id=mockup["image_id"])

# Attach to OpenProject Feature work package
mcp_openproject_add_work_package_attachment(
    work_package_id=feature_id,
    file_data=image_data["base64"],
    filename="feature-auth-login-mockup.png",
    content_type="image/png",
    description="Login page UI mockup for Authentication Feature"
)
```

### Wireframe Generation

```python
# Generate a low-fidelity wireframe
wireframe = mcp_genimage_create_wireframe(
    prompt="Dashboard layout with sidebar navigation, header with user menu, main content area with data cards and charts, footer with links.",
    fidelity="low"  # Options: low, medium, high
)

# Attach to Feature work package
mcp_openproject_add_work_package_attachment(
    work_package_id=feature_id,
    file_data=wireframe["base64"],
    filename="feature-dashboard-wireframe.png",
    content_type="image/png",
    description="Dashboard wireframe layout"
)
```

### Iterative Refinement

```python
# Generate initial mockup
initial = mcp_genimage_create_mockup(
    prompt="User profile settings page with avatar upload, name fields, email, password change section",
    style="modern"
)

# Review and refine based on feedback
refined = mcp_genimage_iterate(
    image_id=initial["image_id"],
    feedback="Add a dark mode toggle at the top right, and include a 'Delete Account' button at the bottom in red"
)

# Export final version
final = mcp_genimage_export(
    image_id=refined["image_id"],
    format="png"
)
```

## Best Practices

### Prompt Writing

**Good Prompts:**

```python
# Specific, detailed prompt
mcp_genimage_create_mockup(
    prompt="E-commerce product listing page showing a grid of 6 product cards, each with product image, title, price, and 'Add to Cart' button. Include category filter sidebar on left, search bar at top, and pagination at bottom. Modern design with white background and blue accent colors."
)

# Clear component description
mcp_genimage_create_wireframe(
    prompt="Mobile app home screen wireframe: top navigation bar with hamburger menu and notifications icon, hero banner area, 3 feature cards in horizontal scroll, recent activity list below, bottom tab navigation with 5 icons."
)
```

**Bad Prompts:**

```python
# Too vague
mcp_genimage_create_mockup(prompt="login page")

# Too complex without structure
mcp_genimage_create_mockup(prompt="entire application with all screens")
```

### Resolution Guidelines

| Use Case | Recommended Resolution |
|----------|----------------------|
| Desktop Web | 1920x1080, 1440x900 |
| Mobile | 375x812 (iPhone), 360x800 (Android) |
| Tablet | 1024x768, 768x1024 |
| Thumbnail/Preview | 400x300, 800x600 |

### Style Options

| Style | Description | Best For |
|-------|-------------|----------|
| `modern` | Clean, minimal design | SaaS, web apps |
| `corporate` | Professional, formal | Enterprise apps |
| `playful` | Colorful, friendly | Consumer apps |
| `minimal` | Ultra-clean, lots of whitespace | Content-focused apps |
| `material` | Google Material Design | Android apps |
| `ios` | Apple Human Interface | iOS apps |

## Integration with SDLC

### During Feature Grooming (PM + UX Designer)

```python
# 1. PM creates Feature in OpenProject
feature = mcp_openproject_create_work_package(
    project_id=project_id,
    subject="Feature: User Authentication",
    type_id=config.openproject.types.feature,
    description="User login, registration, password reset"
)

# 2. UX Designer generates mockups
login_mockup = mcp_genimage_create_mockup(
    prompt="Login page with email/password, social login, forgot password link"
)
register_mockup = mcp_genimage_create_mockup(
    prompt="Registration page with name, email, password fields, terms checkbox"
)

# 3. Attach mockups to Feature (REQUIRED for "Specified" status)
mcp_openproject_add_work_package_attachment(
    work_package_id=feature["work_package"]["id"],
    file_data=login_mockup["base64"],
    filename="feature-auth-login-mockup.png",
    content_type="image/png"
)
mcp_openproject_add_work_package_attachment(
    work_package_id=feature["work_package"]["id"],
    file_data=register_mockup["base64"],
    filename="feature-auth-register-mockup.png",
    content_type="image/png"
)

# 4. SM verifies artifacts before allowing Feature → "Specified"
```

### During Story Grooming

```python
# 1. PM creates Story under Feature
story = mcp_openproject_create_work_package(
    project_id=project_id,
    subject="Story 1.1.1: User Login",
    type_id=config.openproject.types.user_story,
    description="As a user, I want to login so I can access my account"
)

# 2. UX Designer generates story-specific mockup
story_mockup = mcp_genimage_create_mockup(
    prompt="Login page showing validation states: empty, error on invalid email, error on wrong password, success loading state"
)

# 3. Attach to Story
mcp_openproject_add_work_package_attachment(
    work_package_id=story["work_package"]["id"],
    file_data=story_mockup["base64"],
    filename="story-login-states-mockup.png",
    content_type="image/png"
)
```

## RACI for GenImage Operations

| Operation | Responsible | Accountable | Consulted | Informed |
|-----------|-------------|-------------|-----------|----------|
| Generate Feature Mockups | UX Designer | PM | Architect | Dev, SM |
| Generate Story Mockups | UX Designer | PM | Dev | SM |
| Generate Wireframes | UX Designer | PM | Architect | Dev |
| Attach to OpenProject | UX Designer | SM | - | PM |
| Review and Approve | PM | SM | UX Designer | Dev |
| Iterate on Feedback | UX Designer | PM | Dev | SM |

## Troubleshooting

### "Connection Failed"

- Verify GenImage MCP server is running
- Check server URL in configuration
- Test with `mcp_genimage_test_connection()`

### "Invalid Prompt"

- Prompts must be descriptive (minimum 20 characters)
- Avoid special characters that may be interpreted as commands
- Use clear, specific language

### "Image Too Large"

- Reduce resolution for initial iterations
- Export at lower quality for previews
- Use appropriate format (PNG for quality, JPG for size)

### "Style Not Recognized"

- Check available styles with documentation
- Use predefined style names exactly as specified
- Custom styles may require additional configuration
