import pygame

pygame.init()

screen = pygame.display.set_mode((620, 620))
pygame.display.set_caption("Chess")
logo = pygame.image.load("chessicon.jpg")
pygame.display.set_icon(logo)
board = pygame.image.load("board.png")

mouse_down = False

turn = "white"
re_turn = False
move_num = 1 
legal = None
pawn_captureable = False
blocked_squares = []
blocking_squares = []

class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, row, col, color_p, p_name):
        super().__init__()
        self.piece = image
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.xsq = 15 + ((row - 1) * 75)
        self.ysq = 25 + ((col - 1) * 75)
        self.xdis = 15 + ((row - 1) * 75)
        self.ydis = 25 + ((col - 1) * 75)
        self.square = (col, row)
        self.square_prev = (col, row)
        self.selected = False
        self.rounded = 0
        self.row = row
        self.col = col
        self.mouse_state = 0
        self.color_p = color_p
        self.p_name = p_name
        self.move_no = 1

        print(f"Initialized {self.color_p} piece at {self.square}")
        
    def draw(self):
        screen.blit(self.image, (self.xdis, self.ydis))
    
    def move(self):
        global cursorpos
        if self.selected:
            self.xdis, self.ydis = cursorpos[0] - 25, cursorpos[1] - 25

    def check(self):
        global re_turn, legal, move_num, pawn_captureable
              
        if self.rounded == 1:
            changed_square = ((int(cursorpos[1] / 75)) + 1, (int(cursorpos[0] / 75)) + 1)
            stacked_piece = False
            
            if self.p_name == "pawn":
                if changed_square[1] == self.square[1]:
                    if self.square[0] - changed_square[0] == 1 and self.color_p == "white" and\
                        len([x for x in black_pieces if x.square == changed_square]) == 0  or \
                        self.move_no == 1 and 1 <= self.square[0] - changed_square[0] <= 2 and self.color_p == "white" or\
                        self.square[0] - changed_square[0] == -1 and self.color_p == "black" and\
                        len([x for x in white_pieces if x.square == changed_square]) == 0 or \
                        self.move_no == 1 and -1 >= self.square[0] - changed_square[0] >= -2 and self.color_p == "black":
                        legal = True
                        re_turn = False
                        self.move_no += 1
                    else:
                        legal = False
                        re_turn = True
                if self.square[0] - changed_square[0] == 1 and abs(self.square[1] - changed_square[1]) == 1\
                    and self.color_p == "white" and len([x for x in black_pieces if x.square == changed_square]) == 1 or\
                    self.square[0] - changed_square[0] == -1 \
                    and abs(self.square[1] - changed_square[1]) == 1\
                    and self.color_p == "black" and len([x for x in white_pieces if x.square == changed_square]) == 1 :
                    pawn_captureable = True
                    re_turn = False
                    legal = True     
            if self.p_name == "bishop":  
                if self.color_p == 'white':
                    if abs(changed_square[0] - self.square[0]) == abs(changed_square[1] - self.square[1]) and \
                    len([x for x in white_pieces if x.square == changed_square]) == 0:
                        blocked_squares = [x.square for x in white_pieces if \
                                        abs(x.square[0] - self.square[0]) == abs(x.square[1] - self.square[1]) and x != self]
                        for blocking_piece in blocked_squares:
                            legal = True
                            re_turn = False
                            self.move_no += 1
                    
                elif self.color_p == 'black':
                    if abs(changed_square[0] - self.square[0]) == abs(changed_square[1] - self.square[1]) and \
                    len([x for x in black_pieces if x.square == changed_square]) == 0:
                        legal = True 
                        re_turn = False
                        self.move_no += 1
                        
            if self.p_name == "knight":
                if self.color_p == 'white':
                    if abs(abs(changed_square[0] - self.square[0]) + abs(changed_square[1] - self.square[1])) == 3\
                    and abs(abs(changed_square[0] - self.square[0]) - abs(changed_square[1] - self.square[1])) == 1 and \
                    len([x for x in white_pieces if x.square == changed_square]) == 0:
                        legal = True
                        re_turn = False
                        self.move_no += 1

                elif self.color_p == 'black':
                    if abs(abs(changed_square[0] - self.square[0]) + abs(changed_square[1] - self.square[1])) == 3\
                    and abs(abs(changed_square[0] - self.square[0]) - abs(changed_square[1] - self.square[1])) == 1 and \
                    len([x for x in black_pieces if x.square == changed_square]) == 0:
                        legal = True
                        re_turn = False
                        self.move_no += 1
            if self.p_name == "rook":
                if self.color_p == 'white':
                    if changed_square[0] - self.square[0] == 0 or changed_square[1] - self.square[1] == 0 and \
                    len([x for x in white_pieces if x.square == changed_square]) == 0:
                        blocked_squares = [x.square for x in white_pieces if \
                                     x.square[0] == self.square[0] or x.square[1] == self.square[1] if x != self]
                        blocked_squares.extend([x.square for x in black_pieces if \
                                     x.square[0] == self.square[0] or x.square[1] == self.square[1] if x != self])
                        print(blocked_squares, "the legal squares")
                        for squ in blocked_squares:
                            if self.square[0] < squ[0] < changed_square[0] or self.square[0] > squ[0] > changed_square[0] \
                            or self.square[1] < squ[1] < changed_square[1] or self.square[1] > squ[1] > changed_square[1]:
                                print(squ, "the squ")
                                blocking_squares.append(squ)
                        if len(blocking_squares) == 0:
                            legal = True
                            re_turn = False
                            self.move_no += 1
                        blocking_squares.clear()
                        blocked_squares.clear()

                elif self.color_p == 'black':
                    if changed_square[0] - self.square[0] == 0 or changed_square[1] - self.square[1] == 0 and \
                    len([x for x in black_pieces if x.square == changed_square]) == 0:
                        blocked_squares = [x.square for x in black_pieces if \
                                     x.square[0] == self.square[0] or x.square[1] == self.square[1] if x != self ]
                        print(blocked_squares, "the legal squares")
                        for squ in blocked_squares:
                            if self.square[0] < squ[0] < changed_square[0] or self.square[0] > squ[0] > changed_square[0] \
                            or self.square[1] < squ[1] < changed_square[1] or self.square[1] > squ[1] > changed_square[1]:
                                print(squ, "the squ")
                                blocking_squares.append(squ)
                        if len(blocking_squares) == 0:
                            legal = True
                            re_turn = False
                            self.move_no += 1
                        blocking_squares.clear()
                        blocked_squares.clear()
            if self.p_name == "king":
                if self.color_p == 'white':
                    if abs(changed_square[0] - self.square[0]) + abs(changed_square[1] - self.square[1]) <= 2 and \
                    abs(abs(changed_square[0] - self.square[0]) - abs(changed_square[1] - self.square[1])) <= 1 and \
                    len([x for x in white_pieces if x.square == changed_square]) == 0:
                        legal = True
                        re_turn = False
                        self.move_no += 1

                elif self.color_p == 'black':
                    if abs(changed_square[0] - self.square[0]) + abs(changed_square[1] - self.square[1]) <= 2 and \
                    abs(abs(changed_square[0] - self.square[0]) - abs(changed_square[1] - self.square[1])) <= 1 and \
                    len([x for x in black_pieces if x.square == changed_square]) == 0:
                        legal = True
                        re_turn = False
                        self.move_no += 1                
            if self.p_name == "queen":
                if self.color_p == 'white':
                    if abs(changed_square[0] - self.square[0]) == abs(changed_square[1] - self.square[1]) and \
                    len([x for x in white_pieces if x.square == changed_square]) == 0:
                        legal = True
                        re_turn = False
                        self.move_no += 1

                    elif changed_square[0] - self.square[0] == 0 or changed_square[1] - self.square[1] == 0 and \
                    len([x for x in white_pieces if x.square == changed_square]) == 0:
                        legal = True
                        re_turn = False
                        self.move_no += 1

                elif self.color_p == 'black':
                    if abs(changed_square[0] - self.square[0]) == abs(changed_square[1] - self.square[1]) and \
                    len([x for x in black_pieces if x.square == changed_square]) == 0:
                        legal = True
                        re_turn = False
                        self.move_no += 1
                    
                    elif changed_square[0] - self.square[0] == 0 or changed_square[1] - self.square[1] == 0 and \
                    len([x for x in black_pieces if x.square == changed_square]) == 0:
                        legal = True
                        re_turn = False
                        self.move_no += 1

            for sprite in white_pieces:
                if sprite is not self and changed_square == sprite.square:
                    if sprite.color_p == self.color_p:
                        stacked_piece = True
                        re_turn = True
                        print(f"Collision detected: {self.color_p} piece at {self.square} with white piece at {sprite.square}")
                    else:
                        if legal or pawn_captureable:
                            sprite.kill()
                            move_num += 1

            for sprite in black_pieces:
                if sprite is not self and changed_square == sprite.square:
                    if sprite.color_p == self.color_p:
                        stacked_piece = True
                        re_turn = True
                        print(f"Collision detected: {self.color_p} piece at {self.square} with black piece at {sprite.square}")
                    else:
                        if legal or pawn_captureable:
                            sprite.kill()
                            move_num += 1
                        
            if stacked_piece:
                changed_square = self.square
                print("stacked")
            if legal == False:
                changed_square = self.square
                re_turn = True
                print("illegal")
            elif legal or re_turn == False:
                self.square_prev = self.square
                self.square = changed_square
                move_num += 1
                print("legal")

            self.xdis = 15 + (self.square[1] - 1) * 75
            self.ydis = 25 + (self.square[0] - 1) * 75

            
        legal = False
        pawn_captureable = False
        self.rounded = 0
        
    def selection(self):
        global cursorpos
        j = 0
        selec_sq = pygame.Surface((75, 75))
        if self.xdis < cursorpos[0] < (self.xdis + 50) and\
            self.ydis < cursorpos[1] < (self.ydis + 50):
            selec_sq.fill((255, 249, 201))
            self.xsq = self.square[1] * 75 - 60
            self.ysq = self.square[0] * 75 - 50
            screen.blit(selec_sq, (self.xsq - 6, self.ysq - 14))
            for piece in white_pieces:
                if piece.selected == False:
                    j += 1
            if j >= len(white_pieces):    
                self.selected = True
                self.square_prev = self.square
            j = 0
            for piece in black_pieces:
                if piece.selected == False:
                    j += 1
            if j >= len(black_pieces):    
                self.selected = True
                self.square_prev = self.square
            print(f"{self.color_p} piece selected at {self.square}")
            self.mouse_state = 1
        if self.mouse_state == 0:
            self.selected = False

black_pieces = pygame.sprite.Group()
white_pieces = pygame.sprite.Group()

ord = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

def add_piece(colour, group, colm, colmp, color_pieces):
    y = 1
    for n in range(1, 9):
        pawn = MySprite(f"{colour}pawn.png", n, colm, color_pieces, "pawn")
        group.add(pawn)
    for piece in ord:
        piece = MySprite(f"{colour}{piece}.png", y, colmp, color_pieces, f"{piece}")
        group.add(piece)
        y += 1

add_piece("B", black_pieces, 2, 1, "black")
add_piece("W", white_pieces, 7, 8, "white")

run = True
while run:
    screen.blit(board, (-150, -23))
    cursorpos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
            for sprite in black_pieces:
                if sprite.selected:
                    if sprite.mouse_state == 1:
                        if turn == "black":
                            sprite.rounded += 1 
                            sprite.check()
                            sprite.mouse_state = 0
                            if not re_turn:
                                turn = "white"
                            print(f"Turn changed to {turn}")

            for sprite in white_pieces:
                if sprite.selected:
                    if sprite.mouse_state == 1:
                        if turn == "white":
                            sprite.rounded += 1 
                            sprite.check()
                            sprite.mouse_state = 0
                            if not re_turn:
                                turn = "black"
                            print(f"Turn changed to {turn}")

    re_turn = False

    if mouse_down:
        for sprite in black_pieces:
            if turn == "black":
                sprite.selection()
                sprite.move()
        for sprite in white_pieces:
            if turn == "white":
                sprite.selection()
                sprite.move()
    
    boundary = pygame.draw.rect(screen, (10, 10, 10), pygame.Rect(0, 0, 620, 620), 10)
        
    for sprite in black_pieces:
        sprite.draw()
    for sprite in white_pieces:
        sprite.draw()
    
    pygame.display.update()
pygame.quit()

    