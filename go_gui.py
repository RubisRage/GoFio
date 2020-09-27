from game_logic.data_module import GameController

import kivy.app 
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Line, Ellipse, Color
from kivy.core.window import Window

Window.size = 600, 700

class Board(Widget):

    def update_board(self):
        b_width = self.width-0.1*self.width
        step = b_width/18
        origin_x = self.pos[0] + 0.05*self.width
        origin_y = self.pos[1] + 0.05*self.width

        with self.canvas:
            for l in self.l:
                self.canvas.remove(l)
            self.l.clear()

            Color(0,0,0,1)
            for x in range(0,19):
                self.l.append(Line(points=[origin_x+step*x,origin_y,origin_x+step*x, origin_y+b_width]))
                self.l.append(Line(points=[origin_x, origin_y+step*x, origin_x+b_width, origin_y+step*x]))


class GoGame(Widget):
    
    def __init__(self):
        super().__init__()
        self.board = self.ids['board']
        self.board.l = list()
    
    def update(self, dt):
        self.board.update_board()
        
        Clock.schedule_once(self.update, 1.0/60.0)

class GoApp(App):
    def build(self):
        g = GoGame()
        Clock.schedule_once(g.update,0)
        return g

if __name__=="__main__":
    GoApp().run()