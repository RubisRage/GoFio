from game_logic.data_module import GameController
from game_logic.data_module import EMPTY, BLACK, WHITE
from game_logic.exceptions import GoRuleException
import game_logic.data_module as data

import kivy.app 
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Line, Ellipse, Color
from kivy.core.window import Window

Window.size = 600, 700


end_flag = False

class Board(Widget):

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos) and not end_flag:
            x = round((touch.pos[0]-self.origin_x)/self.step,0)
            y = round((touch.pos[1]-self.origin_y)/self.step,0)
            try:
                self.parent.parent.game.throw(int(x), int(y))
            except GoRuleException as e:
                Popup(title="Go rule", 
                        content=Label(text=str(e)),
                        size_hint=(.8,.2)).open()
        

    def update(self):
        b_width = self.width-0.1*self.width
        self.step = b_width/18
        self.origin_x = self.pos[0] + 0.05*self.width
        self.origin_y = self.pos[1] + 0.05*self.width


        with self.canvas:
            for l in self.l:
                self.canvas.remove(l)
            self.l.clear()

            Color(0,0,0,1)
            for x in range(0,19):
                self.l.append(Line(points=[self.origin_x+self.step*x,
                                            self.origin_y,
                                            self.origin_x+self.step*x, 
                                            self.origin_y+b_width]))
                self.l.append(Line(points=[self.origin_x, 
                                            self.origin_y+self.step*x, 
                                            self.origin_x+b_width, 
                                            self.origin_y+self.step*x]))
            
            for s in self.stones:
                self.canvas.remove(s)
            self.stones.clear()

            for x in range(0,19):
                for y in range(0,19):
                    if data.board[x][y] != EMPTY:
                        Color(0,0,0,1) if data.board[x][y] == BLACK else Color(1,1,1,1)
                        pos = [x*self.step+self.origin_x-self.step/2,
                                y*self.step+self.origin_y-self.step/2]
                        self.stones.append(Ellipse(pos=pos, size=[self.step,self.step]))
            

class GoGame(Widget):
    
    def __init__(self):
        super().__init__()
        self.game = GameController()
        self.board = self.ids['board']
        self.board.l = list()
        self.board.stones = list()
    
    def update(self, dt):
        self.board.update() 
        Clock.schedule_once(self.update, 1.0/60.0)
    
    def pass_turn(self):
        self.game.pass_turn()
        end_flag = self.game.ended()
        if end_flag:
                Popup(title="Game end",
                content=Label(text="The game has ended"),
                size_hint=(.8,.2)).open()
        


class GoApp(App):
    def build(self):
        g = GoGame()
        Clock.schedule_once(g.update,0)
        return g

if __name__=="__main__":
    GoApp().run()