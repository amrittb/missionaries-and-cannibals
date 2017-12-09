import math
from anytree import Node, RenderTree

class State():
	def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight):
		self.cannibalLeft = cannibalLeft
		self.missionaryLeft = missionaryLeft
		self.boat = boat
		self.cannibalRight = cannibalRight
		self.missionaryRight = missionaryRight
		self.parent = None
		self.tree_node = Node(str(self))

	def is_goal(self):
		if self.cannibalLeft == 0 and self.missionaryLeft == 0:
			return True
		else:
			return False

	def is_valid(self):
		if self.missionaryLeft >= 0 and self.missionaryRight >= 0 \
                   and self.cannibalLeft >= 0 and self.cannibalRight >= 0 \
                   and (self.missionaryLeft == 0 or self.missionaryLeft >= self.cannibalLeft) \
                   and (self.missionaryRight == 0 or self.missionaryRight >= self.cannibalRight):
			return True
		else:
			return False

	def set_tree_parent(self, parent):
		self.tree_node.parent = parent.get_tree_node()

	def get_tree_node(self):
		return self.tree_node

	def __str__(self):
		return "("+ str(self.missionaryLeft) + "," + str(self.cannibalLeft) + "," + ("0" if (self.boat == "left") else "1") + ")" + (" <- Goal State" if self.is_goal() else "")

	def __eq__(self, other):
		return self.cannibalLeft == other.cannibalLeft and self.missionaryLeft == other.missionaryLeft \
                   and self.boat == other.boat and self.cannibalRight == other.cannibalRight \
                   and self.missionaryRight == other.missionaryRight

	def __hash__(self):
		return hash((self.cannibalLeft, self.missionaryLeft, self.boat, self.cannibalRight, self.missionaryRight))

def get_children(cur_state):
	children = [];
	if cur_state.boat == 'left':
		## Two missionaries cross left to right.
		new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft - 2, 'right',
                                  cur_state.cannibalRight, cur_state.missionaryRight + 2)
		if new_state.is_valid():
			new_state.parent= cur_state
			children.append(new_state)
		
		## Two cannibals cross left to right.
		new_state = State(cur_state.cannibalLeft - 2, cur_state.missionaryLeft, 'right',
                                  cur_state.cannibalRight + 2, cur_state.missionaryRight)
		if new_state.is_valid():
			new_state.parent= cur_state
			children.append(new_state)
		
		## One missionary and one cannibal cross left to right.
		new_state = State(cur_state.cannibalLeft - 1, cur_state.missionaryLeft - 1, 'right',
                                  cur_state.cannibalRight + 1, cur_state.missionaryRight + 1)
		if new_state.is_valid():
			new_state.parent= cur_state
			children.append(new_state)
		
		## One missionary crosses left to right.
		new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft - 1, 'right',
                                  cur_state.cannibalRight, cur_state.missionaryRight + 1)
		if new_state.is_valid():
			new_state.parent= cur_state
			children.append(new_state)
		
		## One cannibal crosses left to right.
		new_state = State(cur_state.cannibalLeft - 1, cur_state.missionaryLeft, 'right',
                                  cur_state.cannibalRight + 1, cur_state.missionaryRight)
		if new_state.is_valid():
			new_state.parent= cur_state
			children.append(new_state)
	else:
		
		## Two missionaries cross right to left.
		new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft + 2, 'left',
                                  cur_state.cannibalRight, cur_state.missionaryRight - 2)
		if new_state.is_valid():
			new_state.parent= cur_state
			children.append(new_state)
		
		## Two cannibals cross right to left.
		new_state = State(cur_state.cannibalLeft + 2, cur_state.missionaryLeft, 'left',
                                  cur_state.cannibalRight - 2, cur_state.missionaryRight)
		if new_state.is_valid():
			new_state.parent= cur_state
			children.append(new_state)
		
		## One missionary and one cannibal cross right to left.
		new_state = State(cur_state.cannibalLeft + 1, cur_state.missionaryLeft + 1, 'left',
                                  cur_state.cannibalRight - 1, cur_state.missionaryRight - 1)
		if new_state.is_valid():
			new_state.parent= cur_state
			children.append(new_state)
		
		## One missionary crosses right to left.
		new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft + 1, 'left',
                                  cur_state.cannibalRight, cur_state.missionaryRight - 1)
		if new_state.is_valid():
			new_state.parent= cur_state
			children.append(new_state)

		## One cannibal crosses right to left.
		new_state = State(cur_state.cannibalLeft + 1, cur_state.missionaryLeft, 'left',
                                  cur_state.cannibalRight - 1, cur_state.missionaryRight)
		if new_state.is_valid():
			new_state.parent = cur_state
			children.append(new_state)
	return children

def breadth_first_search(initial_state):
	if initial_state.is_goal():
		return initial_state

	queue = list()
	explored = set()

	# Add state to the queue
	queue.append(initial_state)

	while queue:
		# Explore all children in this state.
		state = queue.pop(0)

		# Until we find a goal or we reach the end of the queue
		if state.is_goal():
			return state

		explored.add(state)
		children = get_children(state)

		for child in children:
			if (child not in explored) or (child not in queue):
				# If child is not explored and not in queue then
				# Add the child to the queue
				# And set it's tree parent to current state
				queue.append(child)
				child.set_tree_parent(state)
	return None

def main():
	# Initial State
	initial_state = State(3,3,'left',0,0)

	# Finding solution of the problem.
	solution = breadth_first_search(initial_state)

	# State Representation
	print("Missionaries and Cannibals state representation")
	print("State in format: ")
	print("(Missionaries in left side,Cannibals in left side, Boat (0 if left, 1 if right))")

	# Printing Graph
	for pre, fill, node in RenderTree(initial_state.get_tree_node()):
		print("%s%s" %(pre,node.name))

# if called from the command line, call main()
if __name__ == "__main__":
    main()