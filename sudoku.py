import sys
import time

start_time=time.time()
board_str=sys.argv[1]
rows='ABCDEFGHI'
cols=range(9)
variables=[i + str(j) for i in rows for j in cols]
#print(variables)
rblocks=('ABC','DEF','GHI')

#print(board)
#dictfilt = lambda x, y: [  for i in x if i in set(y) ]

def getPeers(var):
    #print(var)
    prows=[var[0] + str(i) for i in range(9)]
    prows.remove(var)
    pcols=[i + var[1] for i in rows]
    pcols.remove(var)
    q=int(var[1])//3
    rcols=range(q*3,q*3+3)
    for rb in rblocks:
        if var[0] in rb:
            pblock=[i + str(j) for i in rb for j in rcols]
    pblock.remove(var)
    return prows+pcols+pblock

def getDomain(key,board):
    domain=[i for i in range(1,10)]
    peers=getPeers(key)
    #print(board['B0'])
    #print([board[i] for i in pcols])
    for d in range(1,10):
        if d in [board[i] for i in peers]:
            domain.remove(d)
    #    elif d in [board[i] for i in pcols]:
    #        domain.remove(d)
    #    elif d in [board[i] for i in pblock]:
    #        domain.remove(d)
    #print(domain)
    return domain


class Board:
    def __init__(self,board_str):
        #self.board=board_str
        self.board=dict([(i,int(board_str[n])) for n, i in enumerate(variables)])
        self.domains=dict([(i,getDomain(i,self.board) if self.board[i]==0 else [self.board[i]]) for i in variables])
        self.peers=dict()
        self.updatePeers()

    def updatePeers(self):
        self.peers={}
        for i in variables:
            if self.board[i]==0:
                self.peers[i]=getPeers(i)


    def updateBoard(self):
        self.updateDomain()
        result=False
        for i in variables:
            if len(self.domains[i])==1 and self.board[i]==0:
                self.board[i]=self.domains[i][0]
                result=True
        return result

    def displayGrid(self):
        for n, i in enumerate(variables):
            if n % 9 == 0 and n > 0:
                print("")
            print(self.board[i], end=" ")

    def complete(self):
        return not any([self.board[i]==0 for i in variables])

    def assign(self,var,val):
        self.board[var]=val
        self.domains

    def updateDomain(self):
        for x in variables:
            if self.board[x]>0:
                continue
            peers = getPeers(x)
            domain=self.domains[x]
            for d in domain:
                if d in [self.board[i] for i in peers]:
                    domain.remove(d)
            #    elif d in [self.board[i] for i in pcols]:
            #        domain.remove(d)
            #    elif d in [self.board[i] for i in pblock]:
            #        domain.remove(d)
            self.domains[x]=domain


def ac3(sudoku):
    qu=list(sudoku.peers.items())
    while qu:
        if revise(sudoku):
            sudoku.updatePeers()
            qu=list(sudoku.peers.items())
        else:
            return False
    return True

def revise(sudoku):
    return sudoku.updateBoard()

def forward_check(var,val,assigndomain):
    peers=getPeers(var)
    for v in peers:
        #print(assigndomain[v])
        if len(assigndomain[v])==1 and assigndomain[v]==val:
            print('fc failed')
            return False
    return True

def unassign(var,val,assignment,assigndomain,removed):
    assignment[var]=0
    for k,v in removed[var]:
        assigndomain[k].append(v)
    removed[var]=[]

def backTrack(assignment,assigndomain,removed):
    var = select_unassigned(assignment, assigndomain)
    #print(var)
    if not var:
        return assignment
    for val,n in order_domain(var,assigndomain):
        fc=forward_check(var,val,assigndomain)
        if fc:
            assignment[var]=val
            peers = getPeers(var)
            for v in peers:
                if val in assigndomain[v]:
                    assigndomain[v].remove(val)
                    removed[var].append((v,val))
            result=backTrack(assignment,assigndomain,removed)
            if result==False:
                #print(result)
                unassign(var,val,assignment,assigndomain,removed)
            else:
                return result
    return False


def select_unassigned(assignment,assigndomain):
    unassigned = filter(lambda i: assignment[i] == 0, variables)
    if not unassigned:
        return False
    fil=dict([(i,assigndomain[i]) for i in unassigned])
    if not fil:
        return False
    var=sorted(fil.items(),key=lambda x: len(x[1]))[0][0]
    return var

def order_domain(var,assigndomain):
    peers=getPeers(var)
    #prows.remove(var); pcols.remove(var); pblock.remove(var)
    least_const={}
    #print(assigndomain[var])
    for val in assigndomain[var]:
        const=0
        for v in peers:
            if val in assigndomain[v]:
                const+=1
        least_const[val]=const
    #print(least_const)
    return sorted(least_const.items(), key=lambda x: x[1])


if __name__ == '__main__':
    sudoku=Board(board_str)
    result=ac3(sudoku)
    method='AC3'
    #sudoku.displayGrid()
    assignment={}; assigndomain={};removed={}
    for v in variables:
        assignment[v]=sudoku.board[v]
        assigndomain[v]=sudoku.domains[v][:]
        removed[v]=list()
    if not result:
        assignment=backTrack(assignment,assigndomain,removed)
        method='BTS'
    sudoku.board=assignment
    sudoku.displayGrid()
    output=''
    for v in variables:
        output+=str(assignment[v])
    output+=' ' + method
    with open('./output.txt','w') as f:
        f.write(output)
    print(time.time() - start_time)

    #print(sudoku.peers.items())


