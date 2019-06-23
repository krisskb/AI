import sys
from collections import deque
import time
import resource
import heapq

inlist=sys.argv[2].split(',')
inlist=[int(x) for x in inlist]
goalList=[0, 1, 2, 3, 4, 5, 6, 7, 8]
goalstr=''.join(str(e) for e in goalList)
childmapping=[]
nodesexp = 0; max_depth=0
start_time=time.time()

class GridState:
    def __init__(self,state,parent,move):
        #print(len(state))
        #d=int(math.sqrt(len(state)))
        self.grid=state
        self.parent=parent
        self.move=move
        if parent==None:
            self.depth=0
        else:
            self.depth=parent.depth+1
        self.priority=manhat(state)+self.depth
        self.state_str=''.join(str(e) for e in state)
    def __cmp__(self, other):
        return cmp(self.priority,other.priority)
    def __lt__(self, other):
        return self.priority < other.priority

    def isGoal(self):
        #print(self.grid==goalList)
        return self.state_str==goalstr

    def getChilds(self):
        #print(np.where(self.grid==0))
        zeroPos=self.grid.index(0)
        #childs={}
        return_childs = []
        global nodesexp; nodesexp += 1
        if zeroPos>=3:
            child=self.grid[0:]
            child[zeroPos]=child[zeroPos-3]
            child[zeroPos-3]=0
            #childs['up']=child.flatten().tolist()
            return_childs.append(GridState(child, self, 'up'))
            #childmapping.append((child,'up',self.grid))
        if zeroPos<=5:
            child = self.grid[0:]
            child[zeroPos] = child[zeroPos+3]
            child[zeroPos+3] = 0
            #childs['down'] = child.flatten().tolist()
            return_childs.append(GridState(child, self, 'down'))
            #childmapping.append((child,'down',self.grid))
        if zeroPos not in [0,3,6]:
            child = self.grid[0:]
            child[zeroPos] = child[zeroPos-1]
            child[zeroPos-1] = 0
            #childs['left']=child.flatten().tolist()
            return_childs.append(GridState(child, self, 'left'))
            #childmapping.append((child, 'left', self.grid))
        if zeroPos not in [2,5,8]:
            child = self.grid[0:]
            child[zeroPos] = child[zeroPos+1]
            child[zeroPos+1] = 0
            #childs['right']=child.flatten().tolist()
            return_childs.append(GridState(child, self, 'right'))
            #childmapping.append((child, 'right', self.grid))
        #print(return_childs)
        return return_childs

def bfs(inlist):
    frontier=deque()
    frontier.append(GridState(inlist, None, ''))
    explored=set()
    global max_depth
    while frontier:
        gState=frontier.popleft()
        #print(state)
        #gState=GridState(state)
        explored.add(gState.state_str)
        if gState.isGoal():
            return gState
        for child in gState.getChilds():
            if child.state_str not in explored:
                frontier.append(child)
                explored.add(child.state_str)
                if child.depth > max_depth:
                    max_depth=child.depth

def ast(inlist):
    frontier=[GridState(inlist, None, '')]
    heapq.heapify(frontier)
    explored=set()
    while frontier:
        gState=heapq.heappop(frontier)
        #print(len(frontier))
        explored.add(gState.state_str)
        if gState.isGoal():
            return gState
        for child in gState.getChilds():
            if child.state_str not in explored:
                heapq.heappush(frontier, child)
                explored.add(child.state_str)
            else:
                for i,fgrid in enumerate(frontier):
                    if child.state_str==fgrid.state_str and child.priority < fgrid.priority:
                        frontier[i]=child

def dfs(inlist):
    frontier=deque()
    frontier.append(GridState(inlist, None, ''))
    explored=set()
    global max_depth
    while frontier:
        gState=frontier.pop()
        explored.add(gState.state_str)
        if gState.isGoal():
            #print(time.time() - start_time)
            return gState
        childs=reversed(gState.getChilds())
        for child in childs:
            if child.state_str not in explored:
                frontier.append(child)
                explored.add(child.state_str)
                if child.depth > max_depth:
                    max_depth=child.depth

def manhat(statelist):
    goalind={0:(0,0),1:(0,1),2:(0,2),3:(1,0),4:(1,1),5:(1,2),6:(2,0),7:(2,1),8:(2,2)}
    dist=0
    for i,e in enumerate(statelist):
        if e != 0:
            ind=divmod(i,3)
            #print(abs(goalind[e][0]-ind[0])+abs(goalind[e][1]-ind[1]))
            dist+=abs(goalind[e][0]-ind[0])+abs(goalind[e][1]-ind[1])
    return dist

alg=sys.argv[1]
nodesexp=0
if alg=='bfs':
    result=bfs(inlist)
if alg=='dfs':
    result=dfs(inlist)
if alg=='ast':
    result=ast(inlist)
path=[]
total_cost=result.depth
print(total_cost)
while result.move != '':
    path.append(result.move)
    result=result.parent
path.reverse()
cpath=str(len(path))
#print(len(path)+1 if alg=='bfs' else len(path))
with open("./output.txt",'w') as fo:
    fo.writelines("path_to_goal: " + str(path))
    fo.write("\ncost_of_path: " + cpath)
    fo.write("\nnodes_expanded: " + str(nodesexp))
    fo.write("\nsearch_depth: " + cpath)
    fo.write("\nmax_search_depth: " + str(total_cost if alg=='ast' else max_depth))
    fo.write("\nrunning_time: " + str(time.time() - start_time))
    fo.write("\nmax_ram_usage: " + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024))
'''
print(path)
print(total_cost)
print(nodesexp)

print('Run time : ' + str(time.time() - start_time))
print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
'''