import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        from kivy.core.window import Window
        self.label = Label()
        Window.bind(mouse_pos=lambda w , p : setattr(self.label, 'text', str(p)))
        return self.label

root = Tk()
l =Label(root, text="this works")
l.pack()
root.title("title to my tkinter")

root.mainloop()

if __name__ == '__main__':
    MyApp().run()