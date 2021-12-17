import os
import sys
import pygame

size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 255))
FPS = 60
clock = pygame.time.Clock()
pygame.init()

hidden_group = pygame.sprite.Group()
fire_exit = pygame.sprite.Group()
water_exit = pygame.sprite.Group()
fire_key = pygame.sprite.Group()
water_key = pygame.sprite.Group()
fire_player = pygame.sprite.Group()
water_player = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
blocks_group = pygame.sprite.Group()
specials_group = pygame.sprite.Group()
animated_sprites = pygame.sprite.Group()
lava_sprite = pygame.sprite.Group()
water_sprite = pygame.sprite.Group()
game_over_sound = pygame.mixer.Sound("data/sounds/gameover.mp3")
victory_sound = pygame.mixer.Sound("data/sounds/victory.mp3")


def load_image(name, colorkey=None):
    """
    функция создани яотносительного пути файла, проверки его существования и загрузки изображения
    :param name: путь к фалу из папки data
    :param colorkey:
    :return: изображение
    """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as error:
        print('Cannot load image:', name)
        raise SystemExit(error)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    """
    функция для закрытия игры
    :return: ничего не выводит
    """
    pygame.quit()
    sys.exit()


def start_screen():
    """
    функция для работы окна меню
    :return: None
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 515 < mouse_pos[0] < 680 and 462 < mouse_pos[1] < 509:
                    return None
                elif 492 < mouse_pos[0] < 697 and 521 < mouse_pos[1] < 569:
                    rule_screen()
        render_start_screen()
        pygame.display.flip()
        clock.tick(FPS)


def render_start_screen():
    """
    функция наполняет окно изображением и текстом
    :return: ничего
    """
    intro_text = ["  Играть", "Правила"]

    fon = pygame.transform.scale(load_image('backgrounds/main_menu.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 450
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.y = text_coord
        intro_rect.x = 490
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def rule_screen():
    """
    функция для создания окна с правилами
    :return: None
    """
    rule_text = [" Игрок должен разбить стену из кирпичей,", "отразив прыгающий мяч платформой.",
                 "Платформа управляется мышью компьютера.", "Для начала игрок получает 3 жизни",
                 "Жизнь теряется, если мяч попадает", "в нижнюю часть экрана.",
                 "Если жизни потеряны - игра окончена.", "Цель - уничтожить все кирпичики."]
    fon = pygame.transform.scale(load_image('backgrounds/fon_rules.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 10
    for line in rule_text:
        string_rendered = font.render(line, True, (185, 198, 237))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.y = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    string_rendered = font.render('На главную', True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 600
    intro_rect.x = 460
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 460 < mouse_pos[0] < 743 and 603 < mouse_pos[1] < 651:
                    return None
        pygame.display.flip()
        clock.tick(FPS)


def next_lvl(lvl):
    """
    функция изменяет уровень на следующий
    :param lvl: текущий уровень
    :return: новый уровень
    """
    generate_level(load_level(f'lvl_{lvl}.txt'))


def load_level(name):
    """
    функция создаёт матрицу из загруженной карты уровня
    :param name: название файлу уровня
    :return: матрица с картой
    """
    fullname = "data/level_maps/" + name
    # читаем уровень, убирая символы перевода строки
    try:
        with open(fullname, 'r') as mapFile:
            level_map = [line.rstrip() for line in mapFile]
    except FileNotFoundError as error:
        print('Cannot load image:', name)
        sys.exit()

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками (' ')
    return list(map(lambda x: x.ljust(max_width, ' '), level_map))


def generate_level(lvl_map):
    """
    функция создаёт объекты на экране по карте
    :param lvl_map: карта уровня
    :return: ничего
    """
    vec = {'b': [Block, 'def_block', blocks_group],
           'm': [Block, 'mud', blocks_group],
           'L': [Liquid, ['top_lava', 'top_lava_reverse'] * 15, lava_sprite],
           'l': [Liquid, ['lava', 'lava_reverse'] * 15, lava_sprite],
           'W': [Liquid, ['top_water', 'top_water_reverse'] * 15, water_sprite],
           'w': [Liquid, ['water', 'water_reverse'] * 15, water_sprite],
           'r': [SpecialBlock, ['red_block', 'red_block_pushed'], [specials_group, fire_player]],
           's': [SpecialBlock, ['blue_block', 'blue_block_pushed'], [specials_group, water_player]],
           'h': [HiddenBlock, ['empty', 'hidden_block'], hidden_group],
           'K': [Key, 'red_key', fire_key],
           'k': [Key, 'blue_key', water_key],
           'E': [Exit, 'lock_red', fire_exit],
           'e': [Exit, 'lock_blue', water_exit]}
    for i in range(len(lvl_map)):
        for j in range(len(lvl_map[i])):
            if lvl_map[i][j] == 'r' or lvl_map[i][j] == 's':
                boy.count += 1
            if lvl_map[i][j] != ' ':
                vec[lvl_map[i][j]][0](120 + 30 * j, 20 + 30 * i, vec[lvl_map[i][j]][1], vec[lvl_map[i][j]][2])


def check_win():
    """
    функция проверяет побуде игрока
    :return: результат проверки
    """
    if boy.find_key and boy.exit and girl.exit and girl.find_key:
        return True
    return False


def win_game():
    """
    функция для работы окна победы
    :return: None
    """
    victory_sound.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 553 < mouse_pos[0] < 702 and 603 < mouse_pos[1] < 644:
                    return None
        fon = pygame.transform.scale(load_image('backgrounds/victory.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 70)
        string_rendered = font.render('Конец', True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.y = 600
        intro_rect.x = 550
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)


def check_lose():
    """
    функция для проверки поражения игрока
    :return: результат проверки
    """
    if boy.lives == 0 or girl.lives == 0:
        return True
    return False


def looser():
    """
    функция для работы окна проигравшего
    :return: None
    """
    game_over_sound.play()
    for i in range(0, 720, 8):
        fon1 = pygame.transform.scale(load_image('backgrounds/gameover.jpg'), (width, height))
        screen.blit(fon1, (0, i - 720))
        pygame.display.flip()
        clock.tick(FPS)
    fon = pygame.transform.scale(load_image('backgrounds/gameover.jpg'), (width, height))
    while True:
        for lose_event in pygame.event.get():
            if lose_event.type == pygame.QUIT:
                terminate()
            elif lose_event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = lose_event.pos
                if 553 < mouse_pos[0] < 702 and 603 < mouse_pos[1] < 644:
                    return None
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 70)
        string_rendered = font.render('Конец', True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.y = 600
        intro_rect.x = 550
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, specious, group):
        """
        функция инициализации класса
        :param x: начальная координата по оси x
        :param y: начальная координата по оси y
        :param specious: вид блока
        :param group: группа спрайтов к которой относится
        """
        super().__init__(group)
        self.image = load_image(f'sprites/blocks/{specious}.png')
        self.rect = self.image.get_rect().move(x, y)


class SpecialBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, set_of_frames, groups):
        """
        функция инициализации класса
        :param x: начальная координата по оси x
        :param y: начальная координата по оси y
        :param set_of_frames: вид блока
        :param groups: группа спрайтов к которой относится
        """
        super().__init__(groups[0], animated_sprites, blocks_group)
        self.x, self.y, self.set_of_frames = x, y, set_of_frames
        self.image = load_image(f'sprites/blocks/{set_of_frames[0]}.png')
        self.rect = self.image.get_rect().move(x, y)
        self.collided = 0
        self.checker = []
        self.require_player = groups[1]

    def update(self):
        """
        функция обновления состояния специального блока
        :return: ничего
        """
        self.checker.append(self.collided)
        if len(self.checker) == 3:
            self.collided = self.check_collide(self.checker)
            boy.check_hidden.append(self.collided)
            if len(boy.check_hidden) == boy.count:
                self.switch_hidden(1 if sum(boy.check_hidden) else 0)
                boy.check_hidden.clear()
            self.image = load_image(f'sprites/blocks/{self.set_of_frames[0 + self.collided]}.png')
            self.checker.clear()
            self.collided = 0
        self.rect = self.image.get_rect().move(self.x, self.y)

    def check_collide(self, checker: list):
        """
        проверяет нажатие на специальный блок
        :param checker: массив с результатами проверок
        :return: окончательный итог проверок
        """
        return 1 if 1 in checker else 0

    def switch_hidden(self, flag):
        """
        функция делает изменяет статус видимости скрытых блоков
        :param flag: новый статус
        :return: ничего
        """
        for h in hidden_group:
            h.visible = flag


class HiddenBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, set_of_frames, group):
        """
        функция инициализации класса
        :param x: начальная координата по оси x
        :param y: начальная координата по оси y
        :param set_of_frames: вид блока
        :param group: группа спрайтов к которой относится
        """
        super().__init__(group, animated_sprites)
        self.x, self.y, self.set_of_frames = x, y, set_of_frames
        self.image = load_image(f'sprites/blocks/{set_of_frames[0]}.png')
        self.rect = self.image.get_rect().move(x, y)
        self.visible = 0

    def update(self):
        """
        функция обновления состояния скрытого блока
        :return: ничего
        """
        self.image = load_image(f'sprites/blocks/{self.set_of_frames[0 + self.visible]}.png')
        self.rect = self.image.get_rect().move(self.x, self.y)


class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, frame, group):
        """
        функция инициализации класса
        :param x: начальная координата по оси x
        :param y: начальная координата по оси y
        :param frame: вид блока
        :param group: группа спрайтов к которой относится
        """
        super().__init__(group, animated_sprites)
        self.type = frame
        self.x, self.y = x, y
        self.image = load_image(f'sprites/other/{frame}.png')
        self.rect = self.image.get_rect().move(self.x, self.y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, frame, group):
        """
        функция инициализации класса
        :param x: начальная координата по оси x
        :param y: начальная координата по оси y
        :param frame: вид блока
        :param group: группа спрайтов к которой относится
        """
        super().__init__(group)
        self.image = load_image(f'sprites/blocks/{frame}.png')
        self.rect = self.image.get_rect().move(x, y)


class Liquid(pygame.sprite.Sprite):
    def __init__(self, x, y, set_of_frames: list, group):
        """
        функция инициализации класса
        :param x: начальная координата по оси x
        :param y: начальная координата по оси y
        :param set_of_frames: вид блока
        :param group: группа спрайтов к которой относится
        """
        super().__init__(animated_sprites, group)
        self.x, self.y, self.set_of_frames = x, y, set_of_frames
        self.number = 0
        self.image = load_image(f'sprites/for_animations/{self.set_of_frames[0]}.png')
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        """
        функция обновления состояния жидкости
        :return: ничего
        """
        self.image = load_image(f'sprites/for_animations/{self.set_of_frames[self.number]}.png')
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.number += 2
        if self.number >= 29:
            self.number = abs(self.number - 31)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_type, player_look, issue, x_h, y_h, life, x, y):
        """
        функция инициализации класса
        :param player_type: тип игрока (огонь, вода)
        :param player_look: название изображения
        :param issue: блок к оторому уязвим
        :param x_h: координата по х начала рисования коичества здоровь
        :param y_h: координата по у начала рисования коичества здоровь
        :param life: количество здоровья
        :param x: координата по х начала
        :param y: координата по у начала
        """
        super().__init__(player_type, animated_sprites)
        self.image = load_image(f'sprites/characters/{player_look}.png')
        self.life = [x_h, y_h, life]
        self.count = 0
        self.exit = False
        self.start = [x, y]
        self.rect = self.image.get_rect().move(self.start)
        self.speed = [0, 0]
        self.gravity = 1
        self.lives = 3
        self.find_key = False
        self.issue = issue
        self.is_jump = False
        self.on_air = True
        self.check_hidden = []

    def update(self):
        """
        функция обновления состояния персонажа
        :return: ничего
        """
        if self.is_jump and not self.on_air:
            self.speed[1] -= 14
        if self.on_air:
            self.speed[1] += self.gravity
        self.on_air = True
        self.rect.y += self.speed[1]
        self.collide(0, self.speed[1])
        self.rect.x += self.speed[0]
        self.collide(self.speed[0], 0)

    def health(self):
        """
        рисует сердца в зависимости от здоровья
        :return: ничего
        """
        lf = pygame.transform.scale(load_image(f'sprites/other/{self.life[2]}.png'), (60, 60))
        for i in range(self.lives):
            screen.blit(lf, (self.life[0], self.life[1] + 65 * i))

    def collide(self, x_speed, y_speed):
        collider = 0
        if pygame.sprite.spritecollideany(self, blocks_group):
            collider = pygame.sprite.spritecollideany(self, blocks_group)
        if pygame.sprite.spritecollideany(self, hidden_group) and \
                pygame.sprite.spritecollideany(self, hidden_group).visible:
            collider = pygame.sprite.spritecollideany(self, hidden_group)
        if pygame.sprite.spritecollideany(self, specials_group):
            special_collider = pygame.sprite.spritecollideany(self, specials_group)
            if self in special_collider.require_player:
                special_collider.collided = 1
        if collider:
            if x_speed > 0:
                self.rect.right = collider.rect.left
            if x_speed < 0:
                self.rect.left = collider.rect.right
            if y_speed < 0:
                self.rect.top = collider.rect.bottom
                self.speed[1] = 0
            if y_speed > 0:
                self.rect.bottom = collider.rect.top
                self.speed[1] = 0
                self.on_air = False
        if pygame.sprite.spritecollideany(self, water_key) and self.issue == lava_sprite:
            key_collider = pygame.sprite.spritecollideany(self, water_key)
            animated_sprites.remove(key_collider)
            self.find_key = True
        if pygame.sprite.spritecollideany(self, fire_key) and self.issue == water_sprite:
            key_collider = pygame.sprite.spritecollideany(self, fire_key)
            animated_sprites.remove(key_collider)
            self.find_key = True
        if pygame.sprite.spritecollideany(self, fire_exit) and self.issue == water_sprite and self.find_key:
            self.exit = True
        elif pygame.sprite.spritecollideany(self, water_exit) and self.issue == lava_sprite and self.find_key:
            self.exit = True

        if pygame.sprite.spritecollideany(self, self.issue):
            self.lives -= 1
            self.rect.topleft = self.start


level = 1
running = True
fon = pygame.transform.scale(load_image('backgrounds/background_1.jpg'), (width, height))
start_screen()
boy = Player(fire_player, 'fire_p', water_sprite, 30, 30, 'live_fire', 170, 550)
girl = Player(water_player, 'water_p', lava_sprite, 1200, 30, 'live_water', 220, 550)
next_lvl(level)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                boy.speed[0] += 4
            if event.key == pygame.K_LEFT:
                boy.speed[0] -= 4
            if event.key == pygame.K_UP and not boy.is_jump:
                boy.is_jump = True
            if event.key == pygame.K_d:
                girl.speed[0] += 4
            if event.key == pygame.K_a:
                girl.speed[0] -= 4
            if event.key == pygame.K_w and not boy.is_jump:
                girl.is_jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                boy.speed[0] -= 4
            if event.key == pygame.K_LEFT:
                boy.speed[0] += 4
            if event.key == pygame.K_UP:
                boy.is_jump = False
            if event.key == pygame.K_d:
                girl.speed[0] -= 4
            if event.key == pygame.K_a:
                girl.speed[0] += 4
            if event.key == pygame.K_w:
                girl.is_jump = False
    screen.blit(fon, (0, 0))
    animated_sprites.update()
    fire_exit.draw(screen)
    water_exit.draw(screen)
    boy.health()
    girl.health()
    animated_sprites.draw(screen)
    blocks_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
    if check_win():
        win_game()
        terminate()
    if check_lose():
        looser()
        terminate()
