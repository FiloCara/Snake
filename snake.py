import time
import random
import os
from typing import List, Union
import keyboard

class SnakeGame:

    """
    """
    def __init__(self, board_size: tuple = (60, 30), speed: int = 0.2, snake_starting_size: int = 4) -> None:
        
        self.board_size = board_size
        self.speed = speed
        self.snake_starting_size = snake_starting_size
        
        # Initialize board object
        self.board = Board(board_size=board_size)
        # Initialize snake object
        self.snake = Snake(starting_size=self.snake_starting_size, board_size=board_size)
        # Initialize fruit object
        self.fruit = Fruit(percentage=0.05, board_size=board_size)
        # Initialize keylistener
        self.listener = KeyListener()
        # Initialize reward
        self.score = None
    
    def run(self) -> None:

        # Initialize score
        self.score = 0 

        # Initialize snake
        self.snake.initalize_snake()

        # Randomly introduce snake in board
        self.board.update(self.snake.snake, self.listener.direction, [])

        # Initialize listener for key press
        keyboard.on_press(self.listener.get_direction)
        
        while True:
        
            # Get pressed button
            direction = self.listener.direction
            
            # Update snake head
            new_head = self.snake.compute_new_head(direction)

            # Randomnly generate fruit
            self.fruit.generate_fruit(snake=self.snake.snake)
            
            # Check if move is permitted
            if self.snake.validate_move(new_head):

                # Check if fruit is eaten
                fruit_eaten = self.fruit.is_eaten(new_head=new_head)
                # Update snake
                self.snake.update_snake(new_head_coordinates=new_head, increase_size=fruit_eaten)
                # Update board
                self.board.update(snake=self.snake.snake, direction=direction, fruits=self.fruit.fruit_coordinates)
                # Update score
                self.score += 10 / self.speed + (10000 if fruit_eaten else 0)

                os.system("cls") # TODO: need to find another way
                print("Score = " + str(self.score))
                print(self.board, end="\r", flush=True)
                time.sleep(self.speed)

            else:
                
                os.system("cls") # TODO: need to find another way
                self.board.game_over()
                print(self.board, end="\r", flush=True)
                print("\n")
                print("Score = " + str(self.score))
                break
        
        answer = input("Do you want to play again? (Y)\n")
        answer = answer.lower()
        if answer == "y":
            self.run()

class Fruit:
    """
    """

    def __init__(self, percentage: float, board_size):
        self.percentage = percentage
        self.board_size = board_size
        self.fruit_coordinates = []
    
    # TODO: improve performance
    def generate_fruit(self, snake: list, fruit_number: int = 1) -> None:
        # Randomnly create fruit in random position if not already in the board
        if (random.random() <= self.percentage) and (len(self.fruit_coordinates) == 0):
            # Random add fruit/s in places where not snake
            for i in range(fruit_number):
                x_position = random.choice([i for i in range(self.board_size[0])])
                y_position = random.choice([j for j in range(self.board_size[1])])
                # Loop until coordinates are ok
                while [x_position, y_position] in snake:
                    x_position = random.choice([i for i in range(self.board_size[0])])
                    y_position = random.choice([j for j in range(self.board_size[1])])
                
                self.fruit_coordinates.append([x_position, y_position])

    # Check if fruit is eaten and eventually remove it
    def is_eaten(self, new_head: list) -> bool:
        if new_head in self.fruit_coordinates:
            self.fruit_coordinates.remove(new_head)
            return True
        return False

# TODO: add docstring
class Board:
    
    """
    """
    def __init__(self, board_size: tuple) -> None:
        self.board_size = board_size
        self.board = self.initialize_board(board_size)

    def initialize_board(self, board_size) -> Union[List, List]:
        board = []
        for i in range(board_size[0]):
            row = [" " for j in range(board_size[1])]
            board.append(row)
        return board
    
    # TODO: avoid complete intialization
    def update(self, snake: list, direction: str, fruits: list) -> None:
        
        # Remove previous snake
        self.board = self.initialize_board(board_size=self.board_size)
        # Put snake in board
        snake_head = snake[0]
        # Update head with direction symbol 
        if direction == "left":
            self.board[snake_head[0]][snake_head[1]] = "\u25c0"
        elif direction == "right":
            self.board[snake_head[0]][snake_head[1]] = "\u25b6"
        elif direction == "top":
            self.board[snake_head[0]][snake_head[1]] = "\u25b2"
        elif direction == "bottom":
            self.board[snake_head[0]][snake_head[1]] = "\u25bc"
        
        for chunk in snake[1:]:
            self.board[chunk[0]][chunk[1]] = "x"
        
        # Add fruit/s
        for fruit in fruits:
            self.board[fruit[0]][fruit[1]] = "\u2764\uFE0F"
    
    def game_over(self, message="Game Over!!!") -> None:
        # Empty board
        self.board = self.initialize_board(board_size=self.board_size)
        # Find position for message
        x_position = self.board_size[0] // 2
        y_position = (self.board_size[1] - len(message)) // 2
        # Introduce message in the center of the board
        self.board[x_position][y_position:y_position + len(message)] = list(message)
    
    def __str__(self) -> str:
        # Format board
        str_board = ""
        # Add upper boarder
        str_board += "-" * (self.board_size[1] + 2) + "\n"
        for i in range(self.board_size[0]):
            str_board += "|" + "".join(self.board[i]) + "|" + "\n"
        # Add lower boarder
        str_board += "-" * (self.board_size[1] + 2)
        return str_board
    

# TODO: add docstring    
class Snake:
    """
    """

    def __init__(self, starting_size, board_size: tuple) -> None:
        self.starting_size = starting_size
        self.board_size = board_size
        
        # snake is a list of coordinates
        self.snake = None
    
    # direction -> "left", "right", "up", "down"
    def compute_new_head(self, direction: str) -> list:

        if direction == "left":
            # Make sure it is not running on the right
            if (self.snake[0][1] - self.snake[1][1]) != 1: 
                return [self.snake[0][0], self.snake[0][1] - 1]
            else:
                # Keep same direction
                return [self.snake[0][0], self.snake[0][1] + 1]

        elif direction == "right":
            # Make sure it is not running on the right
            if (self.snake[0][1] - self.snake[1][1]) != -1:
                # Update snake by adding new head and by removing last element
                return [self.snake[0][0], self.snake[0][1] + 1]
            else:
                # Keep same direction
                return [self.snake[0][0], self.snake[0][1] - 1]
           
        elif direction == "bottom":
            # Make sure it is not running on the top
            if (self.snake[0][0] - self.snake[1][0]) != -1: 
                # Update snake by adding new head and by removing last element
                return [self.snake[0][0] + 1, self.snake[0][1]]
            else:
                # Keep same direction
                return [self.snake[0][0] - 1, self.snake[0][1]]

        elif direction == "top":
            # Make sure it is not running on the bottom
            if (self.snake[0][0] - self.snake[1][0]) != 1: 
                # Update snake by adding new head and by removing last element
                return [self.snake[0][0] - 1, self.snake[0][1]]

            else:
                # Keep same direction
                return [self.snake[0][0] + 1, self.snake[0][1]]
    
    def validate_move(self, new_head_coordinates: list) -> bool:
        # Check if head not over body
        if new_head_coordinates in self.snake[1:]:
            return False
        
        # Check if head in board
        if (new_head_coordinates[0] < 0 or new_head_coordinates[0] > self.board_size[0] - 1) or (new_head_coordinates[1] < 0 or new_head_coordinates[1] > self.board_size[1] - 1): 
            return False
        return True
    
    def update_snake(self, new_head_coordinates: list, increase_size: bool) -> None:
        # Add head at the beginning of the list
        self.snake.insert(0, new_head_coordinates)
        if not increase_size:
            self.snake.pop()
    
    # TODO: the snake must fit the board
    def initalize_snake(self) -> None:
        snake = []
        # Initialize head position coordinates
        x_coord = random.randint(a=4, b=self.board_size[0] - 4)
        y_coord = random.randint(a=4, b=self.board_size[1] - 4)

        snake.append([x_coord, y_coord])

        # Randomly chose if snake is vertical or horizontal
        is_vertical = True if random.random() > 0.5 else False

        for k in range(1, self.starting_size):
            if is_vertical:
                x_coord += 1
            else:
                y_coord += 1
            snake.append([x_coord, y_coord])
        
        self.snake = snake

# TODO: add docstring
class KeyListener:
    """
    """
    def __init__(self, keys={"a":"left", "w":"top", "s":"bottom", "d":"right"}) -> None:
        self.keys = keys
        self.direction = "top"
    
    def get_direction(self, event):
        # Make sure button in keys
        if event.name in self.keys.keys():
            self.direction = self.keys[event.name]


if __name__ == "__main__":

    vertical_board_size = 20
    horizontal_board_size = 20
    game_speed = 0.1
    snake_starting_size = 4 
    
    game = SnakeGame(board_size=(vertical_board_size, horizontal_board_size), 
                     speed=game_speed,
                     snake_starting_size=snake_starting_size)
    game.run()