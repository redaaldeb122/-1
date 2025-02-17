import pygame
import random
import socket
import threading

# تهيئة Pygame
pygame.init()

# إعدادات الشاشة
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("لعبة المقالب المضحكة - Online/Offline")

# الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# تحميل صور الشخصيات
characters = [
    pygame.image.load("images/character1.png"),
    pygame.image.load("images/character2.png"),
    pygame.image.load("images/character3.png"),
    pygame.image.load("images/character4.png"),
    pygame.image.load("images/character5.png"),
    pygame.image.load("images/character6.png"),
]

# مواقع الشخصيات
character_positions = [
    (100, 100),
    (300, 100),
    (500, 100),
    (100, 300),
    (300, 300),
    (500, 300),
]

# المقالب المضحكة
pranks = [
    "لقد اختفت ملابسك!",
    "لقد تحولت إلى قطة!",
    "لقد انقلبت الشاشة رأسًا على عقب!",
    "لقد تم تغيير لونك إلى الأخضر!",
    "لقد تم تصغيرك إلى حجم النملة!",
    "لقد تم تجميدك في مكانك!",
    "لقد تحولت إلى بطاطا!",
    "لقد طار رأسك إلى الفضاء!",
    "لقد أصبحت شفافًا!",
    "لقد تحولت إلى دجاجة!",
]

# تحميل الأصوات المضحكة
prank_sounds = [
    pygame.mixer.Sound("sounds/prank1.wav"),
    pygame.mixer.Sound("sounds/prank2.wav"),
    pygame.mixer.Sound("sounds/prank3.wav"),
    pygame.mixer.Sound("sounds/prank4.wav"),
    pygame.mixer.Sound("sounds/prank5.wav"),
]

# وظيفة لعرض المقالب
def display_prank(prank):
    font = pygame.font.Font(None, 36)
    text = font.render(prank, True, RED)
    screen.blit(text, (screen_width // 2 - 150, screen_height // 2))

# وظيفة لتشغيل الصوت
def play_prank_sound():
    sound = random.choice(prank_sounds)
    sound.play()

# وظيفة للتحكم في الشخصيات
def handle_character_click(mouse_pos):
    for i, pos in enumerate(character_positions):
        if pos[0] <= mouse_pos[0] <= pos[0] + 100 and pos[1] <= mouse_pos[1] <= pos[1] + 100:
            prank = random.choice(pranks)
            display_prank(prank)
            play_prank_sound()

# وظيفة للعب Online
def online_mode():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5555))
    server_socket.listen(1)
    print("في انتظار اتصال...")
    client_socket, addr = server_socket.accept()
    print("تم الاتصال مع:", addr)

    while True:
        data = client_socket.recv(1024).decode()
        if data == "prank":
            prank = random.choice(pranks)
            client_socket.send(prank.encode())
            play_prank_sound()

# وظيفة للعب Offline
def offline_mode():
    running = True
    while running:
        screen.fill(WHITE)

        # رسم الشخصيات
        for i, character in enumerate(characters):
            screen.blit(character, character_positions[i])

        # التحقق من النقر على الشخصيات
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                handle_character_click(mouse_pos)

        pygame.display.flip()

# بدء اللعبة
def start_game(mode):
    if mode == "online":
        online_thread = threading.Thread(target=online_mode)
        online_thread.start()
    else:
        offline_mode()

# واجهة اختيار الوضع
def choose_mode():
    font = pygame.font.Font(None, 48)
    online_text = font.render("Online", True, BLACK)
    offline_text = font.render("Offline", True, BLACK)

    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(online_text, (300, 200))
        screen.blit(offline_text, (300, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 450 and 200 <= mouse_pos[1] <= 250:
                    start_game("online")
                elif 300 <= mouse_pos[0] <= 450 and 300 <= mouse_pos[1] <= 350:
                    start_game("offline")

        pygame.display.flip()

# تشغيل واجهة اختيار الوضع
choose_mode()

# إنهاء Pygame
pygame.quit()
