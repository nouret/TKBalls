import tkinter
from random import randint

size = 30
X = 10
Y = 10
field = [0] * X
F = [0] * X
colors = ["red", "green", "blue", "yellow"]
MV = []
moving = False
time = -1
sum = 0
points = 0

class ball():
	def __init__(self, X, Y, COLOR):
		self.nowx = X
		self.nowy = Y
		self.color = COLOR
		self.newx = X
		self.newy = Y
		self.me = canvas.create_oval(self.nowx * size, self.nowy * size, self.nowx * size + size, self.nowy * size + size, fill=COLOR)

	def move(self, t):
		canvas.coords(self.me, (self.nowx + (self.newx - self.nowx) * t) * size, (self.nowy + (self.newy - self.nowy) * t) * size,
			(self.nowx + (self.newx - self.nowx) * t) * size + size, (self.nowy + (self.newy - self.nowy) * t) * size + size)

	def __eq__(self, other):
		if type(other) == type(0):
			return False
		if type(self) == type(0):
			return False
		return self.nowx == other.nowx and self.nowy == other.nowy

	def remove(self):
		canvas.delete(self.me)

def dfs(x, y):
	global sum
	if field[x][y] == 0:
		return
	if F[x][y] == 1:
		return
	sum += 1
	F[x][y] = 1
	for dx in (1, -1):
		for dy in ([0]):
			nx = x + dx
			ny = y + dy
			if nx < 0 or ny < 0 or nx >= X or ny >= Y:
				continue
			if type(field[nx][ny]) == int:
				continue
			if field[x][y].color == field[nx][ny].color:
				dfs(nx, ny)
	for dx in ([0]):
		for dy in (-1, 1):
			nx = x + dx
			ny = y + dy
			if nx < 0 or ny < 0 or nx >= X or ny >= Y:
				continue
			if type(field[nx][ny]) == int:
				continue
			if field[x][y].color == field[nx][ny].color:
				dfs(nx, ny)

def click(event):
	global moving, points
	if moving:
		return
	global sum
	x = event.x // size
	y = event.y // size
	if field[x][y] == 0:
		return
	sum = 0
	dfs(x, y)
	points += (sum * (sum - 1))
	
	for i in range(X):
		for j in range(Y):
			if F[i][j] and sum > 1:
				field[i][j].remove()
				field[i][j] = 0
			F[i][j] = 0
	if sum > 1:
		moving = True

def move():
	global time, moving, MV
	if moving and time == -1:
		time = 0
		s = 0
		for i in range(X):
			for j in range(Y - 2, -1, -1):
				if type(field[i][j]) != int and field[i][j + 1] == 0:
					field[i][j].newy = j + 1
					MV += [field[i][j]]
					field[i][j] = 0
					s += 1
		if s == 0:
			moving = False
			time = -1
	if moving:
		for elem in MV:
			elem.move(time / 500)
		time += 50
		if time == 550:
			for elem in MV:
				elem.nowy =elem.newy
				field[elem.nowx][elem.nowy] = elem
			MV = []
			time = -1
	root.after(50, move)

def end(event):
	print(points)

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=size * X, height=size * Y)
canvas.bind("<Button-1>", click)
root.bind("<Return>", end)
for i in range (X):
	field[i] = [ball(i, j, colors[randint(0, 3)]) for j in range (Y)]
	F[i] = [0] * Y

canvas.pack()

root.after(50, move)

root.mainloop()
