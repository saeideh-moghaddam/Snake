import random
import arcade

HEIGHT = 600
WIDTH = 600

class Apple(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.apple = arcade.Sprite('apple.png', scale=0.05)
        self.apple.center_x = random.randint(10, w - 10)
        self.apple.center_y = random.randint(10, h - 10)
        
    def draw(self):
        self.apple.draw()
        
class Cactus(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.cactus = arcade.Sprite('cactus.png', scale=0.2)
        self.cactus.center_x = random.randint(10, w - 10)
        self.cactus.center_y = random.randint(10, h - 10)
        
    def draw(self):
        self.cactus.draw()
    
class Flower(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.flower = arcade.Sprite('flower.png', scale=0.08)
        self.flower.center_x = random.randint(10, w - 10)
        self.flower.center_y = random.randint(10, h - 10)
        
    def draw(self):
        self.flower.draw()

class Snake(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.color = arcade.color.BLUE
        self.bodycolor = arcade.color.YELLOW
        self.speed = 1
        self.width = 16
        self.height = 16
        self.center_x = w // 2
        self.center_y = h // 2
        self.r = 8
        self.change_x = 0
        self.change_y = 0
        self.score = 0
        self.body = []
        self.body.append([self.center_x, self.center_y])
        
    def draw(self):
        for i in range(len(self.body)):
            if i == 0:
                arcade.draw_circle_filled(self.body[i][0], self.body[i][1], self.r, self.color)
            else:
                arcade.draw_circle_outline(self.body[i][0], self.body[i][1], self.r, self.bodycolor)

    def move(self, appleX, appleY):
        self.change_x = 0
        self.change_y = 0
        
        if self.center_x > appleX:
            self.change_x = -1
        if self.center_x < appleX:
            self.change_x = 1        
        if self.center_x == appleX:
            self.change_x = 0
            if self.center_y > appleY:
                self.change_y = -1
            if self.center_y < appleY:
                self.change_y = 1
            if self.center_y == appleY:
                self.change_y = 0
        
        for i in range(len(self.body)-1, 0, -1):
                self.body[i][0] = self.body[i-1][0]
                self.body[i][1] = self.body[i-1][1]
                
        self.center_x += self.speed * self.change_x
        self.center_y += self.speed * self.change_y
        
        if self.body:
            self.body[0][0] += self.speed * self.change_x
            self.body[0][1] += self.speed * self.change_y

    def eat(self, mode):
        if mode == 0: 
            self.score += 1
            self.body.append([self.body[len(self.body)-1][0], self.body[len(self.body)-1][1]])
        
        elif mode == 1: 
            self.score -= 1
            self.body.pop()
            
        elif mode == 2: 
            self.score += 2
            self.body.append([self.body[len(self.body)-1][0], self.body[len(self.body)-1][1]])
            self.body.append([self.body[len(self.body)-1][0], self.body[len(self.body)-1][1]])
    
class Game(arcade.Window):
    def __init__(self):
        arcade.Window.__init__(self, WIDTH, HEIGHT, "Snake GAME")
        arcade.set_background_color(arcade.color.BLACK)
        self.snake = Snake(WIDTH, HEIGHT)
        self.apple = Apple(WIDTH, HEIGHT)
        self.cactus = Cactus(WIDTH, HEIGHT)
        self.flower = Flower(WIDTH, HEIGHT)
        
    def on_draw(self):
        
        arcade.start_render()
        self.snake.draw()
        self.apple.draw()
        self.cactus.draw()
        self.flower.draw()
        arcade.draw_text('Score : ', 20, HEIGHT - 25, arcade.color.GREEN)
        arcade.draw_text(str(self.snake.score), 100, HEIGHT - 25, arcade.color.GREEN, italic=True)
        
            
    def on_update(self, delta_time: float):
       
        self.snake.move(self.apple.apple.center_x, self.apple.apple.center_y)
        if arcade.check_for_collision(self.apple.apple, self.snake): 
            self.snake.eat(0)
            self.apple = Apple(WIDTH, HEIGHT)
            
        if arcade.check_for_collision(self.cactus.cactus, self.snake): 
            self.snake.eat(1)
            self.cactus = Cactus(WIDTH, HEIGHT)
            
        if arcade.check_for_collision(self.flower.flower, self.snake): 
            self.snake.eat(2)
            self.flower = Flower(WIDTH, HEIGHT) 
        
if __name__ == '__main__':
    game = Game()
    arcade.run()