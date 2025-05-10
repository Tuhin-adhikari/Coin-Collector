import pygame
import random

class Coin:
    def __init__(self):
        pygame.display.set_caption("Coin Collector")
        self.window = pygame.display.set_mode((640, 480))
        self.robot = pygame.image.load("robot.png")
        self.coin_img = pygame.image.load("coin.png")
        self.coin_img = pygame.transform.scale(self.coin_img, (50, 50))
        self.monster_img = pygame.image.load("monster.png")
        self.monster_img = pygame.transform.scale(self.monster_img, (60, 60))

        self.move_x = 0
        self.coin_velocity = 2
        self.coin_count = 0     #Keep track of coins collected
        self.MAX_COINS = 4  #Maximum number of coins on the screen at a time
        self.MAX_MONSTERS = 2  # Maximum number of monsters on screen at a time
        self.coins = []     #List to store coin data
        self.monsters = []  # List to store monster data

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 25)

    def spawn_random_coins(self):   #method to append random locations for random amount of coins 
        self.coins = []
        num_coins = random.randint(1, self.MAX_COINS)
        current_time = pygame.time.get_ticks()
        for _ in range(num_coins):
            x = random.randint(0, 640 - 50)
            y = random.randint(-300, -50)
            delay_ms = random.randint(1000, 3000)
            start_time = current_time + delay_ms
            self.coins.append([x, y, delay_ms, start_time])

    def reset_coin(self, coin): #Generates random locations 
        coin[0] = random.randint(0, 640 - 50)
        coin[1] = random.randint(-300, -50)
        coin[2] = random.randint(1000, 3000)
        coin[3] = pygame.time.get_ticks() + coin[2]

    def spawn_random_monsters(self):    #Similar for the monsters as well
        current_time = pygame.time.get_ticks()
        if len(self.monsters) < self.MAX_MONSTERS:
            x = random.randint(0, 640 - 60)  
            y = random.randint(-300, -50)  
            delay_ms = random.randint(2000, 5000)  
            start_time = current_time + delay_ms
            self.monsters.append([x, y, delay_ms, start_time])

    def reset_monster(self, monster):
        monster[0] = random.randint(0, 640 - 60)
        monster[1] = random.randint(-300, -50)
        monster[2] = random.randint(2000, 5000)
        monster[3] = pygame.time.get_ticks() + monster[2]

    def game_over(self):    #To execute the end of the game as robot touches the monster
        game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
        self.window.blit(game_over_text, (250, 200))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        exit() 

    def play(self):
        self.game()

    def game(self):
        to_left = False
        to_right = False

        while True:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        to_left = True
                    elif event.key == pygame.K_RIGHT:
                        to_right = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        to_left = False
                    elif event.key == pygame.K_RIGHT:
                        to_right = False

            if to_left and self.move_x > 0:
                self.move_x -= 4
            if to_right and self.move_x + self.robot.get_width() < 640:
                self.move_x += 4

            if len(self.coins) == 0:
                self.spawn_random_coins()

            # Spawn monsters
            self.spawn_random_monsters()

            self.window.fill((0, 0, 0))

            robot_rect = pygame.Rect(self.move_x, 480 - self.robot.get_height(), self.robot.get_width(), self.robot.get_height())

            # Check for monster collisions
            for monster in self.monsters:
                monster_rect = pygame.Rect(monster[0], monster[1], 60, 60)
                if robot_rect.colliderect(monster_rect):
                    self.game_over()

                if current_time >= monster[3]:
                    monster[1] += 2  # Move monster down the screen
                    if monster[1] > 480:  # Reset monster if it moves off the screen
                        self.reset_monster(monster)
                    self.window.blit(self.monster_img, (monster[0], monster[1]))

            # Check for coin collisions
            for coin in self.coins:
                if current_time >= coin[3]:
                    coin[1] += self.coin_velocity
                    coin_rect = pygame.Rect(coin[0], coin[1], 50, 50)

                    if robot_rect.colliderect(coin_rect):
                        self.coin_count += 1
                        self.reset_coin(coin)

                    if coin[1] > 480:
                        self.reset_coin(coin)

                    self.window.blit(self.coin_img, (coin[0], coin[1]))

            self.window.blit(self.robot, (self.move_x, 480 - self.robot.get_height()))
            score_text = self.font.render(f"Coins: {self.coin_count}", True, (255, 255, 255))
            self.window.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    coin_game = Coin()
    coin_game.play()