import math

class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        first_line = self.return_first_line_tickect()
        all_transactions = self.return_all_transactions()
        to_print = first_line
        return str(to_print + all_transactions)
    
    # Returns the Header line to print in the tickect
    def return_first_line_tickect(self):
        len_category = len(self.name)
        first_part = ''.join(['*' for _ in range(15-(len_category//2))])
        if len_category%2 == 0:
            first_line = first_part + self.name + first_part
        else:
            second_part = ''.join(['*' for i in range(14-(len_category//2))])
            first_line = first_part + self.name + second_part
        return first_line + '\n'
    
    # Return all transactions to print
    def return_all_transactions(self):
        total = 0
        all_lines = ''
        for transaction in self.ledger:
            total += transaction['amount']
            tmp_amount = self.amount_to_print(transaction['amount'])
            tmp_description = transaction['description']
            spaces_description = ''.join([' ' if len(str(tmp_description))< 23 else '' for _ in range(23-len(str(tmp_description)))])
            spaces_number = ''.join([' ' for _ in range(7-len(tmp_amount))])
            line = tmp_description[:23] + spaces_description + spaces_number + tmp_amount + '\n'
            all_lines += line
        all_transac = all_lines + 'Total: ' + str(round(total,2))
        return all_transac

    # Formating amount to print
    def amount_to_print(self, amount):
        decimals = int((abs(amount)*100)%100)
        enteros = int(abs(amount)*100//100)
        if amount > 0:
            if len(str(decimals))==1:
                return str(int(abs(amount)*100//100)) + '.' + '0' + str(decimals)
            else:
                return str(int(abs(amount)*100//100)) + '.' + str(decimals)
        else:
            if len(str(decimals))==1:
                return '-' + str(int(abs(amount)*100//100)) + '.' + '0' + str(decimals)
            else:
                return '-' + str(int(abs(amount)*100//100)) + '.' + str(decimals)
        
    # Register a deposit
    def deposit(self, amount, description=''):
        self.ledger.append({'amount':float(amount), 'description':description})
    
    # Record an expense
    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount':float(-amount), 'description':description})
            return True
        return False

    # Get balance
    def get_balance (self):
        return sum(map(lambda total: total['amount'],self.ledger))

    # Make a transfer
    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.name}')
            category.deposit(amount,f'Transfer from {self.name}')
            return True
        return False

    # Review funds
    def check_funds(self, amount):
        return self.get_balance() >= amount

    # Get expenses
    def get_expenses(self):
        # Round, sum and return all expenses for the category
        return round(sum(item['amount'] for item in self.ledger if item['amount'] < 0),2)

def create_spend_chart(categories):
    if len(categories)>4:
        return
    total_spent =sum(sum(item['amount'] for item in category.ledger if item['amount']< 0) for category in categories)

    percentages = []
    for category in categories:
        percentages.append(int(category.get_expenses()*100/total_spent))
    # Creating the string to return    
    ## First Line
    to_return = 'Percentage spent by category\n'
    ## Filling the Table
    for i in range(100,-1,-10):
        to_return += f"{i:3}| "
        for percent in percentages:
            if percent >= i:
                to_return += 'o  '
            else:
                to_return += '   '
        to_return += '\n'
    ## Division Line
    #print(to_return)
    to_return += '    ' + '-'*(len(categories)*3+1) + '\n'
    #print(to_return)
    ## Creating Categories Names Vertically
    ### Find the maximun name of cathegory length
    max_name_len = max(len(category.name) for category in categories)
    ## Lines of Names
    for i in range(max_name_len):
        # Space before category names
        to_return += '     '
        for category in categories:
            if len(category.name) > i:
                to_return += category.name[i] + '  '
            else:
                to_return += '   '
        to_return += '\n'
    # taking off the last change of line
    to_return = to_return[:len(to_return)-1]
    return to_return

def main():

    food = Category('Food')
    food.deposit(1000,'deposit')
    food.withdraw(150.15,'groceries')
    food.withdraw(335.89,'restaurant and more food for dessert')
    clothing = Category('Clothing')
    food.transfer (50,clothing)
    clothing.deposit(1000,'deposit')
    clothing.withdraw(10.26, 'pants')
    clothing.withdraw(111.5, 'shorts')
    clothing.withdraw(21, 'T-shert')
    auto = Category('Auto')
    auto.deposit(1000,'deposit')
    auto.withdraw(10.26, 'fresher')
    auto.withdraw(90.26, 'fresher')
    house = Category('House')
    house.deposit(2000,'deposit')
    house.withdraw(208.26, 'electrodomestic')
    house.withdraw(150, 'cleaners')

    job = Category('Job')
    job.deposit(2000,'deposit')
    job.withdraw(208.26, 'electrodomestic')
    job.withdraw(150, 'cleaners')


    print(food)
    print(f'Total Expenses Food: {food.get_expenses()}')
    print()
    print(clothing)
    print(f'Total Expenses Clothing: {clothing.get_expenses()}')
    print()
    print(auto)
    print(f'Total Expenses Auto: {auto.get_expenses()}')
    print()
    print(house)
    print(f'Total Expenses house: {house.get_expenses()}')
    print()
    list_categories = [food,clothing,auto,house]
    print(create_spend_chart(list_categories))

    #food.deposit(250.15,'deposit')
    #car =  Category('Car')
    #car.deposit(1000,'deposit')

    #print()
    #print()
    #print('----------------------------------')
    #print(str(food.ledger))
    
    #print(f'Balance {food.category}:', food.get_balance())

    #print('----------------------------------------------------')
    #print(f'Balance {clothing.category}:', clothing.ledger)
    #print(f'Balance {clothing.category}:', clothing.get_balance())

if __name__ == '__main__':
  main()
