from random import randint
import arcade

WIDTH = 500
HEIGHT = 500
SIZE = 8

class Snake(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.width = SIZE
        self.height = SIZE
        self.body_pos_size = 0
        self.speed = 7
        self.color = arcade.color.RED
        self.body_pos = []

        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        
        self.change_x = 0
        self.change_y = 0
        
        self.score = 0

    def draw(self):
        arcade.draw_rectangle_outline(self.center_x,self.center_y,self.width,self.height,arcade.color.WHITE,border_width=5,tilt_angle=45)

        for i , pos in enumerate(self.body_pos):
            if i%2 == 0:
                arcade.draw_rectangle_filled(pos[0],pos[1],self.width,self.height,self.color)

    def move(self):
        self.body_pos.append([self.center_x,self.center_y])

        if len(self.body_pos) > self.body_pos_size:
            self.body_pos.pop(0)


        if self.change_x == -1:
            self.center_x -= self.speed
        elif self.change_x == 1:
            self.center_x += self.speed
        
        if self.change_y == -1:
            self.center_y -= self.speed
        elif self.change_y == 1:
            self.center_y += self.speed

    def eat_apple(self):
        self.body_pos_size += 1
        self.score += 1
        self.app_music = arcade.load_sound(":resources:sounds/hit4.wav")
        arcade.play_sound(self.app_music)

    def eat_bahbah(self):
        self.score += 2
        self.bah_music = arcade.load_sound(":resources:sounds/hurt4.wav")
        arcade.play_sound(self.bah_music)

    def eat_ahah(self):
        self.score -= 1
        self.ah_music = arcade.load_sound(":resources:sounds/gameover2.wav")
        arcade.play_sound(self.ah_music)

class Apple(arcade.Sprite):
    def __init__(self):
        super().__init__()
        
        self.width = SIZE*4
        self.height = SIZE*4
        self.radius = 8
        self.color = arcade.color.RED
        
        self.center_x = randint(100,WIDTH-20)
        self.center_y = randint(100,HEIGHT-20)
        
    def draw(self):
        arcade.draw_circle_filled(self.center_x,self.center_y,self.radius,self.color)

class Bahbah(arcade.Sprite):
    def __init__(self):
        super().__init__()
        
        self.width = SIZE*3
        self.height = SIZE*3
        self.radius = 6
        self.color = arcade.color.BLUE
        
        self.center_x = randint(50,WIDTH-100)
        self.center_y = randint(50,HEIGHT-100)
        
    def draw(self):
        arcade.draw_circle_filled(self.center_x,self.center_y,self.radius,self.color)

class Ahah(arcade.Sprite):
    def __init__(self):
        super().__init__()
        
        self.width = SIZE*3
        self.height = SIZE*3
        self.color = arcade.color.GRAY

        self.center_x = randint(25,WIDTH-75)
        self.center_y = randint(25,HEIGHT-75)
        
    def draw(self):
        arcade.draw_rectangle_outline(self.center_x,self.center_y,self.width,self.height,self.color)

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=WIDTH,height=HEIGHT,title="AI-SNAKE",resizable=True)
        arcade.set_background_color(arcade.color.GRAY)
        
        self.snake = Snake()
        self.apple = Apple()
        self.bahbah = Bahbah()
        self.ahah = Ahah()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("(press [SPACE] to start)",220,480,arcade.color.BLACK,width=600,font_size=10,bold=True)
        
        if (self.snake.center_x < 0) or (self.snake.center_x > WIDTH) or (self.snake.center_y < 0) or (self.snake.center_y > HEIGHT):
            self.on_key_press(arcade.key.SPACE,int)

        else:
            text = f"SCORE : {self.snake.score}"
            arcade.draw_text(text,250,5,arcade.color.BLACK,15)

            self.snake.draw()
            self.apple.draw()
            self.bahbah.draw()
            self.ahah.draw()
        
    def on_update(self, delta_time: float):
        self.snake.move()

        if arcade.check_for_collision(self.snake,self.apple):
            self.snake.eat_apple()
            self.apple = Apple()

        elif arcade.check_for_collision(self.snake,self.bahbah):
            self.snake.eat_bahbah()
            self.bahbah = Bahbah()

        elif arcade.check_for_collision(self.snake,self.ahah):
            self.snake.eat_ahah()
            self.ahah = Ahah()

    def ai(self):
        while self.apple.center_y > self.snake.center_y:
            self.snake.change_x = 0
            self.snake.change_y = 1
            self.snake.move()

            if self.apple.center_x <= self.snake.center_x:
                self.snake.change_x = -1
                self.snake.change_y = 0
                self.snake.move()

            if self.apple.center_x > self.snake.center_x:
                self.snake.change_x = 1
                self.snake.change_y = 0
                self.snake.move()


        while self.apple.center_y <= self.snake.center_y:
            self.snake.change_x = 0
            self.snake.change_y = -1
            self.snake.move()

            if self.apple.center_x <= self.snake.center_x:
                self.snake.change_x = -1
                self.snake.change_y = 0
                self.snake.move()

            if self.apple.center_x > self.snake.center_x:
                self.snake.change_x = 1
                self.snake.change_y = 0
                self.snake.move()

    def on_key_press(self, key: int, modifiers: int):  
        if key == arcade.key.SPACE:
            self.ai()
    
snake_game = Game()

arcade.run()