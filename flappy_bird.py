import pygame, sys, random, time, math
from pygame.locals import *

# WINDOWN
WINDOW_WIDTH = 500  # Chiều dài cửa sổ
WINDOW_HEIGHT = 700  # Chiều cao cửa sổ
DISPLAY_FLAPPY_BIRD = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('DANG LAM')
BACKGROUND_IMG = pygame.image.load('background_and_title/background.png')
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (1920, WINDOW_HEIGHT))

# READ FILE HIGHSCORE
file_high_score = open('high_score.txt')
high_score = int(file_high_score.read().strip())
file_high_score.close()

# FPS
FPS = 60
fps_clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 0, 255)
GRAY = (128, 128, 128)
ORANGE = (255, 128, 0)
# PYGAME
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

# MUSIC AND SOUND
pygame.mixer.music.load(r'sound_game/nhacnen2.mp3')
check_music = True
sound_push_button = pygame.mixer.Sound('sound_game/nhannut.wav')
sound_score = pygame.mixer.Sound('sound_game/congdiem.wav')
sound_jump = pygame.mixer.Sound('sound_game/nhay.wav')
sound_collision = pygame.mixer.Sound('sound_game/vacham.wav')
sound_push_button = pygame.mixer.Sound('sound_game/nhannut.wav')
sound_died = pygame.mixer.Sound('sound_game/thua.wav')

## Tra ve False neu 2 hinh vuong doc lap voi nhau
def check_rect_collision(rect_1, rect_2):
    if rect_1[0] <= rect_2[0] + rect_2[2] and rect_2[0] <= rect_1[0] + rect_1[2] and rect_1[1] <= rect_2[1] + rect_2[
        3] and rect_2[1] <= rect_1[1] + rect_1[3]:
        return True
    return False


## Tra ve True neu bird va cham vao 1 trong 3 column
def check_game_over(bird, columns):
    rect_bird = [bird.x, bird.y, bird.width, bird.height]
    for i in range(3):
        rect_column1 = [columns.list_column[i][0], columns.list_column[i][1] - columns.height, columns.width,
                        columns.height]
        rect_column2 = [columns.list_column[i][0], columns.list_column[i][1] + columns.blank, columns.width,
                        columns.height]
        if check_rect_collision(rect_bird, rect_column1) == True or check_rect_collision(rect_bird,
                                                                                         rect_column2) == True:
            return True
    if bird.y + bird.height < 0 or bird.y + bird.height > WINDOW_HEIGHT - 100:
        return True
    return False


## Return True neu toa do chuot nam trong hinh vuong
def check_pos_in_rect(rect, pos_of_mouse):
    if pos_of_mouse[0] >= rect[0] and pos_of_mouse[0] <= (rect[0] + rect[2]) and pos_of_mouse[1] >= rect[1] and pos_of_mouse[1] <= (
            rect[1] + rect[3]):
        return True
    else:
        return False


##TAO SAN LIST_BIRD_SURFACE
LIST_BIRD_SURFACE = []
for i in range(17):
    name_picture = 'bird/bird_' + str(i) + '.png'
    bird_img_temp = pygame.image.load(name_picture)
    bird_img_temp = pygame.transform.scale(bird_img_temp, (60, 60))
    LIST_BIRD_SURFACE.append(bird_img_temp)


##
class Bird:
    def __init__(self, bird_x=100, bird_y=270, bird_width=60, bird_height=60, bird_speed=-5):
        self.width = bird_width
        self.height = bird_height
        self.x = bird_x
        self.y = bird_y
        self.movement = 0
        self.fly = bird_speed
        self.list_surface = LIST_BIRD_SURFACE

    def draw(self, number_of_bird_surface):
        DISPLAY_FLAPPY_BIRD.blit(self.list_surface[number_of_bird_surface], (self.x, self.y))

    def update(self, space_push, mouse_click):
        self.y += self.movement
        self.movement += 0.3
        if mouse_click or space_push:
            self.movement = self.fly


class Columns:
    def __init__(self, column_width=60, column_height=360, column_blank=160, column_distance=220, column_speed=2):
        self.width = column_width
        self.height = column_height
        self.blank = column_blank
        self.distance = column_distance
        self.speed = column_speed
        COLUMN_IMG_BOT = pygame.image.load('pipe/pipe_2.png')
        COLUMN_IMG_BOT = pygame.transform.scale(COLUMN_IMG_BOT, (column_width, column_height))
        COLUMN_IMG_TOP = pygame.image.load('pipe/pipe_1.png')
        COLUMN_IMG_TOP = pygame.transform.scale(COLUMN_IMG_TOP, (column_width, column_height))
        self.surface_bot = COLUMN_IMG_BOT
        self.surface_top = COLUMN_IMG_TOP
        self.list_column = []
        for i in range(3):
            x = i * self.distance + WINDOW_WIDTH
            y = random.randrange(80, WINDOW_HEIGHT - 100 - self.blank - 80, 20)
            self.list_column.append([x, y])

    def draw(self):
        for i in range(3):
            DISPLAY_FLAPPY_BIRD.blit(self.surface_top, (self.list_column[i][0], self.list_column[i][1] - self.height))
            DISPLAY_FLAPPY_BIRD.blit(self.surface_bot, (self.list_column[i][0], self.list_column[i][1] + self.blank))

    def update(self):
        for i in range(3):
            self.list_column[i][0] -= self.speed
        if self.list_column[0][0] < -self.width:
            self.list_column.pop(0)
            x = self.list_column[1][0] + self.distance
            y = random.randrange(80, WINDOW_HEIGHT - 100 - self.blank - 80, 20)
            self.list_column.append([x, y])


class Base:
    def __init__(self, base_width=WINDOW_WIDTH, base_height=100):
        self.width = base_width
        self.height = base_height
        self.x = 0
        self.y = WINDOW_HEIGHT - self.height
        self.speed = 2
        BASE_IMG = pygame.image.load('background_and_title/base.png')
        BASE_IMG = pygame.transform.scale(BASE_IMG, (self.width, self.height))
        self.surface = BASE_IMG

    def draw(self):
        DISPLAY_FLAPPY_BIRD.blit(self.surface, (self.x, self.y))
        DISPLAY_FLAPPY_BIRD.blit(self.surface, (self.x + WINDOW_WIDTH, self.y))

    def update(self):
        self.x -= self.speed
        if self.x < -(WINDOW_WIDTH):
            self.x = 0


class Score:
    def __init__(self):
        self.score = 0
        self.add_score = True

    def draw(self):
        font_score = pygame.font.Font('font_in_game/fontScore.TTF', 40)
        score_surface = font_score.render(str(self.score), True, WHITE)
        score_size = score_surface.get_size()
        DISPLAY_FLAPPY_BIRD.blit(score_surface, ((WINDOW_WIDTH - score_size[0]) // 2, 80))

    def update(self, bird, columns):
        collision = False
        rect_bird = [bird.x, bird.y, bird.width, bird.height]
        for i in range(3):
            rect_column = [columns.list_column[i][0] + columns.width, columns.list_column[i][1], 1, columns.blank]
            if check_rect_collision(rect_bird, rect_column):
                collision = True
                break
        if collision == True:
            if self.add_score == True:
                self.score += 1
            self.add_score = False
        else:
            self.add_score = True


# surface dung cho game_start
title_game = pygame.image.load('background_and_title/title.png')
title_game = pygame.transform.scale(title_game, (300, 80))
button_play_in_game_start = pygame.image.load('button_in_game/playBut.png')
button_play_in_game_start = pygame.transform.scale(button_play_in_game_start, (160, 160))
button_play_in_game_start_1 = pygame.image.load('button_in_game/playBut.png')
button_play_in_game_start_1 = pygame.transform.scale(button_play_in_game_start_1, (163, 163))
button_music_on = pygame.image.load('button_in_game/musicOn.png')
button_music_on = pygame.transform.scale(button_music_on, (80, 60))
button_music_off = pygame.image.load('button_in_game/musicOff.png')
button_music_off = pygame.transform.scale(button_music_off, (80, 60))

# Xu li dau game
def game_start(bird_start,base_start):
    font_high_score = pygame.font.Font('font_in_game/fontScore.TTF', 40)
    surface_high_score = font_high_score.render('HIGH SCORE: ' + str(high_score), True, PINK)
    center_of_button_play=[(WINDOW_WIDTH//2),370+80]
    radius_of_button_play=80
    size_high_score = surface_high_score.get_size()
    rect_music_on = [10, 10, 80, 60]
    rect_music_off = list(rect_music_on)

    number_of_bird_surface = 0
    bird_dich = 0
    bird_up_down = 0
    first_music=False
    global check_music
    if check_music:
        pygame.mixer.music.play(-1)

    pygame.time.set_timer(pygame.USEREVENT, 40)

    while True:
        pos_of_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button==1:
                if check_pos_in_rect(rect_music_on, pos_of_mouse) == True:
                    check_music = not check_music
                    if check_music == False:
                        if first_music == False:
                            first_music = True
                        pygame.mixer.music.pause()
                    else:
                        if first_music == False:
                            pygame.mixer.music.play(-1)
                            first_music = True
                        else:
                            if first_music == False:
                                first_music= True
                            pygame.mixer.music.unpause()
                elif math.sqrt((pos_of_mouse[0] - center_of_button_play[0]) ** 2 + (pos_of_mouse[1] - center_of_button_play[1]) ** 2) <= radius_of_button_play:
                    if check_music:
                        sound_push_button.play()
                    return
            elif event.type == pygame.USEREVENT:
                if bird_up_down == 0:
                    bird_dich += 1
                    bird_start.y += 1
                    if bird_dich == 10:
                        bird_up_down = 1
                else:
                    bird_dich -= 1
                    bird_start.y -= 1
                    if bird_dich == 0:
                        bird_up_down = 0

        DISPLAY_FLAPPY_BIRD.blit(BACKGROUND_IMG, (0, 0))
        DISPLAY_FLAPPY_BIRD.blit(title_game, ((WINDOW_WIDTH - 400) // 2, 150 + bird_dich))
        DISPLAY_FLAPPY_BIRD.blit(surface_high_score, ((WINDOW_WIDTH - size_high_score[0]) // 2, 270))
        bird_start.draw(number_of_bird_surface)
        base_start.draw()
        if math.sqrt((pos_of_mouse[0] - center_of_button_play[0]) ** 2 + (pos_of_mouse[1] - center_of_button_play[1]) ** 2) <= radius_of_button_play:
            DISPLAY_FLAPPY_BIRD.blit(button_play_in_game_start, ((WINDOW_WIDTH - 160) // 2, 370))
        else:
            DISPLAY_FLAPPY_BIRD.blit(button_play_in_game_start_1, ((WINDOW_WIDTH - 163) // 2, 370))
        if check_music == True:
            DISPLAY_FLAPPY_BIRD.blit(button_music_on, (rect_music_on[0], rect_music_on[1]))
        else:
            DISPLAY_FLAPPY_BIRD.blit(button_music_off, (rect_music_off[0], rect_music_off[1]))

        number_of_bird_surface += 1
        if number_of_bird_surface > 16:
            number_of_bird_surface = 0
        base_start.update()
        pygame.display.update()
        fps_clock.tick(FPS)


# surface dung cho game_play
button_pause_game = pygame.image.load('button_in_game/pauseGame.png')
button_pause_game = pygame.transform.scale(button_pause_game, (50, 50))
back_ground_opacity = pygame.image.load('background_and_title/backgroundopacity.png')
back_ground_opacity = pygame.transform.scale(back_ground_opacity, (WINDOW_WIDTH, WINDOW_HEIGHT))
size_button_in_pause = [200, 60] #kich co button trong giao dien pause
button_play_game_in_pause = pygame.image.load('button_in_game/playGame.png')
button_play_game_in_pause = pygame.transform.scale(button_play_game_in_pause, (size_button_in_pause[0], size_button_in_pause[1]))
button_replay_game_in_pause = pygame.image.load('button_in_game/replayGame.png')
button_replay_game_in_pause = pygame.transform.scale(button_replay_game_in_pause, (size_button_in_pause[0], size_button_in_pause[1]))
button_exit_game_in_pause = pygame.image.load('button_in_game/exitGame.png')
button_exit_game_in_pause = pygame.transform.scale(button_exit_game_in_pause, (size_button_in_pause[0], size_button_in_pause[1]))
##

# GAME PLAY
def game_play(bird, columns, score, base, check_replay_in_pause):
    rect_pause_game = [5, 5, 50, 50]
    rect_music=[WINDOW_WIDTH-80-5,0,80,60]
    check_pause = False
    rect_play = [(WINDOW_WIDTH - size_button_in_pause[0]) // 2, 200, size_button_in_pause[0],size_button_in_pause[1]]
    rect_replay = [(WINDOW_WIDTH - size_button_in_pause[0]) // 2, 200 + size_button_in_pause[1] + 20, size_button_in_pause[0], size_button_in_pause[1]]
    rect_exit = [(WINDOW_WIDTH - size_button_in_pause[0]) // 2, 200 + size_button_in_pause[1] * 2 + 20 * 2,size_button_in_pause[0], size_button_in_pause[1]]
    number_of_bird_surface = 0
    first_music=False
    global check_music
    while True:
        score_temp = score.score
        pos_of_mouse = pygame.mouse.get_pos()
        space_push = False
        mouse_click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                space_push = True
                if check_music:
                    sound_jump.play()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if check_pos_in_rect(rect_pause_game, pos_of_mouse):
                    if check_pause == False:
                        if check_music:
                            sound_push_button.play()
                        check_pause = True
                elif check_pause == False:
                    if check_music:
                        sound_jump.play()
                    mouse_click = True
                elif check_pos_in_rect(rect_music, pos_of_mouse):
                    check_music = not check_music
                    if check_music:
                        if first_music == False:
                            pygame.mixer.music.play(-1)
                            first_music=True
                        else:
                            pygame.mixer.music.unpause()
                    else:
                        if first_music == False:
                            first_music = True
                        pygame.mixer.music.pause()

                elif check_pos_in_rect(rect_play, pos_of_mouse):
                    if check_music:
                        sound_push_button.play()
                    check_pause = False
                elif check_pos_in_rect(rect_replay, pos_of_mouse):
                    if check_music:
                        sound_push_button.play()
                    check_replay_in_pause[0] = True
                    return
                elif check_pos_in_rect(rect_exit, pos_of_mouse):
                    if check_music:
                        sound_push_button.play()
                    time.sleep(0.2)
                    pygame.quit()
                    sys.exit()

        DISPLAY_FLAPPY_BIRD.blit(BACKGROUND_IMG, (0, 0))
        columns.draw()
        DISPLAY_FLAPPY_BIRD.blit(button_pause_game, (rect_pause_game[0], rect_pause_game[1]))
        base.draw()
        bird.draw(number_of_bird_surface)
        score.draw()
        if check_game_over(bird, columns) == True:
            if check_music:
                sound_collision.play()
            pygame.mixer.music.stop()
            global high_score
            if score.score > high_score:
                high_score = score.score
                f = open('high_score.txt', 'w')
                f.write(str(high_score))
                f.close()
            return
        if check_pause == False:
            bird.update(space_push, mouse_click)
            score.update(bird, columns)
            if score.score > score_temp:
                if check_music:
                    sound_score.play()
            columns.update()
            base.update()
        else:
            DISPLAY_FLAPPY_BIRD.blit(back_ground_opacity, (0, 0))
            if check_music:
                DISPLAY_FLAPPY_BIRD.blit(button_music_on,(rect_music[0],rect_music[1]))
            else:
                DISPLAY_FLAPPY_BIRD.blit(button_music_off,(rect_music[0],rect_music[1]))
            DISPLAY_FLAPPY_BIRD.blit(button_play_game_in_pause, (rect_play[0], rect_play[1]))
            DISPLAY_FLAPPY_BIRD.blit(button_replay_game_in_pause, (rect_replay[0], rect_replay[1]))
            DISPLAY_FLAPPY_BIRD.blit(button_exit_game_in_pause, (rect_exit[0], rect_exit[1]))
        number_of_bird_surface += 1
        if number_of_bird_surface > 16:
            number_of_bird_surface = 0
        pygame.display.update()
        fps_clock.tick(FPS)
# surface dung cho game_over
game_over_surface = pygame.image.load('background_and_title/gameOver.png')
game_over_surface = pygame.transform.scale(game_over_surface, (380, 100))
table_score = pygame.image.load('background_and_title/tableScore1.png')
table_score = pygame.transform.scale(table_score, (320, 260))
replay_game_in_over_game = pygame.image.load('button_in_game/replay2.png')
replay_game_in_over_game = pygame.transform.scale(replay_game_in_over_game, (200, 100))
replay_game_in_over_game_1 = pygame.image.load('button_in_game/replay2.png')
replay_game_in_over_game_1 = pygame.transform.scale(replay_game_in_over_game_1, (203, 103))
font_score_in_over_game = pygame.font.Font('font_in_game/fontScore.TTF', 40)
font_score_in_over_game_1 = pygame.font.Font('font_in_game/font2.ttf', 40)

# GAME OVER
def game_over(bird, columns, score, base, check_replay_in_pause):
    if check_replay_in_pause[0] == True:
        check_replay_in_pause[0] = False
        return
    game_over_size = game_over_surface.get_size()
    tableSize = table_score.get_size()
    replay_size = replay_game_in_over_game.get_size()
    replay_size_1 = replay_game_in_over_game_1.get_size()
    score_surface = font_score_in_over_game_1.render('- SCORE -', True, GRAY)
    score_surface_1 = font_score_in_over_game.render(str(score.score), True, ORANGE)
    high_score_surface = font_score_in_over_game_1.render('< BEST >', True, GRAY)
    high_score_surface_1 = font_score_in_over_game.render(str(high_score), True, ORANGE)
    score_size = score_surface.get_size()
    score_size_1 = score_surface_1.get_size()
    high_score_size = high_score_surface.get_size()
    high_score_size_1 = high_score_surface_1.get_size()
    rect_replay = [(WINDOW_WIDTH - replay_size[0]) // 2, 60 + game_over_size[1] + tableSize[1] + 20, replay_size[0], replay_size[1]]
    for i in range(3):
        DISPLAY_FLAPPY_BIRD.fill(WHITE)
        pygame.display.update()
        fps_clock.tick(FPS)
    y_of_game_over=-game_over_size[1]
    y_of_table_score=WINDOW_HEIGHT
    x_of_score=-score_size[0]
    x_of_best=WINDOW_WIDTH
    ready_replay=False
    ready_sound=True
    while True:
        pos_of_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if check_pos_in_rect(rect_replay, pos_of_mouse) == True and ready_replay == True:
                    if check_music:
                        sound_push_button.play()
                    return
        DISPLAY_FLAPPY_BIRD.blit(BACKGROUND_IMG, (0, 0))
        columns.draw()
        base.draw()
        bird.draw(0)
        if bird.y < 700:
            bird.update(False,False)
            if (bird.y + bird.height) >= 600 and ready_sound and check_music:
                sound_died.play()
                ready_sound=False
        else:
            if y_of_game_over < 60:
                DISPLAY_FLAPPY_BIRD.blit(game_over_surface, ((WINDOW_WIDTH - game_over_size[0]) // 2, y_of_game_over))
                y_of_game_over+=15
            else:
                DISPLAY_FLAPPY_BIRD.blit(game_over_surface, ((WINDOW_WIDTH - game_over_size[0]) // 2, 60))
                if y_of_table_score > (60 + game_over_size[1] + 10):
                    DISPLAY_FLAPPY_BIRD.blit(table_score, (((WINDOW_WIDTH - tableSize[0]) // 2),y_of_table_score))
                    y_of_table_score-=25
                else:
                    DISPLAY_FLAPPY_BIRD.blit(table_score, ((WINDOW_WIDTH - tableSize[0]) // 2, 60 + game_over_size[1] + 10))
                    if x_of_score < ((WINDOW_WIDTH - score_size[0]) // 2):
                        DISPLAY_FLAPPY_BIRD.blit(score_surface, (x_of_score, 60 + game_over_size[1] + 50))
                        x_of_score+=25
                    else:
                        DISPLAY_FLAPPY_BIRD.blit(score_surface, ((WINDOW_WIDTH - score_size[0]) // 2, 60 + game_over_size[1] + 50))
                        DISPLAY_FLAPPY_BIRD.blit(score_surface_1, ((WINDOW_WIDTH - score_size_1[0]) // 2, 60 + game_over_size[1] + 50 + score_size[1]))
                    if x_of_best > ((WINDOW_WIDTH - high_score_size[0]) // 2):
                        DISPLAY_FLAPPY_BIRD.blit(high_score_surface, (x_of_best, 60 + game_over_size[1] + 50 + score_size[1] + score_size_1[1] + 10))
                        x_of_best-=25
                    else:
                        DISPLAY_FLAPPY_BIRD.blit(high_score_surface, ((WINDOW_WIDTH - high_score_size[0]) // 2,60 + game_over_size[1] + 50 + score_size[1] + score_size_1[1] + 10))
                        DISPLAY_FLAPPY_BIRD.blit(high_score_surface_1, ((WINDOW_WIDTH - high_score_size_1[0]) // 2, 60 + game_over_size[1] + 50 + score_size[1] + score_size_1[1] + high_score_size[1] + 10))
                    if check_pos_in_rect(rect_replay, pos_of_mouse) == True:
                        DISPLAY_FLAPPY_BIRD.blit(replay_game_in_over_game, ((WINDOW_WIDTH - replay_size[0]) // 2, 60 + game_over_size[1] + tableSize[1] + 20))
                        ready_replay=True
                    else:
                        DISPLAY_FLAPPY_BIRD.blit(replay_game_in_over_game_1, ((WINDOW_WIDTH - replay_size_1[0]) // 2, 60 + game_over_size[1] + tableSize[1] + 20))
                        ready_replay=True
        pygame.display.update()
        fps_clock.tick(FPS)

def main():
    check_replay_in_pause = [False]
    while True:
        bird_start = Bird(((WINDOW_WIDTH - 400) // 2) + 300 + 40, 150)
        base_start = Base()
        game_start(bird_start,base_start)
        bird = Bird()
        score = Score()
        columns = Columns()
        base = Base()
        game_play(bird, columns, score, base, check_replay_in_pause)
        game_over(bird, columns, score, base, check_replay_in_pause)

if __name__ == '__main__':
    main()
