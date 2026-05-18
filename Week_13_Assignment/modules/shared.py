import pygame
import sys
import unittest
import io
import time
import math

WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()
BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20

def check_events(on_keydown=None):
    """
    Pump the pygame event queue.
    Calls on_keydown(event) for any KEYDOWN event if provided.
    Returns False if the user quits or presses ESC, True otherwise.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if on_keydown:
                on_keydown(event)
    return True

def run_tests(test_class):
    """
    Run a unittest.TestCase class and return (results, elapsed_seconds).
    Captures all output so nothing bleeds into the terminal unexpectedly.
    """
    stream  = io.StringIO()
    runner  = unittest.TextTestRunner(stream=stream, verbosity=2)
    suite   = unittest.TestLoader().loadTestsFromTestCase(test_class)
    start   = time.time()
    results = runner.run(suite)
    elapsed = time.time() - start
    return results, elapsed

def draw_test_overlay(screen, font, test_class, label):
    """
    Blocking overlay that runs *test_class* and renders a pass/fail summary.
    Returns when the user presses any key or ESC.

    Parameters
    ----------
    screen     : pygame.Surface
    font       : pygame.font.Font
    test_class : unittest.TestCase subclass
    label      : str   human-readable name shown in the header
    """
    WIDTH, HEIGHT = screen.get_size()

    # --- spinner while tests run ---
    spinner_done  = False
    spinner_angle = 0.0

    def draw_spinner(angle):
        screen.fill((20, 22, 30))
        cx, cy, r = WIDTH // 2, HEIGHT // 2, 28
        msg = font.render(f"Running {label} tests…", True, (180, 180, 210))
        screen.blit(msg, msg.get_rect(center=(cx, cy - 60)))
        for i in range(8):
            a    = math.radians(angle + i * 45)
            alpha = int(255 * (i + 1) / 8)
            ex   = int(cx + r * math.cos(a))
            ey   = int(cy + r * math.sin(a))
            dot_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(dot_surf, (100, 180, 255, alpha), (5, 5), 5)
            screen.blit(dot_surf, (ex - 5, ey - 5))
        pygame.display.flip()

    # Run tests on a background thread so the spinner can animate
    import threading
    results_container = [None]
    elapsed_container = [0.0]

    def _run():
        results_container[0], elapsed_container[0] = run_tests(test_class)

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    clock = pygame.time.Clock()
    while thread.is_alive():
        dt = clock.tick(60) / 1000.0
        spinner_angle = (spinner_angle + 180 * dt) % 360
        draw_spinner(spinner_angle)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

    results = results_container[0]
    elapsed = elapsed_container[0]

    # --- build result lines ---
    total   = results.testsRun
    failed  = len(results.failures) + len(results.errors)
    passed  = total - failed

    lines = [
        (f"{label} — Test Results", (200, 210, 255)),
        ("", None),
        (f"  Ran {total} test{'s' if total != 1 else ''} in {elapsed:.3f}s", (160, 160, 190)),
        (f"  Passed : {passed}", (100, 230, 130) if passed == total else (200, 200, 100)),
        (f"  Failed : {failed}", (230, 100, 100) if failed else (100, 180, 120)),
    ]

    for title, tb in results.failures + results.errors:
        lines.append(("", None))
        lines.append((f"  FAIL: {title}", (255, 140, 80)))
        for raw_line in tb.splitlines()[-4:]:          # last 4 lines of traceback
            lines.append((f"    {raw_line}", (210, 150, 120)))

    lines += [
        ("", None),
        ("Press any key to return…", (120, 120, 150)),
    ]

    # --- render overlay ---
    PAD        = 24
    LINE_H     = font.get_linesize() + 4
    box_h      = PAD * 2 + len(lines) * LINE_H
    box_w      = min(WIDTH - 80, 720)
    box_x      = (WIDTH  - box_w) // 2
    box_y      = (HEIGHT - box_h) // 2

    def draw_overlay():
        screen.fill((20, 22, 30))
        pygame.draw.rect(screen, (40, 44, 58),  (box_x, box_y, box_w, box_h), border_radius=10)
        pygame.draw.rect(screen, (80, 90, 140), (box_x, box_y, box_w, box_h), 2, border_radius=10)
        for i, (text, color) in enumerate(lines):
            if not text or color is None:
                continue
            surf = font.render(text, True, color)
            screen.blit(surf, (box_x + PAD, box_y + PAD + i * LINE_H))
        pygame.display.flip()

    draw_overlay()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def draw_loading_spinner(screen, font, message="Loading…"):
    """
    Draw a single spinner frame. Call repeatedly in a loop with an
    incrementing angle.  Returns the surface so callers can blit it
    themselves if needed, but also blits directly to *screen*.

    Typical usage
    -------------
    angle = 0.0
    while loading:
        dt = clock.tick(60) / 1000.0
        angle = draw_loading_spinner(screen, font, "Loading…", angle, dt)
    """
    WIDTH, HEIGHT = screen.get_size()
    screen.fill((20, 22, 30))
    cx, cy, r = WIDTH // 2, HEIGHT // 2, 28
    msg = font.render(message, True, (180, 180, 210))
    screen.blit(msg, msg.get_rect(center=(cx, cy - 60)))
    pygame.display.flip()

def make_font(size=20, bold=False):
    """Return a pygame SysFont using a sensible monospace fallback chain."""
    for name in ("consolas", "jetbrainsmono", "couriernew", "monospace"):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)

def clamp(value, lo, hi):
    """Clamp *value* to [lo, hi]."""
    return max(lo, min(hi, value))

def lerp(a, b, t):
    """Linear interpolation between *a* and *b* by factor *t* ∈ [0, 1]."""
    return a + (b - a) * t

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_out_back(t, s=1.70158):
    t -= 1
    return t * t * ((s + 1) * t + s) + 1

def ease_out_bounce(t):
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375

def ease_in_cubic(t):
    return t * t * t

class Anim:
    def __init__(self, target_dict, key, start, end, duration, ease=None,
                 on_done=None, delay=0.0):
        self.target_dict = target_dict
        self.key         = key
        self.start       = start
        self.end         = end
        self.duration    = duration
        self.ease        = ease or ease_out_cubic
        self.on_done     = on_done
        self.elapsed     = -delay
        self.done        = False

    def update(self, dt):
        if self.done:
            return
        self.elapsed += dt
        if self.elapsed < 0:
            self.target_dict[self.key] = self.start
            return
        t = min(self.elapsed / self.duration, 1.0)
        self.target_dict[self.key] = self.start + (self.end - self.start) * self.ease(t)
        if t >= 1.0:
            self.done = True
            if self.on_done:
                self.on_done()


class AnimManager:
    def __init__(self):
        self._anims = []

    def add(self, anim):
        self._anims.append(anim)

    def tween(self, target_dict, key, start, end, duration,
              ease=None, on_done=None, delay=0.0):
        self.add(Anim(target_dict, key, start, end, duration,
                      ease=ease or ease_out_cubic, on_done=on_done, delay=delay))

    def update(self, dt):
        self._anims = [a for a in self._anims if not a.done]
        for a in self._anims:
            a.update(dt)

    def busy(self):
        return bool(self._anims)

    def clear(self):
        self._anims.clear()

def make_block(value, x, y, alpha=255, scale=1.0):
    return {
        "value": value,
        "x":     float(x),
        "y":     float(y),
        "alpha": float(alpha),
        "scale": float(scale),
    }

def draw_block(screen, font, block, color=(100, 150, 250)):
    alpha = max(0, min(255, int(block["alpha"])))
    scale = max(0.0, block["scale"])
    w     = int(BLOCK_WIDTH  * scale)
    h     = int(BLOCK_HEIGHT * scale)
    if w < 1 or h < 1 or alpha == 0:
        return
    cx = int(block["x"]) + BLOCK_WIDTH  // 2
    cy = int(block["y"]) + BLOCK_HEIGHT // 2
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    r, g, b = color
    pygame.draw.rect(surf, (r, g, b, alpha),       (0, 0, w, h), border_radius=6)
    pygame.draw.rect(surf, (255, 255, 255, alpha // 4), (0, 0, w, h), 2, border_radius=6)
    screen.blit(surf, (cx - w // 2, cy - h // 2))
    txt = font.render(str(block["value"]), True, (230, 230, 230))
    txt.set_alpha(alpha)
    screen.blit(txt, txt.get_rect(center=(cx, cy)))