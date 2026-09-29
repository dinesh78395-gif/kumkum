import os
import math
from PIL import Image, ImageDraw, ImageFont

os.makedirs('images', exist_ok=True)

# Helper function to draw subtle grid / dot screentone
def draw_screentone(draw, box, color, spacing=16, radius=1):
    x1, y1, x2, y2 = box
    for y in range(int(y1), int(y2), spacing):
        for x in range(int(x1), int(x2), spacing):
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)

# Helper function to draw a heart
def draw_heart(draw, cx, cy, size, fill_color, outline_color=None, width=1):
    points = []
    for deg in range(0, 360, 5):
        t = math.radians(deg)
        # Heart formula
        x = 16 * (math.sin(t) ** 3)
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        points.append((cx + x * size / 16, cy + y * size / 16))
    draw.polygon(points, fill=fill_color, outline=outline_color)

# Helper function to draw a star
def draw_star(draw, cx, cy, r_outer, r_inner, fill_color):
    points = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        angle = i * math.pi / 5 - math.pi / 2
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill_color)

# Helper function to draw washi tape
def draw_washi_tape(draw, x, y, w, h, color, angle=0):
    tape = Image.new('RGBA', (w, h), color)
    t_draw = ImageDraw.Draw(tape)
    # Ripped edges
    for i in range(0, h, 6):
        t_draw.line([(0, i), (3, i + 3)], fill=(255, 255, 255, 100), width=1)
        t_draw.line([(w - 1, i), (w - 4, i + 3)], fill=(255, 255, 255, 100), width=1)
    rotated = tape.rotate(angle, expand=True, resample=Image.BICUBIC)
    return rotated

panels = [
    {
        'file': 'miss-me.jpg',
        'title': 'When You Miss Me',
        'subtitle': 'CHAPTER 10 • PANEL 1',
        'bg_top': (255, 242, 246),
        'bg_bot': (252, 230, 238),
        'accent': (229, 115, 115),
        'accent_soft': (248, 187, 208),
        'dark_text': (74, 50, 56),
        'quote': '"Distance means so little\nwhen someone means so much."',
        'subquote': 'Close your eyes. Hear my voice. I am already right beside you. ♡',
        'icon_type': 'miss_me'
    },
    {
        'file': 'sad.jpg',
        'title': "When You're Sad",
        'subtitle': 'CHAPTER 10 • PANEL 2',
        'bg_top': (240, 247, 255),
        'bg_bot': (222, 237, 254),
        'accent': (100, 181, 246),
        'accent_soft': (187, 222, 251),
        'dark_text': (44, 62, 80),
        'quote': '"Even on the rainiest days,\nyou are never holding the umbrella alone."',
        'subquote': "It's okay to feel fragile today. Let me wrap you in my warmth. ♡",
        'icon_type': 'sad'
    },
    {
        'file': 'mad.jpg',
        'title': "When You're Mad At Me",
        'subtitle': 'CHAPTER 10 • PANEL 3',
        'bg_top': (255, 248, 240),
        'bg_bot': (254, 237, 218),
        'accent': (255, 183, 77),
        'accent_soft': (255, 224, 178),
        'dark_text': (80, 58, 42),
        'quote': '"I am so sorry, my love.\nYou matter more to me than being right."',
        'subquote': 'Here is a peace flower, your favorite sweet treat, and endless hugs. ♡',
        'icon_type': 'mad'
    },
    {
        'file': 'cant-sleep.jpg',
        'title': "When You Can't Sleep",
        'subtitle': 'CHAPTER 10 • PANEL 4',
        'bg_top': (246, 242, 254),
        'bg_bot': (233, 224, 251),
        'accent': (149, 117, 205),
        'accent_soft': (209, 196, 233),
        'dark_text': (58, 48, 76),
        'quote': '"Leave the worries of today behind.\nThe stars are keeping watch for us."',
        'subquote': 'Rest your head, breathe softly. I will meet you in our dreams tonight. ♡',
        'icon_type': 'cant_sleep'
    },
    {
        'file': 'hug.jpg',
        'title': 'When You Need A Hug',
        'subtitle': 'CHAPTER 10 • PANEL 5',
        'bg_top': (243, 250, 244),
        'bg_bot': (225, 243, 228),
        'accent': (129, 199, 132),
        'accent_soft': (200, 230, 201),
        'dark_text': (46, 70, 50),
        'quote': '"Tightly, gently, and for as long\nas your heart needs to rest."',
        'subquote': 'Consider yourself wrapped in the warmest, softest embrace right now. ♡',
        'icon_type': 'hug'
    },
    {
        'file': 'birthday.jpg',
        'title': 'On Your Birthday',
        'subtitle': 'CHAPTER 10 • PANEL 6',
        'bg_top': (255, 250, 240),
        'bg_bot': (254, 240, 220),
        'accent': (240, 98, 146),
        'accent_soft': (255, 236, 179),
        'dark_text': (74, 46, 58),
        'quote': '"The world became brighter, sweeter,\nand infinitely more magical the day you were born."',
        'subquote': 'Happy Birthday to my favorite girl. Today and forever, I celebrate you. ♡',
        'icon_type': 'birthday'
    },
]

# Load fonts safely
font_title = ImageFont.truetype('C:/Windows/Fonts/segoescb.ttf', 38)
font_sub = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 16)
font_quote = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 24)
font_subquote = ImageFont.truetype('C:/Windows/Fonts/segoepr.ttf', 17)
font_badge = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 13)
font_dialogue = ImageFont.truetype('C:/Windows/Fonts/segoepr.ttf', 20)

for p in panels:
    W, H = 800, 1060
    img = Image.new('RGBA', (W, H), (253, 250, 245, 255))
    draw = ImageDraw.Draw(img)

    # Vertical gradient wash in panel area
    panel_box = [60, 60, W - 60, H - 60]
    px1, py1, px2, py2 = panel_box
    for y in range(int(py1), int(py2)):
        ratio = (y - py1) / (py2 - py1)
        r = int(p['bg_top'][0] * (1 - ratio) + p['bg_bot'][0] * ratio)
        g = int(p['bg_top'][1] * (1 - ratio) + p['bg_bot'][1] * ratio)
        b = int(p['bg_top'][2] * (1 - ratio) + p['bg_bot'][2] * ratio)
        draw.line([(px1, y), (px2, y)], fill=(r, g, b, 255))

    # Manga Screentone Dots inside panel
    draw_screentone(draw, (px1 + 10, py1 + 10, px2 - 10, py2 - 10), (p['accent'][0], p['accent'][1], p['accent'][2], 30), spacing=18, radius=1.5)

    # Double manga border
    draw.rectangle(panel_box, outline=p['accent'], width=3)
    draw.rectangle([px1 + 8, py1 + 8, px2 - 8, py2 - 8], outline=(255, 255, 255, 200), width=1)
    draw.rectangle([px1 + 12, py1 + 12, px2 - 12, py2 - 12], outline=p['accent_soft'], width=1)

    # Top Chapter Badge / Postmark
    draw.rectangle([px1 + 25, py1 + 25, px1 + 200, py1 + 65], fill=(255, 255, 255, 220), outline=p['accent'], width=1)
    draw.text((px1 + 35, py1 + 34), p['subtitle'], fill=p['accent'], font=font_badge)

    # Postmark circle in top right corner
    pm_cx, pm_cy = px2 - 60, py1 + 60
    draw.ellipse([pm_cx - 32, pm_cy - 32, pm_cx + 32, pm_cy + 32], outline=p['accent'], width=2)
    draw.ellipse([pm_cx - 26, pm_cy - 26, pm_cx + 26, pm_cy + 26], outline=p['accent_soft'], width=1)
    draw_heart(draw, pm_cx, pm_cy + 2, 0.8, p['accent'])

    # Title
    t_bbox = font_title.getbbox(p['title'])
    t_w = t_bbox[2] - t_bbox[0]
    draw.text(((W - t_w) // 2, py1 + 95), p['title'], fill=p['dark_text'], font=font_title)

    # Delicate divider line
    div_y = py1 + 165
    draw.line([(W // 2 - 120, div_y), (W // 2 + 120, div_y)], fill=p['accent'], width=2)
    draw_heart(draw, W // 2, div_y, 0.9, p['accent'])

    # Central Romantic Manga Illustration Illustration Box
    m_box = [px1 + 45, div_y + 35, px2 - 45, div_y + 445]
    mx1, my1, mx2, my2 = m_box
    draw.rectangle(m_box, fill=(255, 255, 255, 240), outline=p['accent_soft'], width=2)
    draw.rectangle([mx1 + 6, my1 + 6, mx2 - 6, my2 - 6], outline=(245, 240, 235), width=1)

    # Manga Artwork inside central frame
    mc_x, mc_y = (mx1 + mx2) // 2, (my1 + my2) // 2

    # Draw specific romantic illustration per mood
    if p['icon_type'] == 'miss_me':
        # Couple silhouettes under cherry blossoms & starry sky
        for angle in range(0, 360, 24):
            bx = mc_x + int(140 * math.cos(math.radians(angle)))
            by = mc_y - 20 + int(90 * math.sin(math.radians(angle)))
            draw_heart(draw, bx, by, 0.6, (255, 192, 203, 180))
        # Warm glowing circle
        draw.ellipse([mc_x - 90, mc_y - 110, mc_x + 90, mc_y + 70], fill=(255, 245, 248), outline=p['accent_soft'], width=2)
        # Tender couple silhouettes
        # Girl head
        draw.ellipse([mc_x - 38, mc_y - 50, mc_x - 6, mc_y - 18], fill=p['dark_text'])
        draw.polygon([(mc_x - 45, mc_y - 18), (mc_x + 2, mc_y - 18), (mc_x - 22, mc_y + 45)], fill=p['dark_text'])
        # Boy head
        draw.ellipse([mc_x + 4, mc_y - 58, mc_x + 38, mc_y - 24], fill=p['dark_text'])
        draw.polygon([(mc_x - 4, mc_y - 24), (mc_x + 48, mc_y - 24), (mc_x + 20, mc_y + 45)], fill=p['dark_text'])
        # Little floating hearts
        draw_heart(draw, mc_x, mc_y - 75, 1.4, p['accent'])
        draw_heart(draw, mc_x - 70, mc_y - 40, 0.7, p['accent'])
        draw_heart(draw, mc_x + 70, mc_y - 40, 0.7, p['accent'])
        # Manga dialogue bubble
        db_x, db_y = mc_x, my2 - 45
        draw.rectangle([db_x - 140, db_y - 22, db_x + 140, db_y + 22], fill=(255, 255, 255), outline=p['accent'], width=2)
        draw.text((db_x - 115, db_y - 14), "Always in my heart... ♡", fill=p['dark_text'], font=font_dialogue)

    elif p['icon_type'] == 'sad':
        # Gentle comforting umbrella + warm tea cup with heart steam
        # Umbrella dome
        ux, uy = mc_x, mc_y - 30
        draw.chord([ux - 110, uy - 90, ux + 110, uy + 40], 180, 360, fill=(235, 245, 255), outline=p['accent'], width=3)
        draw.line([(ux, uy - 90), (ux, uy + 65)], fill=p['accent'], width=3)
        draw.arc([ux - 20, uy + 50, ux, uy + 80], 0, 180, fill=p['accent'], width=3)
        # Gentle raindrops outside umbrella
        for rx, ry in [(-130, -50), (-140, 10), (-120, 60), (130, -40), (140, 20), (120, 70)]:
            draw.line([(ux + rx, uy + ry), (ux + rx - 5, uy + ry + 18)], fill=p['accent_soft'], width=2)
        # Heart steam underneath
        draw_heart(draw, ux, uy + 20, 1.5, p['accent'])
        # Dialogue bubble
        db_x, db_y = mc_x, my2 - 45
        draw.rectangle([db_x - 130, db_y - 22, db_x + 130, db_y + 22], fill=(255, 255, 255), outline=p['accent'], width=2)
        draw.text((db_x - 105, db_y - 14), "I've got you sheltered ♡", fill=p['dark_text'], font=font_dialogue)

    elif p['icon_type'] == 'mad':
        # Peace offering rose & cute contrite folded hands
        # Sunburst warmth
        draw.ellipse([mc_x - 85, mc_y - 85, mc_x + 85, mc_y + 85], fill=(255, 249, 235), outline=p['accent_soft'], width=2)
        # Cute rose
        draw_heart(draw, mc_x, mc_y - 30, 2.0, p['accent'])
        draw_heart(draw, mc_x, mc_y - 45, 1.2, (255, 138, 101))
        # Rose stem and leaves
        draw.line([(mc_x, mc_y - 10), (mc_x, mc_y + 55)], fill=(129, 199, 132), width=4)
        draw.chord([mc_x - 25, mc_y + 10, mc_x, mc_y + 30], 90, 270, fill=(165, 214, 167))
        draw.chord([mc_x, mc_y + 25, mc_x + 25, mc_y + 45], 270, 90, fill=(165, 214, 167))
        # Dialogue bubble
        db_x, db_y = mc_x, my2 - 45
        draw.rectangle([db_x - 150, db_y - 22, db_x + 150, db_y + 22], fill=(255, 255, 255), outline=p['accent'], width=2)
        draw.text((db_x - 135, db_y - 14), "Forgive me? Ice cream on me ♡", fill=p['dark_text'], font=font_dialogue)

    elif p['icon_type'] == 'cant_sleep':
        # Crescent moon & twinkling stars
        draw.ellipse([mc_x - 80, mc_y - 80, mc_x + 60, mc_y + 60], fill=(245, 240, 255), outline=p['accent_soft'], width=2)
        # Crescent Moon
        draw.ellipse([mc_x - 45, mc_y - 65, mc_x + 35, mc_y + 25], fill=(255, 236, 179))
        draw.ellipse([mc_x - 30, mc_y - 75, mc_x + 45, mc_y + 15], fill=(245, 240, 255))
        # Stars
        draw_star(draw, mc_x + 55, mc_y - 45, 16, 7, (255, 213, 79))
        draw_star(draw, mc_x - 65, mc_y - 20, 12, 5, p['accent'])
        draw_star(draw, mc_x + 35, mc_y + 35, 14, 6, p['accent_soft'])
        draw_heart(draw, mc_x - 5, mc_y + 15, 1.2, p['accent'])
        # Dialogue bubble
        db_x, db_y = mc_x, my2 - 45
        draw.rectangle([db_x - 140, db_y - 22, db_x + 140, db_y + 22], fill=(255, 255, 255), outline=p['accent'], width=2)
        draw.text((db_x - 120, db_y - 14), "Sweetest dreams, my girl ♡", fill=p['dark_text'], font=font_dialogue)

    elif p['icon_type'] == 'hug':
        # Big warm hug emblem & radiating warmth
        draw.ellipse([mc_x - 95, mc_y - 80, mc_x + 95, mc_y + 80], fill=(240, 252, 242), outline=p['accent_soft'], width=2)
        # Hug arms curve
        draw.arc([mc_x - 80, mc_y - 60, mc_x + 80, mc_y + 60], 30, 150, fill=p['accent'], width=6)
        draw.arc([mc_x - 80, mc_y - 60, mc_x + 80, mc_y + 60], 210, 330, fill=p['accent'], width=6)
        # Giant heart center
        draw_heart(draw, mc_x, mc_y - 5, 2.2, p['accent'])
        draw_heart(draw, mc_x, mc_y - 5, 1.3, (255, 255, 255))
        draw_heart(draw, mc_x, mc_y - 5, 0.7, p['accent'])
        # Dialogue bubble
        db_x, db_y = mc_x, my2 - 45
        draw.rectangle([db_x - 135, db_y - 22, db_x + 135, db_y + 22], fill=(255, 255, 255), outline=p['accent'], width=2)
        draw.text((db_x - 110, db_y - 14), "Holding you extra tight ♡", fill=p['dark_text'], font=font_dialogue)

    elif p['icon_type'] == 'birthday':
        # Cute birthday cake with single glowing candle
        draw.ellipse([mc_x - 90, mc_y - 80, mc_x + 90, mc_y + 80], fill=(255, 248, 240), outline=p['accent_soft'], width=2)
        # Cake base
        draw.rectangle([mc_x - 65, mc_y + 5, mc_x + 65, mc_y + 55], fill=(255, 230, 235), outline=p['accent'], width=2)
        # Cake top layer
        draw.rectangle([mc_x - 45, mc_y - 30, mc_x + 45, mc_y + 5], fill=(255, 245, 240), outline=p['accent'], width=2)
        # Candle
        draw.rectangle([mc_x - 4, mc_y - 55, mc_x + 4, mc_y - 30], fill=p['accent'], outline=p['accent'])
        # Flame
        draw_heart(draw, mc_x, mc_y - 65, 0.9, (255, 183, 77))
        # Confetti / sparkles
        draw_star(draw, mc_x - 65, mc_y - 45, 12, 5, p['accent'])
        draw_star(draw, mc_x + 65, mc_y - 45, 12, 5, (255, 183, 77))
        draw_heart(draw, mc_x - 70, mc_y + 25, 0.7, p['accent'])
        draw_heart(draw, mc_x + 70, mc_y + 25, 0.7, p['accent'])
        # Dialogue bubble
        db_x, db_y = mc_x, my2 - 45
        draw.rectangle([db_x - 150, db_y - 22, db_x + 150, db_y + 22], fill=(255, 255, 255), outline=p['accent'], width=2)
        draw.text((db_x - 130, db_y - 14), "Make a wish, my princess ♡", fill=p['dark_text'], font=font_dialogue)

    # Bottom Quote Section
    quote_y = div_y + 475
    for line in p['quote'].split('\n'):
        q_bbox = font_quote.getbbox(line)
        q_w = q_bbox[2] - q_bbox[0]
        draw.text(((W - q_w) // 2, quote_y), line, fill=p['dark_text'], font=font_quote)
        quote_y += 34

    # Subquote / handwritten note
    quote_y += 18
    sq_bbox = font_subquote.getbbox(p['subquote'])
    sq_w = sq_bbox[2] - sq_bbox[0]
    draw.text(((W - sq_w) // 2, quote_y), p['subquote'], fill=p['accent'], font=font_subquote)

    # Bottom footer tag
    foot_text = "HANDMADE MANGA • CHAPTER 10 • WITH ALL MY LOVE"
    f_bbox = font_badge.getbbox(foot_text)
    f_w = f_bbox[2] - f_bbox[0]
    draw.text(((W - f_w) // 2, py2 - 35), foot_text, fill=(160, 140, 135), font=font_badge)

    # Convert to RGB and save as JPG
    final_rgb = Image.new('RGB', (W, H), (253, 250, 245))
    final_rgb.paste(img, (0, 0), img)
    out_path = os.path.join('images', p['file'])
    final_rgb.save(out_path, 'JPEG', quality=95)
    print(f"Generated {out_path}")

print("All panels created successfully!")
