"""Life of a Footballer - a self-contained Pygame career football game.

Run with: pip install pygame
          python life_of_a_footballer.py
"""

import json
import math
import os
import random
import sys

import pygame


LOGICAL_SIZE = (1280, 720)
SAVE_NAME = "life_of_footballer_save.json"
PITCH = pygame.Rect(126, 116, 1028, 510)
GOAL_H = 128
FPS = 60
WHITE = (245, 247, 242)
INK = (15, 25, 35)
NAVY = (20, 37, 58)
PANEL = (28, 52, 75)
PANEL_2 = (39, 72, 99)
GOLD = (250, 202, 66)
SKIN = (240, 184, 132)
RED = (224, 81, 75)
BLUE = (71, 151, 238)
GREEN = (85, 195, 104)

PALETTE = [
    (61, 154, 232), (224, 76, 90), (246, 178, 55), (136, 94, 202),
    (46, 181, 125), (238, 110, 168), (70, 196, 202), (236, 236, 236),
]

DIFFICULTIES = {
    "Easy": {
        "description": "Second-division-quality opponent; slow bots and a weak goalkeeper.",
        "speed": 0.78, "keeper": 0.65, "shoot": 0.72, "press": 0.65,
        "star": False, "strength": 62,
    },
    "Medium": {
        "description": "Top-flight relegation-level opponent; balanced bots.",
        "speed": 0.94, "keeper": 0.92, "shoot": 0.91, "press": 0.93,
        "star": None, "strength": 70,
    },
    "Hard": {
        "description": "Top-four-quality opponent; fast pressing, accurate passing, strong goalkeeper.",
        "speed": 1.12, "keeper": 1.18, "shoot": 1.15, "press": 1.17,
        "star": True, "strength": 80,
    },
    "Extremely Hard": {
        "description": "Best team in the league; organised defending, quick counters, very strong goalkeeper.",
        "speed": 1.25, "keeper": 1.34, "shoot": 1.28, "press": 1.29,
        "star": True, "strength": 90,
    },
}

STYLE_NAMES = ["Attacking", "Defensive", "Possession", "Counterattack"]
OBJECTIVE_INFO = {
    "goal": ("Score a goal", 1),
    "assist": ("Get an assist", 1),
    "passes": ("Complete 10 accurate passes", 10),
    "win_two": ("Win by at least two goals", 2),
}


def clamp(value, low, high):
    return max(low, min(high, value))


def vec(x=0, y=0):
    return pygame.Vector2(x, y)


def safe_normal(v, fallback=(1, 0)):
    if v.length_squared() < 0.0001:
        return vec(*fallback)
    return v.normalize()


def lerp_color(a, b, amount):
    return tuple(int(a[i] + (b[i] - a[i]) * amount) for i in range(3))


def team_name(style, opponent=False):
    first = {
        "Attacking": ["Comets", "Rockets", "Blaze"],
        "Defensive": ["Guardians", "Stone", "Fortress"],
        "Possession": ["Rovers", "Circles", "Maestros"],
        "Counterattack": ["Falcons", "Storm", "Vipers"],
    }[style]
    tail = ["United", "City", "Athletic", "FC"]
    prefix = "North" if not opponent else "South"
    return prefix + " " + random.choice(first) + " " + random.choice(tail)


def default_save(position="Midfielder", colour=None):
    starts = {
        "Striker": {"pace": 62, "shooting": 70, "passing": 60, "dribbling": 63, "defending": 55, "stamina": 62},
        "Winger": {"pace": 70, "shooting": 62, "passing": 62, "dribbling": 68, "defending": 54, "stamina": 64},
        "Midfielder": {"pace": 63, "shooting": 62, "passing": 70, "dribbling": 65, "defending": 61, "stamina": 66},
        "Defender": {"pace": 62, "shooting": 56, "passing": 62, "dribbling": 58, "defending": 72, "stamina": 68},
    }
    return {
        "career": True,
        "position": position,
        "colour": list(colour or PALETTE[0]),
        "attributes": starts.get(position, starts["Midfielder"]).copy(),
        "upgrades": {"pace": 0, "shooting": 0, "dribbling": 0},
        "cosmetics": {"trail": False, "badge": False, "celebration": False, "azure_ball": False, "gold_ball": False},
        "credits": 0,
        "xp": 0,
        "level": 1,
        "trust": 50,
        "stats": {
            "matches": 0, "wins": 0, "draws": 0, "losses": 0, "goals": 0,
            "assists": 0, "passes": 0, "tackles": 0, "potm": 0, "highest_rating": 6.0,
        },
        "latest_result": "No matches played yet",
        "team_name": "North Rovers United",
    }


def repaired_save(raw):
    """Merge a potentially old or damaged save into a safe schema."""
    if not isinstance(raw, dict):
        safe = default_save()
        safe["career"] = False
        return safe
    pos = raw.get("position", "Midfielder")
    if pos not in ("Striker", "Winger", "Midfielder", "Defender"):
        pos = "Midfielder"
    base = default_save(pos, raw.get("colour", PALETTE[0]))
    for key in ("career", "position", "colour", "credits", "xp", "level", "trust", "latest_result", "team_name"):
        if key in raw:
            base[key] = raw[key]
    if not isinstance(base["colour"], list) or len(base["colour"]) != 3:
        base["colour"] = list(PALETTE[0])
    base["colour"] = [int(clamp(x if isinstance(x, (int, float)) else 0, 0, 255)) for x in base["colour"]]
    base["credits"] = max(0, int(base["credits"]) if isinstance(base["credits"], (int, float)) else 0)
    base["xp"] = max(0, int(base["xp"]) if isinstance(base["xp"], (int, float)) else 0)
    base["level"] = max(1, int(base["level"]) if isinstance(base["level"], (int, float)) else 1)
    base["trust"] = int(clamp(base["trust"] if isinstance(base["trust"], (int, float)) else 50, 0, 100))
    for group in ("attributes", "upgrades", "cosmetics", "stats"):
        if isinstance(raw.get(group), dict):
            for key in base[group]:
                if key in raw[group]:
                    base[group][key] = raw[group][key]
    for key in base["attributes"]:
        value = base["attributes"][key]
        base["attributes"][key] = int(clamp(value if isinstance(value, (int, float)) else 60, 40, 99))
    for key in base["upgrades"]:
        value = base["upgrades"][key]
        base["upgrades"][key] = int(clamp(value if isinstance(value, (int, float)) else 0, 0, 3))
    for key in base["cosmetics"]:
        base["cosmetics"][key] = bool(base["cosmetics"][key])
    for key in base["stats"]:
        value = base["stats"][key]
        if key == "highest_rating":
            base["stats"][key] = round(float(clamp(value if isinstance(value, (int, float)) else 6, 1, 10)), 1)
        else:
            base["stats"][key] = max(0, int(value) if isinstance(value, (int, float)) else 0)
    # A partial file is not treated as an already-started career. This keeps a
    # damaged/missing save from exposing a meaningless Continue button.
    base["career"] = bool(raw.get("career", False))
    return base


def overall(data):
    a = data["attributes"]
    score = sum(a[k] for k in ("pace", "shooting", "passing", "dribbling", "defending", "stamina")) / 6
    return int(clamp(round(score), 60, 99))


class Button:
    def __init__(self, rect, label, action, accent=False, enabled=True, small=False):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.action = action
        self.accent = accent
        self.enabled = enabled
        self.small = small

    def draw(self, game, surface):
        mouse = game.mouse_pos
        hover = self.enabled and self.rect.collidepoint(mouse)
        if not self.enabled:
            fill = (58, 70, 79)
        elif self.accent:
            fill = lerp_color((206, 146, 37), (250, 202, 66), 0.22 if hover else 0)
        else:
            fill = (67, 111, 143) if hover else PANEL_2
        pygame.draw.rect(surface, fill, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE if hover else (128, 170, 196), self.rect, 2, border_radius=10)
        game.text(surface, self.label, self.rect.center, 19 if self.small else 22,
                  INK if self.accent and self.enabled else WHITE, center=True)


class Player:
    def __init__(self, team, role, pos, home, colour, name, star=False, controlled=False):
        self.team = team
        self.role = role
        self.pos = vec(*pos)
        self.home = vec(*home)
        self.vel = vec()
        self.colour = colour
        self.name = name
        self.star = star
        self.controlled = controlled
        self.radius = 13 if role != "GK" else 14
        self.cooldown = random.uniform(.1, .9)
        self.last_direction = vec(1 if team == 0 else -1, 0)
        self.flash = 0
        self.match_goals = 0
        self.match_assists = 0
        self.match_passes = 0
        self.match_tackles = 0

    def draw(self, surface, match):
        p = (int(self.pos.x), int(self.pos.y))
        shadow = (p[0] + 2, p[1] + 5)
        pygame.draw.circle(surface, (20, 54, 40), shadow, self.radius + 2)
        if self.star:
            pygame.draw.circle(surface, GOLD, p, self.radius + 5, 3)
        if self.controlled:
            pygame.draw.circle(surface, WHITE, p, self.radius + 4, 3)
            pygame.draw.polygon(surface, GOLD, [(p[0], p[1] - 28), (p[0] - 7, p[1] - 19), (p[0] + 7, p[1] - 19)])
        pygame.draw.circle(surface, self.colour, p, self.radius)
        pygame.draw.circle(surface, (17, 32, 46), p, self.radius, 2)
        pygame.draw.circle(surface, SKIN, (p[0], p[1] - 5), 5)
        if self.controlled and match.game.data["cosmetics"]["badge"]:
            match.game.text(surface, "7", (p[0], p[1] + 5), 11, WHITE, center=True)
        if self.flash > 0:
            pygame.draw.circle(surface, WHITE, p, self.radius + 7, 2)


class Ball:
    def __init__(self):
        self.pos = vec(PITCH.center)
        self.vel = vec()
        self.owner = None
        self.last_touch = None
        self.last_pass_from = None
        self.last_pass_team = None
        self.pass_live = False
        self.kick_lock = 0
        self.trail = []

    def release(self, velocity, toucher=None):
        self.owner = None
        self.vel = vec(velocity)
        self.last_touch = toucher
        self.kick_lock = .14

    def draw(self, surface, game):
        if game.data["cosmetics"]["trail"]:
            for index, old in enumerate(self.trail[-10:]):
                radius = max(2, 7 - (len(self.trail[-10:]) - index) // 2)
                pygame.draw.circle(surface, (209, 232, 245), old, radius)
        ball_colour = GOLD if game.data["cosmetics"]["gold_ball"] else ((63, 183, 231) if game.data["cosmetics"]["azure_ball"] else WHITE)
        p = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(surface, (18, 39, 33), (p[0] + 2, p[1] + 3), 9)
        pygame.draw.circle(surface, ball_colour, p, 8)
        pygame.draw.circle(surface, INK, p, 8, 1)
        pygame.draw.circle(surface, (35, 50, 64), (p[0] - 2, p[1] - 2), 2)


class Match:
    def __init__(self, game, difficulty, home_style, away_style, objectives):
        self.game = game
        self.difficulty = difficulty
        self.config = DIFFICULTIES[difficulty]
        self.home_style = home_style
        self.away_style = away_style
        self.home_name = game.data.get("team_name", "North Rovers United")
        self.away_name = game.prematch_away_name
        self.objectives = [{"id": x, "complete": False} for x in objectives]
        self.players = []
        self.home = []
        self.away = []
        self.ball = Ball()
        self.score = [0, 0]
        self.time = 0.0
        self.started = False
        self.kickoff = 1.6
        self.event = "Kick-off approaching"
        self.event_timer = 2.0
        self.charge = 0.0
        self.charging = False
        self.call_timer = 0.0
        self.free_kick = None
        self.confirm = None
        self.finished = False
        self.human_losses = 0
        self.human_fouls = 0
        self.goal_flash = 0.0
        self.last_goal_team = None
        self.make_teams()

    def make_teams(self):
        data = self.game.data
        home_colour = tuple(data["colour"])
        away_colour = (214, 82, 83)
        # Keeper + six readable formation slots. The user replaces the appropriate outfielder.
        hslots = [
            ("GK", (160, 371)), ("Defender", (338, 260)), ("Defender", (338, 482)),
            ("Midfielder", (548, 290)), ("Midfielder", (548, 450)),
            ("Winger", (735, 205)), ("Striker", (792, 370)),
        ]
        aslots = [
            ("GK", (1120, 371)), ("Defender", (942, 260)), ("Defender", (942, 482)),
            ("Midfielder", (732, 290)), ("Midfielder", (732, 450)),
            ("Winger", (545, 535)), ("Striker", (488, 370)),
        ]
        target_role = data["position"]
        possible = [i for i, item in enumerate(hslots) if item[0] == target_role]
        control_slot = possible[-1] if possible else 6
        for i, (role, position) in enumerate(hslots):
            is_human = i == control_slot
            player = Player(0, role, position, position, home_colour,
                            "You" if is_human else "Mate " + str(i), controlled=is_human)
            self.home.append(player)
            self.players.append(player)
            if is_human:
                self.human = player
        star_index = 6 if self.config["star"] is True else (6 if self.config["star"] and random.random() < .45 else -1)
        for i, (role, position) in enumerate(aslots):
            player = Player(1, role, position, position, away_colour, "Rival " + str(i), star=(i == star_index))
            self.away.append(player)
            self.players.append(player)

    def set_event(self, message, seconds=1.65):
        self.event = message
        self.event_timer = seconds

    def objective_progress(self, obj):
        name, target = OBJECTIVE_INFO[obj["id"]]
        if obj["id"] == "goal":
            current = self.human.match_goals
        elif obj["id"] == "assist":
            current = self.human.match_assists
        elif obj["id"] == "passes":
            current = self.human.match_passes
        else:
            current = max(0, self.score[0] - self.score[1])
        return name, min(current, target), target

    def check_objectives(self, final=False):
        for obj in self.objectives:
            if obj["complete"]:
                continue
            _, current, target = self.objective_progress(obj)
            # A two-goal win cannot be complete until the result is confirmed.
            if current >= target and (obj["id"] != "win_two" or final):
                obj["complete"] = True
                self.set_event("Objective complete!", 1.4)

    def controlled_speed(self, sprinting):
        attr = self.game.data["attributes"]
        pace = attr["pace"] + self.game.data["upgrades"]["pace"] * 3
        stamina_factor = .6 + .4 * (self.human_stamina / 100)
        base = 108 + pace * 1.75
        return base * stamina_factor * (1.27 if sprinting and self.human_stamina > 1 else 1)

    @property
    def human_stamina(self):
        return getattr(self.human, "stamina", 100.0)

    def start(self):
        for p in self.players:
            p.stamina = 100.0
        self.ball.pos = vec(PITCH.center)
        self.ball.owner = self.human
        self.human.pos = vec(PITCH.centerx - 36, PITCH.centery)
        self.human.last_direction = vec(1, 0)
        self.started = True
        self.set_event("Kick-off!", 1.4)

    def reset_positions(self, conceding_team=None):
        for p in self.players:
            p.pos = p.home.copy()
            p.vel = vec()
        self.ball.pos = vec(PITCH.center)
        self.ball.vel = vec()
        self.ball.owner = self.human if conceding_team == 1 else self.away[-1]
        self.ball.kick_lock = .5
        self.kickoff = 1.1

    def nearest_player(self, point, team=None, exclude=None):
        candidates = self.players if team is None else (self.home if team == 0 else self.away)
        candidates = [p for p in candidates if p is not exclude]
        return min(candidates, key=lambda p: p.pos.distance_squared_to(point)) if candidates else None

    def team_for_owner(self):
        return self.ball.owner.team if self.ball.owner else None

    def pass_ball(self, passer, target):
        direction = target.pos - passer.pos
        distance = max(1, direction.length())
        speed = clamp(230 + distance * .85, 285, 520)
        self.ball.last_pass_from = passer
        self.ball.last_pass_team = passer.team
        self.ball.pass_live = True
        self.ball.pos = passer.pos + safe_normal(direction) * (passer.radius + 9)
        self.ball.release(safe_normal(direction) * speed, passer)
        passer.cooldown = .52
        if passer is self.human:
            self.set_event("Pass away", .7)

    def shoot_ball(self, shooter, power=1.0):
        goal = vec(PITCH.right + 23 if shooter.team == 0 else PITCH.left - 23, PITCH.centery)
        # Aim towards the open half of the goal, with small skill-dependent variation.
        offset = random.uniform(-GOAL_H * .32, GOAL_H * .32)
        goal.y += offset
        direction = safe_normal(goal - shooter.pos, (1 if shooter.team == 0 else -1, 0))
        shooting = self.game.data["attributes"]["shooting"] if shooter is self.human else 68 * self.config["shoot"] + (10 if shooter.star else 0)
        speed = (390 + shooting * 3.0) * clamp(power, .35, 1.2)
        # Keep a user's completed pass alive through their teammate's shot so
        # that an assist is awarded if it goes in without an opponent touch.
        assisted = (self.ball.last_pass_from is self.human and
                    self.ball.last_pass_team == shooter.team and shooter is not self.human)
        if not assisted:
            self.ball.last_pass_from = None
            self.ball.pass_live = False
        self.ball.pos = shooter.pos + direction * (shooter.radius + 10)
        self.ball.release(direction * speed, shooter)
        shooter.cooldown = .8
        if shooter is self.human:
            self.set_event("Shot!", .8)

    def choose_pass_target(self, player):
        own = self.home if player.team == 0 else self.away
        forward = 1 if player.team == 0 else -1
        best = None
        best_score = -9999
        for mate in own:
            if mate is player:
                continue
            dist = player.pos.distance_to(mate.pos)
            if dist < 45 or dist > 420:
                continue
            forwardness = (mate.pos.x - player.pos.x) * forward
            pressure = min((op.pos.distance_to(mate.pos) for op in (self.away if player.team == 0 else self.home)), default=150)
            score = forwardness * .65 - dist * .17 + pressure * .33
            if self.call_timer > 0 and mate is self.human and player.team == 0:
                score += 120 + self.game.data["trust"] * 1.2
            if score > best_score:
                best_score, best = score, mate
        return best

    def apply_possession(self, player):
        old = self.ball.owner
        if old is player:
            return
        if old is self.human and player.team == 1:
            self.human_losses += 1
            self.set_event("Possession lost", .9)
        # An opponent touch invalidates a pending assist, as required.
        if player.team != self.ball.last_pass_team:
            self.ball.last_pass_from = None
            self.ball.pass_live = False
        if player.team == 0 and self.ball.pass_live and self.ball.last_pass_from is self.human and player is not self.human:
            self.human.match_passes += 1
            self.ball.pass_live = False
            self.set_event("Great pass!", 1.0)
        self.ball.owner = player
        self.ball.vel = vec()
        self.ball.last_touch = player

    def human_tackle(self):
        h = self.human
        victim = self.nearest_player(h.pos, team=1)
        if victim is None or victim is not self.ball.owner or h.pos.distance_to(victim.pos) > 42:
            self.set_event("No tackle there", .65)
            return
        toward_ball = safe_normal(victim.pos - h.pos)
        facing = victim.last_direction
        from_front = toward_ball.dot(facing) > -.15
        chance = .72 if from_front else .43
        chance += (self.game.data["attributes"]["defending"] - 60) * .008
        if random.random() < chance:
            self.apply_possession(h)
            h.match_tackles += 1
            self.set_event("Clean tackle!", 1.15)
        else:
            self.human_fouls += 1
            self.set_event("Foul!", 1.35)
            self.award_free_kick(1, victim.pos)

    def award_free_kick(self, team, position):
        self.ball.owner = None
        self.ball.pos = vec(clamp(position.x, PITCH.left + 25, PITCH.right - 25), clamp(position.y, PITCH.top + 25, PITCH.bottom - 25))
        self.ball.vel = vec()
        self.free_kick = {"team": team, "timer": 1.45}

    def update_human(self, dt, keys):
        h = self.human
        direction = vec()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: direction.x += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]: direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: direction.y += 1
        sprint = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and direction.length_squared() > 0
        if direction.length_squared() > 0:
            direction = direction.normalize()
            h.last_direction = direction
            desired = direction * self.controlled_speed(sprint)
        else:
            desired = vec()
        h.vel = h.vel.lerp(desired, clamp(dt * 11, 0, 1))
        h.pos += h.vel * dt
        h.pos.x = clamp(h.pos.x, PITCH.left + h.radius, PITCH.right - h.radius)
        h.pos.y = clamp(h.pos.y, PITCH.top + h.radius, PITCH.bottom - h.radius)
        if sprint and direction.length_squared() > 0:
            h.stamina = max(0, h.stamina - 19 * dt)
        else:
            h.stamina = min(100, h.stamina + 13 * dt)

    def bot_desired(self, p):
        ball = self.ball
        own = self.home if p.team == 0 else self.away
        other = self.away if p.team == 0 else self.home
        direction_goal = 1 if p.team == 0 else -1
        config_speed = self.config["speed"] if p.team == 1 else .98
        press = self.config["press"] if p.team == 1 else .98
        style = self.away_style if p.team == 1 else self.home_style
        speed = (140 + (20 if p.star else 0)) * config_speed
        if p.role == "GK":
            target = vec(p.home.x, clamp(ball.pos.y, PITCH.centery - 64, PITCH.centery + 64))
            # Keeper steps out modestly at a dangerous loose ball.
            if ball.pos.distance_to(p.pos) < 100 and (ball.pos.x - PITCH.centerx) * direction_goal < 0:
                target = ball.pos
            return target - p.pos, speed * (self.config["keeper"] if p.team == 1 else 1)
        if ball.owner is p:
            goal = vec(PITCH.right if p.team == 0 else PITCH.left, PITCH.centery)
            distance_goal = p.pos.distance_to(goal)
            p.cooldown -= 0.016
            pressure = min(op.pos.distance_to(p.pos) for op in other)
            shoot_range = 225 if p.star else 175
            if distance_goal < shoot_range and p.cooldown <= 0:
                self.shoot_ball(p, 1.0)
                return vec(), speed
            target = self.choose_pass_target(p)
            pass_bias = .012 if style == "Possession" else (.006 if style == "Defensive" else .009)
            if target and p.cooldown <= 0 and (pressure < 63 or random.random() < pass_bias):
                self.pass_ball(p, target)
                return vec(), speed
            target_pos = goal + vec(0, (p.home.y - PITCH.centery) * .35)
            return target_pos - p.pos, speed * 1.08
        if ball.owner is None:
            nearest = self.nearest_player(ball.pos)
            if nearest is p:
                return ball.pos - p.pos, speed * 1.12
            return p.home - p.pos, speed
        if ball.owner.team != p.team:
            dist = p.pos.distance_to(ball.owner.pos)
            closest = min(own, key=lambda q: q.pos.distance_squared_to(ball.owner.pos))
            aggressiveness = 1.22 if style == "Attacking" else (.78 if style == "Defensive" else 1)
            if closest is p or (dist < 135 * press * aggressiveness and p.role != "Defender"):
                return ball.owner.pos - p.pos, speed * press
            # Defenders fall goal-side, preserving an organised shape.
            cover = p.home.lerp(ball.owner.pos, .22)
            cover.x = min(cover.x, ball.owner.pos.x - 45) if p.team == 0 else max(cover.x, ball.owner.pos.x + 45)
            return cover - p.pos, speed
        # Teammate has ball: make supporting runs by style.
        target = p.home.copy()
        if style == "Attacking":
            target.x += 72 * direction_goal
        elif style == "Defensive":
            target.x -= 42 * direction_goal
        elif style == "Counterattack":
            target.x += 105 * direction_goal if ball.owner.pos.x * direction_goal > PITCH.centerx * direction_goal else 20 * direction_goal
        else:
            target = target.lerp(ball.owner.pos, .14)
        return target - p.pos, speed

    def update_bots(self, dt):
        for p in self.players:
            if p.controlled:
                continue
            desired, max_speed = self.bot_desired(p)
            if desired.length_squared() > 1:
                direction = desired.normalize()
                p.last_direction = direction
                wanted = direction * max_speed
            else:
                wanted = vec()
            p.vel = p.vel.lerp(wanted, clamp(dt * 5.4, 0, 1))
            p.pos += p.vel * dt
            p.pos.x = clamp(p.pos.x, PITCH.left + p.radius, PITCH.right - p.radius)
            p.pos.y = clamp(p.pos.y, PITCH.top + p.radius, PITCH.bottom - p.radius)
            p.cooldown = max(-1, p.cooldown - dt)
        # Bots can challenge a human ball carrier without making every contact a foul.
        if self.ball.owner is self.human:
            challenger = self.nearest_player(self.human.pos, team=1)
            if challenger and challenger.pos.distance_to(self.human.pos) < 28 and challenger.cooldown <= 0:
                challenger.cooldown = .8
                chance = .18 * self.config["press"] + (0.12 if challenger.star else 0)
                if random.random() < chance:
                    self.apply_possession(challenger)
                    self.set_event("Tackled", .9)

    def update_ball(self, dt, keys):
        ball = self.ball
        ball.kick_lock = max(0, ball.kick_lock - dt)
        if ball.owner:
            owner = ball.owner
            ahead = owner.last_direction * (owner.radius + 9)
            if owner is self.human:
                sprinting = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and owner.vel.length_squared() > 1500
                control = self.game.data["attributes"]["dribbling"] + self.game.data["upgrades"]["dribbling"] * 4
                distance = owner.radius + (16 if sprinting else 9) - (control - 60) * .08
                ahead = owner.last_direction * max(owner.radius + 6, distance)
                # A low-control sprint can spill the ball ahead, creating a fair turnover risk.
                spill_chance = max(0, (.012 - (control - 60) * .00016))
                if sprinting and random.random() < spill_chance:
                    ball.pos = owner.pos + ahead
                    ball.release(owner.last_direction * 170, owner)
                    self.set_event("Heavy touch", .75)
                    return
            ball.pos = owner.pos + ahead
            ball.vel = owner.vel
        else:
            ball.pos += ball.vel * dt
            ball.vel *= max(0, 1 - 1.4 * dt)
            if ball.pos.y < PITCH.top + 6:
                ball.pos.y = PITCH.top + 6
                ball.vel.y = abs(ball.vel.y) * .68
            if ball.pos.y > PITCH.bottom - 6:
                ball.pos.y = PITCH.bottom - 6
                ball.vel.y = -abs(ball.vel.y) * .68
            in_goal_mouth = abs(ball.pos.y - PITCH.centery) < GOAL_H / 2
            if ball.pos.x <= PITCH.left - 4 or ball.pos.x >= PITCH.right + 4:
                if in_goal_mouth:
                    scorer_team = 0 if ball.pos.x >= PITCH.right else 1
                    self.goal(scorer_team, ball.last_touch)
                    return
                ball.pos.x = clamp(ball.pos.x, PITCH.left + 6, PITCH.right - 6)
                ball.vel.x *= -.68
            if ball.kick_lock <= 0 and ball.vel.length() < 245:
                close = self.nearest_player(ball.pos)
                if close and close.pos.distance_to(ball.pos) < close.radius + 8:
                    self.apply_possession(close)
        ball.trail.append((int(ball.pos.x), int(ball.pos.y)))
        if len(ball.trail) > 18:
            ball.trail.pop(0)

    def goalie_save(self):
        # Handles a keeper getting hands/body on a loose goalbound ball.
        if self.ball.owner:
            return
        keeper = self.home[0] if self.ball.pos.x < PITCH.centerx else self.away[0]
        goal_side = 0 if keeper.team == 0 else 1
        if self.ball.pos.distance_to(keeper.pos) < keeper.radius + 13 and self.ball.vel.length() > 100:
            self.apply_possession(keeper)
            self.set_event("Saved!", 1.1)

    def goal(self, team, scorer):
        self.score[team] += 1
        if scorer is not None:
            scorer.match_goals += 1
        if team == 0 and scorer is self.human:
            self.set_event("GOAL! You scored!", 2.0)
        else:
            self.set_event("GOAL!", 2.0)
        # Assist lives only through an uninterrupted successful pass from the user.
        if team == 0 and scorer is not self.human and self.ball.last_pass_from is self.human and self.ball.last_pass_team == 0:
            self.human.match_assists += 1
            self.set_event("GOAL! Assist awarded!", 2.0)
        self.goal_flash = 1.3
        self.last_goal_team = team
        self.ball.last_pass_from = None
        self.ball.pass_live = False
        self.check_objectives()
        self.reset_positions(conceding_team=1 - team)

    def update_free_kick(self, dt):
        if not self.free_kick:
            return False
        self.free_kick["timer"] -= dt
        if self.free_kick["timer"] > 0:
            return True
        team = self.free_kick["team"]
        taker = self.nearest_player(self.ball.pos, team=team)
        self.apply_possession(taker)
        self.free_kick = None
        self.set_event("Free kick!", 1.1)
        return False

    def update(self, dt, keys):
        self.event_timer = max(0, self.event_timer - dt)
        self.goal_flash = max(0, self.goal_flash - dt)
        self.call_timer = max(0, self.call_timer - dt)
        for p in self.players:
            p.flash = max(0, p.flash - dt)
        if not self.started:
            self.start()
        if self.kickoff > 0:
            self.kickoff -= dt
            return
        if self.update_free_kick(dt):
            return
        self.time += dt
        self.update_human(dt, keys)
        self.update_bots(dt)
        self.update_ball(dt, keys)
        self.goalie_save()
        self.check_objectives()
        if self.time >= 180:
            self.finish()

    def finish(self):
        if self.finished:
            return
        self.finished = True
        self.check_objectives(final=True)
        self.set_event("Full Time!", 2.0)
        self.game.complete_match(self)

    def handle_keydown(self, key):
        if key == pygame.K_x:
            self.call_timer = 2.1
            self.set_event("Calling for a pass", .9)
        elif key == pygame.K_z and self.ball.owner is self.human and self.kickoff <= 0 and not self.free_kick:
            target = self.choose_pass_target(self.human)
            if target:
                self.pass_ball(self.human, target)
        elif key == pygame.K_c and self.ball.owner is self.human:
            self.charging = True
            self.charge = 0
        elif key == pygame.K_v and self.kickoff <= 0 and not self.free_kick:
            self.human_tackle()

    def handle_keyup(self, key):
        if key == pygame.K_c and self.charging:
            self.charging = False
            if self.ball.owner is self.human and self.kickoff <= 0 and not self.free_kick:
                fatigue = .62 + .38 * self.human_stamina / 100
                self.shoot_ball(self.human, (.35 + .65 * self.charge) * fatigue)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Life of a Footballer")
        self.window = pygame.display.set_mode(LOGICAL_SIZE, pygame.RESIZABLE)
        self.canvas = pygame.Surface(LOGICAL_SIZE).convert()
        self.clock = pygame.time.Clock()
        self.fonts = {}
        self.save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_NAME)
        self.data = self.load_save()
        # This also repairs an incomplete save schema on launch.
        self.save()
        self.screen = "welcome"
        self.buttons = []
        self.mouse_pos = (0, 0)
        self.running = True
        self.match = None
        self.difficulty = "Medium"
        self.home_style = random.choice(STYLE_NAMES)
        self.away_style = random.choice(STYLE_NAMES)
        self.prematch_away_name = team_name(self.away_style, True)
        self.prematch_objectives = random.sample(list(OBJECTIVE_INFO), 2)
        self.new_position = "Midfielder"
        self.new_colour = PALETTE[0]
        self.tip_index = 0
        self.tip_timer = 0
        self.return_screen = "welcome"
        self.result = None
        self.level_choices = 0

    def load_save(self):
        try:
            with open(self.save_path, "r", encoding="utf-8") as handle:
                raw = json.load(handle)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            raw = None
        return repaired_save(raw)

    def save(self):
        try:
            temporary = self.save_path + ".tmp"
            with open(temporary, "w", encoding="utf-8") as handle:
                json.dump(self.data, handle, indent=2)
            os.replace(temporary, self.save_path)
        except OSError:
            # A game remains playable if a read-only location prevents persistence.
            pass

    def font(self, size, bold=False):
        key = (size, bold)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(None, size)
            self.fonts[key].set_bold(bold)
        return self.fonts[key]

    def text(self, surface, value, position, size=24, colour=WHITE, center=False, bold=False):
        image = self.font(size, bold).render(str(value), True, colour)
        rect = image.get_rect(center=position) if center else image.get_rect(topleft=position)
        surface.blit(image, rect)
        return rect

    def wrap(self, surface, words, rect, size=20, colour=WHITE, line_height=None, center=False):
        words = str(words).split()
        line = ""
        y = rect.y
        h = line_height or size + 5
        for word in words:
            test = (line + " " + word).strip()
            if self.font(size).size(test)[0] > rect.width and line:
                x = rect.centerx if center else rect.x
                self.text(surface, line, (x, y), size, colour, center=center)
                y += h
                line = word
            else:
                line = test
        if line:
            x = rect.centerx if center else rect.x
            self.text(surface, line, (x, y), size, colour, center=center)
        return y + h

    def panel(self, surface, rect, colour=PANEL, border=(83, 130, 157)):
        pygame.draw.rect(surface, colour, pygame.Rect(rect), border_radius=14)
        pygame.draw.rect(surface, border, pygame.Rect(rect), 2, border_radius=14)

    def add_button(self, rect, label, action, accent=False, enabled=True, small=False):
        button = Button(rect, label, action, accent, enabled, small)
        self.buttons.append(button)
        button.draw(self, self.canvas)

    def background(self):
        self.canvas.fill(NAVY)
        for y in range(0, 720, 32):
            pygame.draw.line(self.canvas, (24, 46, 68), (0, y), (1280, y), 1)

    def header(self, title, subtitle=None):
        self.text(self.canvas, title, (45, 28), 42, WHITE, bold=True)
        if subtitle:
            self.text(self.canvas, subtitle, (47, 76), 20, (170, 203, 219))
        pygame.draw.line(self.canvas, (96, 154, 182), (45, 102), (1235, 102), 2)

    def draw_welcome(self):
        self.background()
        # Simple stadium ambience behind the introduction.
        pygame.draw.rect(self.canvas, (41, 98, 76), (0, 395, 1280, 325))
        for i in range(210):
            x = (i * 73 + 31) % 1280
            y = 408 + ((i * 43) % 205)
            colour = [(239, 91, 93), (249, 208, 79), (93, 183, 226), (238, 238, 232)][i % 4]
            pygame.draw.circle(self.canvas, colour, (x, y), 2)
        self.text(self.canvas, "LIFE OF A", (640, 120), 36, (162, 207, 231), center=True, bold=True)
        self.text(self.canvas, "FOOTBALLER", (640, 163), 70, WHITE, center=True, bold=True)
        self.text(self.canvas, "Build your career. Master the match. Become Best in the World.", (640, 235), 23, GOLD, center=True)
        self.panel(self.canvas, (430, 290, 420, 310), (22, 47, 67))
        self.add_button((470, 320, 340, 52), "New Career", "new_career", True)
        self.add_button((470, 387, 340, 52), "Continue Career", "continue", enabled=bool(self.data.get("career")))
        self.add_button((470, 454, 340, 52), "Controls", "controls_welcome")
        self.add_button((470, 521, 340, 52), "Quit", "quit")
        if not self.data.get("career"):
            self.text(self.canvas, "Start a new career to unlock Continue", (640, 613), 18, (170, 203, 219), center=True)

    def draw_new_career(self):
        self.background()
        self.header("New Career", "Choose the footballer you want to become.")
        self.panel(self.canvas, (54, 135, 738, 485))
        self.text(self.canvas, "Choose a position", (86, 163), 28, GOLD, bold=True)
        descriptions = {
            "Striker": "Finishes moves • higher shooting • starts high",
            "Winger": "Uses the flanks • faster pace • starts wide",
            "Midfielder": "Connects play • stronger passing • starts central",
            "Defender": "Wins the ball • stronger defending • starts deep",
        }
        for i, name in enumerate(("Striker", "Winger", "Midfielder", "Defender")):
            y = 207 + i * 77
            selected = self.new_position == name
            self.add_button((84, y, 450, 60), name + " — " + descriptions[name], "position:" + name, selected, small=True)
        self.text(self.canvas, "Pick your kit colour", (836, 163), 28, GOLD, bold=True)
        for i, colour in enumerate(PALETTE):
            x = 862 + (i % 4) * 83
            y = 220 + (i // 4) * 83
            pygame.draw.circle(self.canvas, colour, (x, y), 29)
            pygame.draw.circle(self.canvas, WHITE if tuple(colour) == tuple(self.new_colour) else (82, 128, 156), (x, y), 34, 3)
            # Palette swatches are directly clickable without covering their colour.
            self.buttons.append(Button((x - 37, y - 37, 74, 74), "", "colour:" + str(i), small=True))
        self.panel(self.canvas, (830, 400, 350, 153), (23, 61, 71))
        self.text(self.canvas, "Your starting strengths", (1005, 422), 22, WHITE, center=True, bold=True)
        preview = default_save(self.new_position, self.new_colour)["attributes"]
        summary = "  •  ".join(("Pace " + str(preview["pace"]), "Shooting " + str(preview["shooting"]), "Passing " + str(preview["passing"])))
        self.wrap(self.canvas, summary, pygame.Rect(853, 462, 305, 62), 19, (193, 219, 230), center=True)
        self.add_button((840, 580, 325, 48), "Begin Career", "begin", True)
        self.add_button((70, 640, 220, 42), "Back", "welcome", small=True)

    def draw_dashboard(self):
        self.background()
        data = self.data
        self.header("Home Dashboard", "Your career at a glance")
        cards = [
            ("CREDITS", str(data["credits"]), GOLD), ("LEVEL", str(data["level"]), (135, 222, 156)),
            ("OVERALL", str(overall(data)), (106, 190, 247)), ("TRUST", str(data["trust"]) + "%", (244, 151, 184)),
        ]
        for i, (name, value, colour) in enumerate(cards):
            x = 45 + i * 191
            self.panel(self.canvas, (x, 132, 171, 99), (28, 61, 80))
            self.text(self.canvas, name, (x + 85, 151), 17, (180, 207, 220), center=True, bold=True)
            self.text(self.canvas, value, (x + 85, 180), 34, colour, center=True, bold=True)
        self.panel(self.canvas, (830, 132, 404, 99), (33, 67, 85))
        self.text(self.canvas, "BEST IN THE WORLD", (1032, 149), 18, GOLD, center=True, bold=True)
        wins = data["stats"]["wins"]
        self.text(self.canvas, "Overall " + str(overall(data)) + "/90   •   Wins " + str(wins) + "/10", (1032, 178), 21, WHITE, center=True)
        ratio = min(1, (min(90, overall(data)) / 90 + min(10, wins) / 10) / 2)
        pygame.draw.rect(self.canvas, (15, 37, 52), (867, 204, 330, 11), border_radius=5)
        pygame.draw.rect(self.canvas, GOLD, (867, 204, int(330 * ratio), 11), border_radius=5)
        self.panel(self.canvas, (45, 258, 530, 285))
        self.text(self.canvas, "Career Brief", (72, 282), 26, GOLD, bold=True)
        self.text(self.canvas, "Position: " + data["position"], (74, 327), 23, WHITE)
        self.text(self.canvas, "Latest result", (74, 370), 19, (168, 205, 221), bold=True)
        self.wrap(self.canvas, data["latest_result"], pygame.Rect(74, 397, 465, 67), 22, WHITE)
        need = data["level"] * 100
        self.text(self.canvas, "XP: " + str(data["xp"]) + " / " + str(need), (74, 493), 20, (185, 216, 230))
        pygame.draw.rect(self.canvas, (16, 42, 57), (74, 520, 437, 10), border_radius=5)
        pygame.draw.rect(self.canvas, (91, 197, 123), (74, 520, int(437 * data["xp"] / need), 10), border_radius=5)
        self.panel(self.canvas, (605, 258, 629, 285))
        self.text(self.canvas, "Ready for matchday?", (920, 285), 28, WHITE, center=True, bold=True)
        self.text(self.canvas, "Improve your skills, earn trust, and lead your team to victory.", (920, 327), 20, (180, 211, 225), center=True)
        self.add_button((690, 378, 462, 55), "Play Next Match", "prematch", True)
        self.add_button((690, 449, 218, 51), "Marketplace", "market")
        self.add_button((934, 449, 218, 51), "Profile", "profile")
        self.add_button((605, 578, 188, 47), "Customise Player", "customise", small=True)
        self.add_button((813, 578, 188, 47), "Helpful Tips", "tips", small=True)
        self.add_button((1021, 578, 213, 47), "Save & Welcome", "save_welcome", small=True)

    def set_prematch(self):
        self.home_style = random.choice(STYLE_NAMES)
        self.away_style = random.choice(STYLE_NAMES)
        self.prematch_away_name = team_name(self.away_style, True)
        self.prematch_objectives = random.sample(list(OBJECTIVE_INFO), 2)
        self.screen = "prematch"

    def draw_prematch(self):
        self.background()
        self.header("Pre-match", "Select a challenge, inspect the opposition, and set your objectives.")
        self.panel(self.canvas, (43, 130, 320, 512))
        self.text(self.canvas, "Difficulty", (203, 155), 28, GOLD, center=True, bold=True)
        for i, name in enumerate(DIFFICULTIES):
            self.add_button((76, 202 + i * 72, 254, 54), name, "difficulty:" + name, self.difficulty == name)
        self.panel(self.canvas, (390, 130, 415, 512))
        self.text(self.canvas, self.data["team_name"], (597, 155), 29, (119, 205, 248), center=True, bold=True)
        self.text(self.canvas, "Style: " + self.home_style, (597, 194), 21, WHITE, center=True)
        self.text(self.canvas, "Team quality: " + str(overall(self.data)), (597, 228), 21, (175, 213, 227), center=True)
        pygame.draw.line(self.canvas, (86, 140, 164), (430, 254), (765, 254), 1)
        self.text(self.canvas, "vs", (597, 276), 22, GOLD, center=True, bold=True)
        self.text(self.canvas, self.prematch_away_name, (597, 311), 28, RED, center=True, bold=True)
        self.text(self.canvas, "Style: " + self.away_style, (597, 349), 21, WHITE, center=True)
        config = DIFFICULTIES[self.difficulty]
        self.text(self.canvas, "Predicted strength: " + str(config["strength"]), (597, 383), 20, (175, 213, 227), center=True)
        if config["star"] is True:
            self.text(self.canvas, "★ Star player expected", (597, 418), 21, GOLD, center=True)
        elif config["star"] is None:
            self.text(self.canvas, "★ A star player may appear", (597, 418), 19, (228, 202, 126), center=True)
        self.panel(self.canvas, (831, 130, 405, 512))
        self.text(self.canvas, "Opponent scouting", (1033, 155), 27, GOLD, center=True, bold=True)
        self.wrap(self.canvas, config["description"], pygame.Rect(865, 199, 338, 98), 21, WHITE, center=True)
        self.text(self.canvas, "Match objectives", (1033, 331), 24, (176, 218, 237), center=True, bold=True)
        for i, item in enumerate(self.prematch_objectives):
            self.text(self.canvas, "• " + OBJECTIVE_INFO[item][0], (874, 375 + i * 43), 21, WHITE)
            self.text(self.canvas, "+8 credits", (1128, 375 + i * 43), 18, GOLD, center=True)
        self.add_button((872, 522, 324, 55), "Start Match", "start_match", True)
        self.add_button((45, 660, 220, 38), "Back Home", "dashboard", small=True)

    def draw_pitch(self):
        # stands and audience
        self.canvas.fill((14, 38, 55))
        pygame.draw.rect(self.canvas, (37, 61, 76), (74, 61, 1132, 600), border_radius=18)
        for i in range(440):
            x = 85 + ((i * 47) % 1110)
            y = 72 + ((i * 67) % 578)
            if PITCH.inflate(56, 56).collidepoint(x, y) and not PITCH.collidepoint(x, y):
                colours = [(240, 218, 104), (231, 93, 100), (104, 176, 231), (230, 233, 230), (102, 190, 132)]
                pygame.draw.circle(self.canvas, colours[i % len(colours)], (x, y), 2)
        # stripes and field
        pygame.draw.rect(self.canvas, (43, 143, 79), PITCH)
        stripe_w = PITCH.width / 10
        for i in range(10):
            if i % 2:
                pygame.draw.rect(self.canvas, (48, 153, 84), (PITCH.left + int(i * stripe_w), PITCH.top, int(stripe_w) + 1, PITCH.height))
        pygame.draw.rect(self.canvas, WHITE, PITCH, 3)
        pygame.draw.line(self.canvas, WHITE, (PITCH.centerx, PITCH.top), (PITCH.centerx, PITCH.bottom), 2)
        pygame.draw.circle(self.canvas, WHITE, PITCH.center, 66, 2)
        pygame.draw.circle(self.canvas, WHITE, PITCH.center, 3)
        left_box = pygame.Rect(PITCH.left, PITCH.centery - 105, 118, 210)
        right_box = pygame.Rect(PITCH.right - 118, PITCH.centery - 105, 118, 210)
        pygame.draw.rect(self.canvas, WHITE, left_box, 2)
        pygame.draw.rect(self.canvas, WHITE, right_box, 2)
        pygame.draw.rect(self.canvas, WHITE, (PITCH.left - 18, PITCH.centery - GOAL_H // 2, 18, GOAL_H), 3)
        pygame.draw.rect(self.canvas, WHITE, (PITCH.right, PITCH.centery - GOAL_H // 2, 18, GOAL_H), 3)

    def draw_match_hud(self):
        m = self.match
        minute = int(m.time)
        pygame.draw.rect(self.canvas, (14, 31, 45), (369, 12, 542, 58), border_radius=12)
        pygame.draw.rect(self.canvas, (108, 156, 179), (369, 12, 542, 58), 2, border_radius=12)
        self.text(self.canvas, m.home_name[:13], (384, 29), 19, (124, 209, 248))
        self.text(self.canvas, str(m.score[0]) + "  -  " + str(m.score[1]), (640, 25), 31, WHITE, center=True, bold=True)
        self.text(self.canvas, m.away_name[:13], (895, 29), 19, (249, 142, 145), center=True)
        self.text(self.canvas, "%d:%02d / 3:00" % (minute // 60, minute % 60), (640, 51), 17, (177, 209, 225), center=True)
        self.panel(self.canvas, (19, 129, 202, 142), (15, 39, 55))
        self.text(self.canvas, "YOUR MATCH", (120, 144), 18, GOLD, center=True, bold=True)
        self.text(self.canvas, "Rating  " + format(self.live_rating(), ".1f"), (37, 175), 21, WHITE)
        self.text(self.canvas, "Stamina", (37, 207), 18, (184, 216, 231))
        pygame.draw.rect(self.canvas, (39, 58, 69), (37, 233, 150, 13), border_radius=6)
        pygame.draw.rect(self.canvas, (87, 206, 120), (37, 233, int(150 * m.human_stamina / 100), 13), border_radius=6)
        self.panel(self.canvas, (1003, 131, 257, 176), (15, 39, 55))
        self.text(self.canvas, "OBJECTIVES", (1132, 146), 18, GOLD, center=True, bold=True)
        for i, obj in enumerate(m.objectives):
            name, cur, target = m.objective_progress(obj)
            colour = (110, 221, 148) if obj["complete"] else WHITE
            self.wrap(self.canvas, name, pygame.Rect(1018, 173 + i * 65, 154, 38), 16, colour)
            self.text(self.canvas, ("✓" if obj["complete"] else str(cur) + "/" + str(target)), (1220, 190 + i * 65), 19, colour, center=True, bold=True)
        if m.charging:
            self.panel(self.canvas, (465, 667, 350, 30), (17, 35, 48))
            pygame.draw.rect(self.canvas, GOLD, (470, 672, int(340 * m.charge), 20), border_radius=8)
            self.text(self.canvas, "SHOT POWER", (640, 682), 14, INK, center=True, bold=True)
        if m.event_timer > 0:
            self.panel(self.canvas, (462, 79, 356, 34), (20, 52, 65))
            self.text(self.canvas, m.event, (640, 96), 21, GOLD, center=True, bold=True)
        if m.free_kick:
            self.text(self.canvas, "FREE KICK", (640, 650), 23, GOLD, center=True, bold=True)

    def draw_match(self):
        self.draw_pitch()
        m = self.match
        for player in m.players:
            player.draw(self.canvas, m)
        m.ball.draw(self.canvas, self)
        self.draw_match_hud()
        if m.goal_flash > 0 and self.data["cosmetics"]["celebration"]:
            for i in range(18):
                angle = i * math.tau / 18 + m.goal_flash * 3
                centre = (640, 390)
                end = (centre[0] + math.cos(angle) * 170, centre[1] + math.sin(angle) * 90)
                pygame.draw.line(self.canvas, GOLD if i % 2 else WHITE, centre, end, 3)
        if self.screen == "pause":
            self.draw_pause()

    def draw_pause(self):
        shade = pygame.Surface(LOGICAL_SIZE, pygame.SRCALPHA)
        shade.fill((0, 0, 0, 155))
        self.canvas.blit(shade, (0, 0))
        self.panel(self.canvas, (425, 128, 430, 465), (23, 53, 73), (176, 220, 239))
        self.text(self.canvas, "PAUSED", (640, 158), 39, WHITE, center=True, bold=True)
        self.add_button((480, 205, 320, 47), "Resume", "resume", True)
        self.add_button((480, 264, 320, 47), "Controls", "controls_pause")
        self.add_button((480, 323, 320, 47), "Restart Match", "confirm_restart")
        self.add_button((480, 382, 320, 47), "Quit Match", "confirm_quit")
        self.text(self.canvas, "WASD / arrows move • Shift sprint • Z pass • C shoot", (640, 466), 16, (190, 217, 231), center=True)
        self.text(self.canvas, "V tackle • X call for pass • Esc resume", (640, 491), 16, (190, 217, 231), center=True)
        if self.match.confirm:
            self.draw_confirmation()

    def draw_confirmation(self):
        action = self.match.confirm
        self.panel(self.canvas, (448, 509, 384, 150), (54, 39, 48), (249, 158, 166))
        wording = "Restart this match? Progress from this match will be lost." if action == "restart" else "Quit this match? No rewards or match stats will be saved."
        self.wrap(self.canvas, wording, pygame.Rect(472, 525, 336, 48), 18, WHITE, center=True)
        self.add_button((480, 594, 142, 41), "Yes", "do_" + action, True, small=True)
        self.add_button((658, 594, 142, 41), "Cancel", "cancel_confirm", small=True)

    def draw_market(self):
        self.background()
        self.header("Marketplace", "Spend credits on permanent skill upgrades and cosmetics.")
        self.text(self.canvas, "Credits: " + str(self.data["credits"]), (1125, 49), 25, GOLD, center=True, bold=True)
        types = [("pace", "Pace", "More maximum speed"), ("shooting", "Shot Power", "Faster, stronger shots"), ("dribbling", "Dribbling Control", "Tighter sprint control")]
        for col, (key, title, desc) in enumerate(types):
            x = 44 + col * 402
            self.panel(self.canvas, (x, 134, 370, 302))
            self.text(self.canvas, title, (x + 185, 158), 28, GOLD, center=True, bold=True)
            self.text(self.canvas, desc, (x + 185, 195), 18, (188, 215, 227), center=True)
            current = self.data["upgrades"][key]
            for tier, price in enumerate((25, 60, 120), 1):
                y = 231 + (tier - 1) * 61
                if current >= tier:
                    label, enabled = title + " " + "I" * tier + "  ✓ Owned", False
                elif current == tier - 1:
                    label, enabled = title + " " + "I" * tier + "  —  " + str(price) + " cr", self.data["credits"] >= price
                else:
                    label, enabled = "Unlock " + title + " " + "I" * tier + " first", False
                self.add_button((x + 23, y, 324, 46), label, "buy_upgrade:" + key + ":" + str(tier), current == tier - 1, enabled, small=True)
        self.panel(self.canvas, (44, 462, 1174, 179))
        self.text(self.canvas, "Cosmetics", (74, 483), 27, GOLD, bold=True)
        items = [
            ("trail", "Ball Trail", 40, "A shimmering trail behind the ball"),
            ("badge", "Number Badge", 25, "Show your number on the pitch"),
            ("celebration", "Goal Celebration", 55, "Burst effect after goals"),
            ("azure_ball", "Azure Ball", 30, "A bright blue match ball"),
            ("gold_ball", "Golden Ball", 50, "A golden match ball"),
        ]
        for i, (key, title, price, desc) in enumerate(items):
            x = 67 + i * 228
            owned = self.data["cosmetics"][key]
            self.text(self.canvas, title, (x + 94, 522), 18, WHITE, center=True, bold=True)
            self.wrap(self.canvas, desc, pygame.Rect(x + 5, 546, 178, 35), 14, (177, 210, 225), center=True)
            self.add_button((x, 590, 188, 35), "Owned" if owned else str(price) + " cr", "buy_cosmetic:" + key, not owned, not owned and self.data["credits"] >= price, small=True)
        self.add_button((45, 660, 215, 38), "Back Home", "dashboard", small=True)
        self.add_button((1014, 660, 215, 38), "Free Colour", "customise", small=True)

    def draw_profile(self):
        self.background()
        self.header("Player Profile", "Every match tells the story of your career.")
        data, stats, attr = self.data, self.data["stats"], self.data["attributes"]
        self.panel(self.canvas, (45, 133, 370, 480))
        pygame.draw.circle(self.canvas, tuple(data["colour"]), (230, 220), 57)
        pygame.draw.circle(self.canvas, WHITE, (230, 220), 61, 3)
        pygame.draw.circle(self.canvas, SKIN, (230, 202), 16)
        self.text(self.canvas, data["position"], (230, 293), 28, GOLD, center=True, bold=True)
        self.text(self.canvas, "Overall " + str(overall(data)), (230, 331), 35, WHITE, center=True, bold=True)
        self.text(self.canvas, "Level " + str(data["level"]) + "  •  " + str(data["xp"]) + "/" + str(data["level"] * 100) + " XP", (230, 372), 20, (185, 218, 233), center=True)
        self.text(self.canvas, "Credits " + str(data["credits"]), (230, 407), 22, GOLD, center=True)
        self.text(self.canvas, "Teammate trust " + str(data["trust"]) + "%", (230, 445), 21, (238, 164, 190), center=True)
        self.text(self.canvas, "Best in the World", (230, 498), 21, WHITE, center=True, bold=True)
        state = "BEST IN THE WORLD!" if overall(data) >= 90 and stats["wins"] >= 10 else ("Need " + str(max(0, 90-overall(data))) + " OVR & " + str(max(0, 10-stats["wins"])) + " wins")
        self.text(self.canvas, state, (230, 529), 18, GOLD, center=True)
        self.panel(self.canvas, (444, 133, 335, 480))
        self.text(self.canvas, "Attributes", (612, 160), 28, GOLD, center=True, bold=True)
        for i, key in enumerate(("pace", "shooting", "passing", "dribbling", "defending", "stamina")):
            y = 207 + i * 58
            self.text(self.canvas, key.title(), (476, y), 21, WHITE)
            pygame.draw.rect(self.canvas, (19, 43, 56), (594, y + 5, 145, 14), border_radius=7)
            pygame.draw.rect(self.canvas, (80, 188, 220), (594, y + 5, int(145 * attr[key] / 99), 14), border_radius=7)
            self.text(self.canvas, attr[key], (756, y), 20, WHITE, center=True)
        self.panel(self.canvas, (807, 133, 428, 480))
        self.text(self.canvas, "Career statistics", (1021, 160), 28, GOLD, center=True, bold=True)
        labels = [
            ("Matches", stats["matches"]), ("Wins / Draws / Losses", str(stats["wins"]) + " / " + str(stats["draws"]) + " / " + str(stats["losses"])),
            ("Goals", stats["goals"]), ("Assists", stats["assists"]), ("Accurate passes", stats["passes"]),
            ("Tackles", stats["tackles"]), ("Player of the Match", stats["potm"]), ("Highest rating", format(stats["highest_rating"], ".1f")),
        ]
        for i, (label, value) in enumerate(labels):
            y = 203 + i * 43
            self.text(self.canvas, label, (840, y), 20, (191, 218, 230))
            self.text(self.canvas, value, (1192, y), 22, WHITE, center=True, bold=True)
        self.add_button((47, 658, 220, 39), "Back Home", "dashboard", small=True)

    def draw_customise(self):
        self.background()
        self.header("Customise Player", "Player colour is always free to change.")
        self.panel(self.canvas, (201, 144, 880, 438))
        self.text(self.canvas, "Select your kit colour", (640, 185), 31, GOLD, center=True, bold=True)
        selected = tuple(self.data["colour"])
        for i, colour in enumerate(PALETTE):
            x = 361 + (i % 4) * 185
            y = 276 + (i // 4) * 120
            pygame.draw.circle(self.canvas, colour, (x, y), 43)
            pygame.draw.circle(self.canvas, WHITE if tuple(colour) == selected else (92, 143, 164), (x, y), 49, 4)
            self.buttons.append(Button((x - 57, y - 57, 114, 114), "", "set_colour:" + str(i), small=True))
        self.text(self.canvas, "This change applies immediately and costs nothing.", (640, 505), 21, (192, 221, 233), center=True)
        self.add_button((492, 538, 296, 43), "Back Home", "dashboard", small=True)

    def draw_tips(self):
        tips = [
            "Hold Shift to sprint, but keep an eye on your stamina. A tired player is slower and cannot strike as hard.",
            "Use Z before you are surrounded. Passing into space is safer than dribbling through a crowd.",
            "Hold C and release it to shoot. A longer charge means a more powerful attempt, but do not wait for defenders.",
            "Press X when a teammate has the ball. Teammate trust makes them much more likely to find you.",
            "Tackle with V only when you are close and facing the ball carrier. Late tackles can give away a free kick.",
            "Marketplace upgrades are permanent. Pace helps recovery runs, while dribbling makes sprinting touches safer.",
        ]
        self.background()
        self.header("Helpful Tips", "A new tip appears every few seconds; use the arrows to browse now.")
        self.panel(self.canvas, (196, 177, 888, 331), (25, 57, 76), (110, 175, 203))
        self.text(self.canvas, "COACH'S NOTE", (640, 218), 25, GOLD, center=True, bold=True)
        self.wrap(self.canvas, tips[self.tip_index], pygame.Rect(290, 274, 700, 120), 29, WHITE, 37, center=True)
        self.text(self.canvas, str(self.tip_index + 1) + " / " + str(len(tips)), (640, 454), 19, (179, 213, 229), center=True)
        self.add_button((250, 535, 175, 47), "‹ Previous", "tip_prev")
        self.add_button((855, 535, 175, 47), "Next ›", "tip_next")
        self.add_button((515, 602, 250, 42), "Back Home", "dashboard", small=True)

    def draw_controls(self):
        self.background()
        self.header("Controls", "Everything you need on matchday.")
        self.panel(self.canvas, (210, 136, 860, 471))
        controls = [
            ("WASD / Arrow keys", "Move your footballer"), ("Hold Shift", "Sprint — drains stamina"),
            ("Z", "Pass while in possession"), ("Hold and release C", "Charge and shoot"),
            ("V", "Tackle an opponent near the ball"), ("X", "Call for a pass from a teammate"),
            ("Escape", "Pause during a match"), ("Mouse", "Select menu buttons"),
        ]
        for i, (key, desc) in enumerate(controls):
            col, row = i % 2, i // 2
            x, y = 255 + col * 395, 190 + row * 87
            self.text(self.canvas, key, (x, y), 24, GOLD, bold=True)
            self.text(self.canvas, desc, (x, y + 30), 20, WHITE)
        self.add_button((525, 635, 230, 42), "Back", "controls_back", small=True)

    def draw_results(self):
        r = self.result
        self.background()
        self.header("Post-match Results", "Match rewards have been saved to your career.")
        colour = GREEN if r["outcome"] == "WIN" else (GOLD if r["outcome"] == "DRAW" else RED)
        self.text(self.canvas, r["outcome"], (640, 137), 35, colour, center=True, bold=True)
        self.text(self.canvas, r["home_name"], (420, 184), 25, (111, 203, 245), center=True)
        self.text(self.canvas, str(r["score"][0]) + " - " + str(r["score"][1]), (640, 168), 47, WHITE, center=True, bold=True)
        self.text(self.canvas, r["away_name"], (860, 184), 25, (246, 145, 150), center=True)
        self.panel(self.canvas, (63, 234, 516, 298))
        self.text(self.canvas, "Your match", (321, 258), 28, GOLD, center=True, bold=True)
        lines = [("Goals", r["goals"]), ("Assists", r["assists"]), ("Accurate passes", r["passes"]), ("Tackles", r["tackles"]), ("Match rating", format(r["rating"], ".1f") + " / 10")]
        for i, (label, value) in enumerate(lines):
            y = 307 + i * 40
            self.text(self.canvas, label, (101, y), 21, (192, 220, 231))
            self.text(self.canvas, value, (522, y), 23, WHITE, center=True, bold=True)
        self.panel(self.canvas, (701, 234, 516, 298))
        self.text(self.canvas, "Rewards & honours", (959, 258), 28, GOLD, center=True, bold=True)
        self.text(self.canvas, "XP gained", (739, 307), 21, (192, 220, 231))
        self.text(self.canvas, "+" + str(r["xp"]), (1160, 307), 23, (128, 222, 150), center=True, bold=True)
        credits_text = ("+" if r["credits"] >= 0 else "") + str(r["credits"])
        self.text(self.canvas, "Credits gained/lost", (739, 347), 21, (192, 220, 231))
        self.text(self.canvas, credits_text, (1160, 347), 23, GOLD if r["credits"] >= 0 else RED, center=True, bold=True)
        self.text(self.canvas, "Objectives", (739, 387), 21, (192, 220, 231))
        self.text(self.canvas, str(r["objectives"]) + " / 2 complete", (1160, 387), 22, WHITE, center=True, bold=True)
        potm = "You" if r["potm"] else r["potm_name"]
        self.text(self.canvas, "Player of the Match", (739, 427), 21, (192, 220, 231))
        self.text(self.canvas, potm, (1160, 427), 22, GOLD if r["potm"] else WHITE, center=True, bold=True)
        self.add_button((486, 588, 308, 52), "Return Home", "return_results", True)

    def draw_levelup(self):
        self.background()
        self.header("Level Up!", "Choose one permanent attribute increase.")
        self.panel(self.canvas, (195, 174, 890, 343), (25, 61, 76), (123, 207, 150))
        self.text(self.canvas, "Level " + str(self.data["level"]) + " reached", (640, 223), 40, GOLD, center=True, bold=True)
        self.text(self.canvas, "Your hard work has earned a new attribute point.", (640, 275), 23, WHITE, center=True)
        choices = [("pace", "+1 Pace", "More speed across the pitch"), ("shooting", "+1 Shooting", "More accurate, stronger shots"), ("dribbling", "+1 Dribbling", "More control under pressure")]
        for i, (key, label, desc) in enumerate(choices):
            x = 235 + i * 285
            self.add_button((x, 338, 240, 54), label, "level:" + key, True)
            self.text(self.canvas, desc, (x + 120, 410), 16, (191, 219, 232), center=True)
        self.text(self.canvas, "Remaining choices: " + str(self.level_choices), (640, 474), 18, (191, 219, 232), center=True)

    def live_rating(self):
        if not self.match:
            return 6.0
        h = self.match.human
        rating = 6.0 + h.match_goals * 1.3 + h.match_assists * .7 + h.match_passes * .055 + h.match_tackles * .24
        rating += sum(1 for obj in self.match.objectives if obj["complete"]) * .2
        rating -= self.match.human_losses * .18 + self.match.human_fouls * .28
        return clamp(rating, 1, 10)

    def complete_match(self, m):
        human = m.human
        rating = self.live_rating()
        if m.score[0] > m.score[1]:
            outcome = "WIN"
            rating += .45
        elif m.score[0] == m.score[1]:
            outcome = "DRAW"
        else:
            outcome = "LOSS"
            rating -= .35
        rating = round(clamp(rating, 1, 10), 1)
        # Sensible POTM comparison against all match participants.
        candidates = []
        for p in m.players:
            passes = p.match_passes
            base_rating = rating if p is human else 6 + p.match_goals * 1.15 + p.match_assists * .55 + p.match_tackles * .12 + random.uniform(-.45, .65)
            score = p.match_goals * 4 + p.match_assists * 2 + passes * .12 + p.match_tackles * .35 + base_rating
            candidates.append((score, p))
        potm_player = max(candidates, key=lambda item: item[0])[1]
        completed = sum(1 for obj in m.objectives if obj["complete"])
        credits = human.match_goals * 12 + human.match_assists * 5 + completed * 8
        if outcome == "WIN":
            credits += 15
        elif outcome == "LOSS":
            credits -= 3
        if potm_player is human:
            credits += 10
        xp = 20 + human.match_goals * 15 + human.match_assists * 10 + completed * 12 + (20 if outcome == "WIN" else 0)
        d, stats = self.data, self.data["stats"]
        stats["matches"] += 1
        stats["goals"] += human.match_goals
        stats["assists"] += human.match_assists
        stats["passes"] += human.match_passes
        stats["tackles"] += human.match_tackles
        stats["highest_rating"] = max(stats["highest_rating"], rating)
        if outcome == "WIN": stats["wins"] += 1
        elif outcome == "DRAW": stats["draws"] += 1
        else: stats["losses"] += 1
        if potm_player is human: stats["potm"] += 1
        d["credits"] = max(0, d["credits"] + credits)
        d["xp"] += xp
        trust_change = human.match_passes * .35 + human.match_assists * 3 + (4 if outcome == "WIN" else (-3 if outcome == "LOSS" else 0)) + (2 if rating >= 7 else 0) - m.human_losses * .45 - m.human_fouls * 2
        d["trust"] = int(clamp(round(d["trust"] + trust_change), 0, 100))
        while d["xp"] >= d["level"] * 100:
            d["xp"] -= d["level"] * 100
            d["level"] += 1
            self.level_choices += 1
        d["latest_result"] = m.home_name + " " + str(m.score[0]) + "–" + str(m.score[1]) + " " + m.away_name + " (" + outcome.title() + ")"
        self.result = {"outcome": outcome, "score": m.score[:], "goals": human.match_goals, "assists": human.match_assists,
                       "passes": human.match_passes, "tackles": human.match_tackles, "rating": rating, "xp": xp, "credits": credits,
                       "objectives": completed, "potm": potm_player is human, "potm_name": potm_player.name,
                       "home_name": m.home_name, "away_name": m.away_name}
        self.save()
        self.screen = "results"

    def buy_upgrade(self, key, tier):
        prices = [25, 60, 120]
        current = self.data["upgrades"].get(key, 0)
        if tier != current + 1 or tier < 1 or tier > 3:
            return
        price = prices[tier - 1]
        if self.data["credits"] < price:
            return
        self.data["credits"] -= price
        self.data["upgrades"][key] = tier
        self.save()

    def buy_cosmetic(self, key):
        prices = {"trail": 40, "badge": 25, "celebration": 55, "azure_ball": 30, "gold_ball": 50}
        if key not in prices or self.data["cosmetics"].get(key) or self.data["credits"] < prices[key]:
            return
        self.data["credits"] -= prices[key]
        self.data["cosmetics"][key] = True
        self.save()

    def handle_action(self, action):
        if not action:
            return
        if action == "quit":
            self.running = False
        elif action == "new_career": self.screen = "new_career"
        elif action == "continue" and self.data.get("career"): self.screen = "dashboard"
        elif action == "welcome": self.screen = "welcome"
        elif action == "begin":
            self.data = default_save(self.new_position, self.new_colour)
            self.data["career"] = True
            self.save()
            self.screen = "dashboard"
        elif action.startswith("position:"): self.new_position = action.split(":", 1)[1]
        elif action.startswith("colour:"): self.new_colour = PALETTE[int(action.split(":")[1])]
        elif action == "prematch": self.set_prematch()
        elif action.startswith("difficulty:"): self.difficulty = action.split(":", 1)[1]
        elif action == "start_match":
            self.match = Match(self, self.difficulty, self.home_style, self.away_style, self.prematch_objectives)
            self.screen = "match"
        elif action == "market": self.screen = "market"
        elif action == "profile": self.screen = "profile"
        elif action == "customise": self.screen = "customise"
        elif action == "tips": self.screen = "tips"
        elif action == "dashboard": self.screen = "dashboard"
        elif action == "save_welcome":
            self.save(); self.screen = "welcome"
        elif action == "controls_welcome": self.return_screen = "welcome"; self.screen = "controls"
        elif action == "controls_pause": self.return_screen = "pause"; self.screen = "controls"
        elif action == "controls_back": self.screen = self.return_screen
        elif action == "tip_prev": self.tip_index = (self.tip_index - 1) % 6; self.tip_timer = 0
        elif action == "tip_next": self.tip_index = (self.tip_index + 1) % 6; self.tip_timer = 0
        elif action == "resume": self.screen = "match"
        elif action == "confirm_restart": self.match.confirm = "restart"
        elif action == "confirm_quit": self.match.confirm = "quit"
        elif action == "cancel_confirm": self.match.confirm = None
        elif action == "do_restart":
            # Existing match state is discarded; no save/reward code runs.
            self.match = Match(self, self.difficulty, self.home_style, self.away_style, random.sample(list(OBJECTIVE_INFO), 2))
            self.screen = "match"
        elif action == "do_quit":
            self.match = None
            self.screen = "dashboard"
        elif action == "return_results":
            if self.level_choices > 0: self.screen = "levelup"
            else: self.screen = "dashboard"
        elif action.startswith("level:"):
            key = action.split(":", 1)[1]
            self.data["attributes"][key] = min(99, self.data["attributes"][key] + 1)
            self.level_choices = max(0, self.level_choices - 1)
            self.save()
            self.screen = "levelup" if self.level_choices else "dashboard"
        elif action.startswith("buy_upgrade:"):
            _, key, tier = action.split(":")
            self.buy_upgrade(key, int(tier))
        elif action.startswith("buy_cosmetic:"):
            self.buy_cosmetic(action.split(":", 1)[1])
        elif action.startswith("set_colour:"):
            self.data["colour"] = list(PALETTE[int(action.split(":")[1])])
            self.save()

    def draw(self):
        self.buttons = []
        if self.screen == "welcome": self.draw_welcome()
        elif self.screen == "new_career": self.draw_new_career()
        elif self.screen == "dashboard": self.draw_dashboard()
        elif self.screen == "prematch": self.draw_prematch()
        elif self.screen in ("match", "pause"): self.draw_match()
        elif self.screen == "market": self.draw_market()
        elif self.screen == "profile": self.draw_profile()
        elif self.screen == "customise": self.draw_customise()
        elif self.screen == "tips": self.draw_tips()
        elif self.screen == "controls": self.draw_controls()
        elif self.screen == "results": self.draw_results()
        elif self.screen == "levelup": self.draw_levelup()
        else: self.screen = "welcome"; self.draw_welcome()
        size = self.window.get_size()
        if size == LOGICAL_SIZE:
            self.window.blit(self.canvas, (0, 0))
        else:
            self.window.blit(pygame.transform.smoothscale(self.canvas, size), (0, 0))
        pygame.display.flip()

    def logical_mouse(self, position):
        width, height = self.window.get_size()
        return (int(position[0] * LOGICAL_SIZE[0] / max(1, width)), int(position[1] * LOGICAL_SIZE[1] / max(1, height)))

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, .05)
            self.mouse_pos = self.logical_mouse(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.window = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    point = self.logical_mouse(event.pos)
                    for button in reversed(self.buttons):
                        if button.enabled and button.rect.collidepoint(point):
                            self.handle_action(button.action)
                            break
                elif event.type == pygame.KEYDOWN:
                    if self.screen == "match":
                        if event.key == pygame.K_ESCAPE:
                            self.screen = "pause"
                        elif self.match:
                            self.match.handle_keydown(event.key)
                    elif self.screen == "pause" and event.key == pygame.K_ESCAPE and not self.match.confirm:
                        self.screen = "match"
                    elif self.screen == "controls" and event.key == pygame.K_ESCAPE:
                        self.screen = self.return_screen
                elif event.type == pygame.KEYUP and self.screen == "match" and self.match:
                    self.match.handle_keyup(event.key)
            keys = pygame.key.get_pressed()
            if self.screen == "match" and self.match:
                if self.match.charging:
                    self.match.charge = min(1, self.match.charge + dt * .72)
                self.match.update(dt, keys)
            elif self.screen == "tips":
                self.tip_timer += dt
                if self.tip_timer > 5:
                    self.tip_index = (self.tip_index + 1) % 6
                    self.tip_timer = 0
            self.draw()
        pygame.quit()


if __name__ == "__main__":
    try:
        Game().run()
    except pygame.error as error:
        print("Pygame could not start:", error)
        sys.exit(1)
