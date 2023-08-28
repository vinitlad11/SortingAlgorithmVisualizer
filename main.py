import pygame
import random
import math
pygame.init()


class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 51, 204, 51
	RED = 255, 0, 0
	BLUE = 204, 236, 255
	BACKGROUND_COLOR = BLUE
	# BACKGROUND_COLOR = 51, 153, 255
	# BACKGROUND_COLOR = BLACK

	GRADIENTS = [   # to change the colour of the array bars
		(255, 153, 0),
		(255, 204, 0),
		(255, 204, 153)

		# (218, 160, 63),
		# (97, 98, 71)

		# (255, 255, 0),
		# (255, 255, 102),
		# (255, 255, 153)
	]

	# FONT = pygame.font.SysFont('comicsans', 20)  # change font here
	# LARGE_FONT = pygame.font.SysFont('comicsans', 30)
	# FONT = pygame.font.SysFont('Jokerman', 20)
	# LARGE_FONT = pygame.font.SysFont('Jokerman', 30)
	FONT = pygame.font.SysFont('Times New Roman', 21)
	LARGE_FONT = pygame.font.SysFont('Times New Roman', 31)
	# FONT = pygame.font.SysFont('Algerian', 20)
	# LARGE_FONT = pygame.font.SysFont('Algerian', 30)

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Fun with Algorithm Visualizer")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor(
		    (self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.WHITE)

	title = draw_info.LARGE_FONT.render(
	    f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 50, draw_info.GREEN)
	# for placing the controls
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 0))

	controls = draw_info.FONT.render(
	    "R - Reset | SPACE - Start Sorting | P - Pause | A - Ascending | D - Descending", 50, draw_info.BLACK)
	# for placing the controls
	draw_info.window.blit(
	    controls, (draw_info.width/2 - controls.get_width()/2, 45))

	sorting = draw_info.FONT.render(
	    "I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort | Q - Quick Sort", 50, draw_info.BLACK)
	# for placing the controls
	draw_info.window.blit(
	    sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
						(draw_info.width + 4) - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):  # for drawing every bar from the list numbers
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		# to change the number of different colour array bars
		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i]

		pygame.draw.rect(draw_info.window, color, (x, y,
		                 draw_info.block_width, draw_info.height), 0, 8, -1, -1, -1, -1)

	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst


def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        pos = i  # positon of an element

        for j in range(i+1, len(lst)):
            if lst[j] <= lst[pos] and ascending:
                pos = j
            if lst[j] > lst[pos] and not ascending:
                pos = j

        lst[i], lst[pos] = lst[pos], lst[i]
        draw_list(draw_info, {pos: draw_info.RED, i: draw_info.GREEN}, True)
        yield True    # to return conttrol to the calling loop so we can give another input if we want to

    return lst

def quick_sort(draw_info, ascending=True):
	arr = draw_info.lst
    # Create a stack to simulate recursion
	stack = []
    # Push the initial range onto the stack
	stack.append((0, len(arr) - 1))

	while len(stack) > 0:
        # Pop the next range from the stack
		start, end = stack.pop()

        # If the range is less than 2, it's already sorted
		if end - start < 1:
			continue

        # Choose the pivot element
		pivot = arr[end]

        # Partition the array
		i = start - 1
		for j in range(start, end):
			if arr[j] <= pivot and ascending:
				i += 1
				arr[i], arr[j] = arr[j], arr[i]
			if arr[j] >= pivot and  not ascending:
				i += 1
				arr[i], arr[j] = arr[j], arr[i]

		arr[i+1], arr[end] = arr[end], arr[i+1]
		draw_list(draw_info, {i+1: draw_info.GREEN, end: draw_info.RED}, True)
		yield True

        # Push the two sub-ranges onto the stack
		stack.append((start, i))
		stack.append((i+2, end))
		
	return arr

#
#
#
#
#
#
def merge_sort(draw_info, ascending=True):
	arr = draw_info.lst
    # Create a list of single-element sublists
	sublists = [[num] for num in arr]
    
    # Merge adjacent sublists until there is only one left
	while len(sublists) > 1:
		merged = []

		for i in range(0, len(sublists), 2):

			left = sublists[i]
			right = sublists[i+1] if i+1 < len(sublists) else []

			for i in range(len(left)):
				draw_list(draw_info, {left[i]: draw_info.GREEN}, True)
				yield True
			for j in range(len(right)):
				draw_list(draw_info, {right[j]: draw_info.RED}, True)
				yield True

			result = []
			i = j = 0
			
			if ascending:
				while i < len(left) and j < len(right):
					if left[i] < right[j]:
						result.append(left[i])
						draw_list(draw_info, {left[i]: draw_info.GREEN}, True)
						yield True
						i += 1
					else:
						result.append(right[j])
						draw_list(draw_info, {right[j]: draw_info.RED}, True)
						yield True
						j += 1

			else:
				while i < len(left) and j < len(right):
					if left[i] > right[j]:
						result.append(left[i])
						draw_list(draw_info, {left[i]: draw_info.GREEN}, True)
						yield True
						i += 1
					else:
						result.append(right[j])
						draw_list(draw_info, {right[j]: draw_info.RED}, True)
						yield True
						j += 1

			result = result + left[i:]
			result = result + right[j:]
			merged.append(result)

		sublists = merged
		for i in range(len(sublists[0])):
				draw_list(draw_info, {sublists[0][i]: draw_info.BLACK}, True)
				yield True
	# Return the final sorted list
	return sublists[0]
#
#
#
#
#
#

def main():
	run = True
	clock = pygame.time.Clock()

	n = 36   # changes the size of the array
	min_val = 0
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(1250, 668, lst)
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(20)  # to change the speed of sorting and controls on top of the window


		if sorting:  # execution flow comes here when 'yield' is encountered in sorting function
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_p and sorting == True:  # to pause the sorting
				sorting = False
			elif event.key == pygame.K_a  and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"
			elif event.key == pygame.K_q and not sorting:
				sorting_algorithm = quick_sort
				sorting_algo_name = "Quick Sort"
			elif event.key == pygame.K_m and not sorting:
				sorting_algorithm = merge_sort
				sorting_algo_name = "Merge Sort"


	pygame.quit()


if __name__ == "__main__":
	main()