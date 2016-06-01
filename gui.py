from tkinter import *

root = Tk()

frame = Frame(root)
frame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

top = Button(frame, text="Hello.", fg = "red")
bottom = Button(frame, text="Hello.", fg = "blue")
left = Button(frame, text="Hello.", fg = "green")
right = Button(bottomFrame, text="Hello.", fg = "purple")

top.pack(side = LEFT)
bottom.pack(side = LEFT)
left.pack(side = LEFT)
right.pack()


root.mainloop()