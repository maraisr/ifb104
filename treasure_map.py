# -----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n8911495
#    Student name: Petrus Marais Rossouw
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
# --------------------------------------------------------------------#


# -----Task Description-----------------------------------------------#
#
#  TREASURE MAP
#
#  This assignment tests your skills at processing data stored in
#  lists, creating reusable code and following instructions to display
#  a complex visual image.  The incomplete Python program below is
#  missing a crucial function, "follow_path".  You are required to
#  complete this function so that when the program is run it traces
#  a path on the screen, drawing "tokens" to indicate discoveries made
#  along the way, while using data stored in a list to determine the
#  steps to be taken.  See the instruction sheet accompanying this
#  file for full details.
#
#  Note that this assignment is in two parts, the second of which
#  will be released only just before the final deadline.  This
#  template file will be used for both parts and you will submit
#  your final solution as a single Python 3 file, whether or not you
#  complete both parts of the assignment.
#
# --------------------------------------------------------------------#


# -----Preamble-------------------------------------------------------#
#
# This section imports necessary functions and defines constant
# values used for creating the drawing canvas.  You should not change
# any of the code in this section.
#

# Import the functions needed to complete this assignment.  You
# should not need to use any other modules for your solution.  In
# particular, your solution must not rely on any non-standard Python
# modules that need to be downloaded and installed separately,
# because the markers will not have access to such modules.

from turtle import *
from math import *
from random import *
# To the person marking this, I was given permission to add this import.
from functools import reduce, partial

# Define constant values used in the main program that sets up
# the drawing canvas.  Do not change any of these values.

grid_size = 100  # pixels
num_squares = 7  # to create a 7x7 map grid
margin = 50  # pixels, the size of the margin around the grid
legend_space = 400  # pixels, the space to leave for the legend
window_height = grid_size * num_squares + margin * 2
window_width = grid_size * num_squares + margin + legend_space
font_size = 18  # size of characters for the coords
starting_points = ['Top left', 'Top right', 'Centre',
                   'Bottom left', 'Bottom right']


#
# --------------------------------------------------------------------#


# -----Functions for Creating the Drawing Canvas----------------------#
#
# The functions in this section are called by the main program to
# manage the drawing canvas for your image.  You should not change
# any of the code in this section.  (Very keen students are welcome
# to draw their own background, provided they do not change the map's
# grid or affect the ability to see it.)
#

# Set up the canvas and draw the background for the overall image
def create_drawing_canvas():
	# Set up the drawing window with enough space for the grid and
	# legend
	setup(window_width, window_height)
	setworldcoordinates(-margin, -margin, window_width - margin,
	                    window_height - margin)

	# Draw as quickly as possible
	tracer(False)

	# Choose a neutral background colour (if you want to draw your
	# own background put the code here, but do not change any of the
	# following code that draws the grid)
	bgcolor('light grey')

	# Get ready to draw the grid
	penup()
	color('slate grey')
	width(2)

	# Draw the horizontal grid lines
	setheading(0)  # face east
	for y_coord in range(0, (num_squares + 1) * grid_size, grid_size):
		penup()
		goto(0, y_coord)
		pendown()
		forward(num_squares * grid_size)

	# Draw the vertical grid lines
	setheading(90)  # face north
	for x_coord in range(0, (num_squares + 1) * grid_size, grid_size):
		penup()
		goto(x_coord, 0)
		pendown()
		forward(num_squares * grid_size)

	# Draw each of the labels on the x axis
	penup()
	y_offset = -27  # pixels
	for x_coord in range(0, (num_squares + 1) * grid_size, grid_size):
		goto(x_coord, y_offset)
		write(str(x_coord), align='center',
		      font=('Arial', font_size, 'normal'))

	# Draw each of the labels on the y axis
	penup()
	x_offset, y_offset = -5, -10  # pixels
	for y_coord in range(0, (num_squares + 1) * grid_size, grid_size):
		goto(x_offset, y_coord + y_offset)
		write(str(y_coord), align='right',
		      font=('Arial', font_size, 'normal'))

	# Reset everything ready for the student's solution
	pencolor('black')
	width(1)
	penup()
	home()
	tracer(True)


# End the program and release the drawing canvas to the operating
# system.  By default the cursor (turtle) is hidden when the
# program ends - call the function with False as the argument to
# prevent this.
def release_drawing_canvas(hide_cursor=True):
	tracer(True)  # ensure any drawing still in progress is displayed
	if hide_cursor:
		hideturtle()
	done()


#
# --------------------------------------------------------------------#


# -----Test Data for Use During Code Development----------------------#
#
# The "fixed" data sets in this section are provided to help you
# develop and test your code.  You can use them as the argument to
# the follow_path function while perfecting your solution.  However,
# they will NOT be used to assess your program.  Your solution will
# be assessed using the random_path function appearing below.  Your
# program must work correctly for any data set that can be generated
# by the random_path function.
#
# Each of the data sets is a list of instructions expressed as
# triples.  The instructions have two different forms.  The first
# instruction in the data set is always of the form
#
#     ['Start', location, token_number]
#
# where the location may be 'Top left', 'Top right', 'Centre',
# 'Bottom left' or 'Bottom right', and the token_number is an
# integer from 0 to 4, inclusive.  This instruction tells us where
# to begin our treasure hunt and the token that we find there.
# (Every square we visit will yield a token, including the first.)
#
# The remaining instructions, if any, are all of the form
#
#     [direction, number_of_squares, token_number]
#
# where the direction may be 'North', 'South', 'East' or 'West',
# the number_of_squares is a positive integer, and the token_number
# is an integer from 0 to 4, inclusive.  This instruction tells
# us where to go from our current location in the grid and the
# token that we will find in the target square.  See the instructions
# accompanying this file for examples.
#

# Some starting points - the following fixed paths just start a path
# with each of the five tokens in a different location


fixed_path_0 = [['Start', 'Top left', 0]]
fixed_path_1 = [['Start', 'Top right', 1]]
fixed_path_2 = [['Start', 'Centre', 2]]
fixed_path_3 = [['Start', 'Bottom left', 3]]
fixed_path_4 = [['Start', 'Bottom right', 4]]

# Some miscellaneous paths which encounter all five tokens once

fixed_path_5 = [['Start', 'Top left', 0], ['East', 1, 1], ['East', 1, 2],
                ['East', 1, 3], ['East', 1, 4]]
fixed_path_6 = [['Start', 'Bottom right', 0], ['West', 1, 1], ['West', 1, 2],
                ['West', 1, 3], ['West', 1, 4]]
fixed_path_7 = [['Start', 'Centre', 4], ['North', 2, 3], ['East', 2, 2],
                ['South', 4, 1], ['West', 2, 0]]

# A path which finds each token twice

fixed_path_8 = [['Start', 'Bottom left', 1], ['East', 5, 2],
                ['North', 2, 3], ['North', 4, 0], ['South', 3, 2],
                ['West', 4, 0], ['West', 1, 4],
                ['East', 3, 1], ['South', 3, 4], ['East', 1, 3]]

# Some short paths

fixed_path_9 = [['Start', 'Centre', 0], ['East', 3, 2],
                ['North', 2, 1], ['West', 2, 3],
                ['South', 3, 4], ['West', 4, 1]]

fixed_path_10 = [['Start', 'Top left', 2], ['East', 6, 3], ['South', 1, 0],
                 ['South', 1, 0], ['West', 6, 2], ['South', 4, 3]]

fixed_path_11 = [['Start', 'Top left', 2], ['South', 1, 0], ['East', 2, 4],
                 ['South', 1, 1], ['East', 3, 4], ['West', 1, 3],
                 ['South', 2, 0]]

# Some long paths

fixed_path_12 = [['Start', 'Top right', 2], ['South', 4, 0],
                 ['South', 1, 1], ['North', 3, 4], ['West', 4, 0],
                 ['West', 2, 0], ['South', 3, 4], ['East', 2, 3],
                 ['East', 1, 1], ['North', 3, 2], ['South', 1, 3],
                 ['North', 3, 2], ['West', 1, 2], ['South', 3, 4],
                 ['East', 3, 0], ['South', 1, 1]]

fixed_path_13 = [['Start', 'Top left', 1], ['East', 5, 3], ['West', 4, 2],
                 ['East', 1, 3], ['East', 2, 2], ['South', 5, 1],
                 ['North', 2, 0], ['East', 2, 0], ['West', 1, 1],
                 ['West', 5, 0], ['South', 1, 3], ['East', 3, 0],
                 ['East', 1, 4], ['North', 3, 0], ['West', 1, 4],
                 ['West', 3, 1], ['South', 4, 1], ['East', 5, 1],
                 ['West', 4, 0]]

# "I've been everywhere, man!" - this path visits every square in
# the grid, with randomised choices of tokens

fixed_path_99 = [['Start', 'Top left', randint(0, 4)]] + \
                [['East', 1, randint(0, 4)] for step in range(6)] + \
                [['South', 1, randint(0, 4)]] + \
                [['West', 1, randint(0, 4)] for step in range(6)] + \
                [['South', 1, randint(0, 4)]] + \
                [['East', 1, randint(0, 4)] for step in range(6)] + \
                [['South', 1, randint(0, 4)]] + \
                [['West', 1, randint(0, 4)] for step in range(6)] + \
                [['South', 1, randint(0, 4)]] + \
                [['East', 1, randint(0, 4)] for step in range(6)] + \
                [['South', 1, randint(0, 4)]] + \
                [['West', 1, randint(0, 4)] for step in range(6)] + \
                [['South', 1, randint(0, 4)]] + \
                [['East', 1, randint(0, 4)] for step in range(6)]


# If you want to create your own test data sets put them here

#
# --------------------------------------------------------------------#


# -----Function for Assessing Your Solution---------------------------#
#
# The function in this section will be used to assess your solution.
# Do not change any of the code in this section.
#
# The following function creates a random data set specifying a path
# to follow.  Your program must work for any data set that can be
# returned by this function.  The results returned by calling this
# function will be used as the argument to your follow_path function
# during marking.  For convenience during code development and
# marking this function also prints the path to be followed to the
# shell window.
#
# Note: For brevity this function uses some Python features not taught
# in IFB104 (dictionaries and list generators).  You do not need to
# understand this code to complete the assignment.
#
def random_path(print_path=True):
	# Select one of the five starting points, with a random token
	path = [['Start', choice(starting_points), randint(0, 4)]]
	# Determine our location in grid coords (assuming num_squares is odd)
	start_coords = {'Top left': [0, num_squares - 1],
	                'Bottom left': [0, 0],
	                'Top right': [num_squares - 1, num_squares - 1],
	                'Centre': [num_squares // 2, num_squares // 2],
	                'Bottom right': [num_squares - 1, 0]}
	location = start_coords[path[0][1]]
	# Keep track of squares visited
	been_there = [location]
	# Create a path up to 19 steps long (so at most there will be 20 tokens)
	for step in range(randint(0, 19)):
		# Find places to go in each possible direction, calculating both
		# the new grid square and the instruction required to take
		# us there
		go_north = [[[location[0], new_square],
		             ['North', new_square - location[1], token]]
		            for new_square in range(location[1] + 1, num_squares)
		            for token in [0, 1, 2, 3, 4]
		            if not ([location[0], new_square] in been_there)]
		go_south = [[[location[0], new_square],
		             ['South', location[1] - new_square, token]]
		            for new_square in range(0, location[1])
		            for token in [0, 1, 2, 3, 4]
		            if not ([location[0], new_square] in been_there)]
		go_west = [[[new_square, location[1]],
		            ['West', location[0] - new_square, token]]
		           for new_square in range(0, location[0])
		           for token in [0, 1, 2, 3, 4]
		           if not ([new_square, location[1]] in been_there)]
		go_east = [[[new_square, location[1]],
		            ['East', new_square - location[0], token]]
		           for new_square in range(location[0] + 1, num_squares)
		           for token in [0, 1, 2, 3, 4]
		           if not ([new_square, location[1]] in been_there)]
		# Choose a free square to go to, if any exist
		options = go_north + go_south + go_east + go_west
		if options == []:  # nowhere left to go, so stop!
			break
		target_coord, instruction = choice(options)
		# Remember being there
		been_there.append(target_coord)
		location = target_coord
		# Add the move to the list of instructions
		path.append(instruction)
	# To assist with debugging and marking, print the list of
	# instructions to be followed to the shell window
	print('Welcome to the Treasure Hunt!')
	print('Here are the steps you must follow...')
	for instruction in path:
		print(instruction)
	# Return the random path
	return path


#
# --------------------------------------------------------------------#


# -----Student's Solution---------------------------------------------#
#
#  Complete the assignment by replacing the dummy function below with
#  your own "follow_path" function.
#

# To the person marking this, I can see pydoc is a thing, however its a syntax im
# not used to at all - however I've tried to adapt, javadoc/jsdoc/tsdoc etc... 
# to Python.

# @description
# Being given a data set, containing a collection of bearings, and a marker, this
# method, follows that path, drawing them on the plane, as well as print a legend
# for the users' viewing. Treat this method as the "entry" point to the app
#
# @param {path: [string, number, number][]} a collection of bearings
#
# @returns void
def follow_path(path):
	start_location = path.pop(0)

	# First we iterate through our list of "unnormalized paths", and
	# convert them to (x, y) coordinates, attributing the
	# token we must draw. With the nature of the input, the start is
	# delt with far differently than the rest of the locations. So
	# we'll deal with that first.

	starting_node = create_node(
		# we need to translate the "Top left" etc.. to actual coordinates
		get_starting_coord(start_location[1]),
		# the create_node also requires the type of token
		start_location[2]
	)

	# our main token "draw_stack", we need to reduce here because unlike
	# other popular languages, map doesn't give us access to accumulated iterable
	draw_stack = reduce(
		# passing in the function we wish to execute at every iteration
		walk_path_reduce_fn,
		# the list we wish to iterate
		path,
		# and the list we are reducing into, in our case, a list with the start_node
		[starting_node]
	)

	draw_legend(draw_stack)

	# Once we've drawn our legend, we simply iterate over our stack, and draw!
	for node in draw_stack:
		# takes our turtle to the "square"
		goto((node.get('x') * grid_size),
		     (node.get('y') * grid_size))

		node.get('render_fn')()  # executes this node's draw method


# @description
# A method that takes the result (the current accumulated list), and item, the current
# item being inspected. This method looks at the accumulated context to solve for,
# the current items coordinates.
#
# @param {result: node[]} the current accumulated list
# @param {item: [string, number, number]} the current item being inspected,
#       the [direction, steps_to_take, token_to_use]
#
# @returns [node[]] a accumulated list of create_node function outputs
#
# @see #create_node
def walk_path_reduce_fn(result, item):
	direction, steps_to_take, token_to_use = item;

	previous_node = result[len(result) - 1]

	# Converts the "North", "South" etc strings to cordinate deltas @see #get_compass_to_coordinates_delta
	coord_delta = get_compass_to_coordinates_delta(direction)

	new_node = create_node(
		reduce(
			lambda deltaResult, deltaItem: [
				# overlays the current coordinates, with whatever we need to adjust it by
				sum(x) for x in zip(deltaResult, coord_delta)
			],
			range(steps_to_take),  # purely to iterate the number of steps to take
			# and the list we are reducing into, the previous nodes x,y coordinates
			[previous_node.get('x'), previous_node.get('y')]
		),
		token_to_use
	)

	return result + [new_node]


# @description
# A method that translates our starting location indicators to coordinates.
#
# @param {verb: string} a string with values "Top left", "Top right", "Centre", "Bottom left", "Bottom right"
#
# @returns [number[]] a coordinate tuple
def get_starting_coord(verb):
	# To the person marking this, this is the best I could come up
	# in terms of a switch case. Forgiveness is a virtue!
	return {
		'Top left': [0, num_squares - 1],
		'Top right': [num_squares - 1, num_squares - 1],
		'Centre': [(num_squares - 1) / 2, (num_squares - 1) / 2],
		'Bottom left': [0, 0],
		'Bottom right': [(num_squares - 1), 0]
	}.get(verb)


# @description
# A method that translates our direction indicators to coordinates deltas. For
# use to zip over a pre-existing cordinate tuple.
#
# @param {verb: string} a string with values "North", "South", "East", "West"
#
# @returns [number[]] a coordinate tuple delta
def get_compass_to_coordinates_delta(verb):
	# To the person marking this, this is the best I could come up
	# in terms of a switch case. Forgiveness is a virtue!
	return {
		'North': [0, 1],
		'South': [0, -1],
		'East': [1, 0],
		'West': [-1, 0]
	}.get(verb)


# @description
# A method that gets give a cordinate tuple, and produces an object, complete with
# its x, and y cordinate. And a function to execute to draw it's attributed token.
#
# @param {coord: [number, number]} a cordinate tuple
# @param {token_type: number} a number that maps directly to our token types
#
# @returns [{x: number, y: number, token_type: number, render_fn: lambda}] an object to represent the node
def create_node(coords, token_type):
	x, y = coords;
	return {
		'x': x,
		'y': y,
		'token_type': token_type,
		# the use of a lambda, becuase I want the scope to remain in tact here
		'render_fn': lambda: get_token_draw_method_from_type(token_type)()
	}


# ---- Legend things ----
legend_title_font_size = 14
legend_padding = 20
legend_token_line_height = grid_size


# @description
# As the name suggests, this method draws the legend. Nothing more, nothing less.
#
# @returns [void]
def draw_legend(draw_stack):
	tokens = get_token_draw_methods()

	# A collection of areas we need to paint on the legend, from top to bottom.
	# ie, title, then icon 1, then icon 2 etc...
	# Each render method, when called will be called with the legend, width / height
	blocks = ([
		          # the title
		          {
			          'height': legend_title_font_size + legend_padding,
			          'render_fn': partial(draw_legend_title, len(draw_stack))
		          }
	          ]
	          # we then append the tokens, because we compute them
	          + list(
				map(
					lambda node: {
						'height': legend_token_line_height,
						'render_fn': partial(
							draw_legend_token,
							node[1],
							# to find the number of types of tokens we see in our draw_stack
							len(list(filter(lambda item: item.get(
								'token_type') == node[0], draw_stack)))
						)
					},
					# enumerate so we get access to the index ie the token_type
					enumerate(tokens)
				)
			))

	# left offset = (square count * grid size) + margin
	# width = window width - left offset - margin
	legend_width = (window_width - (margin * 2 + (num_squares *
	                                              grid_size)) - margin)

	# height of all the blocks + padding per block - 1 + padding for legend
	legend_height = (sum(map(lambda item: item.get('height'), blocks))
	                 + (legend_padding * (len(blocks) - 1)) + legend_padding * 2)

	# Take the turtle to the top corner
	draw_legend_reset_cords(legend_width, legend_height)

	draw_legend_background(legend_width, legend_height)

	# we need to iterate over our blocks, and draw them
	for index, block in enumerate(blocks):
		# always reset, as the coords might be different from inner render methods
		draw_legend_reset_cords(legend_width, legend_height)

		# We need to know how much to offset our y, so we find the previous nodes' height accumulated 
		offset_height = (sum(map(lambda item: item.get('height'), blocks[:index]))
		                 # we also want to add some padding between our items
		                 + legend_padding * index)

		# finally tell the turtle to go there
		sety((pos()[1] - offset_height) - legend_padding)

		# and run our render method for this item
		block.get('render_fn')(legend_width, legend_height)


# @description
# A method to draw the legends background.
#
# @returns [void]
def draw_legend_background(legend_width, legend_height):
	# TODO: Maybe add some rounded corners
	# TODO : Style this
	pencolor("blue")
	fillcolor("white")
	setheading(90)
	begin_fill()
	pendown()
	right(90)
	forward(legend_width)
	right(90)
	forward(legend_height)
	right(90)
	forward(legend_width)
	right(90)
	forward(legend_height)
	penup()
	end_fill()


# @description
# Our legend needs a title, this method draws that.
#
# @returns [void]
def draw_legend_title(total_found, legend_width, legend_height):
	# Move the turtle to the middle of the legend
	goto(
		pos()[0] + legend_width // 2,
		pos()[1] - (legend_title_font_size + (legend_title_font_size // 2))
	)

	# TODO: clean up visual, set colours fontsizes, etc...

	write(
		'%d %s Found!' % (total_found, "Flag" +
		                  ('s' if total_found > 1 else '')),
		False,
		align="center",
		font=('Arial', legend_title_font_size, 'bold')
	)


# @description
# A method to draw each of our tokens, complete with a title and the token itself.
#
# @returns [void]
def draw_legend_token(token, number_of_type, legend_width, legend_height):
	token_render_fn, token_name = token;

	goto(
		pos()[0] + legend_padding,
		pos()[1] - grid_size
	)

	root_pos = pos()  # save pos to come back to later

	title_font_size = 12

	# Draw title
	goto(
		root_pos[0] + grid_size + legend_padding,
		root_pos[1] + (grid_size // 2) - (title_font_size // 2)
	)

	# TODO: clean up visual, set colours fontsizes, etc...

	write('%s (%d)' % (token_name, number_of_type), False, align="left", font=(
		'Arial', title_font_size, 'normal'))

	goto(*root_pos)

	call_and_reset_after_exec(token_render_fn)


# @description
# Resets the turtle's coordinates to the top, left of the legend.
#
# @param {legend_width} the width of the legend
# @param {legend_height} the height of the legend
#
# @returns void
def draw_legend_reset_cords(legend_width, legend_height):
	goto(
		((num_squares * grid_size)) + margin,
		((num_squares * grid_size) // 2) + (legend_height // 2)
	)


# @description
# A util method that wraps another method to capture the turtle's position, 
# executes the method, and resets the turtles position back to what it was before
# the execution. 
#
# @returns
def call_and_reset_after_exec(fn):
	original_pos = pos()
	fn()
	goto(*original_pos)


# @description
# A method that returns a token draw method for a given token_type
#
# @param {token_type: number} a number that maps to a draw method
#
# @returns [(function -> void)[]] a token drawn method
def get_token_draw_method_from_type(token_type):
	return get_token_draw_methods()[token_type][0]


# @description
# With the philosophy, data as a function, and for data immutability - we will
# return a new collection of token draw methods.
#
# @returns [(function -> void)[]] a collection of tuples with token draw method, to pretty name
def get_token_draw_methods():
	return [
		[draw_token_canada, "Canada"],
		[draw_token_china, "China"],
		[draw_token_south_africa, "South Africa"],
		[draw_token_turkey, "Turkey"],
		[draw_token_nepal, "Nepal"]
	]


# ---- Token draw methods ----
# Thank you to the guys over at https://www.flaticon.com/packs/international-flags-4
# for their flag designs.

def reset_turtle():
	penup()
	color("black")
	fillcolor("white")
	seth(90)


# @description
# TODO
#
# @returns
def draw_token_canada():
	write("canada")
	


# @description
# TODO
#
# @returns
def draw_token_nepal():
	write("nepal")


# @description
# TODO
#
# @returns
def draw_token_china():
	write("china")


# @description
# TODO
#
# @returns
def draw_token_south_africa():
	reset_turtle()
	origin_x, origin_y = pos()

	bg_red = '#e03c31'
	bg_blue = '#001489'
	bg_green = '#007749'
	bg_grey =  '#000000'
	bg_yellow = '#ffb81c'
	
	# start with a white background
	call_and_reset_after_exec(partial(draw_square, "white"))

	# draw the red thing
	fillcolor(bg_red)
	seth(90)
	fd(grid_size)
	right(90)
	fd(10)
	begin_fill()
	right(45)
	fd(50)
	seth(0)
	fd(55)
	seth(90)
	fd(36)
	end_fill()

	# draw the blue thing
	goto(origin_x, origin_y)
	fillcolor(bg_blue)
	seth(0)
	fd(10)
	begin_fill()
	right(-45)
	fd(50)
	seth(0)
	fd(55)
	seth(90)
	fd(-36)
	end_fill()

	# draw the green thing
	goto(origin_x, origin_y)
	fillcolor(bg_green)
	seth(0)
	fd(5)
	begin_fill()
	right(-45)
	fd(55)
	seth(0)
	fd(56)
	seth(90)
	fd(22)
	seth(180)
	fd(56)
	right(45)
	fd(56)
	seth(180)
	fd(4)
	seth(270)
	fd(grid_size)
	end_fill()

	# draw yellow triangle
	goto(origin_x, origin_y)
	fillcolor(bg_yellow)
	seth(90)
	begin_fill()
	fd(20)
	right(45)
	fd(40)
	right(-90)
	fd(40)
	end_fill()

	# draw black triangle
	goto(origin_x, origin_y)
	fillcolor(bg_grey)
	seth(90)
	begin_fill()
	fd(26)
	right(45)
	fd(32)
	right(-90)
	fd(32)
	end_fill()


# @description
# Draws the Turkish flag
#
# @returns [void]
def draw_token_turkey():
	reset_turtle()
	origin_x, origin_y = pos()

	bg_colour = '#e30a17'

	# draw background
	call_and_reset_after_exec(partial(draw_square, bg_colour))

	pu()

	# draw white circle
	circle_size = 24;

	goto(origin_x + circle_size + 10, origin_y + grid_size / 2 + circle_size)

	fillcolor("white")
	begin_fill()
	circle(circle_size)
	end_fill()

	# draw smaller circle
	smaller_circle_size = circle_size * 0.8;

	# Please excuse the magic numbers here
	goto(pos()[0] + 9, pos()[1] - 5)

	fillcolor(bg_colour)
	begin_fill()
	circle(smaller_circle_size)
	end_fill()

	# draw star
	star_size = 8

	goto(pos()[0] + 10, pos()[1] - (circle_size - star_size))

	draw_star(star_size, "white")


# TODO : COMMENT ME
def draw_star(size, colour):
	fillcolor(colour)
	seth(90)
	begin_fill()
	for side in range(5):
		fd(size)
		right(120)
		fd(size)
		right(72 - 120)
	end_fill()
	
# TODO : COMMENT ME
def draw_square(color):
	fillcolor(color)
	seth(90)
	begin_fill()
	forward(grid_size)
	right(90)
	forward(grid_size)
	right(90)
	forward(grid_size)
	right(90)
	forward(grid_size)
	end_fill()


# --------------------------------------------------------------------#

# -----Main Program---------------------------------------------------#
#
# This main program sets up the background, ready for you to start
# drawing your solution.  Do not change any of this code except
# as indicated by the comments marked '*****'.
#


# Set up the drawing canvas
create_drawing_canvas()

# Control the drawing speed
# ***** Modify the following argument if you want to adjust
# ***** the drawing speed
speed('fastest')

# Decide whether or not to show the drawing being done step-by-step
# ***** Set the following argument to False if you don't want to wait
# ***** forever while the cursor moves around the screen
tracer(False)

# Give the drawing canvas a title
# ***** Replace this title with a description of your solution's theme
# ***** and its tokens
title("Do you know your global flags?")

# Call the student's function to follow the path
# ***** While developing your program you can call the follow_path
# ***** function with one of the "fixed" data sets, but your
# ***** final solution must work with "random_path()" as the
# ***** argument to the follow_path function.  Your program must
# ***** work for any data set that can be returned by the
# ***** random_path function.
#follow_path([["Start", "Centre", 1]])  # <-- used for code development only, not marking
follow_path(random_path())  # <-- used for assessment

# Exit gracefully
# ***** Change the default argument to False if you want the
# ***** cursor (turtle) to remain visible at the end of the
# ***** program as a debugging aid
release_drawing_canvas()

#
# --------------------------------------------------------------------#
