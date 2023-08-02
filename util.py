class Pair:
    def __init__(self,first,second):
        self.first = first
        self.second = second

    def __str__(self):
        return "(" + str(self.first) + "," + str(self.second) + ")"

    def __add__(self, other):
        if isinstance(other,Pair):
            newFirst = int((self.first + other.first) / 2)
            newSecond = int((self.second + other.second) / 2)
            return Pair(newFirst,newSecond)

    def __eq__(self,other):
        if isinstance(other, Pair):
            if other.first == self.first and other.second == self.second:
                return True
        return False

