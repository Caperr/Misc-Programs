# Sum each row of a given 2d arrays
def check(list):
    # iterate through each row
    for line in list:
        # iterate through each value in the current row
        for block in line:
            # Print out the current value
            print(block, end="")
            # And a plus sign, if it isn't the last value in the row
            if block != line[-1]:
                print("+", end="")
        # Print the equals and the sum.
        print(" =", sum(line))

class matrix:
    # The actual square as a 2-dimentional array
    square = []
    # The length of each side
    size = 0

    # Initialize square
    def __init__(self,size):
        # Create the square as x number of 0s along *  number of x's down
        self.square = [[0 for x in range(size)] for y in range(size)]
        # Save square side length for use later
        self.size = size

    # Print out the square
    def printSquare(self):
        # print initial line separator
        print(" ",end="")
        print("--" * self.size)
        # iterate through each line
        for line in self.square:
            # iterate through each data piece in the current line
            for block in line:
                # if the block is empty, don't print anything
                if block == 0:
                    block = " "
                # Print the data (or lack thereof) with spacing and separator lines
                # Use end= to keep values of current line in the same printed line
                print(str(block) + "|",end="")
            # Next line, so print new line and line separator
            print("\n","--"*self.size)

    # change the data in a block at co-ords (x,y) to value num
    def set(self,x,y,num):
        self.square[abs(y- (self.size-1))][x] = num

    # make a magic square
    def magic(self):
        # If the square is of odd size
        if self.size % 2 == 1:
            # set the starting co-ordinates as the top centre
            x = round(self.size/2)
            # python's rounding is inconsistent for half values. Let's check it gets it right...
            if x < self.size/2:
                x += 1
            # take one off of co-ordinates to compensate for 0-based ordinals
            x -= 1
            y = self.size - 1
            #for every value in the square...
            for i in range(self.size**2):
                # Update the current block
                self.set(x,y,i+1)
                # Check that the next square is empty
                # If it isn't...
                if self.square[abs( ((y + 1) % self.size) - (self.size-1))][abs( (x + 1) % self.size)] != 0:
                    # Keep x value the same, but set the y value one lower
                    y = (y - 1) % self.size
                # If the next square is empty...
                else:
                    # Move the current co-ords up and to the right
                    x = (x + 1) % self.size
                    y = (y + 1) % self.size
        # Magic square algorithm is different for squares of even sizes
        else:
            print("even square size")

    # Prove that the maths was correct by summing all rows, columns and main diagonals
    def prove(self):
        print("\nExpected value:")
        # Find middle value
        x = round((self.size**2) / 2)
        # python's rounding is inconsistent for half values. Let's check it gets it right...
        if x < (self.size**2) / 2:
            x += 1
        # Print out the calculation of expected value, and then the expected value.
        # To work out expected value, square the square's side length, divide that by two, round up, and times that
        # number by side length.
        print(str(self.size) + "*" + str(x),"=",self.size * x)

        # Check the rows
        print("\nRows:")
        check(self.square)

        # Check the columns by rotating the square and then checking the rows.
        # list rotate:
        # http://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
        print("\nColumns:")
        check(zip(*self.square[::-1]))

        # Check the diagonals
        # list large diagonals:
        # http://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
        print("\nDiagonals:")
        # Temporary list for storing both diagonals
        diagonals = []
        # Get diagonals and append into diagonals array as separate arrays
        diagonals.append([self.square[i][i] for i in range(self.size)])
        diagonals.append([self.square[self.size-1-i][i] for i in range(self.size-1,-1,-1)])
        # Check both diagonals
        check(diagonals)

# Instantiate a matrix
m = matrix(3)
# Make a magic square
m.magic()
# Print out the square
m.printSquare()
# Prove the maths
m.prove()
