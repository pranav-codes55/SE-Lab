# Lab 4: LLM-Assisted Debugging & Code Repair (Match-3 Gem Swap)

**Student:** R P Pranav (PES2UG24CS917)  
**Assigned Game:** Match-3 Gem Swap (Roll #57)  

---

## Overview

In this lab, an object-oriented grid-based puzzle game implemented with Pygame was debugged and extended using an LLM-assisted workflow.

### Completed Tasks:
1. **Task 1: Invalid Swap Move Deduction Bug**
   - Fixed logic so that invalid swaps that do not produce any 3-in-a-row combination revert gems without docking moves.
2. **Task 2: Cascade Combo Multiplier**
   - Implemented sequential point multipliers for successive falling tile chain reactions within a single turn.
3. **Task 3: 4-in-a-Row Special Line-Clear Gems (Bombs)**
   - Added functionality where 4 matching gems merge into an enhanced bomb gem that detonates an entire row or column when subsequently matched.
4. **Task 4: Idle Hint Indicator**
   - Implemented an automatic hint indicator that shimmers and highlights an available valid adjacent swap if no user input is received for 5 seconds.

### Files:
- `main.py`: Entry point and Pygame loop.
- `game/board.py`: Board data model, gravity mechanics, match resolution, and hint generator.
- `game/game_engine.py`: Event handling, input dispatch, timer updates, and rendering.
- `requirements.txt`: Python package requirements (`pygame`).
