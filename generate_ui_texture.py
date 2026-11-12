import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2048, 1280
img = Image.new("RGBA", (W, H), (10, 10, 10, 255))
draw = ImageDraw.Draw(img)

font_path = "/home/akidin/.local/share/fonts/Outfit-Bold.ttf"
try:
    font_xl = ImageFont.truetype(font_path, 38)
    font_lg = ImageFont.truetype(font_path, 28)
    font_md = ImageFont.truetype(font_path, 22)
    font_sm = ImageFont.truetype(font_path, 18)
    font_xs = ImageFont.truetype(font_path, 14)
except Exception:
    font_xl = font_lg = font_md = font_sm = font_xs = ImageFont.load_default()

RAIL_W = 100
draw.rectangle([(0, 0), (RAIL_W, H)], fill=(15, 15, 15, 255))
draw.line([(RAIL_W, 0), (RAIL_W, H)], fill=(38, 38, 38, 255), width=2)

draw.rounded_rectangle([(20, 24), (80, 84)], radius=18, fill=(24, 24, 24, 255), outline=(60, 60, 60, 255), width=2)
pts = [(32, 54), (40, 54), (46, 36), (54, 72), (60, 54), (68, 54)]
draw.line(pts, fill=(255, 255, 255, 255), width=3)

draw.line([(30, 104), (70, 104)], fill=(45, 45, 45, 255), width=2)

server_colors = [(35, 35, 40), (28, 32, 28), (40, 30, 32), (30, 35, 42)]
for idx, col in enumerate(server_colors):
    y = 124 + idx * 76
    draw.ellipse([(24, y), (76, y + 52)], fill=col, outline=(55, 55, 60, 255), width=2)
    initials = ["G", "D", "P", "S"][idx]
    draw.text((43, y + 14), initials, fill=(220, 220, 220, 255), font=font_md)

SIDE_W = 340
draw.rectangle([(RAIL_W, 0), (RAIL_W + SIDE_W, H)], fill=(18, 18, 18, 255))
draw.line([(RAIL_W + SIDE_W, 0), (RAIL_W + SIDE_W, H)], fill=(38, 38, 38, 255), width=2)

draw.text((RAIL_W + 28, 32), "Pulse", fill=(245, 245, 245, 255), font=font_lg)
draw.text((RAIL_W + 28, 70), "CHANNELS", fill=(115, 115, 115, 255), font=font_xs)

channels = ["welcome", "announcements", "general", "dev-logs"]
for idx, ch in enumerate(channels):
    y = 104 + idx * 48
    if ch == "general":
        draw.rounded_rectangle([(RAIL_W + 16, y), (RAIL_W + SIDE_W - 16, y + 40)], radius=8, fill=(35, 35, 35, 255))
        draw.text((RAIL_W + 30, y + 8), f"#  {ch}", fill=(255, 255, 255, 255), font=font_md)
    else:
        draw.text((RAIL_W + 30, y + 8), f"#  {ch}", fill=(160, 160, 160, 255), font=font_md)

USER_Y = H - 90
draw.rectangle([(RAIL_W, USER_Y), (RAIL_W + SIDE_W, H)], fill=(14, 14, 14, 255))
draw.line([(RAIL_W, USER_Y), (RAIL_W + SIDE_W, USER_Y)], fill=(38, 38, 38, 255), width=1)
draw.ellipse([(RAIL_W + 20, USER_Y + 18), (RAIL_W + 68, USER_Y + 66)], fill=(45, 45, 45, 255), outline=(100, 100, 100, 255), width=2)
draw.ellipse([(RAIL_W + 56, USER_Y + 54), (RAIL_W + 68, USER_Y + 66)], fill=(52, 211, 153, 255))
draw.text((RAIL_W + 80, USER_Y + 20), "akidindev", fill=(240, 240, 240, 255), font=font_md)
draw.text((RAIL_W + 80, USER_Y + 46), "@akidin • Online", fill=(130, 130, 130, 255), font=font_xs)

CHAT_X = RAIL_W + SIDE_W
draw.rectangle([(CHAT_X, 0), (W, 80)], fill=(16, 16, 16, 255))
draw.line([(CHAT_X, 80), (W, 80)], fill=(38, 38, 38, 255), width=2)
draw.text((CHAT_X + 36, 24), "# general", fill=(250, 250, 250, 255), font=font_xl)
draw.text((CHAT_X + 220, 32), "Real-time communication • Minimal footprint", fill=(140, 140, 140, 255), font=font_sm)

def draw_msg(y_pos, author, tag, time_str, text, is_bot=False, avatar_pulse=False):
    av_x = CHAT_X + 36
    if avatar_pulse:
        draw.rounded_rectangle([(av_x, y_pos), (av_x + 50, y_pos + 50)], radius=12, fill=(20, 20, 20, 255), outline=(70, 70, 70, 255), width=2)
        p = [(av_x + 10, y_pos + 25), (av_x + 18, y_pos + 25), (av_x + 23, y_pos + 12), (av_x + 30, y_pos + 38), (av_x + 35, y_pos + 25), (av_x + 40, y_pos + 25)]
        draw.line(p, fill=(255, 255, 255, 255), width=2)
    else:
        draw.ellipse([(av_x, y_pos), (av_x + 50, y_pos + 50)], fill=(50, 50, 55, 255), outline=(80, 80, 85, 255), width=2)
        draw.text((av_x + 18, y_pos + 14), author[0].upper(), fill=(230, 230, 230, 255), font=font_md)

    content_x = av_x + 68
    draw.text((content_x, y_pos), author, fill=(245, 245, 245, 255), font=font_lg)
    curr_w = draw.textlength(author, font=font_lg)
    if is_bot:
        draw.rounded_rectangle([(content_x + curr_w + 12, y_pos + 4), (content_x + curr_w + 64, y_pos + 26)], radius=4, fill=(50, 50, 60, 255))
        draw.text((content_x + curr_w + 20, y_pos + 6), tag, fill=(210, 225, 255, 255), font=font_xs)
        curr_w += 68
    draw.text((content_x + curr_w + 16, y_pos + 6), time_str, fill=(120, 120, 120, 255), font=font_sm)
    draw.text((content_x, y_pos + 38), text, fill=(225, 225, 225, 255), font=font_md)

draw_msg(130, "Pulse Core", "APP", "10:40 PM", "Pulse active. Clean polling engine initialized.", is_bot=True, avatar_pulse=True)
draw_msg(240, "akidindev", "", "10:42 PM", "Fast message sync running with low resource usage.")

CARD_Y = 360
CARD_X = CHAT_X + 104
CARD_W = 760
CARD_H = 180
draw.rounded_rectangle([(CARD_X, CARD_Y), (CARD_X + CARD_W, CARD_Y + CARD_H)], radius=12, fill=(20, 20, 22, 255), outline=(50, 50, 55, 255), width=2)
draw.line([(CARD_X, CARD_Y), (CARD_X + 6, CARD_Y + CARD_H)], fill=(255, 255, 255, 255), width=6)
draw.text((CARD_X + 30, CARD_Y + 24), "Performance Telemetry", fill=(255, 255, 255, 255), font=font_lg)
draw.text((CARD_X + 30, CARD_Y + 64), "Engine: Snappy Polling  •  Zero Overhead  •  Active Session", fill=(170, 170, 170, 255), font=font_sm)

graph_pts = [
    (CARD_X + 30, CARD_Y + 140), (CARD_X + 140, CARD_Y + 140),
    (CARD_X + 180, CARD_Y + 100), (CARD_X + 220, CARD_Y + 160),
    (CARD_X + 260, CARD_Y + 140), (CARD_X + 420, CARD_Y + 140),
    (CARD_X + 460, CARD_Y + 90), (CARD_X + 500, CARD_Y + 155),
    (CARD_X + 540, CARD_Y + 140), (CARD_X + 720, CARD_Y + 140)
]
draw.line(graph_pts, fill=(255, 255, 255, 255), width=3)
draw.text((CARD_X + 30, CARD_Y + 105), "PULSE STATUS", fill=(120, 120, 120, 255), font=font_xs)

draw_msg(580, "akidindev", "", "10:44 PM", "All systems operational.")

INPUT_Y = H - 120
INPUT_X = CHAT_X + 36
INPUT_W = W - CHAT_X - 72
draw.rounded_rectangle([(INPUT_X, INPUT_Y), (INPUT_X + INPUT_W, INPUT_Y + 64)], radius=12, fill=(22, 22, 22, 255), outline=(55, 55, 55, 255), width=2)
draw.text((INPUT_X + 28, INPUT_Y + 20), "Message #general...", fill=(120, 120, 120, 255), font=font_md)
draw.rounded_rectangle([(INPUT_X + INPUT_W - 54, INPUT_Y + 12), (INPUT_X + INPUT_W - 14, INPUT_Y + 52)], radius=8, fill=(250, 250, 250, 255))
p_send = [(INPUT_X + INPUT_W - 40, INPUT_Y + 24), (INPUT_X + INPUT_W - 24, INPUT_Y + 32), (INPUT_X + INPUT_W - 40, INPUT_Y + 40), (INPUT_X + INPUT_W - 35, INPUT_Y + 32)]
draw.polygon(p_send, fill=(10, 10, 10, 255))

out_path = "/home/akidin/Documents/games and apps/msg app/pulse_ui_render.png"
img.save(out_path, "PNG")
