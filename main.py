import os
import struct
import zlib

W = 1024
H = 1024
BG = (11, 18, 32)
PANEL = (22, 33, 54)
PANEL2 = (17, 27, 46)
INK = (236, 241, 248)
DIM = (158, 174, 196)
GOLD = (250, 201, 40)
RED = (235, 87, 87)
GREEN = (74, 200, 120)
BLUE = (96, 165, 250)
ORANGE = (245, 158, 11)
TEAL = (45, 212, 191)
PURPLE = (192, 132, 252)
MAPDOT = (74, 116, 168)
WHITE = (255, 255, 255)

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
}


class Canvas:
    def __init__(self):
        self.buf = bytearray(BG * W * H)

    def set_px(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.buf[i] = c[0]
            self.buf[i + 1] = c[1]
            self.buf[i + 2] = c[2]

    def fill_rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set_px(xx, yy, c)

    def hline(self, x0, x1, y, c, t=1):
        for yy in range(y, y + t):
            for xx in range(x0, x1 + 1):
                self.set_px(xx, yy, c)

    def vline(self, x, y0, y1, c, t=1):
        for xx in range(x, x + t):
            for yy in range(y0, y1 + 1):
                self.set_px(xx, yy, c)

    def line(self, x0, y0, x1, y1, c):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.set_px(x, y, c)
            self.set_px(x + 1, y, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                    self.set_px(xx, yy, c)

    def ring(self, cx, cy, r, c, t=2):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if (r - t) * (r - t) <= d <= r * r:
                    self.set_px(xx, yy, c)

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def draw_text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            g = FONT.get(ch.upper(), FONT[" "])
            for ry, row in enumerate(g):
                for rx, bit in enumerate(row):
                    if bit == "1":
                        self.fill_rect(cx + rx * scale, y + ry * scale, scale, scale, c)
            cx += 6 * scale

    def center_text(self, y, s, scale, c):
        self.draw_text((W - self.text_w(s, scale)) // 2, y, s, scale, c)

MAP = {
    0: ((2, 6), (10, 16), (20, 22), (38, 62)),
    1: ((2, 7), (10, 17), (20, 22), (37, 62)),
    2: ((3, 8), (11, 17), (20, 21), (34, 36), (38, 62)),
    3: ((4, 9), (12, 16), (33, 36), (38, 61)),
    4: ((5, 11), (13, 16), (31, 31), (32, 36), (38, 60)),
    5: ((6, 14), (31, 32), (33, 38), (40, 59)),
    6: ((7, 15), (31, 38), (41, 57), (58, 59)),
    7: ((7, 16), (31, 33), (35, 38), (38, 42), (44, 56), (58, 59)),
    8: ((8, 15), (31, 32), (36, 38), (38, 42), (45, 55), (58, 58)),
    9: ((8, 13), (32, 40), (38, 42), (45, 50)),
    10: ((9, 12), (32, 40), (39, 42), (44, 47), (49, 51)),
    11: ((10, 12), (32, 40), (40, 42), (44, 46), (49, 51)),
    12: ((11, 13), (33, 40), (44, 46), (49, 51)),
    13: ((12, 13), (16, 18), (33, 40), (49, 52)),
    14: ((16, 19), (34, 39), (49, 53)),
    15: ((16, 20), (34, 38), (50, 55)),
    16: ((17, 21), (35, 38), (51, 55)),
    17: ((17, 21), (35, 38), (52, 55)),
    18: ((18, 21), (35, 37), (53, 58)),
    19: ((18, 21), (35, 37), (53, 59)),
    20: ((18, 20), (35, 36), (53, 59)),
    21: ((18, 20), (35, 36), (54, 58)),
    22: ((18, 19), (35, 36), (54, 57)),
    23: ((18, 19), (60, 61)),
    24: ((18, 18), (60, 61)),
    25: ((18, 18),),
}

PINS = (
    (50.45, 30.52, "1", RED),
    (26.20, 50.60, "2", ORANGE),
    (36.90, 30.70, "3", TEAL),
    (50.85, 4.35, "4", BLUE),
    (4.80, 6.00, "5", PURPLE),
    (40.70, -74.00, "6", GOLD),
)


def map_xy(lat, lon):
    x = int(8 + (lon + 180.0) / 360.0 * 1008.0)
    y = int(104 + (75.0 - lat) / 5.0 * 9.0)
    return x, y


def draw_map(cv):
    for row, segs in MAP.items():
        y = 104 + row * 9
        for a, b in segs:
            for col in range(a, b + 1):
                x = 8 + int(col * 15.75) + 7
                cv.disc(x, y + 4, 3, MAPDOT)
    for lat, lon, num, col in PINS:
        x, y = map_xy(lat, lon)
        cv.disc(x, y, 12, col)
        cv.ring(x, y, 12, WHITE, 2)
        cv.draw_text(x - 5, y - 7, num, 2, WHITE)


def draw_header(cv):
    cv.center_text(16, "SUNDAY, 22 NOVEMBER 2026", 4, INK)
    cv.center_text(60, "THE WORLD IN ONE IMAGE", 2, GOLD)
    cv.hline(8, 1015, 92, GOLD, 3)


STORIES = (
    ("1 UKRAINE | CONFLICT", RED,
     ("Russia fires 186 drones in one",
      "night; Ukraine downs 161"),
     ("Strikes hit 18 sites; Ukrainian",
      "drones set Russian ship ablaze")),
    ("2 BAHRAIN | MIDDLE EAST", ORANGE,
     ("Iran strikes US bases and a",
      "civilian plant in Bahrain"),
     ("IRGC missile-drone attack; 2 hurt,",
      "air defences down more strikes")),
    ("3 ANTALYA | CLIMATE", TEAL,
     ("COP31 final draft drops the words",
      "'fossil fuels' entirely"),
     ("First admission: 1.5C will be",
      "overshot; talks 40 hrs overtime")),
    ("4 BRUSSELS | TRADE", BLUE,
     ("EU and Indonesia sign trade deal",
      "after 10 years of talks"),
     ("Tariffs gone on 98% of goods;",
      "EU exports seen up 40% in 15 yrs")),
    ("5 NIGERIA | DISASTER", PURPLE,
     ("Funeral boat capsizes in Nigeria:",
      "24 dead, 24 rescued"),
     ("Crowded boat failed in Bayelsa;",
      "search goes on for the missing")),
    ("6 NEW YORK | CULTURE", GOLD,
     ("GTA VI: $3.79bn in one day, the",
      "biggest launch in entertainment"),
     ("32.5m pre-orders; Metacritic 99;",
      "beats every film opening ever")),
)


def draw_card(cv, x, y, tag, accent, head, facts):
    cv.fill_rect(x, y, 500, 160, PANEL)
    cv.fill_rect(x, y, 6, 160, accent)
    cv.draw_text(x + 20, y + 14, tag, 2, accent)
    yy = y + 42
    for ln in head:
        cv.draw_text(x + 20, yy, ln, 2, INK)
        yy += 20
    yy += 6
    for ln in facts:
        cv.draw_text(x + 20, yy, ln, 2, DIM)
        yy += 20
    cv.hline(x + 20, x + 479, y + 146, (38, 55, 88), 2)


def draw_markets(cv, x, y):
    cv.fill_rect(x, y, 500, 152, PANEL2)
    cv.fill_rect(x, y, 6, 152, RED)
    cv.draw_text(x + 20, y + 12, "MARKETS | THE AI SELL-OFF", 2, RED)
    rows = (("S&P 500", -3.70), ("NIKKEI", -5.06), ("FTSE 100", -1.02), ("BRENT", 0.57))
    zero = x + 300
    yy = y + 44
    for name, val in rows:
        cv.draw_text(x + 20, yy, name, 2, INK)
        bw = int(abs(val) / 5.5 * 130)
        if val < 0:
            cv.fill_rect(zero - bw, yy + 2, bw, 10, RED)
            cv.draw_text(zero + 10, yy, ("%.2f%%" % val), 2, RED)
        else:
            cv.fill_rect(zero, yy + 2, bw, 10, GREEN)
            cv.draw_text(zero + bw + 10, yy, ("+%.2f%%" % val), 2, GREEN)
        yy += 26
    cv.vline(zero, y + 40, y + 138, DIM, 2)


def draw_good(cv, x, y):
    cv.fill_rect(x, y, 500, 152, PANEL2)
    cv.fill_rect(x, y, 6, 152, GREEN)
    cv.draw_text(x + 20, y + 12, "BRIGHTER NEWS", 2, GREEN)
    lines = ("Lewis Pugh swims 15 km through the",
             "Strait of Hormuz in 3 days, past",
             "burning tankers, to warn of war's",
             "toll on dolphins and coral reefs.")
    yy = y + 44
    for ln in lines:
        cv.draw_text(x + 20, yy, ln, 2, INK)
        yy += 20
    cv.hline(x + 20, x + 479, y + 138, (38, 55, 88), 2)


def build():
    cv = Canvas()
    draw_header(cv)
    draw_map(cv)
    xs = (8, 516)
    ys = (344, 512, 680)
    for i, st in enumerate(STORIES):
        draw_card(cv, xs[i % 2], ys[i // 2], st[0], st[1], st[2], st[3])
    draw_markets(cv, 8, 848)
    draw_good(cv, 516, 848)
    cv.center_text(1008, "SOURCES: AP | REUTERS | AFP | CNN | TAKE-TWO | NEMA | UNFCCC", 1, DIM)
    return cv


def chunk(tag, data):
    c = tag + data
    return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)


def png_bytes(cv):
    raw = b""
    for y in range(H):
        raw += b"\x00" + bytes(cv.buf[y * W * 3:(y + 1) * W * 3])
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", ihdr)
    out += chunk(b"IDAT", zlib.compress(raw, 9))
    out += chunk(b"IEND", b"")
    return out


def main():
    cv = build()
    data = png_bytes(cv)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
