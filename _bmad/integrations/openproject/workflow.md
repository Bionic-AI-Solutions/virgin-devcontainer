# OpenProject Work-Driven Development Workflow

This workflow defines how BMAD agents interact with OpenProject for work management and document storage.

## Core Principle: OpenProject-First

**CRITICAL RULE:** OpenProject is the PRIMARY system for BOTH work management AND document storage.

### Work Management

Before coding ANY functionality:

1. Check OpenProject for current work packages
2. Update work package status when starting work
3. Update status when work is complete
4. NEVER code without an associated work package

### Document Storage

ALL project artifacts must be stored as OpenProject attachments at the appropriate level:

- **Project-level**: Product briefs, project overview docs
- **Epic-level**: Epic specifications, business cases
- **Feature-level**: Feature architecture, technical designs
- **Story-level**: Story specifications, acceptance criteria docs
- **Task-level**: Implementation notes, technical details

**DO NOT store project documents in Archon.** Archon is ONLY for searching external knowledge.

## Mandatory Work Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORK-DRIVEN DEVELOPMENT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. GET WORK                                                     │
│     └── mcp_openproject_list_work_packages(project_id, "open")  │
│                                                                  │
│  2. START WORK                                                   │
│     └── mcp_openproject_update_work_package(id, status_id={config.openproject.statuses.in_progress}) │
│                                                                  │
│  3. RESEARCH (via Archon - see archon/workflow.md)              │
│     └── mcp_archon_rag_search_knowledge_base(...)               │
│                                                                  │
│  4. IMPLEMENT                                                    │
│     └── Write code based on research and requirements           │
│                                                                  │
│  5. MARK DEVELOPED                                               │
│     └── mcp_openproject_update_work_package(id, status_id={config.openproject.statuses.developed}) │
│                                                                  │
│  6. REVIEW                                                       │
│     └── mcp_openproject_update_work_package(id, status_id={config.openproject.statuses.in_testing}) │
│                                                                  │
│  7. MARK TESTED                                                  │
│     └── mcp_openproject_update_work_package(id, status_id={config.openproject.statuses.tested}) │
│                                                                  │
│  8. COMPLETE                                                     │
│     └── mcp_openproject_update_work_package(id, status_id={config.openproject.statuses.closed}) │
│                                                                  │
│  7. NEXT WORK                                                    │
│     └── Return to step 1                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Work Package Hierarchy

OpenProject supports a hierarchical structure that aligns with BMAD:

```
Project
└── Epic (type_id from config)
    └── Feature (type_id from config)
        └── User Story (type_id from config)
            └── Task (type_id from config)
```

### Creating Work Package Hierarchy

**Step 1: Create Epic (with Duplicate Check)**

**CRITICAL: Always check for existing Epic before creating**

```python
# Check for existing Epic
def check_existing_epic(project_id: int, epic_subject: str) -> dict | None:
    """Check if Epic already exists in OpenProject."""
    epics = mcp_openproject_list_work_packages(
        project_id=project_id,
        filters=json.dumps([
            {"type": {"operator": "=", "values": [config.openproject.types.epic]}}
        ]),
        status="all"  # Include closed epics
    )
    for epic in epics.get("work_packages", []):
        if epic_subject.lower() in epic["subject"].lower() or epic["subject"].lower() in epic_subject.lower():
            return epic
    return None

epic_subject = "Epic 1: {Epic Name}"
existing_epic = check_existing_epic(project_id={config.openproject.project_id}, epic_subject=epic_subject)

if existing_epic:
    # Update existing Epic
    epic = mcp_openproject_update_work_package(
        work_package_id=existing_epic["id"],
        description="Updated business goal and scope"
    )
    epic_id = existing_epic["id"]
    print(f"Updated existing Epic {epic_id}")
else:
    # Create new Epic
    epic = mcp_openproject_create_work_package(
        project_id={config.openproject.project_id},
        subject=epic_subject,
        type_id={config.openproject.types.epic},
        description="Business goal and scope",
        status_id={config.openproject.statuses.new},
        priority_id={config.openproject.priorities.high}
    )
    epic_id = epic["work_package"]["id"]

# CRITICAL: When Epic is moved to "In specification" status, attach required artifacts:
# 1. Epic Design Document
mcp_openproject_add_work_package_attachment(
    work_package_id=epic["work_package"]["id"],
    file_data=base64_encoded_design_doc,
    filename="epic-1-design.md",
    content_type="text/markdown",
    description="Epic Design and Implementation Document"
)

# 2. Story Breakdown Document
mcp_openproject_add_work_package_attachment(
    work_package_id=epic["work_package"]["id"],
    file_data=base64_encoded_story_breakdown,
    filename="epic-1-story-breakdown.md",
    content_type="text/markdown",
    description="Story Breakdown Document"
)

# 3. Epic Test Plan (if applicable)
if epic_requires_test_plan:
    mcp_openproject_add_work_package_attachment(
        work_package_id=epic["work_package"]["id"],
        file_data=base64_encoded_test_plan,
        filename="epic-1-test-plan.md",
        content_type="text/markdown",
        description="Epic Test Plan"
    )

# After all artifacts are attached, PM requests SM to verify and approve transition to "Specified" status
# SM uses mcp_openproject_list_work_package_attachments() to check artifacts

# MANDATORY: Create Integration Test Story (Story X.Y.T) for Feature
# This must be created when creating the Feature or during Feature grooming
integration_test_story = mcp_openproject_create_work_package(
    project_id={config.openproject.project_id},
    subject="Story X.Y.T: Feature X.Y Integration Testing and Validation",  # MANDATORY Integration Test Story
    type_id={config.openproject.types.user_story},
    description="""
    As a **Test Team**,
    I want **to validate the complete Feature X.Y functionality**,
    So that **I can ensure all stories work together and the Feature meets its acceptance criteria**.
    
    **Acceptance Criteria:**
    - **Given** all stories in Feature X.Y are implemented
    - **When** I run Feature-level integration tests
    - **Then** all Feature acceptance criteria are met
    - **And** all cross-story integration points work correctly
    - **And** end-to-end Feature functionality is validated
    
    **Test Activities:**
    1. Create Feature integration test plan: `feature-X-Y-integration-test-plan.md`
    2. Attach test plan to Feature X.Y
    3. Run Feature-level integration tests
    4. Validate all Feature acceptance criteria
    5. Test cross-story integration points
    6. Run end-to-end Feature functionality tests
    """,
    status_id={config.openproject.statuses.new},
    priority_id={config.openproject.priorities.high}
)
mcp_openproject_set_work_package_parent(
    work_package_id=integration_test_story["work_package"]["id"],
    parent_id=feature_id
)
```

**CRITICAL PROTOCOL:** Before Epic can transition from "In specification" to "Specified", Scrum Master (SM) must verify all required artifacts are attached using `mcp_openproject_list_work_package_attachments()`.

**MANDATORY:** Every Feature MUST have an Integration Test Story (Story X.Y.T). Feature cannot proceed to "In testing" or be closed if Integration Test Story is missing or not closed.

**Step 2: Create Features under Epic (Recommended for new epics)**

**CRITICAL: Always check for existing Feature before creating**

```python
# Check for existing Feature
def check_existing_feature(epic_id: int, feature_subject: str) -> dict | None:
    """Check if Feature already exists under Epic."""
    children = mcp_openproject_get_work_package_children(
        parent_id=epic_id,
        status="all"  # Include closed features
    )
    for child in children.get("children", []):
        if child["type"] == "Feature":
            if feature_subject.lower() in child["subject"].lower() or child["subject"].lower() in feature_subject.lower():
                return child
    return None

feature_subject = "Feature: {Feature Name}"
existing_feature = check_existing_feature(epic_id=epic_id, feature_subject=feature_subject)

if existing_feature:
    # Update existing Feature
    feature = mcp_openproject_update_work_package(
        work_package_id=existing_feature["id"],
        description="""
        ## Functional Capability
        {Updated statement of what this feature provides}
        
        ## Scope
        **Included:** {Updated stories and functionality included}
        **Excluded:** {Updated functionality explicitly excluded}
        
        ## Integration Test Scope
        {Updated what will be tested at Feature level}
        """
    )
    feature_id = existing_feature["id"]
    print(f"Updated existing Feature {feature_id}")
else:
    # Create new Feature
    feature = mcp_openproject_create_work_package(
        project_id={config.openproject.project_id},
        subject=feature_subject,
        type_id={config.openproject.types.feature},
        description="""
        ## Functional Capability
        {Clear statement of what this feature provides}
        
        ## Scope
        **Included:** {Stories and functionality included}
        **Excluded:** {Functionality explicitly excluded}
        
        ## Integration Test Scope
        {What will be tested at Feature level}
        """,
        status_id={config.openproject.statuses.new},
        priority_id={config.openproject.priorities.high}
    )
    feature_id = feature["work_package"]["id"]
    # Set parent relationship to Epic
    mcp_openproject_set_work_package_parent(
        work_package_id=feature_id,
        parent_id=epic_id
    )

# CRITICAL: When Feature is moved to "In specification" status, attach required artifacts:
# 1. Feature Architecture Document
mcp_openproject_add_work_package_attachment(
    work_package_id=feature["work_package"]["id"],
    file_data=base64_encoded_arch_doc,
    filename="feature-X-architecture.md",
    content_type="text/markdown",
    description="Feature Architecture and Technical Design"
)

# 2. API Documentation (if Feature includes APIs)
if feature_includes_apis:
    mcp_openproject_add_work_package_attachment(
        work_package_id=feature["work_package"]["id"],
        file_data=base64_encoded_api_doc,
        filename="feature-X-api-documentation.md",
        content_type="text/markdown",
        description="API Documentation"
    )

# 3. UI Mocks/Designs (if Feature includes UI) - Images: PNG, JPG, SVG, or design files
if feature_includes_ui:
    mcp_openproject_add_work_package_attachment(
        work_package_id=feature["work_package"]["id"],
        file_data=base64_encoded_ui_mock,
        filename="feature-X-ui-mocks.png",
        content_type="image/png",
        description="UI Mocks/Designs"
    )

# 4. Feature Scope Document
mcp_openproject_add_work_package_attachment(
    work_package_id=feature["work_package"]["id"],
    file_data=base64_encoded_scope_doc,
    filename="feature-X-scope.md",
    content_type="text/markdown",
    description="Feature Scope Document"
)

# After all artifacts are attached, PM requests SM to verify and approve transition to "Specified" status
# SM uses verify_feature_specification_artifacts(feature_id) to check artifacts
```

**Note:** Features are **recommended** for new epics to enable Feature-level integration testing. For existing epics, you may skip Features to avoid retroactive work.

**CRITICAL PROTOCOL:** Before Feature can transition from "In specification" to "Specified", Scrum Master (SM) must verify all required artifacts are attached using `mcp_openproject_list_work_package_attachments()` and `verify_feature_specification_artifacts()`.

**Step 3: Create User Stories under Features (or Epic if no Features)**

**CRITICAL: Always check for existing Story before creating**

**CRITICAL: INCREMENTAL DEVELOPMENT** - Story must be verifiable with previously implemented work, NOT dependent on future work.

```python
# Check for existing Story
def check_existing_story(parent_id: int, story_subject: str) -> dict | None:
    """Check if Story already exists under parent (Feature or Epic)."""
    children = mcp_openproject_get_work_package_children(
        parent_id=parent_id,
        status="all"  # Include closed stories
    )
    for child in children.get("children", []):
        if child["type"] == "User story":
            if story_subject.lower() in child["subject"].lower() or child["subject"].lower() in story_subject.lower():
                return child
    return None

story_subject = "Story X.Y: {Story Name}"  # Or "Story X.Y.Z" if under Feature
parent_id = feature_id  # Or epic_id if no Features
existing_story = check_existing_story(parent_id=parent_id, story_subject=story_subject)

if existing_story:
    # Update existing Story
    story = mcp_openproject_update_work_package(
        work_package_id=existing_story["id"],
        description="""
        As a {updated_persona},
        I want {updated_goal},
        So that {updated_benefit}.

        **Acceptance Criteria:**
        - Given... When... Then...
        """
    )
    story_id = existing_story["id"]
    print(f"Updated existing Story {story_id}")
else:
    # Create new Story
    story = mcp_openproject_create_work_package(
        project_id={config.openproject.project_id},
        subject=story_subject,
        type_id={config.openproject.types.user_story},
        description="""
        As a {persona},
        I want {goal},
        So that {benefit}.

        **Acceptance Criteria:**
        - Given... When... Then...
        """,
        status_id={config.openproject.statuses.new},
        priority_id={config.openproject.priorities.normal}
    )
    story_id = story["work_package"]["id"]
    # Set parent relationship to Feature (or Epic if no Features)
    mcp_openproject_set_work_package_parent(
        work_package_id=story_id,
        parent_id=parent_id
    )

# CRITICAL: When Story is moved to "In specification" status, attach required artifacts:
# 1. Acceptance Criteria (may be in description above, or attach as document)
if not acceptance_criteria_in_description:
    mcp_openproject_add_work_package_attachment(
        work_package_id=story["work_package"]["id"],
        file_data=base64_encoded_ac_doc,
        filename="story-X-Y-acceptance-criteria.md",
        content_type="text/markdown",
        description="Acceptance Criteria Document"
    )

# 2. UI Mocks/Designs (if Story includes UI) - Images: PNG, JPG, SVG, or design files
if story_includes_ui:
    mcp_openproject_add_work_package_attachment(
        work_package_id=story["work_package"]["id"],
        file_data=base64_encoded_ui_mock,
        filename="story-X-Y-ui-mocks.png",
        content_type="image/png",
        description="UI Mocks/Designs"
    )

# 3. Technical Specifications (if Story requires technical details)
if story_requires_technical_details:
    mcp_openproject_add_work_package_attachment(
        work_package_id=story["work_package"]["id"],
        file_data=base64_encoded_tech_spec,
        filename="story-X-Y-technical-spec.md",
        content_type="text/markdown",
        description="Technical Specifications"
    )

# After all artifacts are attached, PM requests SM to verify and approve transition to "Specified" status
# SM uses verify_story_specification_artifacts(story_id) to check artifacts
```

**CRITICAL PROTOCOL:** Before Story can transition from "In specification" to "Specified", Scrum Master (SM) must verify all required artifacts are attached using `mcp_openproject_list_work_package_attachments()` and `verify_story_specification_artifacts()`.

**MANDATORY:** Every Story MUST have a test task (Task X.Y.T). Story cannot be closed if test task is missing or not closed. This is enforced by the `update_story_status_based_on_tasks()` helper function.

**Step 4: Create Tasks under Stories**

**CRITICAL:** Every Story MUST have a test task (Task X.Y.T). The Story cannot be closed until the test task is completed and closed successfully.

**CRITICAL: Always check for existing Tasks before creating** (already implemented in `check_existing_tasks()`)

```python
# CRITICAL: Check for existing tasks first (prevents duplicates)
def check_existing_tasks(story_id: int) -> list[dict]:
    """Check for existing tasks for a story, including closed tasks."""
    children = mcp_openproject_get_work_package_children(
        parent_id=story_id,
        status="all"  # Include closed tasks - CRITICAL!
    )
    return children.get("children", [])

# Get existing tasks
existing = check_existing_tasks(story_id)
existing_subjects = {t["subject"] for t in existing}

# Define tasks to create
tasks_to_create = [
    {
        "subject": "Task X.Y.Z: {Task Name}",
        "type_id": {config.openproject.types.task},
        "description": "Specific implementation work",
        "status_id": {config.openproject.statuses.new}
    },
    # ... other tasks
]

# Filter out duplicates
new_tasks = [t for t in tasks_to_create if t["subject"] not in existing_subjects]

if new_tasks:
    # Create only new tasks
    for task_data in new_tasks:
        task = mcp_openproject_create_work_package(
            project_id={config.openproject.project_id},
            subject=task_data["subject"],
            type_id=task_data["type_id"],
            description=task_data.get("description", ""),
            status_id=task_data.get("status_id", {config.openproject.statuses.new})
        )
        mcp_openproject_set_work_package_parent(
            work_package_id=task["work_package"]["id"],
            parent_id=story_id
        )
else:
    print(f"All tasks already exist for story {story_id}")

# MANDATORY: Create test task (Task X.Y.T) for every Story
test_task = mcp_openproject_create_work_package(
    project_id={config.openproject.project_id},
    subject="Task X.Y.T: Story X.Y Testing and Validation",  # MANDATORY test task
    type_id={config.openproject.types.task},
    description="""
    **MANDATORY Test Task for Story X.Y**
    
    **CRITICAL:** This test task MUST be completed and closed before the Story can be closed.
    
    **Activities:**
    1. Create Story test document: `story-X-Y-test-plan.md`
    2. Attach test document to Story X.Y
    3. Validate all acceptance criteria
    4. Run integration tests
    5. Verify implementation works as expected
    6. Verify code follows architecture patterns
    7. Verify error handling works correctly
    8. Verify documentation is updated
    """,
    status_id={config.openproject.statuses.new},
    priority_id={config.openproject.priorities.high}  # High priority - required for story closure
)
mcp_openproject_set_work_package_parent(
    work_package_id=test_task["work_package"]["id"],
    parent_id=story_id
)
```

**Step 5: Create Bugs under Stories (when validation fails)**

```python
bug = mcp_openproject_create_work_package(
    project_id={config.openproject.project_id},
    subject="Bug: {Brief Description}",
    type_id={config.openproject.types.bug},
    description="""
    **Bug Report:**
    
    **Story:** {Story ID and Title}
    **Task:** {Task ID and Title} (if applicable)
    
    **Expected Behavior:**
    {What should happen}
    
    **Actual Behavior:**
    {What actually happens}
    
    **Steps to Reproduce:**
    1. {Step 1}
    2. {Step 2}
    3. {Step 3}
    
    **Acceptance Criteria Violated:**
    - {AC 1}
    - {AC 2}
    """,
    status_id={config.openproject.statuses.new},
    priority_id={config.openproject.priorities.normal}  # Adjust based on impact
)
# Set parent relationship to Story
mcp_openproject_set_work_package_parent(
    work_package_id=bug["work_package"]["id"],
    parent_id=story_id
)
# Assign bug to dev
mcp_openproject_assign_work_package(
    work_package_id=bug["work_package"]["id"],
    assignee_id=dev_user_id
)
```

## Status Workflow

### Complete Status Flow

**Available Statuses (from OpenProject):**

All status IDs must be retrieved from OpenProject using `mcp_openproject_list_statuses()` and configured in `project-config.yaml`:

```
New
  ↓
[In specification]  ← Requirements being defined (optional)
  ↓
[Specified]         ← Requirements complete (optional)
  ↓
In progress         ← Active development
  ↓
Developed           ← Code/implementation complete
  ↓
In testing          ← Under review/testing
  ↓
Tested              ← Testing complete and passed
  ↓
Closed              ← Complete

Alternative paths:
  - On hold         ← Paused
  - Rejected        ← Not proceeding
  - Test failed     ← Testing failed, needs rework
```

**Status IDs Configuration:**

All status IDs must be configured in `_bmad/_config/project-config.yaml`:

```yaml
openproject:
  statuses:
    new: {ACTUAL_STATUS_ID}  # Query via mcp_openproject_list_statuses()
    in_specification: {ACTUAL_STATUS_ID}
    specified: {ACTUAL_STATUS_ID}
    in_progress: {ACTUAL_STATUS_ID}
    developed: {ACTUAL_STATUS_ID}
    in_testing: {ACTUAL_STATUS_ID}
    tested: {ACTUAL_STATUS_ID}
    test_failed: {ACTUAL_STATUS_ID}
    closed: {ACTUAL_STATUS_ID}
    on_hold: {ACTUAL_STATUS_ID}
    rejected: {ACTUAL_STATUS_ID}
```

**CRITICAL:** Always use `config.openproject.statuses.{status_name}` in code, never hardcode status IDs.

### Recommended Status Flow

For most development workflows, use this flow:

```
New → In progress → Developed → In testing → Tested → Closed
```

**Note:** "Developed" and "Tested" are intermediate states that provide better tracking of work progress.

## Document Storage Workflow

### Principle: Store Documents at Appropriate Level

All project documents are stored as OpenProject attachments. Choose the correct work package level:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENT STORAGE HIERARCHY                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PROJECT LEVEL                                                   │
│  └── Product briefs, project overview, high-level specs         │
│                                                                  │
│  EPIC LEVEL                                                      │
│  └── Epic specifications, business cases, epic architecture     │
│                                                                  │
│  FEATURE LEVEL                                                   │
│  └── Feature architecture, technical designs, API specs         │
│                                                                  │
│  STORY LEVEL                                                     │
│  └── Story specs, detailed acceptance criteria, test cases      │
│                                                                  │
│  TASK LEVEL                                                      │
│  └── Implementation notes, code documentation, technical notes  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Document Types and Storage Location

| Document Type           | Storage Level   | Rationale                 |
| ----------------------- | --------------- | ------------------------- |
| Product Brief           | Project         | Applies to entire project |
| PRD                     | Project or Epic | Requirements scope        |
| Architecture Overview   | Project         | System-wide architecture  |
| Feature Architecture    | Feature         | Feature-specific design   |
| Technical Specification | Feature/Story   | Implementation details    |
| API Documentation       | Feature         | API is feature-level      |
| Acceptance Criteria Doc | Story           | Story-specific criteria   |
| Test Strategy           | Feature         | Feature-level testing     |
| Test Cases              | Story           | Story-specific tests      |
| Implementation Notes    | Task            | Task-specific details     |
| Code Documentation      | Task            | Implementation reference  |

### Attaching Documents

1. **Via OpenProject UI**: Upload directly to work package
2. **Via API**: Use OpenProject attachment API
3. **Link in Description**: Reference document location in work package description

### Document Naming Convention

```
{WorkPackageID}-{DocumentType}-{Version}.{ext}

Examples:
- WP-123-architecture-v1.md
- WP-456-acceptance-criteria-v2.md
- WP-789-implementation-notes.md
```

## Agent Integration Points

### PM Agent

- **Grooming (Responsible):** Creates and grooms Epics, Features, User Stories (from PRD)
- **Epic Grooming:** When Epic is "In specification", ensures all required artifacts are attached:
  - Epic Design Document
  - Story Breakdown Document
  - Epic Test Plan (if applicable)
- **Feature Grooming:** When Feature is "In specification", ensures all required artifacts are attached:
  - Feature Architecture Document
  - API Documentation (if Feature includes APIs)
  - UI Mocks/Designs (if Feature includes UI)
  - Feature Scope Document
- **Story Grooming:** When Story is "In specification", ensures all required artifacts are attached:
  - Acceptance Criteria Document (or in description)
  - UI Mocks/Designs (if Story includes UI)
  - Technical Specifications (if Story requires technical details)
- **Updates:** Feature/Story acceptance criteria, priorities
- **Queries:** Sprint backlog, story/feature status
- **Status Updates:** Epic → "In progress" (when first story starts), Feature → "In progress" (when first story starts)
- **Documents:** Stores product briefs at Project level, PRDs at Epic level, Feature architecture at Feature level
- **Accountable for:** Grooming quality and artifact completeness

### Dev Agent

- **Queries:** Assigned work packages, task/bug details
- **Updates:** Task status (New → In progress → Developed → In testing), Bug status (New → In progress → Developed → In testing)
- **Creates:** Sub-tasks for implementation breakdown
- **Status Updates:** Uses `update_task_status_and_parent()` function to automatically update parent Story status
- **Documents:** Stores implementation notes at Task level

### SM Agent (Scrum Master)

- **Protocol Enforcement (Accountable):** Verifies required artifacts before allowing work packages to transition from "In specification" to "Specified"
- **Epic Specification Protocol:** Verifies Epic Design Document, Story Breakdown Document, Epic Test Plan (if applicable) are attached before allowing Epic → "Specified"
- **Feature Specification Protocol:** Verifies Feature Architecture Document, API Documentation (if APIs), UI Mocks (if UI), Feature Scope Document are attached before allowing Feature → "Specified"
- **Story Specification Protocol:** Verifies Acceptance Criteria, UI Mocks (if UI), Technical Specifications (if required) are attached before allowing Story → "Specified"
- Uses `mcp_openproject_list_work_package_attachments()` and helper functions to check artifacts
- Blocks status transitions if artifacts are missing
- **Queries:** Sprint progress, blockers
- **Updates:** Sprint assignments, priorities
- **Reports:** Sprint status, velocity
- **Documents:** Sprint reports at Project level
- **Accountable for:** Protocol enforcement, artifact verification, blocking incomplete work packages

### Architect Agent

- **Creates:** Technical tasks from architecture decisions
- **Links:** Stories to technical specifications
- **Documents:** Stores architecture docs at Feature level, system architecture at Project level

### TEA Agent (Test Team)

- **Creates:** Test-related tasks, Bugs (when validation fails)
- **Updates:** Task status (In testing → Tested → Closed), Bug status (In testing → Tested → Closed), Feature status (In testing → Tested → Closed)
- **Status Updates:** 
  - Uses `update_task_status_and_parent()` when closing tasks
  - Uses `update_bug_status_and_check_story()` when closing bugs
  - Runs Feature-level integration tests and updates Feature status
- **Links:** Test cases to stories
- **Documents:** Stores test strategies at Feature level, test cases at Story level, Feature integration test plans at Feature level

## Sprint Planning Workflow

### 1. Backlog Grooming

```python
# Get unscheduled stories
backlog = mcp_openproject_query_work_packages(
    project_id={config.openproject.project_id},
    filters=f'[{{"type":{{"operator":"=","values":["{config.openproject.types.user_story}"]}}}},{{"status":{{"operator":"=","values":["{config.openproject.statuses.new}","{config.openproject.statuses.in_specification}","{config.openproject.statuses.specified}","{config.openproject.statuses.confirmed}"]}}}}]'
)
```

### 2. Sprint Assignment

```python
# Move story to sprint
mcp_openproject_update_work_package(
    work_package_id=story_id,
    status_id={config.openproject.statuses.scheduled}  # Use config, not hardcoded ID
)
```

### 3. Task Breakdown

```python
# Create implementation tasks under story
for task_def in story_tasks:
    task = mcp_openproject_create_work_package(
        project_id={config.openproject.project_id},
        subject=task_def["subject"],
        type_id={config.openproject.types.task},
        description=task_def["description"]
    )
    mcp_openproject_set_work_package_parent(
        work_package_id=task["work_package"]["id"],
        parent_id=story_id
    )
```

## Reporting Queries

### Sprint Status

```python
# Get all in-progress work
in_progress = mcp_openproject_list_work_packages(
    project_id={config.openproject.project_id},
    status="open"
)

# Get completed this sprint
completed = mcp_openproject_query_work_packages(
    project_id={config.openproject.project_id},
    filters=f'[{{"status":{{"operator":"=","values":["{config.openproject.statuses.closed}"]}}}},{{"updatedAt":{{"operator":">t-","values":["14"]}}}}]'
)
```

### Blockers

```python
# Find blocked items
blocked = mcp_openproject_query_work_packages(
    project_id={config.openproject.project_id},
    filters=f'[{{"status":{{"operator":"=","values":["{config.openproject.statuses.on_hold}"]}}}}]'
)

# Find items with blocking relations
relations = mcp_openproject_list_work_package_relations(
    relation_type="blocked"
)
```

## Best Practices

### 1. Always Use Full Work Package Cycle

- Never code without checking current work packages
- Always update status when starting/completing work
- Document blockers and decisions in comments

### 2. Maintain Hierarchy

- Features should always link to Epics (if Features are used)
- Stories should always link to Features (if Features exist) or Epics (if no Features)
- Tasks should always link to Stories
- Bugs should always link to Stories
- Use consistent naming: 
  - "Epic N:", 
  - "Feature N.F:" (if Features exist), 
  - "Story N.M:" or "Story N.F.M:" (if under Feature), 
  - "Task N.M.P:" or "Task N.F.M.P:" (if Story is under Feature),
  - "Bug: [Description]"

### 3. Keep Acceptance Criteria Complete

- Include full Given/When/Then statements
- Link to technical specifications
- Include test requirements

### 4. Use Comments for Context

```python
mcp_openproject_add_work_package_comment(
    work_package_id=task_id,
    comment="Implementation decision: Using approach X because...",
    notify=True
)
```

### 5. Log Time for Planning

```python
mcp_openproject_log_time(
    work_package_id=task_id,
    hours=2.5,
    comment="Implemented feature X"
)
```
