# Agent Integration Mixin

This file defines the standard integration capabilities that ALL BMAD agents should have. When activated, agents should load this mixin in addition to their persona.

## CRITICAL INTEGRATION RULES

### System Responsibilities

| System          | Responsibility                                          |
| --------------- | ------------------------------------------------------- |
| **OpenProject** | Work management + ALL project documents (attachments)   |
| **Archon**      | Search EXTERNAL knowledge only (library docs, patterns) |

### Document Storage Hierarchy

**ALL project documents must be stored as OpenProject attachments at the appropriate level:**

| Work Package Level | Documents to Store                                 |
| ------------------ | -------------------------------------------------- |
| **Project**        | Product briefs, project overview, high-level specs |
| **Epic**           | Epic specifications, business cases                |
| **Feature**        | Feature architecture, technical designs, API specs |
| **Story**          | Story specifications, acceptance criteria docs     |
| **Task**           | Implementation notes, technical details            |

**⚠️ DO NOT store project documents in Archon. Archon is ONLY for searching external knowledge.**

## Integration Activation Block

Add this to the agent activation sequence after loading the base persona:

```xml
<integration-activation critical="MANDATORY">
  <step n="I1">Load project configuration from {project-root}/_bmad/_config/project-config.yaml</step>
  <step n="I2">Store integration settings:
    - openproject_project_id = {config.openproject.project_id}
    - types = {config.openproject.types}
    - statuses = {config.openproject.statuses}
    - priorities = {config.openproject.priorities}
  </step>
  <step n="I3">If openproject.enabled=true, verify OpenProject MCP is available</step>
  <step n="I4">If archon.enabled=true, verify Archon MCP is available (for search only)</step>
  <step n="I5">REMEMBER: OpenProject = work + documents, Archon = external search only</step>
</integration-activation>
```

## Standard Integration Capabilities

### OpenProject Capabilities (Work Management + Documents)

All agents have access to these OpenProject operations:

```yaml
openproject_capabilities:
  work_management:
    - list_work_packages: "Get open/closed work packages"
    - get_work_package: "Get specific work package details"
    - search_work_packages: "Search by subject"
    - get_work_package_children: "Get child items"
    - get_work_package_hierarchy: "Get full hierarchy"
    - create_work_package: "Create epic/feature/story/task"
    - update_work_package: "Update any field"
    - update_work_package_status: "Change status with comment"
    - assign_work_package: "Assign to user"
    - set_work_package_parent: "Set parent relationship"
    - add_work_package_comment: "Add comments"
    - log_time: "Log time entry"

  document_storage:
    - list_work_package_attachments: "List attachments on work package"
    - delete_attachment: "Delete attachment"
    # Note: Upload via OpenProject UI or API directly

  document_guidelines:
    project_level: "Product briefs, project overview docs"
    epic_level: "Epic specifications, business cases"
    feature_level: "Architecture docs, technical designs, API specs"
    story_level: "Story specs, acceptance criteria, test cases"
    task_level: "Implementation notes, technical details"
```

### Archon Capabilities (External Knowledge Search ONLY)

Archon is ONLY for searching external knowledge sources:

```yaml
archon_capabilities:
  external_search_only:
    - rag_search_knowledge_base: "Search external documentation"
    - rag_search_code_examples: "Find code examples from external sources"
    - rag_read_full_page: "Read complete external documentation page"
    - rag_get_available_sources: "List external knowledge sources"
    - rag_list_pages_for_source: "Browse external documentation structure"

  # IMPORTANT: Do NOT use Archon for project documents!
  # The following operations should NOT be used for project artifacts:
  # - manage_document (don't store project docs here)
  # - find_documents (don't look for project docs here)
```

## Consolidated RACI Matrix

The following table provides a comprehensive RACI matrix for all BMAD agents across the SDLC lifecycle.

**Legend:** R = Responsible, A = Accountable, C = Consulted, I = Informed

### Work Package Management RACI

| Activity | PM | SM | Dev | TEA | Architect | UX Designer | Analyst | Tech Writer |
|----------|----|----|-----|-----|-----------|-------------|---------|-------------|
| Epic Creation | R/A | I | I | I | C | I | C | I |
| Epic Grooming | R | A | C | C | C | C | C | I |
| Feature Creation | R/A | I | C | I | C | C | I | I |
| Feature Grooming | R | A | C | C | C | R (UI) | I | I |
| Story Creation | R/A | C | C | C | C | C | I | I |
| Story Grooming | R | A | C | C | C | C (UI) | I | I |
| Task Creation | C | C | R/A | C | C | I | I | I |
| Bug Creation | I | I | C | R/A | I | I | I | I |
| Bug Triage | C | A | R | C | C | I | I | I |

### Status Transition RACI

| Transition | PM | SM | Dev | TEA | Architect | UX Designer |
|------------|----|----|-----|-----|-----------|-------------|
| New → In specification | R | A | I | I | C | C |
| In specification → Specified | R | A* | C | C | C | R (artifacts) |
| Specified → In progress | I | A | R | I | I | I |
| In progress → Developed | I | I | R/A | I | I | I |
| Developed → In testing | I | I | R | A | I | I |
| In testing → Tested | I | I | C | R/A | I | I |
| In testing → Test failed | I | I | I | R/A | I | I |
| Tested → Closed | A | R | I | I | I | I |

*SM is Accountable for verifying specification artifacts before allowing "In specification" → "Specified" transition.

### Artifact Ownership RACI

| Artifact | PM | SM | Dev | TEA | Architect | UX Designer | Analyst | Tech Writer |
|----------|----|----|-----|-----|-----------|-------------|---------|-------------|
| Product Brief | A | I | I | I | C | I | R | I |
| PRD | R/A | C | C | C | C | C | C | I |
| Epic Design Doc | R | A | C | C | C | C | C | I |
| Feature Architecture | C | I | C | I | R/A | I | I | C |
| API Documentation | C | I | C | C | R/A | I | I | C |
| UI Mockups | A | C | C | I | C | R | I | I |
| Acceptance Criteria | R/A | A | C | C | C | C | I | I |
| Test Strategy | C | I | C | R/A | C | I | I | I |
| Test Cases | I | I | C | R/A | I | I | I | I |
| Implementation Notes | I | I | R/A | I | I | I | I | I |
| Technical Documentation | C | I | C | I | C | I | I | R/A |
| Sprint Reports | C | R/A | I | I | I | I | I | I |

### Tool Usage RACI

| Tool | PM | SM | Dev | TEA | Architect | UX Designer | Analyst | Tech Writer |
|------|----|----|-----|-----|-----------|-------------|---------|-------------|
| OpenProject MCP - Work Packages | R | R | R | R | R | C | C | C |
| OpenProject MCP - Attachments | R | A | R | R | R | R | R | R |
| OpenProject MCP - Status Updates | R | A | R | R | C | I | I | I |
| GenImage MCP - Mockups | C | I | C | I | C | R/A | I | I |
| Archon MCP - External Search | R | I | R | R | R | R | R | R |

### Integration Testing RACI

| Activity | PM | SM | Dev | TEA | Architect | UX Designer |
|----------|----|----|-----|-----|-----------|-------------|
| Feature Integration Test Plan | C | I | C | R/A | C | I |
| Live System Dependency Check | I | I | C | R/A | C | I |
| Infrastructure Story Creation | C | A | C | R | R | I |
| Integration Test Execution | I | I | C | R/A | I | I |
| Integration Test Results Review | A | R | C | R | C | I |

## Agent-Specific Integration Behaviors

### PM Agent Integration

```yaml
pm_integration:
  primary_actions:
    - **Grooming (Responsible):** Create and groom Epics, Features, User Stories using OpenProject MCP tools
    - Create Epics using `mcp_openproject_create_work_package(type_id=config.openproject.types.epic)`
    - Create Features using `mcp_openproject_create_work_package(type_id=config.openproject.types.feature)` (recommended for new epics)
    - Create User Stories using `mcp_openproject_create_work_package(type_id=config.openproject.types.user_story)`
    - Set parent relationships using `mcp_openproject_set_work_package_parent()`
    - **Epic Grooming:** When Epic is "In specification", ensure all required artifacts are attached:
      - Epic Design Document
      - Story Breakdown Document
      - Epic Test Plan (if applicable)
    - **Feature Grooming:** When Feature is "In specification", ensure all required artifacts are attached:
      - Feature Architecture Document
      - API Documentation (if Feature includes APIs)
      - UI Mocks/Designs (if Feature includes UI)
      - Feature Scope Document
    - **Story Grooming:** When Story is "In specification", ensure all required artifacts are attached:
      - Acceptance Criteria Document (or in description)
      - UI Mocks/Designs (if Story includes UI)
      - Technical Specifications (if Story requires technical details)
    - Update Epic/Feature status → "In progress" when first story starts (automatic via helper functions)
    - Store product briefs as Project-level attachments in OpenProject
    - Store PRDs as Epic-level attachments in OpenProject
    - Store Feature architecture as Feature-level attachments in OpenProject
    - Search Archon for EXTERNAL research and best practices

  document_storage:
    product_brief: "OpenProject Project-level attachment"
    prd: "OpenProject Epic-level attachment"
    feature_architecture: "OpenProject Feature-level attachment"
    api_documentation: "OpenProject Feature-level attachment"
    ui_mocks: "OpenProject Feature/Story-level attachment"
    research_findings: "OpenProject Project/Epic-level attachment"

  workflow_triggers:
    - "[PR] Create PRD" → Store as OpenProject attachment + Create work structure
    - "[ES] Create Epics/Features/Stories" → Create in OpenProject using MCP tools with docs as attachments
    - "[IR] Implementation Readiness" → Query OpenProject using MCP tools
    - Work package "In specification" → Attach required artifacts → Request SM approval for "Specified" status
```

### Dev Agent Integration

```yaml
dev_integration:
  primary_actions:
    - Query assigned tasks/bugs from OpenProject using `mcp_openproject_list_work_packages()`
    - Update task status using `mcp_openproject_update_work_package()`: New → In progress → Developed → In testing
    - Update bug status using `mcp_openproject_update_work_package()`: New → In progress → Developed → In testing
    - **CRITICAL:** Use `update_task_status_and_parent()` function when updating task status to automatically update parent Story
    - Search Archon for EXTERNAL patterns and documentation
    - Log time against work packages using `mcp_openproject_log_time()`
    - Store implementation notes as Task-level attachments in OpenProject

  document_storage:
    implementation_notes: "OpenProject Task-level attachment"
    technical_details: "OpenProject Task-level attachment"
    code_documentation: "OpenProject Task-level attachment"

  workflow_triggers:
    - Start task → Update OpenProject status to "In progress" using MCP tools
    - Implementation → Search Archon for EXTERNAL patterns/examples
    - Mark developed → Update OpenProject status to "Developed" using MCP tools
    - Mark ready for testing → Update OpenProject status to "In testing" using MCP tools + call `update_task_status_and_parent()`
    - Complete task → Store notes in OpenProject + Update status using MCP tools
```

### Architect Agent Integration

```yaml
architect_integration:
  primary_actions:
    - Store architecture docs as Feature-level attachments in OpenProject
    - Store system architecture as Project-level attachment in OpenProject
    - Create architecture work packages in OpenProject
    - Search Archon for EXTERNAL architecture patterns
    - Store ADRs as Feature-level attachments in OpenProject

  document_storage:
    system_architecture: "OpenProject Project-level attachment"
    feature_architecture: "OpenProject Feature-level attachment"
    technical_spec: "OpenProject Feature/Story-level attachment"
    adr: "OpenProject Feature-level attachment"

  workflow_triggers:
    - "[CA] Create Architecture" → Store as OpenProject attachment + Create tasks
    - Technical decision → Store ADR as OpenProject attachment
```

### SM Agent Integration (Scrum Master)

```yaml
sm_integration:
  primary_actions:
    - **Protocol Enforcement (Accountable):** Verify required artifacts before allowing work packages to transition from "In specification" to "Specified"
    - **Epic Specification Protocol:** Verify Epic Design Document, Story Breakdown Document, Epic Test Plan (if applicable) are attached
    - **Feature Specification Protocol:** Verify Feature Architecture Document, API Documentation (if APIs), UI Mocks (if UI), Feature Scope Document are attached
    - **Story Specification Protocol:** Verify Acceptance Criteria, UI Mocks (if UI), Technical Specifications (if required) are attached
    - Use `mcp_openproject_list_work_package_attachments()` to check artifacts
    - Use helper functions: `verify_feature_specification_artifacts()`, `verify_story_specification_artifacts()`
    - Block status transitions if artifacts are missing
    - Sprint planning using OpenProject
    - Status reporting from OpenProject
    - Blocker tracking in OpenProject
    - Store sprint reports as Project-level attachments in OpenProject

  document_storage:
    sprint_report: "OpenProject Project-level attachment"
    retrospective: "OpenProject Project-level attachment"

  workflow_triggers:
    - "[SP] Sprint Planning" → Query/update OpenProject
    - "[SS] Sprint Status" → Generate report, store in OpenProject
    - Work package "In specification" → "Specified" transition → Verify artifacts before allowing
```

### TEA Agent Integration (Test Team)

```yaml
tea_integration:
  primary_actions:
    - Create test work packages in OpenProject using `mcp_openproject_create_work_package()`
    - Create Bugs when validation fails using `mcp_openproject_create_work_package(type_id=config.openproject.types.bug)`
    - Update task status: In testing → Tested → Closed using `mcp_openproject_update_work_package()`
    - Update bug status: In testing → Tested → Closed using `mcp_openproject_update_work_package()`
    - Run Feature-level integration tests and update Feature status: In testing → Tested → Closed
    - **CRITICAL:** 
      - Use `update_task_status_and_parent()` when closing tasks
      - Use `update_bug_status_and_check_story()` when closing bugs
    - Store test strategies as Feature-level attachments in OpenProject
    - Store test cases as Story-level attachments in OpenProject
    - Store Feature integration test plans as Feature-level attachments in OpenProject
    - Search Archon for EXTERNAL testing patterns

  document_storage:
    test_strategy: "OpenProject Feature-level attachment"
    feature_integration_test_plan: "OpenProject Feature-level attachment"
    test_cases: "OpenProject Story-level attachment"
    test_results: "OpenProject Story/Task-level attachment"

  workflow_triggers:
    - Test planning → Search Archon for EXTERNAL patterns + Store strategy in OpenProject
    - Test creation → Create work packages + Attach test cases in OpenProject
    - Test execution → Update status in OpenProject using MCP tools
    - Feature integration testing → Run tests, update Feature status using MCP tools
    - Bug creation → Create bug using MCP tools, assign to dev
    - Bug validation → Validate fixes, update bug status using MCP tools
```

## Integration Menu Items

Add these menu items to all agents:

```xml
<integration-menu>
  <item cmd="OPW or fuzzy match on openproject-work">[OPW] Show OpenProject Work Packages</item>
  <item cmd="OPC or fuzzy match on openproject-create">[OPC] Create OpenProject Work Package</item>
  <item cmd="OPA or fuzzy match on openproject-attach">[OPA] View OpenProject Attachments</item>
  <item cmd="AKS or fuzzy match on archon-search">[AKS] Search External Knowledge (Archon)</item>
</integration-menu>
```

**Note:** Removed "Create Archon Document" menu item. All project documents go to OpenProject.

## Integration Handlers

```xml
<integration-handlers>
  <handler cmd="OPW">
    Execute: mcp_openproject_list_work_packages(project_id={openproject_project_id}, status="open")
    Display: Formatted list of work packages with status
  </handler>

  <handler cmd="OPC">
    Ask: Work package type (Epic/Feature/Story/Task)
    Ask: Subject and description
    Execute: mcp_openproject_create_work_package(project_id={openproject_project_id}, type_id=..., subject=..., description=...)
    Remind: Attach relevant documents to this work package
  </handler>

  <handler cmd="OPA">
    Ask: Work package ID
    Execute: mcp_openproject_list_work_package_attachments(work_package_id=...)
    Display: List of attachments on work package
  </handler>

  <handler cmd="AKS">
    Ask: Search query (remind: 2-5 keywords, EXTERNAL docs only)
    Execute: mcp_archon_rag_search_knowledge_base(query=..., match_count=5)
    Display: Search results with snippets
    Offer: Read full page for any result
    Remind: This searches EXTERNAL documentation only, not project documents
  </handler>
</integration-handlers>
```

## Configuration Reference

All settings come from `_bmad/_config/project-config.yaml`:

| Setting Path                       | Description                 |
| ---------------------------------- | --------------------------- |
| `openproject.project_id`           | OpenProject project ID      |
| `openproject.types.epic`           | Epic type ID                |
| `openproject.types.feature`        | Feature type ID             |
| `openproject.types.user_story`     | User Story type ID          |
| `openproject.types.task`           | Task type ID                |
| `openproject.statuses.new`              | New status ID               |
| `openproject.statuses.in_specification` | In specification status ID  |
| `openproject.statuses.specified`        | Specified status ID         |
| `openproject.statuses.in_progress`      | In Progress status ID        |
| `openproject.statuses.developed`        | Developed status ID          |
| `openproject.statuses.in_testing`       | In Testing status ID         |
| `openproject.statuses.tested`            | Tested status ID             |
| `openproject.statuses.test_failed`      | Test failed status ID        |
| `openproject.statuses.closed`           | Closed status ID             |
| `openproject.statuses.on_hold`          | On hold status ID            |
| `openproject.statuses.rejected`         | Rejected status ID           |
| `archon.rag.default_match_count`   | Default search result count |

## Usage Example

When an agent activates:

```
1. Load base persona (pm.md, dev.md, etc.)
2. Load integration mixin (this file)
3. Read project-config.yaml
4. Store config values for use in workflows
5. Display standard menu + integration menu items
6. REMEMBER: OpenProject for work + documents, Archon for external search only
```

When executing a workflow:

```
1. Check if integration is enabled in config
2. Use configured IDs for all MCP calls
3. Follow OpenProject-First rule for work management
4. Store ALL project documents as OpenProject attachments
5. Use Archon ONLY for searching external knowledge
6. Attach documents at appropriate work package level
```

## Document Storage Quick Reference

| Document Type        | OpenProject Level | Example                      |
| -------------------- | ----------------- | ---------------------------- |
| Product Brief        | Project           | High-level product vision    |
| PRD                  | Project/Epic      | Requirements document        |
| System Architecture  | Project           | Overall system design        |
| Feature Architecture | Feature           | Feature-specific design      |
| Technical Spec       | Feature/Story     | Implementation details       |
| API Documentation    | Feature           | API design and specs         |
| Acceptance Criteria  | Story             | Detailed story criteria      |
| Test Strategy        | Feature           | Testing approach             |
| Test Cases           | Story             | Specific test scenarios      |
| Implementation Notes | Task              | Code documentation           |
| ADR                  | Feature           | Architecture Decision Record |
