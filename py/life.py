#!/usr/bin/env python3
import random, time, copy

# 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 - fiengine token
# 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 - songs_token
# apython-345600 - google console cloud id

# cells contain row which then contain item. [row][x]
# treat 0 index as main draw
def RandomFill(draw, w, h):
	cells = []
	luck = 0
	for y in range(h):
	 	row = []
	 	for x in range(w):
	 		r = random.randint(0, 1)
	 		row.append(draw[r])

	 		if r: luck += 1
	 		
	 	cells.append(row)

	return cells, luck


def main():
	
	w = 70
	h = 20
	border = '-'
	outline = '0'
	blank = ' '
	cells, alive = RandomFill(list([outline, blank]), w, h)
	newcells = copy.deepcopy(cells)

	gen = 0

	try:
		while True:

			gen += 1

			print('Generation: %d \t\t Alive: %d' % (gen, alive))
			print(border * w)

			for y, row in enumerate(cells):
				for x in range(len(row)):

					print(cells[y][x], end='')

					top = (y - 1) % h
					bottom = (y + 1) % h
					right = (x + 1) % w
					left = (x - 1) % w
					adjacent = 0

					box = [cells[top][left], cells[top][x], cells[top][right],
						   cells[y][left], cells[y][x], cells[y][right],
						   cells[bottom][left], cells[bottom][x], cells[bottom][right]]

					for i in box:
						if i == outline: adjacent += 1

					if not((cells[y][x] == outline) and (adjacent == 2 or adjacent == 3)): newcells[y][x] = blank
					if (cells[y][x] == blank and adjacent == 3): newcells[y][x] = outline

				print()

			print(border * w)

			cells = copy.deepcopy(newcells)
			time.sleep(0.7)


	except KeyboardInterrupt:
		pass


if __name__ == '__main__':
	main() 