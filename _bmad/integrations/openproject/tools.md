# OpenProject MCP Tools Reference

This document provides the complete reference for OpenProject MCP tools used in BMAD workflows.

## OpenProject is the PRIMARY System For:

1. **Work Management**: Projects, Epics, Features, User Stories, Tasks
2. **Status Tracking**: Workflow management and sprint execution
3. **Document Storage**: ALL project artifacts as attachments at appropriate work package level

### Document Storage Hierarchy

| Work Package Level | Documents to Store                                           |
| ------------------ | ------------------------------------------------------------ |
| **Project**        | Product briefs, project overview, high-level specs           |
| **Epic**           | Epic specifications, business cases, epic-level architecture |
| **Feature**        | Feature architecture, technical designs, feature specs       |
| **User Story**     | Story specifications, detailed acceptance criteria docs      |
| **Task**           | Implementation notes, technical details, code documentation  |

## Configuration

All OpenProject settings are stored in `_bmad/_config/project-config.yaml` under the `openproject:` section.

**Required Setup:**

1. Get your `project_id` from `mcp_openproject_list_projects(active_only=True)`
2. Get type IDs from `mcp_openproject_list_types(project_id=YOUR_ID)`
3. Update `project-config.yaml` with these values

## Tool Categories

### Connection & Discovery

| Tool                                         | Description           | Parameters                          |
| -------------------------------------------- | --------------------- | ----------------------------------- |
| `mcp_openproject_test_connection()`          | Test API connectivity | None                                |
| `mcp_openproject_list_projects(active_only)` | List all projects     | `active_only`: bool (default: true) |
| `mcp_openproject_get_project(project_id)`    | Get project details   | `project_id`: int (required)        |

### Work Package Management

| Tool                                                   | Description              | Key Parameters                                          |
| ------------------------------------------------------ | ------------------------ | ------------------------------------------------------- |
| `mcp_openproject_list_work_packages(...)`              | List work packages       | `project_id`, `status` ("open"/"closed"/"all")          |
| `mcp_openproject_get_work_package(work_package_id)`    | Get work package details | `work_package_id`: int                                  |
| `mcp_openproject_create_work_package(...)`             | Create epic/story/task   | `project_id`, `subject`, `type_id`, `description`, etc. |
| `mcp_openproject_update_work_package(...)`             | Update work package      | `work_package_id`, any updateable fields                |
| `mcp_openproject_delete_work_package(work_package_id)` | Delete work package      | `work_package_id`: int                                  |

### Hierarchy Management

| Tool                                                                  | Description             | Parameters                    |
| --------------------------------------------------------------------- | ----------------------- | ----------------------------- |
| `mcp_openproject_set_work_package_parent(work_package_id, parent_id)` | Set parent relationship | Both required                 |
| `mcp_openproject_remove_work_package_parent(work_package_id)`         | Remove parent           | `work_package_id`             |
| `mcp_openproject_get_work_package_children(parent_id, ...)`           | Get children            | `parent_id`, optional filters |
| `mcp_openproject_get_work_package_hierarchy(work_package_id)`         | Get full hierarchy      | `work_package_id`             |

### Bulk Operations

| Tool                                                                   | Description       | Parameters                                |
| ---------------------------------------------------------------------- | ----------------- | ----------------------------------------- |
| `mcp_openproject_bulk_create_work_packages(project_id, work_packages)` | Batch create      | `project_id`, JSON array of work packages |
| `mcp_openproject_bulk_update_work_packages(updates)`                   | Batch update      | JSON array of update objects              |
| `mcp_openproject_query_work_packages(...)`                             | Advanced query    | Filters, sorting, grouping, pagination    |
| `mcp_openproject_search_work_packages(query, ...)`                     | Search by subject | `query` string, optional filters          |

### Reference Data

| Tool                                                  | Description             | Parameters              |
| ----------------------------------------------------- | ----------------------- | ----------------------- |
| `mcp_openproject_list_types(project_id)`              | List work package types | `project_id` (optional) |
| `mcp_openproject_list_statuses()`                     | List all statuses       | None                    |
| `mcp_openproject_list_priorities()`                   | List priority levels    | None                    |
| `mcp_openproject_list_users(active_only)`             | List users              | `active_only`: bool     |
| `mcp_openproject_get_available_assignees(project_id)` | Get assignable users    | `project_id`            |

### Status & Comments

| Tool                                                                          | Description     | Parameters                                                            |
| ----------------------------------------------------------------------------- | --------------- | --------------------------------------------------------------------- |
| `mcp_openproject_update_work_package_status(work_package_id, status_id, ...)` | Change status   | `work_package_id`, `status_id`, optional `comment`, `percentage_done` |
| `mcp_openproject_add_work_package_comment(work_package_id, comment, ...)`     | Add comment     | `work_package_id`, `comment` text, `notify` bool                      |
| `mcp_openproject_list_work_package_activities(work_package_id, ...)`          | List activities | `work_package_id`, `limit`                                            |

### Time Tracking

| Tool                                                     | Description         | Parameters                                                                |
| -------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------- |
| `mcp_openproject_log_time(work_package_id, hours, ...)`  | Log time entry      | `work_package_id`, `hours`, optional `activity_id`, `spent_on`, `comment` |
| `mcp_openproject_list_time_entries(...)`                 | List time entries   | Optional filters: `work_package_id`, `project_id`, `user_id`, date range  |
| `mcp_openproject_list_time_entry_activities(project_id)` | List activity types | `project_id` (optional)                                                   |

### Relations

| Tool                                                                      | Description     | Parameters                                  |
| ------------------------------------------------------------------------- | --------------- | ------------------------------------------- |
| `mcp_openproject_create_work_package_relation(from_id, to_id, type, ...)` | Create relation | IDs and relation type                       |
| `mcp_openproject_list_work_package_relations(work_package_id, ...)`       | List relations  | `work_package_id`, optional `relation_type` |
| `mcp_openproject_delete_work_package_relation(relation_id)`               | Delete relation | `relation_id`                               |

**Relation Types:** `relates`, `duplicates`, `duplicated`, `blocks`, `blocked`, `precedes`, `follows`, `includes`, `partof`, `requires`, `required`

### Watchers

| Tool                                                                    | Description    | Parameters        |
| ----------------------------------------------------------------------- | -------------- | ----------------- |
| `mcp_openproject_add_work_package_watcher(work_package_id, user_id)`    | Add watcher    | Both required     |
| `mcp_openproject_remove_work_package_watcher(work_package_id, user_id)` | Remove watcher | Both required     |
| `mcp_openproject_list_work_package_watchers(work_package_id)`           | List watchers  | `work_package_id` |

### Assignment

| Tool                                                        | Description     | Parameters                                                  |
| ----------------------------------------------------------- | --------------- | ----------------------------------------------------------- |
| `mcp_openproject_assign_work_package(work_package_id, ...)` | Assign/reassign | `work_package_id`, optional `assignee_id`, `responsible_id` |

### Attachments (Document Storage)

**IMPORTANT:** All project documents should be stored as attachments at the appropriate work package level.

| Tool                                                             | Description       | Parameters        |
| ---------------------------------------------------------------- | ----------------- | ----------------- |
| `mcp_openproject_list_work_package_attachments(work_package_id)` | List attachments  | `work_package_id` |
| `mcp_openproject_delete_attachment(attachment_id)`               | Delete attachment | `attachment_id`   |

**Document Storage Guidelines:**

| Document Type        | Store At Level  | Example                                |
| -------------------- | --------------- | -------------------------------------- |
| Product Brief        | Project         | Overall product vision document        |
| PRD                  | Project or Epic | Requirements for the product/epic      |
| Architecture Doc     | Feature         | Technical architecture for the feature |
| Technical Spec       | Feature/Story   | Detailed technical specifications      |
| Acceptance Criteria  | Story           | Story-specific acceptance criteria doc |
| Implementation Notes | Task            | Task-specific technical notes          |
| Test Strategy        | Story/Feature   | Testing approach documentation         |
| API Documentation    | Feature         | API specs for the feature              |

**Note:** To upload attachments, use the OpenProject UI or API directly. The MCP tools support listing and deleting attachments.

### Custom Fields & Schema

| Tool                                                                                | Description                 | Parameters        |
| ----------------------------------------------------------------------------------- | --------------------------- | ----------------- |
| `mcp_openproject_list_custom_fields()`                                              | List custom fields          | None              |
| `mcp_openproject_update_work_package_custom_fields(work_package_id, custom_fields)` | Update custom fields        | JSON mapping      |
| `mcp_openproject_get_work_package_schema(work_package_id)`                          | Get schema with transitions | `work_package_id` |

## Standard Work Package Type IDs

These are typical defaults - verify with `mcp_openproject_list_types()`:

| Type       | Default ID | Usage                     |
| ---------- | ---------- | ------------------------- |
| Epic       | 40         | High-level business goals |
| Feature    | 39         | Functional capabilities   |
| User Story | 41         | User-centric requirements |
| Task       | 36         | Implementation work items |
| Bug        | 42         | Defects and issues        |
| Milestone  | 37         | Key project checkpoints   |

## Standard Status IDs

**CRITICAL:** These are typical defaults - **ALWAYS verify with `mcp_openproject_list_statuses()`** and configure actual IDs in `_bmad/_config/project-config.yaml`.

| Status Name       | Default ID | Description                | Usage in BMAD |
| ----------------- | ---------- | -------------------------- | ------------- |
| New               | 71         | Initial state              | All work packages |
| In specification  | 72         | Requirements being defined | Optional planning phase |
| Specified         | 73         | Requirements complete      | Optional planning phase |
| In progress       | 77         | Active development         | Main development phase |
| Developed         | 78         | Code/implementation complete | After development, before testing |
| In testing        | 79         | Under review/testing       | Testing phase |
| Tested            | 80         | Testing complete and passed | After successful testing |
| Test failed       | 81         | Testing failed, needs rework | Error path |
| Closed            | 82         | Complete                   | End of successful journey |
| On hold           | 83         | Paused                     | Optional pause state |
| Rejected          | 84         | Not proceeding             | Optional cancellation |

**Note:** Additional statuses may exist in your OpenProject instance. Always query `mcp_openproject_list_statuses()` to get actual status IDs and names.

## Standard Priority IDs

| Priority  | Default ID |
| --------- | ---------- |
| Low       | 72         |
| Normal    | 73         |
| High      | 74         |
| Immediate | 75         |

## Common Usage Patterns

### Create Epic with Features and Stories

**CRITICAL: Always check for existing work packages before creating**

```python
# Helper functions for duplicate checking
def check_existing_epic(project_id: int, epic_subject: str) -> dict | None:
    """Check if Epic already exists."""
    epics = mcp_openproject_list_work_packages(
        project_id=project_id,
        filters=json.dumps([{"type": {"operator": "=", "values": [config.openproject.types.epic]}}]),
        status="all"
    )
    for epic in epics.get("work_packages", []):
        if epic_subject.lower() in epic["subject"].lower() or epic["subject"].lower() in epic_subject.lower():
            return epic
    return None

def check_existing_feature(epic_id: int, feature_subject: str) -> dict | None:
    """Check if Feature already exists under Epic."""
    children = mcp_openproject_get_work_package_children(parent_id=epic_id, status="all")
    for child in children.get("children", []):
        if child["type"] == "Feature" and (feature_subject.lower() in child["subject"].lower() or child["subject"].lower() in feature_subject.lower()):
            return child
    return None

def check_existing_story(parent_id: int, story_subject: str) -> dict | None:
    """Check if Story already exists under parent."""
    children = mcp_openproject_get_work_package_children(parent_id=parent_id, status="all")
    for child in children.get("children", []):
        if child["type"] == "User story" and (story_subject.lower() in child["subject"].lower() or child["subject"].lower() in story_subject.lower()):
            return child
    return None

# 1. Create Epic (with duplicate check)
epic_subject = "Epic 1: Epic Name"
existing_epic = check_existing_epic(project_id={config.openproject.project_id}, epic_subject=epic_subject)

if existing_epic:
    epic_id = existing_epic["id"]
    epic = mcp_openproject_update_work_package(work_package_id=epic_id, description="Updated epic description...")
    print(f"Updated existing Epic {epic_id}")
else:
    epic = mcp_openproject_create_work_package(
        project_id={config.openproject.project_id},
        subject=epic_subject,
        type_id={config.openproject.types.epic},
        description="Epic description...",
        status_id={config.openproject.statuses.new},
        priority_id={config.openproject.priorities.high}
    )
    epic_id = epic["work_package"]["id"]

# 2. Create Feature under Epic (with duplicate check)
feature_subject = "Feature: Feature Name"
existing_feature = check_existing_feature(epic_id=epic_id, feature_subject=feature_subject)

if existing_feature:
    feature_id = existing_feature["id"]
    feature = mcp_openproject_update_work_package(work_package_id=feature_id, description="Updated functional capability description...")
    print(f"Updated existing Feature {feature_id}")
else:
    feature = mcp_openproject_create_work_package(
        project_id={config.openproject.project_id},
        subject=feature_subject,
        type_id={config.openproject.types.feature},
        description="Functional capability description...",
        status_id={config.openproject.statuses.new},
        priority_id={config.openproject.priorities.high}
    )
    feature_id = feature["work_package"]["id"]
    mcp_openproject_set_work_package_parent(work_package_id=feature_id, parent_id=epic_id)

# 3. Create User Story under Feature (with duplicate check)
story_subject = "Story 1.1.1: Story Name"  # Epic.Feature.Story numbering
existing_story = check_existing_story(parent_id=feature_id, story_subject=story_subject)

if existing_story:
    story_id = existing_story["id"]
    story = mcp_openproject_update_work_package(work_package_id=story_id, description="Updated story description...")
    print(f"Updated existing Story {story_id}")
else:
    story = mcp_openproject_create_work_package(
        project_id={config.openproject.project_id},
        subject=story_subject,
        type_id={config.openproject.types.user_story},
        description="As a... I want... So that...",
        status_id={config.openproject.statuses.new},
        priority_id={config.openproject.priorities.normal}
    )
    story_id = story["work_package"]["id"]
    mcp_openproject_set_work_package_parent(work_package_id=story_id, parent_id=feature_id)

# Note: If no Features, link Story directly to Epic and use "Story 1.1" numbering
```

### Work Status Flow

```python
# Start work
mcp_openproject_update_work_package(
    work_package_id=work_id,
    status_id={config.openproject.statuses.in_progress}
)

# Mark developed (after implementation complete)
mcp_openproject_update_work_package(
    work_package_id=work_id,
    status_id={config.openproject.statuses.developed}
)

# Move to review/testing
mcp_openproject_update_work_package(
    work_package_id=work_id,
    status_id={config.openproject.statuses.in_testing}
)

# Mark tested (after validation passes)
mcp_openproject_update_work_package(
    work_package_id=work_id,
    status_id={config.openproject.statuses.tested}
)

# Complete
mcp_openproject_update_work_package(
    work_package_id=work_id,
    status_id={config.openproject.statuses.closed}
)

# For Tasks: Use update_task_status_and_parent() to automatically update parent Story
# For Bugs: Use update_bug_status_and_check_story() to check parent Story when closing
```

### Query Open Work

```python
# Get all open work for project
work_packages = mcp_openproject_list_work_packages(
    project_id={config.openproject.project_id},
    status="open"
)

# Search for specific items
results = mcp_openproject_search_work_packages(
    query="authentication",
    project_id={config.openproject.project_id},
    status="open"
)
```
