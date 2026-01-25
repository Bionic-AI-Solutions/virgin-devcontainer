# BMAD BMM Workflow: groom-story

**Workflow Type:** Story Grooming  
**Agent:** PM (Product Manager)  
**Phase:** Pre-Implementation  
**Status:** MANDATORY WORKFLOW

## Purpose

Groom a story by breaking it down into implementable tasks and creating them in OpenProject BEFORE implementation begins. This is a mandatory agile practice that must be completed before the story moves to "In progress".

**CRITICAL:** If the Story is in "In specification" status, ensure all required specification artifacts are attached before requesting transition to "Specified" status. Scrum Master (SM) will verify artifacts before allowing the transition.

## Workflow Steps

### Step 1: Review Story

1. Get story from OpenProject
2. Review acceptance criteria
3. Identify all tasks needed to complete the story
4. Ensure tasks are granular (30 min - 4 hours of work)
5. Map each task to specific acceptance criteria

### Step 2: Create Story File

1. Create story file in `_bmad-output/implementation-artifacts/`
2. Include all acceptance criteria
3. Break down into tasks with subtasks
4. Map each task to specific acceptance criteria

### Step 3: Attach Specification Artifacts (if Story is "In specification")

**CRITICAL:** If Story is in "In specification" status, ensure all required artifacts are attached:

1. ✅ **Acceptance Criteria** - Complete in Story description or as attached document
2. ✅ **UI Mocks/Designs** (if Story includes UI) - Attach UI mockups (images: PNG, JPG, SVG, or design files)
3. ✅ **Technical Specifications** (if Story requires technical details) - Attach technical spec document

**Protocol:** After attaching artifacts, request Scrum Master (SM) to verify and approve transition to "Specified" status. SM will use `mcp_openproject_list_work_package_attachments()` to verify artifacts.

### Step 4: Create Tasks in OpenProject

**CRITICAL:** All tasks MUST be created in OpenProject during grooming, before story moves to "In progress".

**⚠️ DUPLICATE PREVENTION:** Always check for existing tasks (including closed ones) before creating new tasks.

```python
# Step 4.1: Check for existing tasks (CRITICAL - prevents duplicates)
def check_existing_tasks(story_id: int) -> list[dict]:
    """
    Check for existing tasks for a story, including closed tasks.
    CRITICAL: Use status="all" to include closed tasks.
    """
    children = mcp_openproject_get_work_package_children(
        parent_id=story_id,
        status="all"  # Include closed tasks - CRITICAL!
    )
    return children.get("children", [])

# Get existing tasks
existing = check_existing_tasks(story_id)
existing_subjects = {t["subject"] for t in existing}

# Step 4.2: Define all tasks needed for the story
# CRITICAL: Every Story MUST have a test task (Task X.Y.T)
all_tasks = [
    {
        "subject": "Task 1: [Task Title]",
        "type_id": 36,  # Task
        "description": "Detailed description with acceptance criteria...",
    },
    # ... all other implementation tasks
    {
        "subject": "Task X.Y.T: Story X.Y Testing and Validation",  # MANDATORY Test task
        "type_id": {config.openproject.types.task},
        "description": """
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
        "status_id": {config.openproject.statuses.new},
        "priority_id": {config.openproject.priorities.high}  # High priority - required for story closure
    },
]

# Step 4.3: Filter out duplicates
new_tasks = [
    t for t in all_tasks
    if t["subject"] not in existing_subjects
]

if not new_tasks:
    print(f"No new tasks to create for story {story_id} (all tasks already exist)")
else:
    # Step 4.4: Bulk create new tasks
    result = mcp_openproject_bulk_create_work_packages(
        project_id={config.openproject.project_id},
        work_packages=json.dumps(new_tasks),  # Must be JSON string
        continue_on_error=True
    )
    
    # Step 4.5: Set parent relationships
    for task in result.get("created", []):
        mcp_openproject_set_work_package_parent(
            work_package_id=task["id"],
            parent_id=story_id
        )
```

### Step 5: Verify Tasks Created

1. Verify all tasks are created: `mcp_openproject_get_work_package_children(parent_id=story_id)`
2. Verify all tasks are linked (parent relationship set)
3. Verify task descriptions are complete

### Step 6: Update Story Status

**ONLY after all tasks are created:**

```python
mcp_openproject_update_work_package(
    work_package_id=story_id,
    status_id={config.openproject.statuses.in_progress}  # Use config, not hardcoded ID
)
```

## Checklist

**Before marking story as "In progress":**

- [ ] Story acceptance criteria reviewed
- [ ] Story broken down into tasks
- [ ] Story file created with all tasks
- [ ] **If Story is "In specification": All required artifacts attached (Acceptance Criteria, UI Mocks if UI, Technical Specs if required)**
- [ ] **If Story is "In specification": SM has verified artifacts and approved transition to "Specified"**
- [ ] **Checked for existing tasks (including closed) - prevents duplicates**
- [ ] All new tasks created in OpenProject
- [ ] All tasks linked to story (parent relationship)
- [ ] **MANDATORY: Test task (Task X.Y.T) created - Story cannot be closed without this task**
- [ ] Task descriptions include acceptance criteria
- [ ] Story status updated to "In progress" (use config.openproject.statuses.in_progress)

**CRITICAL:** The test task (Task X.Y.T) is MANDATORY. The Story cannot be closed until this test task is completed and closed successfully. This is enforced by the `update_story_status_based_on_tasks()` helper function.

## Outputs

1. Story file in `_bmad-output/implementation-artifacts/`
2. All tasks created in OpenProject
3. Story marked as "In progress" (ready for Dev)

## Integration with Other Workflows

- **create-story:** Creates story, then calls groom-story
- **sprint-planning:** Grooms stories for sprint, creates tasks
- **dev-story:** Verifies tasks exist before starting implementation

## References

- **Epic-Story Lifecycle:** `@bmad/bmm/workflows/epic-story-lifecycle` - Complete lifecycle, status transitions, and helper functions
- **PM Agent:** `@bmad/bmm/agents/pm` - Product Manager agent for story grooming
