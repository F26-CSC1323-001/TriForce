import math
import os
import random

import pygame

W, H = 900, 600
HERE = os.path.dirname(os.path.abspath(__file__))

#|sprite |
SPRITE_FILE = os.path.join(HERE, "sprite.png")
SPRITE_FRAMES = 41      # how many frames from my piskel drawing 
SPRITE_FPS = 7
SPRITE_HEIGHT = 240     # on-screen height of one frame
SPRITE_COLS = None      
SPRITE_AREA = pygame.Rect(W // 2 - 220, 170, 440, 320)   # sprite sits at the bottom-middle of this box

# | titles|
# name, title PNG, main colour, accent colour
GAMES = [
    ("Tekken", "tek8.png", (230, 40, 70), (255, 100, 170)),
    ("Street Fighter 6", "sf6.png", (255, 120, 40), (255, 205, 80)),
    ("Guilty Gear Strive", "ggs.png", (255, 60, 140), (255, 165, 60)),
]
CELL_W, CELL_H, CELL_GAP, CELL_Y = 270, 126, 20, 24

#|screen 1: choose your input|
INPUTS = [
    ("Keyboard", ""),
    ("Fight Stick", ""),
    ("Controller", ""),

]

# |screen 3: choose what to practice |
PRACTICES = [
    ("Attack Practice", "Guitar Hero style: hit the motion + button on the line"),
    ("Defense Practice", "Hold the direction for each color, push block on yellow"),
    ("Back", ""),
]

# |screen 3b: pick a difficulty (shown after choosing Attack or Defense)|
DIFFICULTIES = [
    ("Easy", "Slow and forgiving, simple inputs only"),
    ("Medium", "Standard speed and timing"),
    ("Hard", "Fast, tight timing, full move list (defense hides the legend)"),
    ("Back", ""),
]

# Helps with my game title pngs that have bad backgrounds
TITLE_REMOVE_WHITE = True          
TITLE_WHITE_TOLERANCE = 40         
TITLE_WHITE_ONLY_OUTSIDE = False   
                                 

BG_EDGE, BG_CENTER = (4, 5, 9), (14, 17, 28)
FG, MUTED, LINE = (232, 234, 240), (128, 134, 154), (44, 50, 72)
CELL_BG = (14, 17, 26)
DEFAULT_MAIN, DEFAULT_ACC = (90, 140, 255), (150, 190, 255)
GOOD_COL, BAD_COL = (110, 225, 150), (255, 90, 90)

LETTER_KEYS = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e,
               pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j]

# ---------------------------------------------------------------------------
# PRACTICE SETTINGS  (everything you'll probably want to tweak is up here)
# ---------------------------------------------------------------------------
# Movement: arrow keys or WASD.  You always face RIGHT, so LEFT = back.
# Buttons (arcade layout):   U I O
#                            J K L
BTN_KEYS = [pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_j, pygame.K_k, pygame.K_l]
BTN_KEY_NAMES = "UIOJKL"
BTN_COLORS = [(255, 120, 120), (255, 190, 90), (255, 235, 110),
              (110, 170, 255), (120, 225, 150), (200, 140, 255)]

# per game: (label shown on screen, key slot 0-5 from BTN_KEYS)
GAME_BUTTONS = {
    "Tekken": [("1", 0), ("2", 1), ("3", 3), ("4", 4)],
    "Street Fighter 6": [("LP", 0), ("MP", 1), ("HP", 2), ("LK", 3), ("MK", 4), ("HK", 5)],
    "Guilty Gear Strive": [("P", 0), ("K", 1), ("S", 2), ("H", 3), ("D", 4)],
}

# ---- attack practice ----
# travel = seconds for a note to fall to the line, gap = random seconds between notes,
# approach = how early before the line you may start a motion, perfect/good = timing windows (seconds),
# tier = hardest move tier allowed (1 = buttons + simple, 2 = + QCF/dashes, 3 = + DP/QCB/long motions)
ATTACK_LEVELS = {
    "Easy":   {"travel": 2.8, "gap": (1.8, 2.5), "approach": 1.00, "perfect": 0.12, "good": 0.25, "tier": 1},
    "Medium": {"travel": 2.2, "gap": (1.2, 1.8), "approach": 0.70, "perfect": 0.09, "good": 0.18, "tier": 2},
    "Hard":   {"travel": 1.6, "gap": (0.8, 1.3), "approach": 0.55, "perfect": 0.07, "good": 0.14, "tier": 3},
}

# each note: (direction steps in numpad notation, needs a button?, small name shown beside it, tier)
# numpad:  7 8 9 / 4 5 6 / 1 2 3   (6 = forward, 4 = back, 2 = down)
_FIREBALL_GAME = [
    ([], True, "", 1),
    ([], True, "", 1),
    ([3], True, "d/f", 1),
    ([2, 3, 6], True, "QCF", 2),
    ([6, 6], False, "Dash", 2),
    ([4, 4], False, "Back dash", 2),
    ([6, 2, 3], True, "DP", 3),
    ([2, 1, 4], True, "QCB", 3),
]
ATTACK_POOLS = {
    "Tekken": [
        ([], True, "", 1),
        ([], True, "", 1),
        ([3], True, "d/f", 1),
        ([2], False, "Crouch", 1),
        ([6, 6], False, "Dash", 2),
        ([4, 4], False, "Back dash", 2),
        ([6, 2, 3], True, "f,d,d/f", 3),
    ],
    "Street Fighter 6": _FIREBALL_GAME,
    "Guilty Gear Strive": _FIREBALL_GAME,
}

# ---- defense practice ----
# wait = random pause before a color shows (only counts down while you're neutral),
# react = seconds you get to start holding the right thing, hold = how long the color stays up,
# push = push-block color allowed, legend = color legend shown at the start (H toggles it)
DEFENSE_LEVELS = {
    "Easy":   {"wait": (1.2, 2.5), "react": 0.90, "hold": 0.70, "push": False, "legend": True},
    "Medium": {"wait": (0.8, 2.0), "react": 0.60, "hold": 1.00, "push": True,  "legend": True},
    "Hard":   {"wait": (0.5, 1.5), "react": 0.40, "hold": 1.30, "push": True,  "legend": False},
}
RESULT_TIME = 0.9
# push block = hold these two button slots together. None = that game has no push block.
PUSH_BLOCK = {
    "Tekken": None,
    "Street Fighter 6": (1, 4),        # MP + MK (Drive Parry)
    "Guilty Gear Strive": (0, 1),      # P + K  <- check/change to the real Faultless Defense buttons
}
COLOR_BACK, COLOR_DOWNBACK, COLOR_PUSH, COLOR_FORWARD = (70, 130, 255), (255, 70, 70), (255, 210, 60), (255,255,255)


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def glow(size, color, peak=1.0, power=2.0, step=1):
    """Black-background radial glow, meant for additive blits."""
    s = pygame.Surface((size, size))
    c = size // 2
    for r in range(c, 0, -step):
        f = peak * (1 - r / c) ** power
        pygame.draw.circle(s, (int(color[0] * f), int(color[1] * f), int(color[2] * f)), (c, c), r)
    return s


def make_bg():
    s = pygame.Surface((W, H))
    s.fill(BG_EDGE)
    top = int(math.hypot(W, H) / 2)
    for r in range(top, 0, -6):
        pygame.draw.circle(s, mix(BG_CENTER, BG_EDGE, (r / top) ** 0.9), (W // 2, H // 2 + 20), r)
    return s


def find_grid(sw, sh, n):
    best = None
    for cols in range(1, n + 1):
        rows = -(-n // cols)
        if sw % cols or sh % rows:
            continue
        score = (abs(sw // cols - sh // rows), cols * rows - n)
        if best is None or score < best[0]:
            best = (score, cols, rows)
    return (best[1], best[2]) if best else None


def load_sprite_frames():
    sheet = pygame.image.load(SPRITE_FILE).convert_alpha()
    sw, sh = sheet.get_size()
    if SPRITE_COLS:
        cols, rows = SPRITE_COLS, -(-SPRITE_FRAMES // SPRITE_COLS)
    else:
        cols, rows = find_grid(sw, sh, SPRITE_FRAMES) or (1, SPRITE_FRAMES)
    fw, fh = sw // cols, sh // rows
    scale = SPRITE_HEIGHT / fh
    scale = int(scale) if scale >= 1 else scale
    size = (max(1, round(fw * scale)), max(1, round(fh * scale)))
    print(f"[sprite] sheet {sw}x{sh} -> grid {cols}x{rows}, frames {fw}x{fh}, "
          f"scale {scale}, on screen {size[0]}x{size[1]}")
    frames = []
    for i in range(SPRITE_FRAMES):
        rect = ((i % cols) * fw, (i // cols) * fh, fw, fh)
        frames.append(pygame.transform.scale(sheet.subsurface(rect).copy(), size))
    return frames


def remove_white_box(img):
    """If the image has a solid white box around it, make the white transparent."""
    w, h = img.get_size()
    lim = 255 - TITLE_WHITE_TOLERANCE

    def near_white(c):
        return c.a > 200 and c.r >= lim and c.g >= lim and c.b >= lim

    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    if not all(near_white(img.get_at(p)) for p in corners):
        return img      # no white box (already transparent), nothing to do

    if TITLE_WHITE_ONLY_OUTSIDE:
        cleared, seen = set(), set()
        stack = ([(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)]
                 + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
        while stack:
            p = stack.pop()
            if p in seen:
                continue
            seen.add(p)
            if not near_white(img.get_at(p)):
                continue
            cleared.add(p)
            x, y = p
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= q[0] < w and 0 <= q[1] < h and q not in seen:
                    stack.append(q)
    else:
        cleared = {(x, y) for x in range(w) for y in range(h) if near_white(img.get_at((x, y)))}

    out = img.copy()
    for p in cleared:
        out.set_at(p, (255, 255, 255, 0))
    # soften the one-pixel edge so the lettering doesn't get a harsh pale outline
    fringe = set()
    for x, y in cleared:
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= q[0] < w and 0 <= q[1] < h and q not in cleared:
                fringe.add(q)
    for p in fringe:
        c = out.get_at(p)
        out.set_at(p, (c.r, c.g, c.b, min(c.a, max(0, 255 - min(c.r, c.g, c.b)))))
    return out


def load_title(filename, box, text, font):
    """Return (bright, dim) versions of a title image scaled to fit box."""
    path = os.path.join(HERE, filename)
    try:
        img = pygame.image.load(path).convert_alpha()
        print(f"[title] loaded {filename} ({img.get_width()}x{img.get_height()})")
    except (pygame.error, OSError):
        print(f"[title] couldn't load {path}, showing text instead")
        img = font.render(text, True, FG)
    iw, ih = img.get_size()
    k = min(box[0] / iw, box[1] / ih)
    img = pygame.transform.smoothscale(img, (max(1, int(iw * k)), max(1, int(ih * k))))
    if TITLE_REMOVE_WHITE:
        img = remove_white_box(img)
    dim = img.copy()
    dim.set_alpha(110)
    return img, dim


# | generic list menu (used by screen 1 and screen 3) |
def menu_rects(n, top, row_h=52, gap=12, width=560):
    x = (W - width) // 2
    return [pygame.Rect(x, top + i * (row_h + gap), width, row_h) for i in range(n)]


def draw_menu(scr, fonts, rects, options, idx, main_col, acc_col):
    f_card, f_small = fonts
    for i, (r, (label, desc)) in enumerate(zip(rects, options)):
        sel = i == idx
        pygame.draw.rect(scr, mix(CELL_BG, main_col, 0.20) if sel else CELL_BG, r, border_radius=12)
        pygame.draw.rect(scr, main_col if sel else LINE, r, 2 if sel else 1, border_radius=12)
        # letter badge
        badge = pygame.Rect(r.x + 10, r.y + 9, r.h - 18, r.h - 18)
        pygame.draw.rect(scr, acc_col if sel else LINE, badge, border_radius=8)
        letter = f_card.render(chr(ord("A") + i), True, (10, 10, 16) if sel else MUTED)
        scr.blit(letter, letter.get_rect(center=badge.center))
        # text
        name = f_card.render(label, True, FG if sel else MUTED)
        scr.blit(name, (badge.right + 16, r.y + 6))
        d = f_small.render(desc, True, MUTED)
        scr.blit(d, (badge.right + 16, r.bottom - d.get_height() - 6))


def draw_heading(scr, font, small, heading, sub, y=40):
    h = font.render(heading, True, FG)
    scr.blit(h, h.get_rect(center=(W // 2, y + 20)))
    s = small.render(sub, True, MUTED)
    scr.blit(s, s.get_rect(center=(W // 2, y + 62)))


def menu_event(e, idx, rects, n):
    """Returns (new_idx, chosen_or_None) for a list menu."""
    if e.type == pygame.KEYDOWN:
        if e.key in (pygame.K_UP, pygame.K_w):
            return (idx - 1) % n, None
        if e.key in (pygame.K_DOWN, pygame.K_s):
            return (idx + 1) % n, None
        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            return idx, idx
        if e.key in LETTER_KEYS[:n]:
            i = LETTER_KEYS.index(e.key)
            return i, i
    elif e.type == pygame.MOUSEMOTION:
        for i, r in enumerate(rects):
            if r.collidepoint(e.pos):
                return i, None
    elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        for i, r in enumerate(rects):
            if r.collidepoint(e.pos):
                return i, i
    return idx, None


# ---------------------------------------------------------------------------
# PRACTICE SCREENS
# ---------------------------------------------------------------------------
DIR_VEC = {1: (-1, 1), 2: (0, 1), 3: (1, 1), 4: (-1, 0), 6: (1, 0), 7: (-1, -1), 8: (0, -1), 9: (1, -1)}


def draw_arrow(scr, center, size, d, color):
    """Arrow for a numpad direction (1-9, not 5), drawn with polygons so no font is needed."""
    dx, dy = DIR_VEC[d]
    a = math.atan2(dy, dx)
    ca, sa = math.cos(a), math.sin(a)
    shape = [(-.5, -.14), (.1, -.14), (.1, -.34), (.5, 0), (.1, .34), (.1, .14), (-.5, .14)]
    pts = [(center[0] + (x * ca - y * sa) * size, center[1] + (x * sa + y * ca) * size) for x, y in shape]
    pygame.draw.polygon(scr, color, pts)


def draw_button(scr, font, center, r, label, slot):
    pygame.draw.circle(scr, BTN_COLORS[slot], center, r)
    pygame.draw.circle(scr, (10, 10, 16), center, r, 2)
    t = font.render(label, True, (10, 10, 16))
    scr.blit(t, t.get_rect(center=center))


def draw_stat(scr, small, card, x, y, label, value, col=FG):
    scr.blit(small.render(label, True, MUTED), (x, y))
    scr.blit(card.render(str(value), True, col), (x, y + 20))


class Pad:
    """The ONE place the practice screens get input from (keyboard version).

    Anything that replaces this (e.g. teammate's motion control) just needs:
      .dir       numpad direction, 5 = neutral (you face right: 4 = back)
      .btns      list of bools, held state per button slot (same slots as BTN_KEYS)
      .pressed   button slots that went down since the last update()
      update()   call once per frame; returns True if .dir changed
      handle_event(e)   optional, gets every pygame event
      neutral()  True when nothing is held
    """

    def __init__(self):
        self.dir = 5
        self.btns = [False] * len(BTN_KEYS)
        self.pressed = []
        self._queue = []

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key in BTN_KEYS:
            self._queue.append(BTN_KEYS.index(e.key))

    def update(self):
        self.pressed, self._queue = self._queue, []
        k = pygame.key.get_pressed()
        dx = int(bool(k[pygame.K_RIGHT] or k[pygame.K_d])) - int(bool(k[pygame.K_LEFT] or k[pygame.K_a]))
        dy = int(bool(k[pygame.K_UP] or k[pygame.K_w])) - int(bool(k[pygame.K_DOWN] or k[pygame.K_s]))
        old = self.dir
        self.dir = 5 + dx + 3 * dy
        self.btns = [bool(k[b]) for b in BTN_KEYS]
        return self.dir != old          # True when the direction changed this frame

    def neutral(self):
        return self.dir == 5 and not any(self.btns)


class AttackGame:
    """Guitar Hero style: notes fall to the line, perform the motion + button as they arrive."""
    LANE = pygame.Rect(W // 2 - 190, 120, 380, 360)
    HIT_Y = 430

    def __init__(self, fonts):
        self.fonts = fonts            # (card, small, big)

    def start(self, game, diff):
        self.game, self.diff = game, diff
        self.cfg = ATTACK_LEVELS[diff]
        self.speed = (self.HIT_Y - (self.LANE.top - 40)) / self.cfg["travel"]
        self.buttons = GAME_BUTTONS[game]
        self.labels = {slot: label for label, slot in self.buttons}
        self.pool = [n for n in ATTACK_POOLS[game] if n[3] <= self.cfg["tier"]]
        self.time = 0.0
        self.next_spawn = 0.5
        self.notes = []
        self.score = self.combo = self.best = self.hits = self.total = 0
        self.flash = ("", FG, 0.0)

    # ----- notes -----
    def spawn(self):
        steps, needs_btn, name, _ = random.choice(self.pool)
        btn = random.choice(self.buttons)[1] if needs_btn else None
        self.notes.append({"steps": steps, "btn": btn, "name": name,
                           "hit": self.time + self.cfg["travel"], "p": 0})

    def active(self):
        """The note you're currently allowed to play (always the oldest one)."""
        if self.notes and self.time >= self.notes[0]["hit"] - self.cfg["approach"]:
            return self.notes[0]
        return None

    def miss(self, text):
        self.notes.pop(0)
        self.total += 1
        self.combo = 0
        self.flash = (text, BAD_COL, 0.7)

    def finish(self, note, err):
        """err = seconds after the line (negative = early)."""
        if err < -self.cfg["good"]:
            self.miss("EARLY")
            return
        text, base = ("PERFECT", 100) if abs(err) <= self.cfg["perfect"] else ("GOOD", 50)
        self.notes.pop(0)
        self.combo += 1
        self.best = max(self.best, self.combo)
        self.score += base * (1 + min(self.combo, 40) // 10)
        self.hits += 1
        self.total += 1
        self.flash = (text, GOOD_COL if text == "PERFECT" else (150, 200, 255), 0.6)

    # ----- input -----
    def on_dir(self, d):
        n = self.active()
        if not n or not n["steps"]:
            return
        s, p = n["steps"], n["p"]
        if p < len(s):
            if d == s[p]:
                p += 1
            #elif d != 5:                       # wrong direction: restart (maybe it's the first step)
            #    p = 1 if d == s[0] else 0
            n["p"] = p
            if p == len(s) and n["btn"] is None:
                self.finish(n, self.time - n["hit"])

    def on_button(self, slot, d):
        n = self.active()
        if not n or n["btn"] is None:
            return
        if n["p"] < len(n["steps"]):
            return                              # motion not finished yet, ignore
        if n["steps"] and d != n["steps"][-1]:
            return                              # must still be holding the last direction
        if slot != n["btn"]:
            self.miss("WRONG BUTTON")
            return
        self.finish(n, self.time - n["hit"])

    def update(self, dt):
        self.time += dt
        if self.time >= self.next_spawn:
            self.spawn()
            self.next_spawn = self.time + random.uniform(*self.cfg["gap"])
        if self.notes and self.time > self.notes[0]["hit"] + self.cfg["good"]:
            self.miss("MISS")
        text, col, left = self.flash
        self.flash = (text, col, max(0.0, left - dt))

    # ----- drawing -----
    def draw_note(self, scr, n, y, main, acc):
        f_card, f_small, _ = self.fonts
        ICON, GAP, PAD = 44, 10, 14
        icons = len(n["steps"]) + (n["btn"] is not None)
        w = icons * ICON + (icons - 1) * GAP + 2 * PAD
        box = pygame.Rect(0, 0, w, 60)
        box.center = (W // 2, int(y))
        is_t = n is self.notes[0]
        pygame.draw.rect(scr, (26, 30, 48), box, border_radius=12)
        pygame.draw.rect(scr, acc if is_t else LINE, box, 2, border_radius=12)
        x = box.x + PAD + ICON // 2
        for i, d in enumerate(n["steps"]):
            col = acc if (is_t and i < n["p"]) else FG       # steps you've already done light up
            draw_arrow(scr, (x, box.centery), 40, d, col)
            x += ICON + GAP
        if n["btn"] is not None:
            draw_button(scr, f_small, (x, box.centery), ICON // 2 - 2, self.labels[n["btn"]], n["btn"])
        if n["name"]:
            scr.blit(f_small.render(n["name"], True, MUTED), (box.right + 10, box.centery - 9))

    def draw(self, scr, main, acc, inp):
        f_card, f_small, f_big = self.fonts
        draw_heading(scr, f_big, f_small, "Attack Practice", f"{self.game}  |  {inp}  |  {self.diff}", y=20)
        L = self.LANE
        pygame.draw.rect(scr, CELL_BG, L, border_radius=14)
        pygame.draw.rect(scr, LINE, L, 1, border_radius=14)
        zone = pygame.Rect(L.x + 8, self.HIT_Y - 38, L.w - 16, 76)
        pygame.draw.rect(scr, mix(CELL_BG, main, 0.18), zone, border_radius=12)
        pygame.draw.rect(scr, main, zone, 2, border_radius=12)

        scr.set_clip(L.inflate(-4, -4))
        for n in reversed(self.notes):
            y = self.HIT_Y - (n["hit"] - self.time) * self.speed
            self.draw_note(scr, n, y, main, acc)
        scr.set_clip(None)

        text, col, left = self.flash
        if left > 0:
            t = f_card.render(text, True, col)
            t.set_alpha(min(255, int(left * 600)))
            scr.blit(t, t.get_rect(center=(W // 2, L.bottom + 28)))

        # left: score panel
        acc_pct = f"{round(100 * self.hits / self.total)}%" if self.total else "--"
        draw_stat(scr, f_small, f_card, 50, 140, "SCORE", self.score)
        draw_stat(scr, f_small, f_card, 50, 215, "COMBO", self.combo, acc if self.combo else FG)
        draw_stat(scr, f_small, f_card, 50, 290, "BEST COMBO", self.best)
        draw_stat(scr, f_small, f_card, 50, 365, "ACCURACY", acc_pct)
        draw_stat(scr, f_small, f_card, 50, 440, "HITS", f"{self.hits} / {self.total}")

        # right: which key is which button
        scr.blit(f_small.render("BUTTONS", True, MUTED), (670, 140))
        for i, (label, slot) in enumerate(self.buttons):
            cy = 185 + i * 36
            draw_button(scr, f_small, (688, cy), 15, label, slot)
            scr.blit(f_small.render(f"press {BTN_KEY_NAMES[slot]}", True, FG), (715, cy - 9))
        scr.blit(f_small.render("MOVE", True, MUTED), (670, 185 + len(self.buttons) * 36 + 12))
        scr.blit(f_small.render("arrows or WASD", True, FG), (670, 185 + len(self.buttons) * 36 + 34))
        scr.blit(f_small.render("(left = back)", True, MUTED), (670, 185 + len(self.buttons) * 36 + 56))

        hint = f_small.render("Do the motion, then press the button as the note hits the box     Esc: back", True, MUTED)
        scr.blit(hint, hint.get_rect(center=(W // 2, H - 20)))


class DefenseGame:
    """A color flashes; hold the direction (or push block) it stands for."""

    def __init__(self, fonts):
        self.fonts = fonts            # (card, small, big)

    def build_cues(self, game, allow_push):
        labels = {slot: label for label, slot in GAME_BUTTONS[game]}
        cues = [
            {"name": "BACK", "color": COLOR_BACK, "dir": 4, "hint": "stand block: hold LEFT"},
            {"name": "DOWN-BACK", "color": COLOR_DOWNBACK, "dir": 1, "hint": "low block: DOWN+LEFT"},
        ]
        pb = PUSH_BLOCK.get(game) if allow_push else None
        if pb:
            a, b = pb
            cues.append({"name": "PUSH BLOCK", "color": COLOR_PUSH, "btns": pb,
                         "hint": f"{labels[a]}+{labels[b]}  ({BTN_KEY_NAMES[a]}+{BTN_KEY_NAMES[b]})"})
        return cues

    def start(self, game, diff):
        self.game, self.diff = game, diff
        self.cfg = DEFENSE_LEVELS[diff]
        self.cues = self.build_cues(game, self.cfg["push"])
        self.state = "wait"
        self.timer = random.uniform(*self.cfg["wait"])
        self.cue = None
        self.t = 0.0
        self.react = None
        self.neutral = True
        self.msg = ("", FG)
        self.last_ok = True
        self.passed = self.total = self.streak = self.best = 0
        self.times = []
        self.show_legend = self.cfg["legend"]

    def holding(self, pad):
        c = self.cue
        if "dir" in c:
            return pad.dir == c["dir"]
        return all(pad.btns[s] for s in c["btns"])

    def finish(self, ok, text, col):
        self.total += 1
        self.last_ok = ok
        if ok:
            self.passed += 1
            self.streak += 1
            self.best = max(self.best, self.streak)
            self.times.append(self.react)
        else:
            self.streak = 0
        self.msg = (text, col)
        self.state = "result"
        self.timer = RESULT_TIME if ok else RESULT_TIME + 0.6

    def update(self, dt, pad):
        self.neutral = pad.neutral()
        if self.state == "wait":
            if self.neutral:                    # the wait only counts down while you're not holding anything
                self.timer -= dt
            if self.timer <= 0:
                self.cue = random.choice(self.cues)
                self.t, self.react, self.state = 0.0, None, "cue"
        elif self.state == "cue":
            self.t += dt
            ok = self.holding(pad)
            if self.react is None:
                if ok:
                    self.react = self.t
                elif self.t > self.cfg["react"]:
                    self.finish(False, "TOO SLOW / WRONG", BAD_COL)
            elif not ok:
                self.finish(False, "LET GO TOO EARLY", BAD_COL)
            elif self.t >= self.cfg["hold"]:
                self.finish(True, f"{int(self.react * 1000)} ms, {int(self.react *1000 // 16.66666 + 1)} frames", GOOD_COL)
        else:
            self.timer -= dt
            if self.timer <= 0:
                self.state = "wait"
                self.timer = random.uniform(*self.cfg["wait"])

    def draw(self, scr, main, acc, inp):
        f_card, f_small, f_big = self.fonts
        draw_heading(scr, f_big, f_small, "Defense Practice", f"{self.game}  |  {inp}  |  {self.diff}", y=20)

        panel = pygame.Rect(W // 2 - 190, 120, 380, 220)
        if self.state == "cue":
            pygame.draw.rect(scr, self.cue["color"], panel, border_radius=18)
        else:
            pygame.draw.rect(scr, CELL_BG, panel, border_radius=18)
            pygame.draw.rect(scr, LINE, panel, 2, border_radius=18)
            if self.state == "wait":
                text, col = ("Get ready...", MUTED) if self.neutral else ("Let go of everything", (255, 200, 90))
                t = f_card.render(text, True, col)
                scr.blit(t, t.get_rect(center=panel.center))
            else:
                t = f_big.render(self.msg[0], True, self.msg[1])
                scr.blit(t, t.get_rect(center=(panel.centerx, panel.centery - (0 if self.last_ok else 16))))
                if not self.last_ok:
                    a = f_card.render(f"It was: {self.cue['name']}", True, self.cue["color"])
                    scr.blit(a, a.get_rect(center=(panel.centerx, panel.centery + 34)))

        # legend (press H to hide it once you know the colors)
        if self.show_legend:
            n = len(self.cues)
            lw, lg = 280, 12
            x0 = (W - (n * lw + (n - 1) * lg)) // 2
            for i, c in enumerate(self.cues):
                r = pygame.Rect(x0 + i * (lw + lg), 365, lw, 76)
                pygame.draw.rect(scr, CELL_BG, r, border_radius=12)
                pygame.draw.rect(scr, LINE, r, 1, border_radius=12)
                sw = pygame.Rect(r.x + 12, r.y + 12, 52, 52)
                pygame.draw.rect(scr, c["color"], sw, border_radius=10)
                if "dir" in c:
                    draw_arrow(scr, sw.center, 36, c["dir"], (10, 10, 16))
                else:
                    t = f_small.render("2x", True, (10, 10, 16))
                    scr.blit(t, t.get_rect(center=sw.center))
                scr.blit(f_card.render(c["name"], True, FG), (r.x + 74, r.y + 8))
                scr.blit(f_small.render(c["hint"], True, MUTED), (r.x + 74, r.y + 46))
        else:
            t = f_small.render("Colors hidden - press H to show them", True, MUTED)
            scr.blit(t, t.get_rect(center=(W // 2, 400)))

        avg = f"{int(1000 * sum(self.times) / len(self.times))} ms" if self.times else "--"
        fast = f"{int(1000 * min(self.times))} ms" if self.times else "--"
        stats = (f"Streak {self.streak}     Best streak {self.best}     Correct {self.passed}/{self.total}"
                 f"     Avg reaction {avg}     Fastest {fast}")
        s = f_small.render(stats, True, FG)
        scr.blit(s, s.get_rect(center=(W // 2, 485)))

        hint = f_small.render("Hold what the color means (left = back)     H: hide/show colors     Esc: back",
                              True, MUTED)
        scr.blit(hint, hint.get_rect(center=(W // 2, H - 20)))


def main():
    pygame.init()
    print("[files] looking in", HERE)
    print("[files] PNGs found there:", sorted(f for f in os.listdir(HERE) if f.lower().endswith(".png")))
    scr = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Fighting Game Trainer")
    clock = pygame.time.Clock()
    face = "segoeui,helveticaneue,dejavusans,arial"
    f_card, f_small = (pygame.font.SysFont(face, n, b) for n, b in ((26, True), (16, False)))
    f_big = pygame.font.SysFont(face, 40, True)
    bg = make_bg()
    frames = load_sprite_frames()

    x0 = (W - (3 * CELL_W + 2 * CELL_GAP)) // 2
    cells = [pygame.Rect(x0 + i * (CELL_W + CELL_GAP), CELL_Y, CELL_W, CELL_H) for i in range(3)]
    titles = [load_title(f, (CELL_W - 36, CELL_H - 36), name, f_card) for name, f, _, _ in GAMES]
    spots = [glow(420, main_col, 0.35, 2.0, 2) for _, _, main_col, _ in GAMES]

    input_rects = menu_rects(len(INPUTS), 170)
    practice_rects = menu_rects(len(PRACTICES), 150, row_h=68, gap=12)
    diff_rects = menu_rects(len(DIFFICULTIES), 150, row_h=68, gap=12)

    pad = Pad()
    attack = AttackGame((f_card, f_small, f_big))
    defense = DefenseGame((f_card, f_small, f_big))

    scene = "input"          # "input" -> "title" -> "practice" -> "difficulty" -> "attack" / "defense"
    ii = 0                   
    pi = 0                  
    di = 1                   # difficulty menu cursor (starts on Medium)
    chosen_practice = None
    chosen_input = None
    chosen_game = None
    gi, t = 0, 0.0
    running = True
    while running:
        dt = min(clock.tick(60) / 1000.0, 0.1)
        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            pad.handle_event(e)
            if e.type == pygame.QUIT:
                running = False
                continue

            # |screen 1: input|
            if scene == "input":
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                    continue
                ii, chosen = menu_event(e, ii, input_rects, len(INPUTS))
                if chosen is not None:
                    chosen_input = INPUTS[chosen][0]
                    print("Input:", chosen_input)
                    scene = "title"

            # | screen 2: title / game picker|
            elif scene == "title":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        scene = "input"
                    elif e.key in (pygame.K_LEFT, pygame.K_a):
                        gi = (gi - 1) % len(GAMES)
                    elif e.key in (pygame.K_RIGHT, pygame.K_d):
                        gi = (gi + 1) % len(GAMES)
                    elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        chosen_game = GAMES[gi][0]
                        print("Game:", chosen_game)
                        pi = 0
                        scene = "practice"
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    for i, r in enumerate(cells):
                        if r.collidepoint(e.pos):
                            gi = i
                            chosen_game = GAMES[gi][0]
                            print("Game:", chosen_game)
                            pi = 0
                            scene = "practice"

            # | screen 3: what to practice |
            elif scene == "practice":
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    scene = "title"
                    continue
                pi, chosen = menu_event(e, pi, practice_rects, len(PRACTICES))
                if chosen is not None:
                    label = PRACTICES[chosen][0]
                    if label == "Back":
                        scene = "title"
                    else:
                        print("Practice:", label, "|", chosen_game, "|", chosen_input)
                        chosen_practice = label
                        scene = "difficulty"

            # | screen 3b: difficulty |
            elif scene == "difficulty":
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    scene = "practice"
                    continue
                di, chosen = menu_event(e, di, diff_rects, len(DIFFICULTIES))
                if chosen is not None:
                    diff = DIFFICULTIES[chosen][0]
                    if diff == "Back":
                        scene = "practice"
                    else:
                        print("Difficulty:", diff)
                        if chosen_practice == "Attack Practice":
                            attack.start(chosen_game, diff)
                            scene = "attack"
                        else:
                            defense.start(chosen_game, diff)
                            scene = "defense"

            # | screens 4/5: attack + defense practice |
            elif scene in ("attack", "defense"):
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        scene = "practice"
                    elif scene == "defense" and e.key == pygame.K_h:
                        defense.show_legend = not defense.show_legend

        # read the keyboard once per frame, then feed the active practice screen
        changed = pad.update()
        if scene == "attack":
            if changed:
                attack.on_dir(pad.dir)
            for slot in pad.pressed:
                attack.on_button(slot, pad.dir)
            attack.update(dt)
        elif scene == "defense":
            defense.update(dt, pad)

        t += dt
        scr.blit(bg, (0, 0))

        if scene == "input":
            draw_heading(scr, f_big, f_small, "Choose your input",
                         "Up / Down + Enter, click, or press the letter")
            draw_menu(scr, (f_card, f_small), input_rects, INPUTS, ii, DEFAULT_MAIN, DEFAULT_ACC)
            hint = f_small.render("Esc: quit", True, MUTED)
            scr.blit(hint, hint.get_rect(center=(W // 2, H - 20)))

        elif scene == "title":
            for i, r in enumerate(cells):
                if r.collidepoint(mouse):
                    gi = i
            _, _, main_col, acc_col = GAMES[gi]

            # sprite spotlight, tinted to the highlighted game, then the sprite
            spot = spots[gi]
            scr.blit(spot, spot.get_rect(center=SPRITE_AREA.center), special_flags=pygame.BLEND_RGB_ADD)
            frame = frames[int(t * SPRITE_FPS) % len(frames)]
            scr.set_clip(SPRITE_AREA)
            scr.blit(frame, frame.get_rect(midbottom=SPRITE_AREA.midbottom))
            scr.set_clip(None)

            # game titles across the top
            for i, (r, (_, _, gm, ga)) in enumerate(zip(cells, GAMES)):
                sel = i == gi
                pygame.draw.rect(scr, mix(CELL_BG, gm, 0.20) if sel else CELL_BG, r, border_radius=12)
                pygame.draw.rect(scr, gm if sel else LINE, r, 2 if sel else 1, border_radius=12)
                img = titles[i][0 if sel else 1]
                scr.blit(img, img.get_rect(center=r.center))
                if sel:
                    pygame.draw.line(scr, ga, (r.x + 24, r.bottom - 10), (r.right - 24, r.bottom - 10), 3)

            hint = f_small.render("< > or A / D: highlight     Enter or click: select     Esc: back", True, MUTED)
            scr.blit(hint, hint.get_rect(center=(W // 2, H - 20)))

        elif scene == "practice":
            gm = next(g for g in GAMES if g[0] == chosen_game)
            draw_heading(scr, f_big, f_small, "What do you want to practice?",
                         f"{chosen_game}  |  {chosen_input}", y=20)
            draw_menu(scr, (f_card, f_small), practice_rects, PRACTICES, pi, gm[2], gm[3])
            hint = f_small.render("Up / Down + Enter, click, or press the letter     Esc: back", True, MUTED)
            scr.blit(hint, hint.get_rect(center=(W // 2, H - 20)))

        elif scene == "difficulty":
            gm = next(g for g in GAMES if g[0] == chosen_game)
            draw_heading(scr, f_big, f_small, "Choose a difficulty",
                         f"{chosen_practice}  |  {chosen_game}", y=20)
            draw_menu(scr, (f_card, f_small), diff_rects, DIFFICULTIES, di, gm[2], gm[3])
            hint = f_small.render("Up / Down + Enter, click, or press the letter     Esc: back", True, MUTED)
            scr.blit(hint, hint.get_rect(center=(W // 2, H - 20)))

        else:  # attack / defense practice
            gm = next(g for g in GAMES if g[0] == chosen_game)
            (attack if scene == "attack" else defense).draw(scr, gm[2], gm[3], chosen_input)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
