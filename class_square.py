

class Square:
    def __init__(self, num, y, x):
        self.num = num
        self.cordinates = [y, x]
        self.possible_num = []

    def return_num(self):
        return self.num

    def return_possible(self):
        return self.possible_num

    def is_zero(self):
        if self.num == 0:
            return True
        return False

    def return_cordinates(self):
        return self.cordinates

    def erase_num(self):
        self.possible_num.remove(self.num)
        self.num = 0

    def change_num(self, num):
        self.num = num

    def remove_possible(self, possible):
        self.possible_num.remove(possible)

    def add_possible(self, possible):
        self.possible_num.append(possible)

    def print(self, num1, num2):
        #Tämä funtkio on vain testausta varten

        if self.num == 0:
            for n in range(num1, num2):
                if n in self.possible_num:
                    print(str(n) + " ", end="")
                else:
                    print("  ", end="")
        else:
            for n in range(num1, num2):
                print(str(self.num) + " ", end="")

        print("| ", end="")

    def number_of_possibilities(self):
        return len(self.possible_num)