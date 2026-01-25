---
name: 'step-04-final-validation'
description: 'Validate complete coverage of all requirements and ensure implementation readiness'

# Path Definitions
workflow_path: '{project-root}/_bmad/bmm/workflows/3-solutioning/create-epics-and-stories'

# File References
thisStepFile: '{workflow_path}/steps/step-04-final-validation.md'
workflowFile: '{workflow_path}/workflow.md'
outputFile: '{planning_artifacts}/epics.md'

# Task References
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'

# Template References
epicsTemplate: '{workflow_path}/templates/epics-template.md'
---

# Step 4: Final Validation

## STEP GOAL:

To validate complete coverage of all requirements and ensure stories are ready for development.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: Process validation sequentially without skipping
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a product strategist and technical specifications writer
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring validation expertise and quality assurance
- ✅ User brings their implementation priorities and final review

### Step-Specific Rules:

- 🎯 Focus ONLY on validating complete requirements coverage
- 🚫 FORBIDDEN to skip any validation checks
- 💬 Validate FR coverage, story completeness, and dependencies
- 🚪 ENSURE all stories are ready for development

## EXECUTION PROTOCOLS:

- 🎯 Validate every requirement has story coverage
- 💾 Check story dependencies and flow
- 📖 Verify architecture compliance
- 🚫 FORBIDDEN to approve incomplete coverage

## CONTEXT BOUNDARIES:

- Available context: Complete epic and story breakdown from previous steps
- Focus: Final validation of requirements coverage and story readiness
- Limits: Validation only, no new content creation
- Dependencies: Completed story generation from Step 3

## VALIDATION PROCESS:

### 1. FR Coverage Validation

Review the complete epic and story breakdown to ensure EVERY FR is covered:

**CRITICAL CHECK:**

- Go through each FR from the Requirements Inventory
- Verify it appears in at least one story
- Check that acceptance criteria fully address the FR
- No FRs should be left uncovered

### 2. Architecture Implementation Validation

**Check for Starter Template Setup:**

- Does Architecture document specify a starter template?
- If YES: Epic 1 Story 1 must be "Set up initial project from starter template"
- This includes cloning, installing dependencies, initial configuration

**Database/Entity Creation Validation:**

- Are database tables/entities created ONLY when needed by stories?
- ❌ WRONG: Epic 1 creates all tables upfront
- ✅ RIGHT: Tables created as part of the first story that needs them
- Each story should create/modify ONLY what it needs

### 3. Story Quality Validation

**CRITICAL:** Every Story MUST have a test task (Task X.Y.T). Verify this requirement is met.

**CRITICAL: INCREMENTAL DEVELOPMENT** - Verify each story can be verified with previously implemented work, NOT dependent on future work.

**Each story must:**

- Be completable by a single dev agent
- Have clear acceptance criteria
- Reference specific FRs it implements
- Include necessary technical details
- **Not have forward dependencies** (can only depend on PREVIOUS stories)
- Be implementable without waiting for future stories
- **Be verifiable incrementally** - can be tested with previous work, not blocked by future work
- **Dependencies flow forward only** - Story N can depend on Story N-1, N-2, etc., but NOT on Story N+1

### 4. Feature Structure Validation (if Features exist)

**Check that:**

- Features represent functional capabilities, not technical layers
- Features are appropriately sized for integration testing
- Features have clear scope (included/excluded)
- Integration test scope is identified for each Feature
- Stories are properly organized under Features
- **MANDATORY: Each Feature has an Integration Test Story (Story X.Y.T) identified/created** - Feature cannot be closed without this story

### 5. Epic Structure Validation

**Check that:**

- Epics deliver user value, not technical milestones
- Dependencies flow naturally
- Foundation stories only setup what's needed
- No big upfront technical work
- Features (if present) properly organize stories

### 6. Dependency Validation (CRITICAL)

**Epic Independence Check:**

- Does each epic deliver COMPLETE functionality for its domain?
- Can Epic 2 function without Epic 3 being implemented?
- Can Epic 3 function standalone using Epic 1 & 2 outputs?
- ❌ WRONG: Epic 2 requires Epic 3 features to work
- ✅ RIGHT: Each epic is independently valuable

**Within-Epic Story Dependency Check:**
For each epic (and Feature if applicable), review stories in order:

- **If Features exist**: Check dependencies within Feature (Story N.F.1, N.F.2, etc.)
- **If no Features**: Check dependencies within Epic (Story N.1, N.2, etc.)
- Can Story N.F.1 (or N.1) be completed without future stories?
- Can Story N.F.2 (or N.2) be completed using only previous story output?
- Can Story N.F.3 (or N.3) be completed using only previous stories?
- ❌ WRONG: "This story depends on a future story"
- ❌ WRONG: Story references features not yet implemented
- ✅ RIGHT: Each story builds only on previous stories

**Feature Dependency Check (if Features exist):**
- Can Feature N.1 be completed without Feature N.2?
- Can Feature N.2 use Feature N.1 outputs but function independently?
- ✅ RIGHT: Features can build on previous Features but must be independently testable

### 7. Feature Integration Test Requirements Validation (if Features exist)

**Check that:**

- Each Feature has identified integration test scope
- Feature integration test requirements are documented
- Features are sized appropriately for integration testing
- Feature boundaries are clear and testable

### 8. Complete and Save

If all validations pass:

- Update any remaining placeholders in the document
- Ensure proper formatting
- Save the final epics.md

**Present Final Menu:**
**All validations complete!** [C] Complete Workflow

When C is selected, the workflow is complete and the epics.md is ready for development.
