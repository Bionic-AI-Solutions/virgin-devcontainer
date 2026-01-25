---
name: 'step-02b-create-features'
description: 'Create Features for each epic to organize stories into testable, cohesive chunks. Features are recommended for new epics to enable Feature-level integration testing.'

# Path Definitions
workflow_path: '{project-root}/_bmad/bmm/workflows/3-solutioning/create-epics-and-stories'

# File References
thisStepFile: '{workflow_path}/steps/step-02b-create-features.md'
nextStepFile: '{workflow_path}/steps/step-03-create-stories.md'
workflowFile: '{workflow_path}/workflow.md'
outputFile: '{planning_artifacts}/epics.md'

# Task References
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'

# Template References
epicsTemplate: '{workflow_path}/templates/epics-template.md'
---

# Step 2b: Create Features for Epics

## STEP GOAL:

To create Features for each epic, organizing stories into testable, cohesive chunks that enable Feature-level integration testing. Features are **recommended** for new epics going forward.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a product strategist and technical specifications writer
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring Feature design and organization expertise
- ✅ User brings their product vision and testing priorities

### Step-Specific Rules:

- 🎯 Focus ONLY on creating Features for approved epics
- 🚫 FORBIDDEN to create stories in this step
- 💬 Organize Features around functional capabilities and integration boundaries
- 🚪 GET explicit approval for Feature structure
- 🔗 **CRITICAL: Features enable Feature-level integration testing before closure**

## EXECUTION PROTOCOLS:

- 🎯 Design Features collaboratively based on epic structure
- 💾 Update Feature structure in {outputFile}
- 📖 Document Feature-to-Epic relationships
- 🚫 FORBIDDEN to load next step until user approves Feature structure

## FEATURE CREATION PROCESS:

### 1. Review Epic Structure

Load {outputFile} and review:

- Approved epics_list from Step 2
- Epic goals and FR coverage
- Epic dependencies and flow

### 2. Explain Feature Purpose and Benefits

**FEATURE PURPOSE:**

Features serve as an intermediate layer between Epics and Stories that:

1. **Enable Integration Testing**: Features require Feature-level integration tests before closure
2. **Organize Stories**: Group related stories into cohesive functional capabilities
3. **Improve Testability**: Each Feature can be tested independently as a complete unit
4. **Support Incremental Delivery**: Features can be delivered and validated independently

**FEATURE DESIGN PRINCIPLES:**

1. **Functional Cohesion**: Group stories that work together to deliver a complete capability
2. **Integration Boundaries**: Features should represent natural integration test boundaries
3. **Testable Units**: Each Feature should be testable end-to-end
4. **Story Organization**: Features help organize stories within large epics

**FEATURE vs EPIC vs STORY:**

- **Epic**: High-level user value (e.g., "User Authentication & Profiles")
- **Feature**: Functional capability within epic (e.g., "User Registration", "User Login", "Profile Management")
- **Story**: Specific user action (e.g., "Register with Email", "Login with Password")

**CRITICAL: Feature Specification Artifacts Required**

When Features are created in OpenProject and moved to "In specification" status, the following artifacts MUST be attached before the Feature can transition to "Specified" status:

1. ✅ **Feature Architecture Document** - Feature-specific architecture design
2. ✅ **API Documentation** (if Feature includes APIs) - API endpoint specifications, request/response schemas
3. ✅ **UI Mocks/Designs** (if Feature includes UI) - UI mockups (images: PNG, JPG, SVG, or design files like Figma, Sketch)
4. ✅ **Feature Scope Document** - Included/excluded functionality, story breakdown

**Protocol:** Scrum Master (SM) is accountable for verifying these artifacts are attached before allowing Feature → "Specified" transition. Product Manager (PM) is responsible for creating and attaching these artifacts during Feature grooming.

### 3. Determine Feature Strategy

**Ask the user:**

"Do you want to create Features for these epics? Features are recommended for new epics as they enable Feature-level integration testing and better organization of stories."

**Options:**
- **YES**: Create Features for all epics (recommended)
- **NO**: Skip Features, create stories directly under epics (for simple epics or existing projects)
- **SELECTIVE**: Create Features only for specific epics

**If user selects NO:**
- Skip to next step (step-03-create-stories)
- Stories will be created directly under epics
- Note: This is acceptable for simple epics or when retrofitting existing epics

**If user selects YES or SELECTIVE:**
- Proceed with Feature creation

### 4. Design Features for Each Epic

For each epic (or selected epics), work with user to identify Features:

#### A. Epic Analysis

For each epic:

1. **Review Epic Goal**: What user value does this epic deliver?
2. **Review FR Coverage**: Which functional requirements are in this epic?
3. **Identify Capabilities**: What distinct functional capabilities are needed?

#### B. Feature Identification

**Feature Identification Guidelines:**

- Look for natural groupings of related functionality
- Consider integration test boundaries
- Identify cohesive functional capabilities
- Think about what can be tested together

**Example Feature Breakdown:**

_Epic 1: User Authentication & Profiles_

- Feature 1.1: User Registration
  - Stories: Register with Email, Email Verification, Profile Setup
- Feature 1.2: User Authentication
  - Stories: Login with Password, Password Reset, Session Management
- Feature 1.3: Profile Management
  - Stories: View Profile, Edit Profile, Privacy Settings

_Epic 2: Content Creation_

- Feature 2.1: Content Authoring
  - Stories: Create Post, Edit Post, Save Draft
- Feature 2.2: Content Publishing
  - Stories: Publish Post, Schedule Post, Unpublish Post
- Feature 2.3: Content Media
  - Stories: Upload Image, Embed Video, Manage Attachments

#### C. Create Feature Structure

For each Feature, document:

1. **Feature Number**: Epic.Feature (e.g., 1.1, 1.2, 2.1)
2. **Feature Name**: Clear functional capability name
3. **Feature Description**: What capability this Feature provides
4. **Story Preview**: Brief overview of stories that will be in this Feature
5. **Integration Test Scope**: What will be tested at Feature level
6. **MANDATORY: Integration Test Story**: Every Feature MUST include an Integration Test Story (Story X.Y.T) for validating the complete Feature

**CRITICAL:** When creating Features in OpenProject, ensure each Feature includes an Integration Test Story (Story X.Y.T). This story validates the complete Feature functionality and must be completed before the Feature can be closed. The `update_feature_status_based_on_stories()` helper function enforces this requirement and blocks Feature progression if Integration Test Story is missing or not closed.

**Integration Test Story Format:**
- **Story Number**: Story X.Y.T (where T indicates Test/Integration story)
- **Story Title**: "Feature X.Y Integration Testing and Validation"
- **User Story**: "As a Test Team, I want to validate the complete Feature X.Y functionality, So that I can ensure all stories work together and the Feature meets its acceptance criteria."
- **Acceptance Criteria**: Include Given/When/Then statements for Feature-level validation
- **Test Activities**: List all integration test activities

**Format:**

```
## Epic {{N}}: {{epic_title_N}}

{{epic_goal_N}}

### Feature {{N}}.{{F}}: {{feature_name_N_F}}

**Functional Capability:** {{feature_description}}

**Scope:**
- **Included:** {{stories_and_functionality_included}}
- **Excluded:** {{functionality_explicitly_excluded}}

**Story Preview:**
- Story {{N}}.{{F}}.1: {{story_name}}
- Story {{N}}.{{F}}.2: {{story_name}}
- ...

**Integration Test Scope:**
{{what_will_be_tested_at_feature_level}}
```

### 5. Present Feature Structure for Review

Display the complete Feature structure:

- Features per epic
- Feature descriptions and scope
- Story previews
- Integration test scope

### 6. Collaborative Refinement

Ask user:

- "Does this Feature structure organize stories logically?"
- "Are Features appropriately sized for integration testing?"
- "Do Features represent natural functional boundaries?"
- "Should we adjust any Feature groupings?"

### 7. Get Final Approval

**CRITICAL:** Must get explicit user approval:

"Do you approve this Feature structure for proceeding to story creation?"

If user wants changes:

- Make the requested adjustments
- Update the Feature structure
- Re-present for approval
- Repeat until approval is received

## CONTENT TO UPDATE IN DOCUMENT:

After approval, update {outputFile}:

1. Add Feature sections under each Epic
2. Document Feature-to-Epic relationships
3. Include Feature descriptions and scope
4. Note integration test requirements

**Document Structure:**

```
## Epic {{N}}: {{epic_title_N}}

{{epic_goal_N}}

### Feature {{N}}.{{F}}: {{feature_name_N_F}}

{{feature_description}}

[Stories will be created under Features in next step]
```

### 8. Present MENU OPTIONS

Display: "**Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue"

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}
- IF P: Execute {partyModeWorkflow}
- IF C: Save approved Feature structure to {outputFile}, update frontmatter, then only then load, read entire file, then execute {nextStepFile}
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#8-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution completes, redisplay the menu
- User can chat or ask questions - always respond when conversation ends, redisplay the menu options

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and the approved Feature structure is saved to document, will you then load, read entire file, then execute {nextStepFile} to execute and begin story creation step.

**Note:** If user chose to skip Features, proceed directly to story creation with stories under epics.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Features designed around functional capabilities
- Features organized logically within epics
- Feature structure approved by user
- Integration test scope identified for each Feature
- Document updated with Feature structure

### ❌ SYSTEM FAILURE:

- Features organized by technical layers
- Missing Feature descriptions
- No user approval obtained
- Feature structure not saved to document

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
