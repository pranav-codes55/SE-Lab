# Lab 7: Fuzz Testing for Input Validation Bugs

**Student:** R P Pranav (PES2UG24CS917)  
**Semester / Section:** 5C  
**Assigned System:** Income Tax Parser (Roll #57)  

---

## Overview

This lab explored fuzz testing as a dynamic security and robustness evaluation technique, using the **Hypothesis** property-based testing framework to identify and fix input validation bugs in `income_tax_parser.py`.

### Key Deliverables:
- **`income_tax_parser.py`**: Fixed and defensive parser implementation fortified against unexpected inputs, non-string data types, boundary edge cases, malformed tokens, and crash scenarios.
- **`test_income_tax_parser.py`**: Hypothesis fuzz test suite testing arbitrary generated strings and edge cases across all three parser functions.
- **`PES2UG24CS917_Lab7_Report.pdf`**: Complete multi-screenshot lab submission document containing:
  - **SS1**: Buggy module execution crashing with `ValueError` on malformed user input.
  - **SS2**: Hypothesis test failure tracebacks across all functions against the unhardened module.
  - **SS3**: Fixed module execution demonstrating graceful input handling (`Invalid input`) without crashes.
  - **SS4**: Hypothesis test suite execution passing 100% cleanly on the hardened module.
- **`PES2UG24CS917_Lab7_Report.docx`**: Word document source for the submission report.
- **`Lab_7_FuzzTesting_Student_Handout.pdf`**: Official lab manual and instructions.
