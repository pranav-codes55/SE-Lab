# Software Engineering Lab Deliverables (UE24CS341A)

**Student Details:**
- **Name:** R P Pranav
- **SRN:** PES2UG24CS917
- **Course:** Software Engineering (UE24CS341A)
- **Institution:** PES University

---

## Repository Structure

```
Lab/
├── Lab 1/  # Requirements Engineering: UML Use Case & Requirements Traceability Matrix (RTM)
├── Lab 2/  # Version Control, Git Branching & CI/CD Pipeline (GitHub Actions)
├── Lab 3/  # Component Modeling & Architectural Pattern Selection
├── Lab 4/  # LLM-Assisted Debugging & Code Repair (Pygame Match-3 Gem Swap)
├── Lab 5/  # Static Code Analysis (Pylint, Bandit, Flake8)
├── Lab 6/  # White-Box Testing: Code Coverage & Branch Coverage Analysis
└── Lab 7/  # Fuzz Testing for Input Validation (Hypothesis Library)
```

---

## Lab Overview & Summaries

### [Lab 1: Requirements Engineering & Traceability](./Lab/Lab%201)
- **Topic:** Use Case Modeling & Requirements Traceability Matrix (RTM)
- **Scenario:** Digital Art Commission & Watermarking Portal
- **Deliverables:**
  - `use_case_diagram.drawio`: Complete UML Use Case diagram mapping Client Buyer and Digital Artist workflows.
  - `Digital_Art_Commission_Watermarking_Portal_RTM_PES2UG24CS917.docx`: Detailed bidirectional Requirements Traceability Matrix mapping functional and non-functional requirements to design sections, units, and test cases.

### [Lab 2: Git, Version Control & CI/CD](./Lab/Lab%202)
- **Topic:** Version Control Workflows, Testing & GitHub Actions CI Automation
- **Deliverables:**
  - Python application (`app.py`), requirements, and automated unit test suite (`tests/test_app.py`).
  - `.github/workflows/ci.yml`: Continuous Integration workflow for automated testing on push and pull requests.
  - Verification of passing tests, deliberate error injection, and revert commits.

### [Lab 3: Component Modeling & Architecture](./Lab/Lab%203)
- **Topic:** Component Modeling & Architectural Pattern Selection
- **Deliverables:**
  - `Lab_3_Architecture_Student_handout.pdf`: Lab specifications and guidelines.
  - `PES2UG24CS917_Component_Diagram.pdf` / `.docx`: UML Component Diagram with modular interfaces and ports.
  - `Lab3_Architecture_Justification_PES2UG24CS917.pdf` / `.docx`: Written justification for architectural design and pattern selection.

### [Lab 4: LLM-Assisted Debugging & Code Repair](./Lab/Lab%204)
- **Topic:** Match-3 Gem Swap Repair & Feature Implementation
- **Deliverables:**
  - Object-oriented Pygame Match-3 Gem Swap game (`main.py`, `game/board.py`, `game/game_engine.py`).
  - Task 1: Fixed invalid swap move deduction bug.
  - Task 2: Implemented cascade combo multiplier for falling chain reactions.
  - Task 3: Implemented 4-in-a-row special line-clear gems (row/column detonation bombs).
  - Task 4: Implemented idle hint indicator (5-second shimmer/pulsing highlight for available valid moves).

### [Lab 5: Static Code Analysis](./Lab/Lab%205)
- **Topic:** Static Code Analysis & Code Quality Enforcement (Pylint, Bandit, Flake8)
- **Scenario:** Support Ticket Tracker
- **Deliverables:**
  - `support_ticket_tracker_before.py`: Original script before remediation.
  - `support_ticket_tracker.py`: Clean, secure, and refactored script.
  - Before & After Analysis Reports: `pylint_report_before.txt` / `pylint_report_after.txt`, `bandit_report_before.txt` / `bandit_report_after.txt`, `flake8_report_before.txt` / `flake8_report_after.txt`.

### [Lab 6: Code Coverage & Branch Coverage](./Lab/Lab%206)
- **Topic:** White-Box Testing & Coverage Measurement
- **Scenario:** Income Tax Calculator
- **Deliverables:**
  - `income_tax.py`: Implementation under test.
  - `CodeCoverageTest_PES2UG24CS917_income_tax.py` & `BranchCoverageTest_PES2UG24CS917_income_tax.py`: Test suites achieving full statement and branch coverage.
  - `Coverage_Analysis_Terminal_Screenshots_PES2UG24CS917.pdf` / `.png`: Terminal verification reports.
  - `Git_Commits_History_PES2UG24CS917.pdf` / `.png`: Git commit progression logs.

### [Lab 7: Fuzz Testing with Hypothesis](./Lab/Lab%207)
- **Topic:** Fuzzing for Input Validation Bugs
- **Scenario:** Income Tax Parser & Validator
- **Deliverables:**
  - `Lab_7_FuzzTesting_Student_Handout.pdf`: Student instructions and guidelines.
  - `income_tax_parser.py`: Robust parser with defensive input handling against malformed inputs.
  - `test_income_tax_parser.py`: Property-based fuzz test suite using the Hypothesis library.
  - `PES2UG24CS917_Lab7_Report.pdf` / `.docx`: Authentic multi-screenshot report covering buggy module execution, failing Hypothesis tests, fixed module execution, and passing Hypothesis tests.
