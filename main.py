import hashlib
import time
import random

# We control the Hardness using N, where N is the number of Zeros in the start of the hash after adding the nonce
N = 2
zeros = "0" * N

# Dummy for the blockchain users
User_Names = ["Nada", "Sarah", "Yasmin", "Mariam", "Nesma", "Noor", "Habiba", "Ahmed", "Mohamed", "Nadeen", "Yumna", "Mai", "Yehia", "Mahmoud", "Omar"]


class Verification:
    def __init__(self, initial_block_chain):
        nonce = 0
        final_block_chain = hashlib.sha256(initial_block_chain.encode()).hexdigest()
        if final_block_chain.startswith(zeros):
            self.final_data = f"{initial_block_chain}"
            self.final_hash = final_block_chain
        else:
            while True:
                self.trial_block_chain = f"{initial_block_chain}{nonce}"
                final_block_chain = hashlib.sha256(self.trial_block_chain.encode()).hexdigest()
                if final_block_chain.startswith(zeros):
                    self.final_data = f"{initial_block_chain}{nonce}"
                    self.final_hash = final_block_chain
                    self.nonce = nonce
                    break
                else:
                    nonce += 1


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time_ns()
        self.sentence = f"At {self.timestamp} {self.sender} sends {self.receiver} {self.amount} BC"


class Block:
    def __init__(self, transactions_list, Attacker):
        self.transactions_list = transactions_list
        tempdata = ""
        for i in range(len(transactions_list)):
            tempdata = tempdata + transactions_list[i].sentence + "\n"
        temp_hash = Verification(tempdata)
        self.data = temp_hash.final_data
        self.hash_data = temp_hash.final_hash
        self.children = []
        self.prev_hash = None
        self.Attacker = Attacker

    def print_block(self):
        print("*******************************************")
        print(f"Attacker Block: {self.Attacker}")
        print(f"Previous Hash: {self.prev_hash}")
        #print(f"Data: {self.data}")
        print(f"Current Hash: {self.hash_data}")
        print("*******************************************")


class BlockChain:
    def __init__(self):
        self.root = None
        self.longest_branch = []
        self.last_block = None

    def find_temp_long(self, root):
        Path = []
        Path.append(root)
        if len(root.children) == 0:
            return Path
        elif len(root.children) == 1:
            Path.extend(self.find_temp_long(root.children[0]))
            return Path
        else:
            max = 0
            Longest_List = []
            for x in root.children:
                temp = self.find_temp_long(x)
                if len(temp) > max:
                    max = len(temp)
                    Longest_List = temp
            Path.extend(Longest_List)
            return Path


    def find_longest_branch(self):
        if self.root is None:
            self.longest_branch = []
        else:
            self.longest_branch.append(self.root)
            self.longest_branch = self.find_temp_long(self.root)


    def push_back(self, transactions_list, prev_hash, Attacker):
        new_block = Block(transactions_list, Attacker)
        if self.root is None:
            self.root = new_block
            self.last_block = new_block
            self.longest_branch.append(new_block)
        elif prev_hash is None or prev_hash == self.last_block.hash_data:
            new_block.prev_hash = self.last_block.hash_data
            self.last_block.children.append(new_block)
            self.last_block = new_block
            self.longest_branch.append(new_block)
        else:
            q = []
            q.append(self.root)  # Enqueue root
            while len(q) != 0:
                n = len(q)
                while n > 0:
                    p = q[0]
                    if prev_hash == p.hash_data:
                        new_block.prev_hash = p.hash_data
                        p.children.append(new_block)
                        return new_block
                    q.pop(0)
                    for i in range(len(p.children)):
                        q.append(p.children[i])
                    n -= 1
            self.find_longest_branch()
            self.last_block = self.longest_branch[-1]
        return new_block

    def print_list(self):
        self.find_longest_branch()
        for temp in self.longest_branch:
            temp.print_block()


######################################  Create User Random Transactions  ##########################################
list_transactions = []
for i in range(100):
    trans = Transaction(random.choice(User_Names), random.choice(User_Names), random.randint(0, 10))
    list_transactions.append(trans)

##########################  Create User Blocks from the random User Transactions  #################################
# List containing Blocks
list_Blocks = []
# Number of transactions in different blocks
list_no_transactions_in_block = [6, 4, 8, 7, 7, 8, 6, 1, 4, 2, 5, 2, 8, 8, 7, 3, 6, 8]
sum = 0
for i in range(len(list_no_transactions_in_block)):
    Block_transactions = []
    j = sum
    while j < sum + list_no_transactions_in_block[i]:
        Block_transactions.append(list_transactions[j])
        j = j + 1
    sum = sum + list_no_transactions_in_block[i]
    list_Blocks.append(Block_transactions)

######################################  Create Attacker Random Transactions  ##########################################
list_Attacker_transactions = []
for i in range(50):
    trans = Transaction(random.choice(User_Names), random.choice(User_Names), random.randint(0, 10))
    list_Attacker_transactions.append(trans)

##########################  Create User Blocks from the random User Transactions  #################################
# List containing Blocks
List_Attacker_Blocks = []
# Number of transactions in different blocks
list_no_Attacker_transactions_in_block = [3, 2, 4, 4, 3, 4, 3, 1, 2, 1, 2, 1, 4, 4, 3, 2, 3, 2, 2]
sum = 0
for i in range(len(list_no_Attacker_transactions_in_block)):
    Block_transactions = []
    j = sum
    while j < sum + list_no_Attacker_transactions_in_block[i]:
        Block_transactions.append(list_Attacker_transactions[j])
        j = j + 1
    sum = sum + list_no_Attacker_transactions_in_block[i]
    List_Attacker_Blocks.append(Block_transactions)

#######################################  Push User Blocks in Blockchain  ##########################################
B_Chain = BlockChain()
TempBlock = None
AttackHash = None
for i in range(len(list_Blocks)):
    # Simulate User
    if i == 0:
        TempBlock = B_Chain.push_back(list_Blocks[0], None, False)
    else:
        TempBlock = B_Chain.push_back(list_Blocks[i], TempBlock.hash_data, False)

    # Simulate Attacker choosing to create a branch in node 7 can range from [0-17] which is all the user blocks
    if i == 7:
        AttackHash = TempBlock.hash_data


####################################  Push Attacker Blocks in Blockchain  #########################################
# The Attacker chose to add 13 (ie: 19 - 6) blocks it can vary from [0-18] depending on the power of the attacker
for i in range(len(List_Attacker_Blocks)-8):
    # Simulate Attacker Trying to make it's branch the longest branch
    if i == 0:
        TempBlock = B_Chain.push_back(List_Attacker_Blocks[0], AttackHash, True)
    else:
        TempBlock = B_Chain.push_back(List_Attacker_Blocks[i], TempBlock.hash_data, True)

B_Chain.print_list()


