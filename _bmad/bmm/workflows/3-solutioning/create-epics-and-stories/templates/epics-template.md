---
stepsCompleted: []
inputDocuments: []
---

# {{project_name}} - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for {{project_name}}, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

{{fr_list}}

### NonFunctional Requirements

{{nfr_list}}

### Additional Requirements

{{additional_requirements}}

### FR Coverage Map

{{requirements_coverage_map}}

## Epic List

{{epics_list}}

<!-- Repeat for each epic in epics_list (N = 1, 2, 3...) -->

## Epic {{N}}: {{epic_title_N}}

{{epic_goal_N}}

<!-- If Features exist, repeat for each Feature (F = 1, 2, 3...) within epic N -->
<!-- If no Features, skip Feature section and go directly to stories -->

### Feature {{N}}.{{F}}: {{feature_name_N_F}}

**Functional Capability:** {{feature_description}}

**Scope:**
- **Included:** {{stories_and_functionality_included}}
- **Excluded:** {{functionality_explicitly_excluded}}

**Integration Test Scope:**
{{what_will_be_tested_at_feature_level}}

<!-- Repeat for each story (M = 1, 2, 3...) within Feature F (or Epic N if no Features) -->

### Story {{N}}.{{F}}.{{M}}: {{story_title_N_F_M}}
<!-- OR Story {{N}}.{{M}}: {{story_title_N_M}} if no Features -->

As a {{user_type}},
I want {{capability}},
So that {{value_benefit}}.

**Acceptance Criteria:**

<!-- for each AC on this story -->

**Given** {{precondition}}
**When** {{action}}
**Then** {{expected_outcome}}
**And** {{additional_criteria}}

<!-- End story repeat -->
