import random
import math
import pygame

GRID_SIZE = 8
TILE_SIZE = 60
GEM_COLORS = [
    (220, 50, 50),   # Red
    (50, 200, 50),   # Green
    (50, 100, 240),  # Blue
    (240, 200, 40),  # Yellow
    (180, 50, 220),  # Purple
    (240, 130, 40),  # Orange
]


class Gem:
   
    def __init__(self, color, target_row, col, is_bomb=False, bomb_type=None):
        self.color = color
        self.target_row = target_row
        self.col = col
        self.is_bomb = is_bomb
        self.bomb_type = bomb_type  # 'row' or 'col'
        # Start higher up to animate falling down
        self.current_y = (target_row - 2) * TILE_SIZE
        self.target_y = target_row * TILE_SIZE
        self.fall_speed = 12.0

    def update(self):
        if self.current_y < self.target_y:
            self.current_y += self.fall_speed
            if self.current_y > self.target_y:
                self.current_y = self.target_y

    def is_animating(self):
        return self.current_y < self.target_y


class Board:
    """Manages animated gem grid, gravity drops, score, and game limits."""

    def __init__(self, offset_x, offset_y, target_score=500, max_moves=20):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.target_score = target_score
        self.max_moves = max_moves
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected = None
        self.score = 0
        self.moves_remaining = max_moves
        self.last_swap = None
        self.hint = None
        self.reset()

    def reset(self):
        """Reset board grid, score, and move limits."""
        self.score = 0
        self.moves_remaining = self.max_moves
        self.selected = None
        self.last_swap = None
        self.hint = None
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                color = random.choice(GEM_COLORS)
                gem = Gem(color, r, c)
                gem.current_y = gem.target_y  # Snap instantly on initial start
                self.grid[r][c] = gem

        self.resolve_matches()
        self.score = 0

    def is_animating(self):
        """Returns True if any gem is currently dropping down."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] and self.grid[r][c].is_animating():
                    return True
        return False

    def swap_gems(self, pos1, pos2):
        """Swap positions and target render coordinates of two gems."""
        r1, c1 = pos1
        r2, c2 = pos2

        g1, g2 = self.grid[r1][c1], self.grid[r2][c2]
        self.grid[r1][c1], self.grid[r2][c2] = g2, g1

        if self.grid[r1][c1]:
            self.grid[r1][c1].target_row = r1
            self.grid[r1][c1].col = c1
            self.grid[r1][c1].target_y = r1 * TILE_SIZE
            self.grid[r1][c1].current_y = r1 * TILE_SIZE

        if self.grid[r2][c2]:
            self.grid[r2][c2].target_row = r2
            self.grid[r2][c2].col = c2
            self.grid[r2][c2].target_y = r2 * TILE_SIZE
            self.grid[r2][c2].current_y = r2 * TILE_SIZE

    def is_adjacent(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def find_match_details(self):
        """Scan grid for matches and identify 4-in-a-row groups for bomb creation."""
        matched = set()
        four_matches = []  # list of (coords_list, orientation, color)

        # Horizontal runs
        for r in range(GRID_SIZE):
            c = 0
            while c < GRID_SIZE:
                gem = self.grid[r][c]
                if not gem:
                    c += 1
                    continue
                run = [(r, c)]
                c_next = c + 1
                while c_next < GRID_SIZE and self.grid[r][c_next] and self.grid[r][c_next].color == gem.color:
                    run.append((r, c_next))
                    c_next += 1
                if len(run) >= 3:
                    matched.update(run)
                    if len(run) >= 4:
                        four_matches.append((run, 'row', gem.color))
                c = c_next

        # Vertical runs
        for c in range(GRID_SIZE):
            r = 0
            while r < GRID_SIZE:
                gem = self.grid[r][c]
                if not gem:
                    r += 1
                    continue
                run = [(r, c)]
                r_next = r + 1
                while r_next < GRID_SIZE and self.grid[r_next][c] and self.grid[r_next][c].color == gem.color:
                    run.append((r_next, c))
                    r_next += 1
                if len(run) >= 3:
                    matched.update(run)
                    if len(run) >= 4:
                        four_matches.append((run, 'col', gem.color))
                r = r_next

        return matched, four_matches

    def find_matches(self):
        """Scan grid for horizontal and vertical 3-in-a-row color matches."""
        matched, _ = self.find_match_details()
        return matched

    def detonate_bomb(self, pos):
        """Trigger detonation of a bomb gem at pos=(r, c), clearing its row or column."""
        r, c = pos
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            gem = self.grid[r][c]
            if gem and gem.is_bomb:
                return self.resolve_matches(trigger_coords={pos})
        return 0

    def find_hint(self):
        """Find a valid adjacent pair of gems that would produce a match if swapped."""
        # 1. Check horizontal swaps
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 1):
                if self.grid[r][c] and self.grid[r][c + 1]:
                    self.grid[r][c], self.grid[r][c + 1] = self.grid[r][c + 1], self.grid[r][c]
                    matches = self.find_matches()
                    self.grid[r][c], self.grid[r][c + 1] = self.grid[r][c + 1], self.grid[r][c]
                    if matches:
                        return ((r, c), (r, c + 1))

        # 2. Check vertical swaps
        for r in range(GRID_SIZE - 1):
            for c in range(GRID_SIZE):
                if self.grid[r][c] and self.grid[r + 1][c]:
                    self.grid[r][c], self.grid[r + 1][c] = self.grid[r + 1][c], self.grid[r][c]
                    matches = self.find_matches()
                    self.grid[r][c], self.grid[r + 1][c] = self.grid[r + 1][c], self.grid[r][c]
                    if matches:
                        return ((r, c), (r + 1, c))

        return None

    def drop_and_refill(self):
        for c in range(GRID_SIZE):
            empty_slots = 0
            for r in range(GRID_SIZE - 1, -1, -1):
                if self.grid[r][c] is None:
                    empty_slots += 1
                elif empty_slots > 0:
                    gem = self.grid[r][c]
                    gem.target_row = r + empty_slots
                    gem.col = c
                    gem.target_y = (r + empty_slots) * TILE_SIZE
                    self.grid[r + empty_slots][c] = gem
                    self.grid[r][c] = None

            for r in range(empty_slots):
                color = random.choice(GEM_COLORS)
                gem = Gem(color, r, c)
                gem.current_y = -((empty_slots - r) * TILE_SIZE)
                self.grid[r][c] = gem

    def resolve_matches(self, trigger_coords=None):
        total_points = 0
        cascade_step = 1
        first_pass = True
        while True:
            matched, four_matches = self.find_match_details()
            if first_pass and trigger_coords:
                matched = matched | set(trigger_coords)
            first_pass = False

            if not matched:
                break

            # 1. Determine bombs to create from 4-in-a-row matches
            bombs_to_spawn = {}  # (r, c) -> (color, bomb_type)
            for run, orientation, color in four_matches:
                spawn_pos = None
                if hasattr(self, 'last_swap') and self.last_swap:
                    for p in self.last_swap:
                        if p in run:
                            spawn_pos = p
                            break
                if not spawn_pos:
                    spawn_pos = run[len(run) // 2]
                bombs_to_spawn[spawn_pos] = (color, orientation)

            # 2. Check for bomb detonation among matched gems
            cleared_coords = set(matched)
            bombs_to_detonate = [
                pos for pos in matched
                if self.grid[pos[0]][pos[1]] and self.grid[pos[0]][pos[1]].is_bomb
            ]
            detonated_bombs = set()

            while bombs_to_detonate:
                b_pos = bombs_to_detonate.pop()
                if b_pos in detonated_bombs:
                    continue
                detonated_bombs.add(b_pos)
                bgem = self.grid[b_pos[0]][b_pos[1]]
                if not bgem:
                    continue

                br, bc = b_pos
                affected = set()
                if bgem.bomb_type == 'col':
                    for r in range(GRID_SIZE):
                        affected.add((r, bc))
                else:  # 'row' or default
                    for c in range(GRID_SIZE):
                        affected.add((br, c))

                for pos in affected:
                    if pos not in cleared_coords:
                        cleared_coords.add(pos)
                        pr, pc = pos
                        if self.grid[pr][pc] and self.grid[pr][pc].is_bomb and pos not in detonated_bombs:
                            bombs_to_detonate.append(pos)

            # 3. Ensure newly spawned bombs survive the initial match
            for spawn_pos in bombs_to_spawn:
                cleared_coords.discard(spawn_pos)

            # 4. Award points based on cascade multiplier
            round_points = len(cleared_coords) * 10 * cascade_step
            total_points += round_points

            # 5. Clear tiles
            for r, c in cleared_coords:
                self.grid[r][c] = None

            # 6. Place the newly spawned Bomb Gems
            for (sr, sc), (b_color, b_type) in bombs_to_spawn.items():
                bgem = Gem(b_color, sr, sc, is_bomb=True, bomb_type=b_type)
                bgem.current_y = sr * TILE_SIZE
                self.grid[sr][sc] = bgem

            # 7. Reset last_swap so subsequent cascades don't use player swap pos
            self.last_swap = None

            # 8. Drop and refill
            self.drop_and_refill()
            cascade_step += 1

        return total_points

    def process_swap(self, pos1, pos2):
        if not self.is_adjacent(pos1, pos2) or self.is_game_over() or self.is_animating():
            return False

        self.hint = None
        self.swap_gems(pos1, pos2)
        matches = self.find_matches()

        if not matches:
            self.swap_gems(pos1, pos2)  # Revert invalid swap
            return False

        self.last_swap = (pos1, pos2)
        self.moves_remaining -= 1
        points_earned = self.resolve_matches()
        self.score += points_earned
        return True

    def is_game_over(self):
        return self.score >= self.target_score or self.moves_remaining <= 0

    def check_result(self):
        if self.score >= self.target_score:
            return "WIN"
        if self.moves_remaining <= 0:
            return "LOSS"
        return None

    def update(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c]:
                    self.grid[r][c].update()

    def render(self, surface):
        board_rect = pygame.Rect(
            self.offset_x, self.offset_y, GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE
        )
        pygame.draw.rect(surface, (20, 22, 28), board_rect, border_radius=8)
        pygame.draw.rect(surface, (60, 65, 75), board_rect, width=3, border_radius=8)

        ticks = pygame.time.get_ticks()

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                gem = self.grid[r][c]
                if gem:
                    x = self.offset_x + c * TILE_SIZE
                    y = self.offset_y + gem.current_y
                    tile_rect = pygame.Rect(x + 2, int(y) + 2, TILE_SIZE - 4, TILE_SIZE - 4)

                    pygame.draw.rect(surface, gem.color, tile_rect, border_radius=10)
                    pygame.draw.rect(
                        surface, (255, 255, 255), tile_rect, width=1, border_radius=10
                    )

                    if gem.is_bomb:
                        # Animated glowing border pulsing between golden-yellow and white
                        glow_color = (255, 225, 80) if (ticks // 250) % 2 == 0 else (255, 255, 255)
                        pygame.draw.rect(surface, glow_color, tile_rect, width=3, border_radius=10)

                        # Center bomb emblem
                        cx = x + TILE_SIZE // 2
                        cy = int(y) + TILE_SIZE // 2
                        pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 13)
                        pygame.draw.circle(surface, (30, 32, 40), (cx, cy), 10)
                        pygame.draw.circle(surface, (255, 215, 0), (cx, cy), 6)

                        # Directional stripe indicator
                        if gem.bomb_type == 'row':
                            pygame.draw.line(surface, (255, 255, 255), (x + 6, cy), (x + TILE_SIZE - 6, cy), 3)
                        elif gem.bomb_type == 'col':
                            pygame.draw.line(surface, (255, 255, 255), (cx, int(y) + 6), (cx, int(y) + TILE_SIZE - 6), 3)

        # Render idle hint with a pulsing golden-white shimmer effect
        if self.hint:
            pulse = 0.5 + 0.5 * math.sin(ticks * 0.007)
            hint_color = (
                255,
                int(215 + 40 * pulse),
                int(40 + 190 * pulse),
            )
            border_w = int(3 + pulse * 2)

            for hr, hc in self.hint:
                if 0 <= hr < GRID_SIZE and 0 <= hc < GRID_SIZE:
                    gem = self.grid[hr][hc]
                    if gem:
                        hx = self.offset_x + hc * TILE_SIZE
                        hy = self.offset_y + gem.current_y
                        hint_rect = pygame.Rect(hx + 1, int(hy) + 1, TILE_SIZE - 2, TILE_SIZE - 2)
                        pygame.draw.rect(surface, hint_color, hint_rect, width=border_w, border_radius=12)

        if self.selected:
            sr, sc = self.selected
            sel_x = self.offset_x + sc * TILE_SIZE
            sel_y = self.offset_y + sr * TILE_SIZE
            sel_rect = pygame.Rect(sel_x + 2, sel_y + 2, TILE_SIZE - 4, TILE_SIZE - 4)
            pygame.draw.rect(
                surface, (255, 255, 255), sel_rect, width=4, border_radius=10
            )