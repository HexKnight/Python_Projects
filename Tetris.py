"""
	@name: Classic Tetris
	@author: SmartBeam
	@date: 03/04/2021
"""

from random import choice, randint


BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, WHITE = COLORS = range(8)

def color(text, color, background=None):
	assert 0 <= color < 8, f"Unknown foreground color value {color}!"
	if background != None:
		assert 0 <= background < 8, f"Unknown background color value {background}!"
	output = f'\x1b[{30+color}'
	if background != None:
		output += f';{40+background}'
	output += f'm{text}\x1b[m'
	return output

clear = lambda : print('\x1b[2J\x1b[H', end='')


class Tetris:
	
	_PIECES = (
		((1, 0), (1, 1), (1, 2), (1, 3)),
		((1, 0), (1, 1), (1, 2), (2, 2)),
		((2, 0), (2, 1), (1, 2), (2, 2)),
		((1, 1), (2, 1), (1, 2), (2, 2)),
		((0, 1), (1, 1), (1, 2), (2, 2)),
		((2, 0), (1, 1), (2, 1), (1, 2)),
		((1, 1), (0, 2), (1, 2), (2, 2))
	)
	
	def __init__(self):
		self.SCORING = (0, 40, 100, 300, 1200)
		self.WIDTH, self.HEIGHT = 10, 20
		self.grid = {
			(x, y): None
			for x in range(self.WIDTH)
			for y in range(self.HEIGHT)
		}
		self.score = 0
		self.level = 0
		self.piece = None
		self.next = None
		self._new_piece()
		self._game_over = False
	
	def step(self, rotate, move):
		if not self._game_over:
			self._rotate(rotate)
			self._move(move)
			if self._is_piece_overlaping():
				self._attach()
				self._clear_lines()
				self._new_piece()
			else:
				self.piece['y'] += 1
	
	def restart(self):
		self.__init__()
	
	def _grid_piece(self, piece=None):
		piece = self.piece if piece == None else piece
		pos_extractor = lambda vec: (vec[0]+piece['x'], vec[1]+piece['y'])
		return tuple(map(pos_extractor, piece['shape']))
	
	def _rotate(self, times, piece=None):
		assert 0 <= times <= 3, "rotation must be a value between 0 and 3!"
		piece = self.piece if piece == None else piece
		if times == 0:
			return
		else:
			shape = list(piece['shape'])
			pos_x, pos_y = piece['x'], piece['y']
			for i in range(len(piece['shape'])):
				x, y = shape[i][0], shape[i][1]
				x, y = 3 - y, x
				if (not 0 <= x + pos_x < self.WIDTH) or (not 0 <= y + pos_y < self.HEIGHT) or self.grid[x+pos_x, y+pos_y] in COLORS:
					return
				else:
					shape[i] = x, y
			else:
				piece['shape'] = tuple(shape)
			self._rotate(times-1, piece)
	
	def _move(self, dist):
		if dist == 0:
			return
		elif dist > 0:
			for (x, y) in self._grid_piece():
				if x >= self.WIDTH-1 or self.grid[x+1, y] != None:
					return
			else:
				self.piece['x'] += 1
				self._move(dist-1)
		elif dist < 0:
			for (x, y) in self._grid_piece():
				if x <= 0 or self.grid[x-1, y] != None:
					return
			else:
				self.piece['x'] -= 1
				self._move(dist+1)
	
	def _is_piece_overlaping(self):
		for (x, y) in self._grid_piece():
			if y == self.HEIGHT - 1:
				return True
			if (x, y+1) in self.grid and self.grid[x, y+1] != None:
				return True
		else:
			return False
	
	def _attach(self):
		for pos in self._grid_piece():
			self.grid[pos] = self.piece['color']
	
	def _clear_lines(self):
		lines = []
		for y in range(self.HEIGHT):
			for x in range(self.WIDTH):
				if self.grid[x, y] == None:
					break
			else:
				lines.append(y)
				for x in range(self.WIDTH):
					self.grid[x, 0] = None
		for line_y in lines:
			for x in range(self.WIDTH):
				for y in range(line_y-1, -1, -1):
					self.grid[x, y+1] = self.grid[x, y]
		lines = len(lines)
		self.score += self.SCORING[lines] * (self.level + 1)
		self.level += lines
		return lines
	
	def _new_piece(self):
		if self.next == None:
			self.piece = {
				'shape': list(choice(self._PIECES)),
				'x': self.WIDTH / 2 - 2,
				'y': -4,
				'color': choice(range(RED, WHITE)),
			}
			self._rotate(randint(0, 3))
		else:
			self.piece = self.next
		for _ in range(4):
			if not self._is_piece_overlaping():
				self.piece['y'] += 1
		for vec in self._grid_piece():
			if vec[1] < 0:
				self._game_over = True
		self.next = {
			'shape': list(choice(self._PIECES)),
			'x': self.WIDTH / 2 - 2,
			'y': - 4,
			'color': choice(range(RED, WHITE)),
		}
		self._rotate(randint(0, 3), self.next)
		
	@property
	def is_game_over(self):
		return self._game_over
	
	def __str__(self):
		corner = '+'
		top_bottom = '--'
		left_right = '|'
		filled = '[]'
		empty = '  '
		output = corner + top_bottom*self.WIDTH + corner + '\n'
		for y in range(self.HEIGHT):
			line = left_right
			if self._game_over and y == self.HEIGHT/4:
				line += color('  G A M E  O V E R  ', RED, WHITE)
			else:
				for x in range(self.WIDTH):
					if (x, y) in self._grid_piece():
						line += color(filled, self.piece['color'])
					elif self.grid[x, y] == None:
						line += empty
					else:
						line += color(filled, self.grid[x, y])
			line += left_right
			if y == self.HEIGHT / 2 - 3 or y == self.HEIGHT / 2 + 2:
				line += ' ' + corner + top_bottom*4 + corner
			elif self.HEIGHT / 2 - 3 < y < self.HEIGHT / 2 + 2:
				y -= self.HEIGHT / 2 - 2
				line += ' ' + left_right
				for x in range(4):
					if (x, y) in self.next['shape']:
						line += color(filled, self.next['color'])
					else:
						line += empty
				line += left_right
			output += line + '\n'
		output += corner + (top_bottom * self.WIDTH) + corner + '\n'
		output += f'Score: {self.score}'
		return output;


if __name__ == "__main__":
	game = Tetris()
	
	while not game.is_game_over:
		clear()
		print(game)
		inp = input(color('[in](move, rotate): ', BLUE))
		
		if inp in ('q', 'Q', 'quit', 'exit'):
			break
		
		try:
			move, rotate = map(int, inp.split(' '))
		except ValueError:
			try:
				move, rotate = int(inp), 0
			except ValueError:
				move, rotate = 0, 0
		
		try:
			game.step(rotate, move)
		except:
			print('Error, wrong value(s)!')
			input()
	clear()
	print(game)
