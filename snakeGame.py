from graphics import Rectangle, Point, GraphWin, color_rgb, Text
import time
import random

class SnakeGame(GraphWin):
    def __init__(self, gameMode = 'normal', render = True, popName = False, numOfPlayers = 1):
        if render:
            GraphWin.__init__(self, 'Snake Game', 800, 600)
            self.setBackground(color_rgb(30,30,30))
        
        self.render = render
        self.gameMode = gameMode
        self.popName = popName
        self.snake = [Snake(self) for _ in range(numOfPlayers)]
        self.gameRunning = True

        if self.render:
            self.drawHud()
        self.start()
    
    def start(self):
        while self.gameRunning:
            self.frame()
    
    def frame(self):
        self.getKeyboard()
        self.moveSnake()
        self.snakeColision()
        self.checkGameOver()
        if self.gameRunning and self.render:
            time.sleep(1/10)
    
    def drawHud(self):
        self.scoreText = Text(Point(730, 20) ,'Score: 0')
        self.scoreText.setTextColor(color_rgb(255,255,255))
        self.scoreText.draw(self)
    
    def refreshHud(self):
        for snake in self.snake:
            maxScore = 0
            if snake.score > maxScore:
                maxScore = snake.score
        self.scoreText.setText('Score: ' + str(maxScore))
    
    def snakeColision(self):
        for snake in self.snake:
            if snake.alive:
                snakeHeadX = snake.body[0].getP1().getX()
                snakeHeadY = snake.body[0].getP1().getY()
                # Own body colision
                for i in range(len(snake.body)):
                    if i > 0:
                        if snakeHeadX == snake.body[i].getP1().getX():
                            if snakeHeadY == snake.body[i].getP1().getY():
                                snake.die()
                # Walls Colision
                if snakeHeadX < 0:
                    snake.die()
                elif snakeHeadX > 780:
                    snake.die()
                if snakeHeadY < 0:
                    snake.die()
                elif snakeHeadY > 580:
                    snake.die()
                # Apple Colision
                if snakeHeadX == snake.food.getP1().getX():
                    if snakeHeadY == snake.food.getP1().getY():
                        snake.foodRespawn()
                        snake.addBody()
                        snake.score += 1
                        if self.render:
                            self.refreshHud()
                
    
    def checkGameOver(self):
        self.gameRunning = False
        for snake in self.snake:
            if snake.alive == True:
                self.gameRunning = True
        if self.gameRunning == False and self.render:
            self.close()
    
    def getKeyboard(self):
        key = self.checkKey()
        for snake in self.snake:
            if snake.alive:
                if key == 'Left' and snake.direction != 'Right':
                    snake.direction = 'Left'
                elif key == 'Right' and snake.direction != 'Left':
                    snake.direction = 'Right'
                elif key == 'Up' and snake.direction != 'Down':
                    snake.direction = 'Up'
                elif key == 'Down' and snake.direction != 'Up':
                    snake.direction = 'Down'
    
    def moveSnake(self):
        for snake in self.snake:
            snake.moveBody()

                
class Snake():
    def __init__(self, graphWin):
        self.body = [Rectangle(Point(600 + 20 * i, 280), Point(620  + 20 * i, 300)) for i in range(5)]
        self.graphWin = graphWin
        self.direction = 'Left'
        self.alive = True
        self.score = 0
        self.steps = 0
        if self.graphWin.gameMode == 'aitrain':
            self.brain = 0
        if self.graphWin.render:
            for body in self.body:
                body.setFill(color_rgb(255,255,255))
                body.draw(self.graphWin)
        self.food = Food(self.graphWin)
    
    def moveBody(self):
        self.steps += 1
        direction = self.direction
        self.body[-1].undraw()
        self.body.pop(-1)
        headX = self.body[0].getP1().getX()
        headY = self.body[0].getP1().getY()
        if direction == 'Left': headX -= 20
        elif direction == 'Right': headX += 20
        elif direction == 'Up': headY -= 20
        elif direction == 'Down': headY += 20
        
        p1 = Point(headX, headY)
        p2 = Point(p1.getX() + 20, p1.getY() + 20)
        head = Rectangle(p1, p2)
        head.setFill(color_rgb(255,255,255))
        head.draw(self.graphWin)
        self.body.insert(0, head)

    def die(self):
        self.alive = False
        for body in self.body:
            if self.graphWin.render:
                body.undraw()
            body = None

    def mapSnake(self):
        snakeCoords = []
        for body in self.body:
            snakeCoords.append([int(body.getP1().getX() / 20), int(body.getP1().getY() / 20)])
        return snakeCoords
    
    def mapNoSnake(self):
        snakeCoords = self.mapSnake()
        noSnakeCoords = []
        for x in range(40):
            for y in range(30):
                noSnakeCoords.append([x,y])
        for coord in snakeCoords:
            noSnakeCoords.remove(coord)
        return noSnakeCoords
    
    def addBody(self):
        lastBodyP1 = self.body[-1].getP1()
        lastBodyP2 = self.body[-1].getP2()
        self.body.append(Rectangle(lastBodyP1, lastBodyP2))
        self.body[-1].setFill(color_rgb(255,255,255))
        self.body[-1].draw(self.graphWin)
        self.body[-1].direction = self.body[-2]
    
    def foodRespawn(self):
        if self.graphWin.render:
            self.food.undraw()
        noSnakeCoords = self.mapNoSnake()
        randomCoord = noSnakeCoords[random.randrange(0, len(noSnakeCoords))]
        p1 = Point(randomCoord[0] * 20, randomCoord[1] * 20)
        p2 = Point(randomCoord[0] * 20 + 20, randomCoord[1] * 20 + 20)
        self.food = Food(self.graphWin, p1, p2)

class Food(Rectangle):
    def __init__(self, graphWin, p1 = Point(100,280), p2 = Point(120 ,300)):
        Rectangle.__init__(self, p1, p2)
        if graphWin.render:
            self.setFill(color_rgb(255,0,0))
            self.draw(graphWin)
    
    
        