# BMAD BMM Workflow: epic-story-lifecycle

**Workflow Type:** Epic and Story Lifecycle Management  
**Agent:** PM (Product Manager), SM (Scrum Master), Dev, Test Team  
**Phase:** All Phases  
**Status:** MANDATORY WORKFLOW

## Purpose

Define the complete lifecycle management for Epics, Features, Stories, Tasks, and Bugs in OpenProject, including status transitions, documentation requirements, and quality gates. This workflow ensures proper hierarchy, comprehensive documentation, and automated status transitions.

---

## OpenProject Status Reference

**Available Statuses (from OpenProject):**

The following statuses are available for all work package types. **CRITICAL:** Query OpenProject to get actual status IDs using `mcp_openproject_list_statuses()` and update `project-config.yaml` with actual values.

| Status Name | Usage | Typical Flow Position |
|-------------|-------|----------------------|
| **New** | Initial state when work package is created | Start of journey |
| **In specification** | Requirements being defined/refined | Optional planning phase |
| **Specified** | Requirements complete and approved | Optional planning phase |
| **In progress** | Active development/work in progress | Main development phase |
| **Developed** | Code/implementation complete | After development, before testing |
| **In testing** | Under review/testing/validation | Testing phase |
| **Tested** | Testing complete and passed | After successful testing |
| **Test failed** | Testing failed, needs rework | Error path |
| **Closed** | Complete and done | End of successful journey |
| **On hold** | Paused/temporarily stopped | Optional pause state |
| **Rejected** | Cancelled/not proceeding | Optional cancellation |

**Status ID Configuration:**

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

**Note:** All code examples in this document use `config.openproject.statuses.{status_name}` to reference status IDs. Replace placeholders with actual IDs from OpenProject.

---

## Work Package Hierarchy

```
Project
└── Epic (type_id=40)
    └── Feature (type_id=39, if present) [OPTIONAL but RECOMMENDED for new epics]
        └── User Story (type_id=41)
            └── Task (type_id=36) / Bug (type_id=42)
```

**CRITICAL:** Maintain this hierarchy using OpenProject parent-child relationships.

**Note on Features:**
- Features are **recommended** for breaking down epics into sizable, testable chunks
- For **new epics going forward**, use Features when appropriate
- For **existing epics**, do NOT retroactively create Features (to avoid wasting time)

---

## EPIC Requirements

### 1. Epic Creation and Documentation

**CRITICAL: DUPLICATE PREVENTION** - Before creating an Epic, **ALWAYS check if it already exists** in OpenProject. If it exists, update the existing Epic instead of creating a duplicate.

**Requirement:** Every Epic MUST have:

- **High-Level Description:** Business goal, scope, success criteria, dependencies, technical considerations, timeline
- **Story Breakdown:** Complete list of all stories with goals and dependencies
- **Test Story (MANDATORY):** A dedicated test story (Story X.T) for validating the complete epic
- **Design Document:** High-level design and implementation document attached to the epic
- **Incremental Development:** Epic must be structured so each story can be verified with previously implemented work, not dependent on future work that would block verification

**CRITICAL:** Every Epic MUST include a Test Story (Story X.T) that validates the complete Epic functionality. This story is created during Epic creation and must be completed before the Epic can be closed.

**CRITICAL: INCREMENTAL DEVELOPMENT** - Epic stories MUST be structured incrementally:
- Each story can be verified with previously implemented work
- Stories are NOT dependent on future work that would block verification
- Dependencies flow forward only (Story N can depend on Story N-1, N-2, etc., but NOT on Story N+1)
- Foundation stories setup only what's needed for immediate next stories, not everything upfront

**Implementation:**

```python
# CRITICAL: Check for existing Epic before creating
def check_existing_epic(project_id: int, epic_subject: str) -> dict | None:
    """
    Check if Epic already exists in OpenProject.
    Returns existing Epic if found, None otherwise.
    """
    # List all epics in project (including closed)
    epics = mcp_openproject_list_work_packages(
        project_id=project_id,
        filters=json.dumps([
            {"type": {"operator": "=", "values": [config.openproject.types.epic]}}
        ]),
        status="all"  # Include closed epics
    )
    
    # Check for matching subject (case-insensitive, partial match for similar names)
    for epic in epics.get("work_packages", []):
        if epic_subject.lower() in epic["subject"].lower() or epic["subject"].lower() in epic_subject.lower():
            return epic
    
    return None

# Check if Epic already exists
epic_subject = "Epic X: [Epic Name]"
existing_epic = check_existing_epic(project_id=8, epic_subject=epic_subject)

if existing_epic:
    # Update existing Epic instead of creating duplicate
    epic_id = existing_epic["id"]
    epic = mcp_openproject_update_work_package(
        work_package_id=epic_id,
        description="""
        ## Business Goal
        [Updated statement of business value]
        
        ## Scope
        **Included:** [Updated features included]
        **Excluded:** [Updated features explicitly excluded]
        
        ## Success Criteria
        - [Updated measurable success criteria]
        
        ## Story Breakdown
        ### Story X.1: [Story Name]
        **Goal:** [What this story accomplishes]
        **Dependencies:** [Other stories or systems]
        
        ### Story X.T: Epic X Testing and Validation
        **Goal:** Validate complete epic functionality
        **Test Document:** epic-X-test-plan.md
        """
    )
    print(f"Updated existing Epic {epic_id}: {epic_subject}")
else:
    # Create new Epic with comprehensive description
    epic = mcp_openproject_create_work_package(
        project_id=8,
        subject=epic_subject,
        type_id=40,  # Epic
    description="""
    ## Business Goal
    [Clear statement of business value]
    
    ## Scope
    **Included:** [Features included]
    **Excluded:** [Features explicitly excluded]
    
    ## Success Criteria
    - [Measurable success criteria]
    
    ## Story Breakdown
    ### Story X.1: [Story Name]
    **Goal:** [What this story accomplishes]
    **Dependencies:** [Other stories or systems]
    
    ### Story X.T: Epic X Testing and Validation
    **Goal:** Validate complete epic functionality
    **Test Document:** epic-X-test-plan.md
    """,
    priority_id=74  # High
)

# Attach design document
mcp_openproject_add_work_package_attachment(
    work_package_id=epic["work_package"]["id"],
    file_data=base64_encoded_design_doc,
    filename="epic-X-design.md",
    content_type="text/markdown",
    description="Epic X Design and Implementation Document"
)

# MANDATORY: Create Test Story (Story X.T) for Epic
# This must be created when creating the Epic or during Epic grooming
test_story = mcp_openproject_create_work_package(
    project_id=8,
    subject="Story X.T: Epic X Testing and Validation",  # MANDATORY Test Story
    type_id=41,  # User Story
    description="""
    As a **Test Team**,
    I want **to validate the complete Epic X functionality**,
    So that **I can ensure all stories work together and the Epic meets its acceptance criteria**.
    
    **Acceptance Criteria:**
    - **Given** all stories in Epic X are implemented
    - **When** I run Epic-level integration tests
    - **Then** all Epic acceptance criteria are met
    - **And** all cross-story integration points work correctly
    - **And** end-to-end Epic functionality is validated
    
    **Test Activities:**
    1. Create Epic test plan: `epic-X-test-plan.md`
    2. Attach test plan to Epic X
    3. Run Epic-level integration tests
    4. Validate all Epic acceptance criteria
    5. Test cross-story integration points
    6. Run end-to-end Epic functionality tests
    """,
    priority_id=74  # High
)
mcp_openproject_set_work_package_parent(
    work_package_id=test_story["work_package"]["id"],
    parent_id=epic_id
)
```

### 2. Epic Status Transitions

**Rule:** Epic status transitions are **IMMEDIATE** when conditions are met.

**Complete Epic Journey:**

```
New
  ↓ (PM creates epic with design doc)
In specification (optional - if requirements need refinement)
  ↓ [QUALITY GATE: Required artifacts attached - see Specification Quality Gates]
Specified (optional - if requirements need approval)
  ↓
[First story → "In progress"] → Epic → "In progress"
  ↓ (Active development)
[Last story → "Closed"] → Epic → "Closed"
```

**Status Transition Table:**

| When | Epic Status | Action Owner | MCP Tool Call | Notes |
|------|-------------|--------------|---------------|-------|
| Created | "New" | PM | `mcp_openproject_create_work_package(..., status_id={STATUS_NEW})` | Initial state |
| Requirements refinement | "In specification" | PM | `mcp_openproject_update_work_package(work_package_id=epic_id, status_id={STATUS_IN_SPECIFICATION})` | Optional - PM responsible for grooming |
| Requirements complete | "Specified" | PM | `mcp_openproject_update_work_package(work_package_id=epic_id, status_id={STATUS_SPECIFIED})` | **QUALITY GATE:** SM must verify required artifacts before allowing transition |
| First story → "In progress" | Epic → "In progress" | PM/Dev | `mcp_openproject_update_work_package(work_package_id=epic_id, status_id={STATUS_IN_PROGRESS})` | **IMMEDIATE** |
| Last story → "Closed" | Epic → "Closed" | Test Team | `mcp_openproject_update_work_package(work_package_id=epic_id, status_id={STATUS_CLOSED})` | **IMMEDIATE** |
| Paused | "On hold" | PM/SM | `mcp_openproject_update_work_package(work_package_id=epic_id, status_id={STATUS_ON_HOLD})` | Optional |
| Cancelled | "Rejected" | PM | `mcp_openproject_update_work_package(work_package_id=epic_id, status_id={STATUS_REJECTED})` | Optional |

**Note:** Replace `{STATUS_XXX}` placeholders with actual status IDs from OpenProject (query via `mcp_openproject_list_statuses()`).

**Implementation:**

```python
def update_epic_status_based_on_stories(epic_id: int):
    """
    Update epic status based on story statuses.
    Called IMMEDIATELY when story status changes.
    CRITICAL: Every Epic MUST have a Test Story (Story X.T).
    """
    # Get all stories for epic
    children = mcp_openproject_get_work_package_children(
        parent_id=epic_id,
        status="all"  # Include closed stories
    )
    stories = [c for c in children.get("children", []) if c["type"] == "User story"]
    
    if not stories:
        return
    
    # CRITICAL: Check if Epic has Test Story
    test_story = next((s for s in stories if "T" in s["subject"] or "test" in s["subject"].lower() and ("epic" in s["subject"].lower() or "validation" in s["subject"].lower())), None)
    
    # Get status IDs from config (replace with actual IDs from OpenProject)
    STATUS_IN_PROGRESS = config.openproject.statuses.in_progress
    STATUS_CLOSED = config.openproject.statuses.closed
    
    # Check if any story is in progress
    any_in_progress = any(s["status"]["id"] == STATUS_IN_PROGRESS for s in stories)
    if any_in_progress:
        epic = mcp_openproject_get_work_package(work_package_id=epic_id)
        if epic["work_package"]["status"]["id"] != STATUS_IN_PROGRESS:
            mcp_openproject_update_work_package(
                work_package_id=epic_id,
                status_id=STATUS_IN_PROGRESS  # "In progress"
            )
    
    # Check if all stories are closed (including Test Story)
    all_closed = all(s["status"]["id"] == STATUS_CLOSED for s in stories)
    
    # CRITICAL: Epic can only be closed if:
    # 1. Test Story exists
    # 2. All stories (including Test Story) are closed
    if all_closed:
        if not test_story:
            # Epic cannot be closed without Test Story
            mcp_openproject_add_work_package_comment(
                work_package_id=epic_id,
                comment="⚠️ BLOCKER: Epic cannot be closed. Missing Test Story (Story X.T). PM must create Test Story before Epic can be closed.",
                notify=True
            )
            return  # Do not close epic - Test Story is mandatory
        
        # Verify Test Story is also closed
        test_story_closed = test_story["status"]["id"] == STATUS_CLOSED
        if not test_story_closed:
            mcp_openproject_add_work_package_comment(
                work_package_id=epic_id,
                comment=f"⚠️ BLOCKER: Epic cannot be closed. Test Story '{test_story['subject']}' is not closed. Test Story must be completed and closed before Epic can be closed.",
                notify=True
            )
            return  # Do not close epic - Test Story must be closed first
        
        epic = mcp_openproject_get_work_package(work_package_id=epic_id)
        if epic["work_package"]["status"]["id"] != STATUS_CLOSED:
            mcp_openproject_update_work_package(
                work_package_id=epic_id,
                status_id=STATUS_CLOSED  # "Closed"
            )
```

---

## FEATURE Requirements

### 1. Feature Creation and Documentation

**CRITICAL: DUPLICATE PREVENTION** - Before creating a Feature, **ALWAYS check if it already exists** under the parent Epic in OpenProject. If it exists, update the existing Feature instead of creating a duplicate.

**Requirement:** Every Feature MUST have:

- **Description:** Functional capability description with clear scope
- **Architecture Document:** Feature-level architecture and technical design attached
- **Story Breakdown:** Complete list of all stories under this feature with goals and dependencies
- **Integration Test Story:** A dedicated integration test story (Story X.Y.T) for validating the complete Feature
- **Parent Relationship:** Linked to Epic (parent)

**CRITICAL:** Every Feature MUST include an Integration Test Story (Story X.Y.T) that validates the complete Feature functionality. This story is created during Feature grooming and must be completed before the Feature can be closed.

**Implementation:**

```python
# CRITICAL: Check for existing Feature before creating
def check_existing_feature(epic_id: int, feature_subject: str) -> dict | None:
    """
    Check if Feature already exists under Epic in OpenProject.
    Returns existing Feature if found, None otherwise.
    """
    # Get all children of Epic (including closed)
    children = mcp_openproject_get_work_package_children(
        parent_id=epic_id,
        status="all"  # Include closed features
    )
    
    # Check for matching Feature by subject
    for child in children.get("children", []):
        if child["type"] == "Feature":
            if feature_subject.lower() in child["subject"].lower() or child["subject"].lower() in feature_subject.lower():
                return child
    
    return None

# Check if Feature already exists
feature_subject = "Feature: [Feature Name]"
existing_feature = check_existing_feature(epic_id=epic_id, feature_subject=feature_subject)

if existing_feature:
    # Update existing Feature instead of creating duplicate
    feature_id = existing_feature["id"]
    feature = mcp_openproject_update_work_package(
        work_package_id=feature_id,
        description="""
        ## Functional Capability
        [Updated statement of what this feature provides]
        
        ## Scope
        **Included:** [Updated stories and functionality included]
        **Excluded:** [Updated functionality explicitly excluded]
        
        ## Story Breakdown
        ### Story X.Y.1: [Story Name]
        **Goal:** [What this story accomplishes]
        **Dependencies:** [Other stories or systems]
        
        ## Technical Considerations
        [Updated architecture decisions, technical constraints, integration points]
        """
    )
    print(f"Updated existing Feature {feature_id}: {feature_subject}")
else:
    # Create new Feature with comprehensive description
    feature = mcp_openproject_create_work_package(
        project_id=8,
        subject=feature_subject,
        type_id=39,  # Feature
    description="""
    ## Functional Capability
    [Clear statement of what this feature provides]
    
    ## Scope
    **Included:** [Stories and functionality included]
    **Excluded:** [Functionality explicitly excluded]
    
    ## Story Breakdown
    ### Story X.Y.1: [Story Name]
    **Goal:** [What this story accomplishes]
    **Dependencies:** [Other stories or systems]
    
    ## Technical Considerations
    [Architecture decisions, technical constraints, integration points]
    """,
    priority_id=74  # High
)

# Set parent relationship to Epic
mcp_openproject_set_work_package_parent(
    work_package_id=feature["work_package"]["id"],
    parent_id=epic_id
)

# Attach architecture document
mcp_openproject_add_work_package_attachment(
    work_package_id=feature["work_package"]["id"],
    file_data=base64_encoded_arch_doc,
    filename="feature-X-architecture.md",
    content_type="text/markdown",
    description="Feature Architecture and Technical Design"
)

# MANDATORY: Create Integration Test Story (Story X.Y.T) for Feature
# This must be created when creating the Feature or during Feature grooming
integration_test_story = mcp_openproject_create_work_package(
    project_id=8,
    subject="Story X.Y.T: Feature X.Y Integration Testing and Validation",  # MANDATORY Integration Test Story
    type_id=41,  # User Story
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
    priority_id=74  # High
)
mcp_openproject_set_work_package_parent(
    work_package_id=integration_test_story["work_package"]["id"],
    parent_id=feature_id
)
```

### 2. Feature Status Transitions

**Rule:** Feature status transitions are **IMMEDIATE** when conditions are met. **CRITICAL:** Features require integration testing at the Feature level before closure.

**Complete Feature Journey:**

```
New
  ↓ (PM creates feature with architecture doc)
In specification (optional - if requirements need refinement)
  ↓
Specified (optional - if requirements need approval)
  ↓
[First story → "In progress"] → Feature → "In progress"
  ↓ (Active development - stories being worked on)
[All stories → "Closed"] → Feature → "In testing" (AUTOMATIC - Integration testing phase)
  ↓ (Test Team runs Feature-level integration tests)
[Integration tests pass] → Feature → "Tested"
  ↓ (Feature validated)
Feature → "Closed"
```

**Alternative Paths:**
- If integration tests fail: "In testing" → "Test failed" → Fix issues → "In progress" → Stories updated → "In testing" → Repeat until "Tested" → "Closed"
- If paused: Any status → "On hold" → Resume → Continue journey
- If cancelled: Any status → "Rejected"

**Status Transition Table:**

| When | Feature Status | Action Owner | MCP Tool Call | Notes |
|------|---------------|--------------|---------------|-------|
| Created | "New" | PM | `mcp_openproject_create_work_package(..., status_id={STATUS_NEW})` | Initial state |
| Requirements refinement | "In specification" | PM | `mcp_openproject_update_work_package(work_package_id=feature_id, status_id={STATUS_IN_SPECIFICATION})` | Optional - PM responsible for grooming |
| Requirements complete | "Specified" | PM | `mcp_openproject_update_work_package(work_package_id=feature_id, status_id={STATUS_SPECIFIED})` | **QUALITY GATE:** SM must verify required artifacts before allowing transition |
| First story → "In progress" | Feature → "In progress" | PM/Dev | `mcp_openproject_update_work_package(work_package_id=feature_id, status_id={STATUS_IN_PROGRESS})` | **IMMEDIATE** |
| All stories → "Closed" | Feature → "In testing" | Test Team | `mcp_openproject_update_work_package(work_package_id=feature_id, status_id={STATUS_IN_TESTING})` | **IMMEDIATE** - Integration testing required |
| Integration tests pass | Feature → "Tested" | Test Team | `mcp_openproject_update_work_package(work_package_id=feature_id, status_id={STATUS_TESTED})` | Integration tests validated |
| Feature validated | Feature → "Closed" | Test Team | `mcp_openproject_update_work_package(work_package_id=feature_id, status_id={STATUS_CLOSED})` | Feature complete |
| Integration tests fail | Feature → "Test failed" | Test Team | `mcp_openproject_update_work_package(work_package_id=feature_id, status_id={STATUS_TEST_FAILED})` | Creates issues, returns to "In progress" |
| Paused | "On hold" | PM/SM | `mcp_openproject_update_work_package(work_package_id=feature_id, status_id={STATUS_ON_HOLD})` | Optional |
| Cancelled | "Rejected" | PM | `mcp_openproject_update_work_package(work_package_id=feature_id, status_id={STATUS_REJECTED})` | Optional |

**Note:** Replace `{STATUS_XXX}` placeholders with actual status IDs from OpenProject (query via `mcp_openproject_list_statuses()`).

### 3. Feature Specification Quality Gates

**CRITICAL:** Before a Feature can transition from "In specification" to "Specified", the following artifacts MUST be attached to the Feature work package in OpenProject:

**Required Artifacts for Feature "Specified" Status:**

1. ✅ **Feature Architecture Document** (`feature-X-architecture.md`)
   - Feature-specific architecture design
   - Technical design decisions
   - Integration points and dependencies
   - Data models and schemas (if applicable)

2. ✅ **API Documentation** (if Feature includes APIs)
   - API endpoint specifications
   - Request/response schemas
   - Authentication/authorization requirements
   - API versioning strategy

3. ✅ **UI Mocks/Designs** (if Feature includes UI components)
   - UI mockups (images: PNG, JPG, or design files)
   - User interaction flows
   - Responsive design specifications
   - Accessibility requirements

4. ✅ **Feature Scope Document**
   - Included functionality
   - Excluded functionality
   - Story breakdown with dependencies

**Protocol Enforcement:**

- **PM Responsibility:** Create and attach all required artifacts during Feature grooming
- **SM Accountability:** Verify all required artifacts are attached before allowing Feature to transition to "Specified" status
- **Enforcement Method:** SM must check OpenProject attachments using `mcp_openproject_list_work_package_attachments(work_package_id=feature_id)` before approving status transition
- **Artifact Validation:** SM must verify:
  - Architecture document exists and is complete
  - API documentation exists (if APIs are part of Feature)
  - UI mocks exist (if UI is part of Feature)
  - All artifacts are properly attached to Feature work package

**Implementation:**

```python
def verify_feature_specification_artifacts(feature_id: int) -> bool:
    """
    Verify that all required artifacts are attached to Feature before allowing "Specified" status.
    Called by SM before approving Feature status transition from "In specification" to "Specified".
    
    Returns:
        bool: True if all required artifacts are present, False otherwise
    """
    # Get all attachments for Feature
    attachments = mcp_openproject_list_work_package_attachments(work_package_id=feature_id)
    attachment_names = [a["fileName"] for a in attachments.get("attachments", [])]
    
    # Check for required artifacts
    has_architecture = any("architecture" in name.lower() for name in attachment_names)
    has_api_doc = any("api" in name.lower() and ("doc" in name.lower() or "spec" in name.lower()) for name in attachment_names)
    has_ui_mocks = any(name.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".fig", ".sketch")) or "mock" in name.lower() or "design" in name.lower() for name in attachment_names)
    
    # Get Feature to check if it includes APIs or UI
    feature = mcp_openproject_get_work_package(work_package_id=feature_id)
    description = feature["work_package"].get("description", {}).get("raw", "").lower()
    
    requires_api = "api" in description or "endpoint" in description or "rest" in description
    requires_ui = "ui" in description or "user interface" in description or "frontend" in description or "interface" in description
    
    # Validate required artifacts
    if not has_architecture:
        return False, "Missing: Feature architecture document"
    
    if requires_api and not has_api_doc:
        return False, "Missing: API documentation (Feature includes APIs)"
    
    if requires_ui and not has_ui_mocks:
        return False, "Missing: UI mocks/designs (Feature includes UI)"
    
    return True, "All required artifacts present"

# Usage by SM before approving Feature "Specified" status:
is_valid, message = verify_feature_specification_artifacts(feature_id=123)
if not is_valid:
    # Block status transition, inform PM
    raise ValueError(f"Cannot transition Feature to 'Specified': {message}")
else:
    # Allow status transition
    mcp_openproject_update_work_package(
        work_package_id=feature_id,
        status_id=config.openproject.statuses.specified
    )
```

**Implementation:**

```python
def update_feature_status_based_on_stories(feature_id: int):
    """
    Update feature status based on story statuses.
    Called IMMEDIATELY when story status changes.
    CRITICAL: Features require integration testing before closure.
    CRITICAL: Every Feature MUST have an Integration Test Story (Story X.Y.T).
    """
    # Get all stories for feature
    children = mcp_openproject_get_work_package_children(
        parent_id=feature_id,
        status="all"  # Include closed stories
    )
    stories = [c for c in children.get("children", []) if c["type"] == "User story"]
    
    if not stories:
        return
    
    # CRITICAL: Check if Feature has Integration Test Story
    integration_test_story = next((s for s in stories if "T" in s["subject"] or "integration test" in s["subject"].lower() or "test" in s["subject"].lower() and "integration" in s["subject"].lower()), None)
    if not integration_test_story:
        # Feature cannot proceed without Integration Test Story
        feature = mcp_openproject_get_work_package(work_package_id=feature_id)
        current_status = feature["work_package"]["status"]["id"]
        STATUS_IN_PROGRESS = config.openproject.statuses.in_progress
        
        # Only warn if Feature is in progress or later - allow creation phase
        if current_status == STATUS_IN_PROGRESS:
            mcp_openproject_add_work_package_comment(
                work_package_id=feature_id,
                comment="⚠️ BLOCKER: Feature cannot be closed. Missing Integration Test Story (Story X.Y.T). PM must create Integration Test Story before Feature can be closed.",
                notify=True
            )
        return  # Do not proceed with status updates - Integration Test Story is mandatory
    
    # Get status IDs from config (replace with actual IDs from OpenProject)
    STATUS_IN_PROGRESS = config.openproject.statuses.in_progress
    STATUS_IN_TESTING = config.openproject.statuses.in_testing
    STATUS_CLOSED = config.openproject.statuses.closed
    
    # Get current feature status
    feature = mcp_openproject_get_work_package(work_package_id=feature_id)
    current_status = feature["work_package"]["status"]["id"]
    
    # Check if any story is in progress
    any_in_progress = any(s["status"]["id"] == STATUS_IN_PROGRESS for s in stories)
    if any_in_progress:
        if current_status != STATUS_IN_PROGRESS:
            mcp_openproject_update_work_package(
                work_package_id=feature_id,
                status_id=STATUS_IN_PROGRESS  # "In progress"
            )
        return  # Don't proceed to testing if stories are still in progress
    
    # Check if all stories are closed
    all_closed = all(s["status"]["id"] == STATUS_CLOSED for s in stories)
    if all_closed:
        # CRITICAL: Feature must go to "In testing" for integration tests before closure
        if current_status not in [STATUS_IN_TESTING, STATUS_TESTED, STATUS_CLOSED]:
            mcp_openproject_update_work_package(
                work_package_id=feature_id,
                status_id=STATUS_IN_TESTING  # "In testing" - Integration testing required
            )
        # Note: Feature closure ("Closed") is MANUAL by Test Team after integration tests pass
        # Do NOT automatically close feature - Test Team must validate integration tests first
```

### 3. Feature Integration Testing Requirements

**CRITICAL:** Every Feature MUST undergo Feature-level integration testing before closure.

**CRITICAL: LIVE SYSTEMS REQUIRED** - Integration tests MUST use live systems, NOT mocks or fixtures:
- **Unit tests** can use mocks and fixtures
- **Integration tests** MUST use live, running systems
- If a live system dependency is not available, **IMMEDIATELY flag and stop tests**
- Create infrastructure stories/epics to start unavailable dependencies
- Do NOT bypass or skip integration tests due to missing dependencies

**Integration Test Requirements:**

1. **Test Document:** Create `feature-X-integration-test-plan.md` attached to Feature
2. **Test Coverage:**
   - All stories within Feature work together
   - Cross-story integration points validated
   - Feature-level acceptance criteria met
   - End-to-end Feature functionality verified
3. **Test Execution:**
   - Run Feature-level integration tests
   - Validate all Feature acceptance criteria
   - Document test results
4. **Test Validation:**
   - If tests pass: Feature → "Tested" → "Closed"
   - If tests fail: Feature → "Test failed" → Create issues → Fix → Return to "In progress" → Stories updated → "In testing"

**Implementation:**

```python
# When all stories are closed, Feature automatically goes to "In testing"
# Test Team then runs integration tests

def check_live_system_dependencies(feature_id: int) -> tuple[bool, list[str]]:
    """
    Check if all live system dependencies required for Feature integration tests are available.
    
    Returns:
        tuple: (all_available: bool, missing_dependencies: list[str])
    """
    feature = mcp_openproject_get_work_package(work_package_id=feature_id)
    description = feature["work_package"].get("description", {}).get("raw", "").lower()
    
    # Identify required dependencies from Feature description
    required_deps = []
    missing_deps = []
    
    # Common dependency patterns
    if "database" in description or "postgres" in description or "mysql" in description:
        required_deps.append("database")
    if "redis" in description or "cache" in description:
        required_deps.append("redis")
    if "api" in description or "service" in description:
        required_deps.append("api_service")
    if "minio" in description or "s3" in description or "storage" in description:
        required_deps.append("object_storage")
    
    # Check each dependency (implement actual health checks)
    for dep in required_deps:
        if not check_dependency_health(dep):
            missing_deps.append(dep)
    
    return len(missing_deps) == 0, missing_deps

def check_dependency_health(dependency: str) -> bool:
    """
    Check if a live system dependency is healthy and available.
    Returns True if available, False otherwise.
    """
    # Implement actual health checks based on dependency type
    # This is a placeholder - implement actual checks
    try:
        if dependency == "database":
            # Check database connection
            return check_database_connection()
        elif dependency == "redis":
            # Check Redis connection
            return check_redis_connection()
        elif dependency == "api_service":
            # Check API service health
            return check_api_service_health()
        elif dependency == "object_storage":
            # Check object storage availability
            return check_object_storage_availability()
        return True
    except Exception:
        return False

def run_feature_integration_tests(feature_id: int):
    """
    Run Feature-level integration tests.
    Called by Test Team when Feature is in "In testing" status.
    
    CRITICAL: Integration tests MUST use live systems. If dependencies are unavailable,
    tests are stopped and infrastructure work is created.
    """
    feature = mcp_openproject_get_work_package(work_package_id=feature_id)
    
    # Verify Feature is in "In testing" status
    if feature["work_package"]["status"]["id"] != config.openproject.statuses.in_testing:
        raise ValueError("Feature must be in 'In testing' status to run integration tests")
    
    # CRITICAL: Check live system dependencies BEFORE running tests
    all_available, missing_deps = check_live_system_dependencies(feature_id)
    
    if not all_available:
        # STOP tests - dependencies not available
        error_msg = f"⚠️ BLOCKER: Integration tests cannot run. Missing live system dependencies: {', '.join(missing_deps)}. Create infrastructure stories/epics to start these dependencies."
        
        # Add comment to Feature
        mcp_openproject_add_work_package_comment(
            work_package_id=feature_id,
            comment=error_msg,
            notify=True
        )
        
        # Create infrastructure work packages for missing dependencies
        create_infrastructure_work_for_dependencies(feature_id, missing_deps)
        
        # Raise error to stop test execution
        raise ValueError(error_msg)
    
    # All dependencies available - proceed with integration tests
    test_results = run_integration_test_suite(feature_id)
    
    if test_results.all_passed:
        # Update Feature to "Tested"
        mcp_openproject_update_work_package(
            work_package_id=feature_id,
            status_id=config.openproject.statuses.tested  # "Tested"
        )
        
        # Add comment with test results
        mcp_openproject_add_work_package_comment(
            work_package_id=feature_id,
            comment=f"Feature integration tests passed. All {test_results.total_tests} tests passed."
        )
        
        # Feature can now be closed by Test Team
    else:
        # Update Feature to "Test failed"
        mcp_openproject_update_work_package(
            work_package_id=feature_id,
            status_id=config.openproject.statuses.test_failed  # "Test failed"
        )
        
        # Create issues for failed tests
        for failure in test_results.failures:
            create_issue_from_test_failure(feature_id, failure)
        
        # Add comment with test results
        mcp_openproject_add_work_package_comment(
            work_package_id=feature_id,
            comment=f"Feature integration tests failed. {test_results.failed_count}/{test_results.total_tests} tests failed. Issues created."
        )
        
        # Feature returns to "In progress" for fixes
        # Dev fixes issues, updates stories, Feature will return to "In testing" when all stories closed again

def create_infrastructure_work_for_dependencies(feature_id: int, missing_deps: list[str]):
    """
    Create infrastructure stories/epics for missing live system dependencies.
    Called when integration tests are blocked due to unavailable dependencies.
    """
    feature = mcp_openproject_get_work_package(work_package_id=feature_id)
    project_id = feature["work_package"]["project"]["id"]
    
    # Get parent Epic
    epic_id = feature["work_package"].get("parent", {}).get("id")
    if not epic_id:
        # Feature might be directly under project - need to find or create Epic
        epic_id = find_or_create_infrastructure_epic(project_id)
    
    for dep in missing_deps:
        # Check if infrastructure story/epic already exists
        dep_subject = f"Infrastructure: Setup {dep.replace('_', ' ').title()}"
        existing = check_existing_story(epic_id, dep_subject) if epic_id else None
        
        if not existing:
            # Create infrastructure story for dependency
            infra_story = mcp_openproject_create_work_package(
                project_id=project_id,
                subject=dep_subject,
                type_id=config.openproject.types.user_story,
                description=f"""
                As a **DevOps/Infrastructure Team**,
                I want **to set up and start the {dep.replace('_', ' ')} live system**,
                So that **Feature integration tests can run with live dependencies**.
                
                **Acceptance Criteria:**
                - **Given** {dep.replace('_', ' ')} is not running
                - **When** I start the {dep.replace('_', ' ')} service
                - **Then** {dep.replace('_', ' ')} is healthy and available for integration tests
                - **And** health check endpoint returns 200 OK
                - **And** service is accessible from test environment
                
                **Priority:** HIGH - Blocks Feature integration testing
                """,
                status_id=config.openproject.statuses.new,
                priority_id=config.openproject.priorities.high
            )
            
            # Link to Epic
            if epic_id:
                mcp_openproject_set_work_package_parent(
                    work_package_id=infra_story["work_package"]["id"],
                    parent_id=epic_id
                )
            
            # Link to Feature as dependency
            mcp_openproject_create_work_package_relation(
                work_package_id=feature_id,
                target_id=infra_story["work_package"]["id"],
                relation_type="blocks"  # Feature is blocked by infrastructure
            )
            
            print(f"Created infrastructure story for {dep}: {infra_story['work_package']['id']}")

def find_or_create_infrastructure_epic(project_id: int) -> int:
    """
    Find or create an Infrastructure Epic for dependency setup.
    """
    # Check for existing Infrastructure Epic
    epics = mcp_openproject_list_work_packages(
        project_id=project_id,
        filters=json.dumps([
            {"type": {"operator": "=", "values": [config.openproject.types.epic]}},
            {"subject": {"operator": "~", "values": ["Infrastructure"]}}
        ]),
        status="all"
    )
    
    if epics.get("work_packages"):
        return epics["work_packages"][0]["id"]
    
    # Create new Infrastructure Epic
    epic = mcp_openproject_create_work_package(
        project_id=project_id,
        subject="Epic: Infrastructure Setup",
        type_id=config.openproject.types.epic,
        description="""
        ## Business Goal
        Ensure all external dependencies and live systems are available and ready for integration testing.
        
        ## Scope
        **Included:** Database setup, Redis setup, API services, Object storage, External service integrations
        **Excluded:** Application code (handled in feature epics)
        
        ## Success Criteria
        - All required live systems are running and healthy
        - Health checks pass for all dependencies
        - Integration tests can run without blocking
        """,
        status_id=config.openproject.statuses.new,
        priority_id=config.openproject.priorities.high
    )
    
    return epic["work_package"]["id"]
```

---

## STORY Requirements

### 1. Story Creation and Documentation

**CRITICAL: DUPLICATE PREVENTION** - Before creating a Story, **ALWAYS check if it already exists** under the parent Feature (or Epic) in OpenProject. If it exists, update the existing Story instead of creating a duplicate.

**CRITICAL: INCREMENTAL DEVELOPMENT** - Every Story MUST be incremental, meaning:
- Development can be verified with previously implemented work
- Story is NOT dependent on future work that would block verification
- Story can be tested and validated independently of future stories
- Dependencies flow forward only (Story N can depend on Story N-1, N-2, etc., but NOT on Story N+1)

**Requirement:** Every Story MUST have:

- **Well-Written Description:** User story format with acceptance criteria
- **Tasks:** All tasks articulated and detailed (created during grooming)
- **UI Document:** For UI stories, wireframe or UI design document attached
- **Test Task (MANDATORY):** A test task (Task X.Y.T) that includes creating and attaching a Story test document

**CRITICAL:** Every Story MUST have a test task (Task X.Y.T). The Story CANNOT be closed until the test task is completed and closed successfully. This is enforced by the `update_story_status_based_on_tasks()` helper function.

**Implementation:**

```python
# CRITICAL: Check for existing Story before creating
def check_existing_story(parent_id: int, story_subject: str) -> dict | None:
    """
    Check if Story already exists under parent (Feature or Epic) in OpenProject.
    Returns existing Story if found, None otherwise.
    """
    # Get all children of parent (including closed)
    children = mcp_openproject_get_work_package_children(
        parent_id=parent_id,
        status="all"  # Include closed stories
    )
    
    # Check for matching Story by subject
    for child in children.get("children", []):
        if child["type"] == "User story":
            if story_subject.lower() in child["subject"].lower() or child["subject"].lower() in story_subject.lower():
                return child
    
    return None

# Check if Story already exists
story_subject = "Story X.Y: [Story Name]"
parent_id = feature_id  # Or epic_id if no Features
existing_story = check_existing_story(parent_id=parent_id, story_subject=story_subject)

if existing_story:
    # Update existing Story instead of creating duplicate
    story_id = existing_story["id"]
    story = mcp_openproject_update_work_package(
        work_package_id=story_id,
        description="""
        As a **[User Role]**,
        I want **[Updated Functionality]**,
        So that **[Updated Business Value]**.
        
        **Acceptance Criteria:**
        - **Given** [Updated Context]
        - **When** [Updated Action]
        - **Then** [Updated Expected Result]
        """
    )
    print(f"Updated existing Story {story_id}: {story_subject}")
else:
    # Create new Story with comprehensive description
    story = mcp_openproject_create_work_package(
        project_id=8,
        subject=story_subject,
        type_id=41,  # User Story
    description="""
    As a **[User Role]**,
    I want **[Functionality]**,
    So that **[Business Value]**.
    
    **Acceptance Criteria:**
    - **Given** [Context]
    - **When** [Action]
    - **Then** [Expected Result]
    """,
    priority_id=73  # Normal
)

# For UI stories, attach wireframe/UI document
if is_ui_story:
    mcp_openproject_add_work_package_attachment(
        work_package_id=story["work_package"]["id"],
        file_data=base64_encoded_ui_doc,
        filename="story-X-Y-ui-design.md",
        content_type="text/markdown",
        description="Story X.Y UI Design and Wireframe"
    )

# MANDATORY: Create test task (Task X.Y.T) for Story
# This must be created during story grooming
test_task = mcp_openproject_create_work_package(
    project_id=8,
    subject="Task X.Y.T: Story X.Y Testing and Validation",  # MANDATORY test task
    type_id=36,  # Task
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
    priority_id=74  # High priority - required for story closure
)
mcp_openproject_set_work_package_parent(
    work_package_id=test_task["work_package"]["id"],
    parent_id=story["work_package"]["id"]
)
```

### 2. Story Status Transitions

**Rule:** Story status transitions are **IMMEDIATE** when conditions are met.

**Complete Story Journey:**

```
New
  ↓ (PM creates story with acceptance criteria)
In specification (optional - if requirements need refinement)
  ↓
Specified (optional - if requirements need approval)
  ↓
[First task → "In progress"] → Story → "In progress"
  ↓ (Dev implements tasks)
[All implementation tasks → "Developed"] → Story remains "In progress"
  ↓
[Test task → "In testing" + all other tasks "Closed"] → Story → "In testing"
  ↓ (Test Team validates)
[All tasks + bugs "Closed"] → Story → "Closed"
```

**Status Transition Table:**

| When | Story Status | Action Owner | MCP Tool Call | Notes |
|------|-------------|--------------|---------------|-------|
| Created | "New" | PM | `mcp_openproject_create_work_package(..., status_id={STATUS_NEW})` | Initial state |
| Requirements refinement | "In specification" | PM | `mcp_openproject_update_work_package(work_package_id=story_id, status_id={STATUS_IN_SPECIFICATION})` | Optional - PM responsible for grooming |
| Requirements complete | "Specified" | PM | `mcp_openproject_update_work_package(work_package_id=story_id, status_id={STATUS_SPECIFIED})` | **QUALITY GATE:** SM must verify required artifacts before allowing transition |
| First task → "In progress" | Story → "In progress" | Dev | `mcp_openproject_update_work_package(work_package_id=story_id, status_id={STATUS_IN_PROGRESS})` | **IMMEDIATE** |
| Test task → "In testing" + all other tasks "Closed" | Story → "In testing" | Dev | `mcp_openproject_update_work_package(work_package_id=story_id, status_id={STATUS_IN_TESTING})` | **IMMEDIATE** |
| All tasks (including test task) + bugs → "Closed" | Story → "Closed" | Dev/Test Team | `mcp_openproject_update_work_package(work_package_id=story_id, status_id={STATUS_CLOSED})` | **IMMEDIATE** - **BLOCKED if test task missing or not closed** |
| Validation fails | "Test failed" | Test Team | `mcp_openproject_update_work_package(work_package_id=story_id, status_id={STATUS_TEST_FAILED})` | Creates bugs |
| Paused | "On hold" | PM/SM | `mcp_openproject_update_work_package(work_package_id=story_id, status_id={STATUS_ON_HOLD})` | Optional |
| Cancelled | "Rejected" | PM | `mcp_openproject_update_work_package(work_package_id=story_id, status_id={STATUS_REJECTED})` | Optional |

**Note:** Replace `{STATUS_XXX}` placeholders with actual status IDs from OpenProject (query via `mcp_openproject_list_statuses()`).

### 3. Story Specification Quality Gates

**CRITICAL:** Before a Story can transition from "In specification" to "Specified", the following artifacts MUST be attached to the Story work package in OpenProject:

**Required Artifacts for Story "Specified" Status:**

1. ✅ **Acceptance Criteria Document** (or in Story description)
   - Complete Given/When/Then statements
   - All acceptance criteria clearly defined
   - Test scenarios identified

2. ✅ **UI Mocks/Designs** (if Story includes UI components)
   - UI mockups (images: PNG, JPG, or design files)
   - User interaction flows
   - Responsive design specifications

3. ✅ **Technical Specifications** (if Story requires technical details)
   - Implementation approach
   - Technical constraints
   - Integration requirements

**Protocol Enforcement:**

- **PM Responsibility:** Create and attach all required artifacts during Story grooming
- **SM Accountability:** Verify all required artifacts are attached before allowing Story to transition to "Specified" status
- **Enforcement Method:** SM must check OpenProject attachments using `mcp_openproject_list_work_package_attachments(work_package_id=story_id)` before approving status transition
- **Artifact Validation:** SM must verify:
  - Acceptance criteria are complete and clear
  - UI mocks exist (if Story includes UI)
  - Technical specifications exist (if Story requires technical details)
  - All artifacts are properly attached to Story work package

**Implementation:**

```python
def verify_story_specification_artifacts(story_id: int) -> bool:
    """
    Verify that all required artifacts are attached to Story before allowing "Specified" status.
    Called by SM before approving Story status transition from "In specification" to "Specified".
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    # Get all attachments for Story
    attachments = mcp_openproject_list_work_package_attachments(work_package_id=story_id)
    attachment_names = [a["fileName"] for a in attachments.get("attachments", [])]
    
    # Get Story to check acceptance criteria and if it includes UI
    story = mcp_openproject_get_work_package(work_package_id=story_id)
    description = story["work_package"].get("description", {}).get("raw", "").lower()
    
    # Check for acceptance criteria (should be in description or attachment)
    has_acceptance_criteria = "given" in description and "when" in description and "then" in description
    has_acceptance_criteria_doc = any("acceptance" in name.lower() or "criteria" in name.lower() for name in attachment_names)
    
    # Check for UI mocks
    has_ui_mocks = any(name.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".fig", ".sketch")) or "mock" in name.lower() or "design" in name.lower() or "ui" in name.lower() for name in attachment_names)
    
    # Check if Story includes UI
    requires_ui = "ui" in description or "user interface" in description or "frontend" in description or "interface" in description or "screen" in description
    
    # Validate required artifacts
    if not (has_acceptance_criteria or has_acceptance_criteria_doc):
        return False, "Missing: Acceptance criteria (must be in description or attached document)"
    
    if requires_ui and not has_ui_mocks:
        return False, "Missing: UI mocks/designs (Story includes UI components)"
    
    return True, "All required artifacts present"

# Usage by SM before approving Story "Specified" status:
is_valid, message = verify_story_specification_artifacts(story_id=456)
if not is_valid:
    # Block status transition, inform PM
    raise ValueError(f"Cannot transition Story to 'Specified': {message}")
else:
    # Allow status transition
    mcp_openproject_update_work_package(
        work_package_id=story_id,
        status_id=config.openproject.statuses.specified
    )
```

**Implementation:**

```python
def update_story_status_based_on_tasks(story_id: int):
    """
    Update story status based on task statuses.
    Called IMMEDIATELY when task status changes.
    """
    # Get all tasks for story
    children = mcp_openproject_get_work_package_children(
        parent_id=story_id,
        status="all"  # Include closed tasks
    )
    tasks = [c for c in children.get("children", []) if c["type"] == "Task"]
    bugs = [c for c in children.get("children", []) if c["type"] == "Bug"]
    
    if not tasks:
        return
    
    # Get status IDs from config (replace with actual IDs from OpenProject)
    STATUS_IN_PROGRESS = config.openproject.statuses.in_progress
    STATUS_IN_TESTING = config.openproject.statuses.in_testing
    STATUS_CLOSED = config.openproject.statuses.closed
    
    # Check if any task is in progress
    any_in_progress = any(t["status"]["id"] == STATUS_IN_PROGRESS for t in tasks)
    if any_in_progress:
        story = mcp_openproject_get_work_package(work_package_id=story_id)
        if story["work_package"]["status"]["id"] != STATUS_IN_PROGRESS:
            mcp_openproject_update_work_package(
                work_package_id=story_id,
                status_id=STATUS_IN_PROGRESS  # "In progress"
            )
    
    # Check if test task is in testing and all other tasks are closed
    test_task = next((t for t in tasks if "T" in t["subject"] or "test" in t["subject"].lower()), None)
    if test_task and test_task["status"]["id"] == STATUS_IN_TESTING:
        other_tasks_closed = all(t["status"]["id"] == STATUS_CLOSED for t in tasks if t["id"] != test_task["id"])
        if other_tasks_closed:
            story = mcp_openproject_get_work_package(work_package_id=story_id)
            if story["work_package"]["status"]["id"] != STATUS_IN_TESTING:
                mcp_openproject_update_work_package(
                    work_package_id=story_id,
                    status_id=STATUS_IN_TESTING  # "In testing"
                )
    
    # CRITICAL: Check if test task exists and is closed
    test_task = next((t for t in tasks if "T" in t["subject"] or "test" in t["subject"].lower() or "verify" in t["subject"].lower()), None)
    if not test_task:
        # Story cannot be closed without a test task
        mcp_openproject_add_work_package_comment(
            work_package_id=story_id,
            comment="⚠️ BLOCKER: Story cannot be closed. Missing test task (Task X.Y.T). PM must create test task before story can be closed.",
            notify=True
        )
        return  # Do not close story - test task is mandatory
    
    # Check if test task is closed
    test_task_closed = test_task["status"]["id"] == STATUS_CLOSED
    if not test_task_closed:
        # Story cannot be closed until test task is closed
        mcp_openproject_add_work_package_comment(
            work_package_id=story_id,
            comment=f"⚠️ BLOCKER: Story cannot be closed. Test task '{test_task['subject']}' is not closed. Test task must be completed and closed before story can be closed.",
            notify=True
        )
        return  # Do not close story - test task must be closed first
    
    # Check if all tasks (including test task) and bugs are closed
    all_tasks_closed = all(t["status"]["id"] == STATUS_CLOSED for t in tasks)
    all_bugs_closed = all(b["status"]["id"] == STATUS_CLOSED for b in bugs) if bugs else True
    
    # CRITICAL: Story can only be closed if:
    # 1. Test task exists AND is closed
    # 2. All other tasks are closed
    # 3. All bugs are closed
    if test_task_closed and all_tasks_closed and all_bugs_closed:
        story = mcp_openproject_get_work_package(work_package_id=story_id)
        if story["work_package"]["status"]["id"] != STATUS_CLOSED:
            mcp_openproject_update_work_package(
                work_package_id=story_id,
                status_id=STATUS_CLOSED  # "Closed"
            )
```

---

## TASK Requirements

### 1. Task Creation (During Story Grooming)

**CRITICAL:** Before creating tasks, **ALWAYS check for existing tasks** to prevent duplicates.

**Requirement:**
- Check for existing tasks using `status="all"` (includes closed tasks)
- Filter by subject to identify duplicates
- Only create tasks that don't already exist

**Implementation:**

```python
def check_existing_tasks(story_id: int) -> list[dict]:
    """
    Check for existing tasks for a story, including closed tasks.
    CRITICAL: Use status="all" to include closed tasks.
    """
    children = mcp_openproject_get_work_package_children(
        parent_id=story_id,
        status="all"  # Include closed tasks
    )
    return children.get("children", [])

def create_story_tasks(story_id: int, tasks: list[dict]):
    """
    Create tasks for a story, checking for duplicates first.
    """
    # Get existing tasks
    existing = check_existing_tasks(story_id)
    existing_subjects = {t["subject"] for t in existing}
    
    # Filter out duplicates
    new_tasks = [
        t for t in tasks
        if t["subject"] not in existing_subjects
    ]
    
    if not new_tasks:
        print(f"No new tasks to create for story {story_id}")
        return
    
    # Create new tasks
    result = mcp_openproject_bulk_create_work_packages(
        project_id=8,
        work_packages=json.dumps(new_tasks),
        continue_on_error=True
    )
    
    # Set parent relationships
    for task in result.get("created", []):
        mcp_openproject_set_work_package_parent(
            work_package_id=task["id"],
            parent_id=story_id
        )
```

### 2. Test Task Requirements

**Requirement:** Every story MUST have a test task named "Task X.Y.T: Story X.Y Testing and Validation".

**Test Task Must:**
- Create a Story test document (`story-X-Y-test-plan.md`)
- Attach the test document to the story
- Validate all acceptance criteria
- Run integration tests

**Implementation:**

```python
# Create test task
test_task = mcp_openproject_create_work_package(
    project_id=8,
    subject="Task X.Y.T: Story X.Y Testing and Validation",
    type_id=36,  # Task
    description="""
    **Test Task for Story X.Y**
    
    **Activities:**
    1. Create Story test document: `story-X-Y-test-plan.md`
    2. Attach test document to Story X.Y
    3. Validate all acceptance criteria
    4. Run integration tests
    5. Document test results
    
    **Test Document Location:** `_bmad-output/planning-artifacts/story-X-Y-test-plan.md`
    """,
    status_id=config.openproject.statuses.new  # "New"
)

# Set parent relationship
mcp_openproject_set_work_package_parent(
    work_package_id=test_task["work_package"]["id"],
    parent_id=story_id
)
```

### 3. Task Status Transitions

**Rule:** Task status transitions are **IMMEDIATE** when conditions are met. Parent Story status MUST be updated immediately when task status changes.

**Complete Task Journey:**

```
New
  ↓ (PM creates task during story grooming)
[Dev starts work] → Task → "In progress"
  ↓ (Dev implements)
[Dev completes implementation] → Task → "Developed"
  ↓ (Dev marks ready for testing)
Task → "In testing"
  ↓ (Test Team validates)
[Validation passes] → Task → "Tested"
  ↓
Task → "Closed"
```

**Alternative Paths:**
- If validation fails: "In testing" → "Test failed" → Create bug → Fix → "In testing" → "Tested" → "Closed"
- If paused: Any status → "On hold" → Resume → Continue journey
- If cancelled: Any status → "Rejected"

**Status Transition Table:**

| When | Task Status | Action Owner | MCP Tool Call | Parent Story Update |
|------|-------------|--------------|---------------|---------------------|
| Created | "New" | PM | `mcp_openproject_create_work_package(..., status_id={STATUS_NEW})` | No update |
| Dev starts work | Task → "In progress" | Dev | `mcp_openproject_update_work_package(work_package_id=task_id, status_id={STATUS_IN_PROGRESS})` | **IMMEDIATELY** call `update_story_status_based_on_tasks(story_id)` |
| Dev completes implementation | Task → "Developed" | Dev | `mcp_openproject_update_work_package(work_package_id=task_id, status_id={STATUS_DEVELOPED})` | No parent update (intermediate state) |
| Dev marks ready for testing | Task → "In testing" | Dev | `mcp_openproject_update_work_package(work_package_id=task_id, status_id={STATUS_IN_TESTING})` | **IMMEDIATELY** call `update_story_status_based_on_tasks(story_id)` |
| Test validates | Task → "Tested" | Test Team | `mcp_openproject_update_work_package(work_package_id=task_id, status_id={STATUS_TESTED})` | No parent update (intermediate state) |
| Task closed | Task → "Closed" | Test Team | `mcp_openproject_update_work_package(work_package_id=task_id, status_id={STATUS_CLOSED})` | **IMMEDIATELY** call `update_story_status_based_on_tasks(story_id)` |
| Test fails | Task → "Test failed" | Test Team | `mcp_openproject_update_work_package(work_package_id=task_id, status_id={STATUS_TEST_FAILED})` | No parent update (bug created instead) |
| Paused | "On hold" | PM/SM | `mcp_openproject_update_work_package(work_package_id=task_id, status_id={STATUS_ON_HOLD})` | No parent update |
| Cancelled | "Rejected" | PM | `mcp_openproject_update_work_package(work_package_id=task_id, status_id={STATUS_REJECTED})` | No parent update |

**Note:** Replace `{STATUS_XXX}` placeholders with actual status IDs from OpenProject (query via `mcp_openproject_list_statuses()`).

**Implementation:**

```python
def update_task_status_and_parent(task_id: int, new_status_id: int):
    """
    Update task status and IMMEDIATELY update parent story status.
    CRITICAL: Always call this function when updating task status.
    """
    # Update task status
    mcp_openproject_update_work_package(
        work_package_id=task_id,
        status_id=new_status_id
    )
    
    # Get task to find parent story
    task = mcp_openproject_get_work_package(work_package_id=task_id)
    parent_id = task["work_package"].get("parent", {}).get("id")
    
    if parent_id:
        # IMMEDIATELY update parent story status
        update_story_status_based_on_tasks(parent_id)

# Usage example:
# When Dev starts task:
update_task_status_and_parent(task_id=123, new_status_id=config.openproject.statuses.in_progress)  # "In progress"

# When Dev marks ready for testing:
update_task_status_and_parent(task_id=123, new_status_id=config.openproject.statuses.in_testing)  # "In testing"

# When Test Team closes task:
update_task_status_and_parent(task_id=123, new_status_id=config.openproject.statuses.closed)  # "Closed"
```

**CRITICAL RULE:** Every task status update MUST trigger immediate parent Story status update. Never update task status without updating parent Story.

---

## BUG Requirements

### 1. Bug Creation and Documentation

**Requirement:** Every Bug MUST have:

- **Detailed Description:** Expected vs actual behavior, steps to reproduce, acceptance criteria violated
- **Parent Relationship:** Linked to Story (parent)
- **Priority:** High (74), Normal (73), or Low (72) based on impact
- **Initial Status:** New (71)
- **Assignment:** Assigned to Dev for fixing

**Implementation:**

```python
# Create Bug with detailed description
bug = mcp_openproject_create_work_package(
    project_id=8,
    subject="Bug: [Brief Description]",
    type_id=42,  # Bug
    description="""
    **Bug Report:**
    
    **Story:** [Story ID and Title]
    **Task:** [Task ID and Title] (if applicable)
    
    **Expected Behavior:**
    [What should happen]
    
    **Actual Behavior:**
    [What actually happens]
    
    **Steps to Reproduce:**
    1. [Step 1]
    2. [Step 2]
    3. [Step 3]
    
    **Acceptance Criteria Violated:**
    - [AC 1]
    - [AC 2]
    
    **Test Results:**
    - Unit tests: [Pass/Fail]
    - Integration tests: [Pass/Fail]
    - Performance tests: [Pass/Fail]
    
    **Environment:**
    - [Environment details if relevant]
    """,
    status_id=config.openproject.statuses.new,  # "New"
    priority_id=73  # Normal (adjust based on impact)
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

### 2. Bug Status Transitions

**Rule:** Bug status transitions follow validation workflow. Parent Story status MUST be checked when bug status changes.

**Complete Bug Journey:**

```
New
  ↓ (Test Team creates bug from validation failure)
[Dev starts fix] → Bug → "In progress"
  ↓ (Dev investigates and fixes)
[Dev completes fix] → Bug → "Developed"
  ↓ (Dev marks ready for testing)
Bug → "In testing"
  ↓ (Test Team validates fix)
[Validation passes] → Bug → "Tested"
  ↓
Bug → "Closed"
```

**Alternative Paths:**
- If validation fails: "In testing" → "Test failed" → Dev fixes again → "In progress" → "Developed" → "In testing" → Repeat until "Closed"
- If paused: Any status → "On hold" → Resume → Continue journey
- If duplicate/invalid: Any status → "Rejected"

**Status Transition Table:**

| When | Bug Status | Action Owner | MCP Tool Call | Parent Story Impact |
|------|-----------|--------------|---------------|---------------------|
| Created | "New" | Test Team | `mcp_openproject_create_work_package(..., status_id={STATUS_NEW})` | Story remains in current status |
| Dev starts fix | "In progress" | Dev | `mcp_openproject_update_work_package(work_package_id=bug_id, status_id={STATUS_IN_PROGRESS})` | No parent update |
| Dev completes fix | "Developed" | Dev | `mcp_openproject_update_work_package(work_package_id=bug_id, status_id={STATUS_DEVELOPED})` | No parent update (intermediate state) |
| Dev marks ready for testing | "In testing" | Dev | `mcp_openproject_update_work_package(work_package_id=bug_id, status_id={STATUS_IN_TESTING})` | No parent update |
| Test validates fix | "Tested" | Test Team | `mcp_openproject_update_work_package(work_package_id=bug_id, status_id={STATUS_TESTED})` | No parent update (intermediate state) |
| Bug closed | "Closed" | Test Team | `mcp_openproject_update_work_package(work_package_id=bug_id, status_id={STATUS_CLOSED})` | **IMMEDIATELY** check if all bugs closed → Update Story status |
| Test fails validation | "Test failed" | Test Team | `mcp_openproject_update_work_package(work_package_id=bug_id, status_id={STATUS_TEST_FAILED})` | No parent update (iterate) |
| Paused | "On hold" | PM/SM | `mcp_openproject_update_work_package(work_package_id=bug_id, status_id={STATUS_ON_HOLD})` | No parent update |
| Duplicate/Invalid | "Rejected" | Test Team/PM | `mcp_openproject_update_work_package(work_package_id=bug_id, status_id={STATUS_REJECTED})` | No parent update |

**Note:** Replace `{STATUS_XXX}` placeholders with actual status IDs from OpenProject (query via `mcp_openproject_list_statuses()`).

**Implementation:**

```python
def update_bug_status_and_check_story(bug_id: int, new_status_id: int):
    """
    Update bug status and check if parent story can be updated.
    CRITICAL: When bug is closed, check if all bugs for story are closed.
    """
    # Update bug status
    mcp_openproject_update_work_package(
        work_package_id=bug_id,
        status_id=new_status_id
    )
    
    # Get status ID from config (replace with actual ID from OpenProject)
    STATUS_CLOSED = config.openproject.statuses.closed
    
    # If bug is closed, check parent story
    if new_status_id == STATUS_CLOSED:  # "Closed"
        # Get bug to find parent story
        bug = mcp_openproject_get_work_package(work_package_id=bug_id)
        parent_id = bug["work_package"].get("parent", {}).get("id")
        
        if parent_id:
            # Check if all bugs and tasks for story are closed
            update_story_status_based_on_tasks(parent_id)

# Usage example:
# When Test Team closes bug:
update_bug_status_and_check_story(bug_id=456, new_status_id=config.openproject.statuses.closed)  # "Closed"
# This will automatically check if story can be closed
```

### 3. Bug Quality Gates

**Bug Creation Quality Gate:**

**Before bug can be created:**
- ✅ Validation failure identified
- ✅ Expected vs actual behavior documented
- ✅ Steps to reproduce included
- ✅ Acceptance criteria violated identified
- ✅ Test results included

**Bug Fix Quality Gate:**

**Before bug can be marked "In testing":**
- ✅ Fix implemented
- ✅ Tests run
- ✅ Fix documented in bug comment

**Bug Closure Quality Gate:**

**Before bug can be closed:**
- ✅ Fix validated by Test Team
- ✅ Tests pass
- ✅ No regressions
- ✅ Test team approval

---

## Document Locations

**CRITICAL:** Never create duplicate documentation. Use these locations:

- **Epic Design:** `_bmad-output/planning-artifacts/epic-X-design.md` or `_bmad-output/epic-X-design.md`
- **Feature Architecture:** `_bmad-output/planning-artifacts/feature-X-architecture.md` or `_bmad-output/feature-X-architecture.md`
- **Feature Integration Test Plan:** `_bmad-output/planning-artifacts/feature-X-integration-test-plan.md` or `_bmad-output/feature-X-integration-test-plan.md`
- **Story UI Design:** `_bmad-output/planning-artifacts/story-X-Y-ui-design.md` or `_bmad-output/story-X-Y-ui-design.md`
- **Story Test Plan:** `_bmad-output/planning-artifacts/story-X-Y-test-plan.md` or `_bmad-output/story-X-Y-test-plan.md`
- **Epic Test Plan:** `_bmad-output/planning-artifacts/epic-X-test-plan.md` or `_bmad-output/epic-X-test-plan.md`

**Attach documents to OpenProject work packages as needed, but store source in `_bmad-output/`.**

---

## Action Owner Responsibilities

### Product Manager (PM)

**Epic Grooming (Responsible):**
- Create epic with comprehensive description
- Include story breakdown
- Create test story (Story X.T)
- Attach design document
- **When Epic is "In specification":** Ensure all required artifacts are attached:
  - Epic Design Document
  - Story Breakdown Document
  - Epic Test Plan (if applicable)
- **Accountable for:** Epic grooming quality and artifact completeness

**Feature Grooming (Responsible):**
- Create feature with functional capability description
- Include story breakdown
- **MANDATORY:** Create Integration Test Story (Story X.Y.T) for Feature validation
- **When Feature is "In specification":** Ensure all required artifacts are attached:
  - Feature Architecture Document
  - API Documentation (if Feature includes APIs)
  - UI Mocks/Designs (if Feature includes UI)
  - Feature Scope Document
- Link feature to epic (parent relationship)
- **Accountable for:** Feature grooming quality, artifact completeness, and Integration Test Story creation

**Story Grooming (Responsible):**
- Create story with acceptance criteria
- Break down into tasks
- **When Story is "In specification":** Ensure all required artifacts are attached:
  - Acceptance Criteria Document (or in description)
  - UI Mocks/Designs (if Story includes UI)
  - Technical Specifications (if Story requires technical details)
- **CRITICAL:** Check for existing tasks before creating
- **MANDATORY:** Create test task (Task X.Y.T) - Story cannot be closed without test task
- Attach UI documents for UI stories
- **Accountable for:** Story grooming quality, artifact completeness, and test task creation

**Feature Integration Testing:**
- Run Feature-level integration tests when Feature is in "In testing" status
- Create Feature integration test plan document (`feature-X-integration-test-plan.md`)
- Attach test plan to Feature
- Validate all Feature acceptance criteria
- Update Feature status: "In testing" → "Tested" (if tests pass) or "Test failed" (if tests fail)
- Close Feature only after integration tests pass and Feature is validated
- **Accountable for:** Feature integration test quality and Feature closure validation

### Scrum Master (SM)

**Protocol Enforcement (Accountable):**

**Epic Specification Protocol:**
- **Before Epic transitions from "In specification" to "Specified":**
  - Verify Epic Design Document is attached
  - Verify Story Breakdown Document is attached
  - Verify Epic Test Plan is attached (if applicable)
  - Use `mcp_openproject_list_work_package_attachments(work_package_id=epic_id)` to check artifacts
  - Block status transition if artifacts are missing
  - Inform PM of missing artifacts

**Feature Specification Protocol:**
- **Before Feature transitions from "In specification" to "Specified":**
  - Verify Feature Architecture Document is attached
  - Verify API Documentation is attached (if Feature includes APIs)
  - Verify UI Mocks/Designs are attached (if Feature includes UI)
  - Verify Feature Scope Document is attached
  - Use `mcp_openproject_list_work_package_attachments(work_package_id=feature_id)` to check artifacts
  - Use `verify_feature_specification_artifacts(feature_id)` helper function
  - Block status transition if artifacts are missing
  - Inform PM of missing artifacts

**Story Specification Protocol:**
- **Before Story transitions from "In specification" to "Specified":**
  - Verify Acceptance Criteria are complete (in description or attached document)
  - Verify UI Mocks/Designs are attached (if Story includes UI)
  - Verify Technical Specifications are attached (if Story requires technical details)
  - Use `mcp_openproject_list_work_package_attachments(work_package_id=story_id)` to check artifacts
  - Use `verify_story_specification_artifacts(story_id)` helper function
  - Block status transition if artifacts are missing
  - Inform PM of missing artifacts

**Accountable for:** Protocol enforcement, artifact verification, blocking incomplete work packages from moving to "Specified" status

### Developer (Dev)

**Task Implementation:**
- Update task status to "In progress" when starting work
- Update task status to "Developed" when implementation complete
- Update task status to "In testing" when ready for validation
- **IMMEDIATELY** call `update_task_status_and_parent()` for status changes that affect parent Story
- **CRITICAL:** Always use `update_task_status_and_parent()` function for "In progress", "In testing", and "Closed" transitions
- **Accountable for:** Task implementation quality and immediate parent status updates

**Bug Fix:**
- Fix bugs assigned
- Update bug status to "In progress" when starting fix
- Update bug status to "Developed" when fix implementation complete
- Update bug status to "In testing" when fix ready for validation
- Add comment with fix details (what was fixed, how, test results)
- **Accountable for:** Bug fix quality and completeness

### Test Team

**Test Validation:**
- Create test documents
- Attach test documents to stories/epics
- Validate acceptance criteria
- Close tasks/stories when validated
- **IMMEDIATELY** call `update_task_status_and_parent()` when closing tasks
- Update task status to "Tested" when validation passes
- Update task status to "Closed" when task complete
- Update bug status to "Tested" when fix validation passes
- Update bug status to "Closed" when bug resolved
- **IMMEDIATELY** call `update_task_status_and_parent()` when closing tasks
- **IMMEDIATELY** call `update_bug_status_and_check_story()` when closing bugs
- **IMMEDIATELY** update epic status to "Closed" when last story closed
- **Accountable for:** Validation quality and immediate parent status updates

**Bug Management:**
- Create bugs when validation fails
- Include detailed bug description (expected vs actual, steps to reproduce, AC violated)
- Assign bugs to dev
- Validate bug fixes
- Close bugs when validated
- **IMMEDIATELY** call `update_bug_status_and_check_story()` when closing bugs
- **Accountable for:** Bug creation quality, validation quality, and immediate parent status checks

---

## Integration with Other Workflows

- **create-epics-and-stories:** Creates epics and stories following these requirements
- **groom-story:** Creates tasks following duplicate prevention rules
- **dev-story:** Updates statuses following immediate transition rules
- **test-validation:** Validates and closes work packages following these rules

---

---

## Complete Journey Summary

### Epic Journey

**Status Flow:**
```
New → [In specification] → [Specified] → In progress → Closed
```

**Key Transitions:**
- **New → In progress:** When first story transitions to "In progress" (automatic)
- **In progress → Closed:** When last story transitions to "Closed" (automatic)

**Ownership:**
- **Creation:** PM (creates epic with design doc)
- **Status Updates:** PM/Dev (→ In progress), Test Team (→ Closed)

### Feature Journey

**Status Flow:**
```
New → [In specification] → [Specified] → In progress → In testing → Tested → Closed
```

**Alternative Paths:**
- **In testing → Test failed:** When integration tests fail (creates issues, returns to "In progress")
- **Any status → On hold:** When paused
- **Any status → Rejected:** When cancelled

**Key Transitions:**
- **New → In progress:** When first story transitions to "In progress" (automatic)
- **In progress → In testing:** When all stories transition to "Closed" (automatic - integration testing required)
- **In testing → Tested:** When integration tests pass (Test Team)
- **Tested → Closed:** When Feature validated (Test Team)
- **In testing → Test failed:** When integration tests fail (Test Team - creates issues)

**Ownership:**
- **Creation:** PM (creates feature with architecture doc)
- **Status Updates:** PM/Dev (→ In progress), Test Team (→ In testing, → Tested, → Closed)
- **Integration Testing:** Test Team (runs Feature-level integration tests, validates Feature)

### Story Journey

**Status Flow:**
```
New → [In specification] → [Specified] → In progress → In testing → Closed
```

**Alternative Paths:**
- **In testing → Test failed:** When validation fails (creates bugs)
- **Any status → On hold:** When paused
- **Any status → Rejected:** When cancelled

**Key Transitions:**
- **New → In progress:** When first task transitions to "In progress" (automatic)
- **In progress → In testing:** When test task is "In testing" AND all other tasks "Closed" (automatic)
- **In testing → Closed:** When all tasks AND all bugs are "Closed" (automatic)

**Ownership:**
- **Creation:** PM (creates story with acceptance criteria)
- **Status Updates:** Dev (→ In progress, → In testing), Dev/Test Team (→ Closed)

### Task Journey

**Status Flow:**
```
New → In progress → Developed → In testing → Tested → Closed
```

**Alternative Paths:**
- **In testing → Test failed:** When validation fails (creates bug)
- **Any status → On hold:** When paused
- **Any status → Rejected:** When cancelled

**Key Transitions:**
- **New → In progress:** Dev starts work (triggers parent Story → "In progress")
- **In progress → Developed:** Dev completes implementation
- **Developed → In testing:** Dev marks ready for testing (triggers parent Story → "In testing")
- **In testing → Tested:** Test Team validates successfully
- **Tested → Closed:** Test Team closes task (triggers parent Story status check)

**Ownership:**
- **Creation:** PM (creates during story grooming)
- **Status Updates:** Dev (→ In progress, → Developed, → In testing), Test Team (→ Tested, → Closed)
- **Parent Updates:** Automatic via `update_task_status_and_parent()` function

### Bug Journey

**Status Flow:**
```
New → In progress → Developed → In testing → Tested → Closed
```

**Alternative Paths:**
- **In testing → Test failed:** When validation fails (iterate fix cycle)
- **Any status → On hold:** When paused
- **Any status → Rejected:** When duplicate/invalid

**Key Transitions:**
- **New → In progress:** Dev starts fixing bug
- **In progress → Developed:** Dev completes fix implementation
- **Developed → In testing:** Dev marks fix ready for testing
- **In testing → Tested:** Test Team validates fix successfully
- **Tested → Closed:** Test Team closes bug (triggers parent Story status check)

**Ownership:**
- **Creation:** Test Team (creates from validation failure)
- **Status Updates:** Dev (→ In progress, → Developed, → In testing), Test Team (→ Tested, → Closed)
- **Parent Updates:** Automatic via `update_bug_status_and_check_story()` function when bug closed

---

## Status Transition Rules Summary

### Automatic Parent Updates

| Child Status Change | Parent Update | Function |
|---------------------|--------------|----------|
| Task → "In progress" | Story → "In progress" | `update_story_status_based_on_tasks()` |
| Task → "In testing" | Story → "In testing" (if test task) | `update_story_status_based_on_tasks()` |
| Task → "Closed" | Story → "Closed" (if all tasks + bugs closed) | `update_story_status_based_on_tasks()` |
| Bug → "Closed" | Story → "Closed" (if all tasks + bugs closed) | `update_story_status_based_on_tasks()` |
| Story → "In progress" | Epic/Feature → "In progress" | `update_epic_status_based_on_stories()` / `update_feature_status_based_on_stories()` |
| Story → "Closed" | Epic → "Closed" (if last story) | `update_epic_status_based_on_stories()` |
| All stories → "Closed" | Feature → "In testing" (integration testing required) | `update_feature_status_based_on_stories()` |
| Feature integration tests pass | Feature → "Tested" | Test Team (manual) |
| Feature validated | Feature → "Closed" | Test Team (manual) |

### Status Recording Location

**All status transitions are recorded in:**
- **System:** OpenProject database
- **Tool:** `mcp_openproject_update_work_package(work_package_id, status_id)`
- **Visibility:** OpenProject UI and API
- **Persistence:** Permanent record in OpenProject

### Agent Accountability Matrix

| Work Package | Creation | Status Updates | Closure | Accountable Agent |
|--------------|----------|----------------|---------|-------------------|
| **Epic** | PM | PM/Dev (→ In progress), Test Team (→ Closed) | Test Team | PM (creation), Test Team (closure) |
| **Feature** | PM | PM/Dev (→ In progress), Test Team (→ In testing, → Tested, → Closed) | Test Team | PM (creation), Test Team (integration testing & closure) |
| **Story** | PM | Dev (→ In progress, → In testing), Dev/Test Team (→ Closed) | Dev/Test Team | PM (creation), Dev (implementation), Test Team (validation) |
| **Task** | PM | Dev (→ In progress, → Developed, → In testing), Test Team (→ Tested, → Closed) | Test Team | PM (creation), Dev (implementation), Test Team (validation) |
| **Bug** | Test Team | Dev (→ In progress, → Developed, → In testing), Test Team (→ Tested, → Closed) | Test Team | Test Team (creation/validation), Dev (fix) |

---

## References

- **OpenProject Integration:** `@bmad/integrations/openproject` - MCP tools and workflow
- **OpenProject Status Query:** Use `mcp_openproject_list_statuses()` to get actual status IDs
