# ending.py
import pygame
import setup as st

class EndingSequence:
    def __init__(self, outcome):
        """outcome: 'victory' or 'defeat'"""
        self.outcome = outcome
        self.phase = "fade_out"
        self.timer = 0
        self.fade_alpha = 0

        self.fade_surface = pygame.Surface((st.screen_width, st.screen_height))
        self.fade_surface.fill((0, 0, 0))

        self.dialogue_lines = [
            "Take heed, Struggler.",
            "Struggle, contend, writhe...",
            "that is the only sword",
            "of those who resort",
            "to the non-believer...",
            "It is a path you carve",
            "with your own two hands!..."
        ]
        self.dialogue_line_index = 0
        self.dialogue_char_index = 0
        self.dialogue_char_timer = 0
        self.line_hold_timer = 0

        self.credits_lines = [
            "BLEACH: Final Substitute Soul Reaper",
            "",
            "Created by Kritartha",
        ]
        self.credits_y = st.screen_height + 40
        self.credits_font = pygame.font.SysFont("georgia", 36)
        self.credits_font_small = pygame.font.SysFont("georgia", 22)
        self.dialogue_font = pygame.font.SysFont("georgia", 30)

    def update(self, ichigo):
        self.timer += 1

        if self.outcome == "victory":
            self._update_victory(ichigo)
        else:
            self._update_defeat()

    def _update_victory(self, ichigo):
        if self.phase == "fade_out":
            self.fade_alpha = min(255, self.fade_alpha + 7)
            if self.fade_alpha >= 255:
                self.phase = "revert"
                self.timer = 0
                if ichigo.mode == "bankai":
                    ichigo.activateDeactivateBankai()
                ichigo.transform_state = "inactive"
                ichigo.action = "idle"
                ichigo.movement_state = "idle"
                self.fade_alpha = 255

        elif self.phase == "revert":
            self.ichigo = ichigo
            self.fade_alpha = max(0, self.fade_alpha - 7)
            if self.fade_alpha <= 0 and self.timer > 60:
                self.phase = "dialogue"
                self.timer = 0
                self.fade_alpha = 255

        elif self.phase == "dialogue":
            current_line = self.dialogue_lines[self.dialogue_line_index]

            if self.dialogue_char_index < len(current_line):
                self.dialogue_char_timer += 1
                if self.dialogue_char_timer >= 2:
                    self.dialogue_char_index += 1
                    self.dialogue_char_timer = 0
            else:
                # line fully revealed — hold briefly then advance
                self.line_hold_timer += 1
                if self.line_hold_timer >= 60:
                    self.line_hold_timer = 0
                    self.dialogue_line_index += 1
                    self.dialogue_char_index = 0
                    if self.dialogue_line_index >= len(self.dialogue_lines):
                        self.phase = "credits"
                        self.timer = 0

        elif self.phase == "credits":
            self.credits_y -= 1.6
            total_height = len(self.credits_lines) * 50
            if self.credits_y < -total_height - 100:
                self.phase = "done"

    def _update_defeat(self):
        if self.phase == "fade_out":
            self.fade_alpha = min(255, self.fade_alpha + 7)
            if self.fade_alpha >= 255:
                self.phase = "message"
                self.timer = 0

        elif self.phase == "message":
            if self.timer > 120:
                self.phase = "done"

    def draw(self, win):
        if self.outcome == "victory":
            self._draw_victory(win)
        else:
            self._draw_defeat(win)

    def _draw_victory(self, win):
        if self.phase == "fade_out":
            self.fade_surface.set_alpha(self.fade_alpha)
            win.blit(self.fade_surface, (0, 0))

        elif self.phase == "revert":
            win.blit(st.bg, (0, 0))
            win.blit(st.ground, (0, st.feet_y_initial))
            if hasattr(self, "ichigo"):
                self.ichigo.draw(win)
            self.fade_surface.set_alpha(self.fade_alpha)
            win.blit(self.fade_surface, (0, 0))

        elif self.phase == "dialogue":
            win.fill((0, 0, 0))
            if self.dialogue_line_index < len(self.dialogue_lines):
                current_line = self.dialogue_lines[self.dialogue_line_index]
                shown = current_line[:self.dialogue_char_index]
                text_surf = self.dialogue_font.render(shown, True, (230, 230, 230))
                rect = text_surf.get_rect(center=(st.screen_width // 2, st.screen_height // 2))
                win.blit(text_surf, rect)

        elif self.phase == "credits":
            win.fill((0, 0, 0))
            y = self.credits_y
            for i, line in enumerate(self.credits_lines):
                font = self.credits_font if i == 0 else self.credits_font_small
                color = (255, 215, 130) if i == 0 else (200, 200, 200)
                if line.strip() != "":
                    surf = font.render(line, True, color)
                    rect = surf.get_rect(center=(st.screen_width // 2, y + i * 50))
                    win.blit(surf, rect)

    def _draw_defeat(self, win):
        if self.phase == "fade_out":
            self.fade_surface.set_alpha(self.fade_alpha)
            win.blit(self.fade_surface, (0, 0))

        elif self.phase == "message":
            win.fill((0, 0, 0))
            font = pygame.font.SysFont("georgia", 44)
            surf = font.render("DEFEATED", True, (180, 30, 30))
            rect = surf.get_rect(center=(st.screen_width // 2, st.screen_height // 2))
            win.blit(surf, rect)

    def is_done(self):
        return self.phase == "done"