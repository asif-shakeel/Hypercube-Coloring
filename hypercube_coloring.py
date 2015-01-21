import numpy
import random
import pylab
from sets import Set


class hypercube(object):

    def __init__(self, n):
        """ 
        initializes a hypercube object 
        n: dimensions of the hypercube.
        vertices: 0 ... 2^n - 1, as an n bit binary string.
        direction: 0 ... n-1, the bit that flips from a vertex to an adjacent vertex connected to it by an edge.
        edge: an ordered pair (ordered by lex) of adjacent vertices (differing only in one bit), for instance ('000', '001').
        edges: a dictionary indexed by edges whose  values are the directions of the edges.
        edgeAsVertexDirection: edges in (vertex, direction) form. There are two (vertex,direction) 
                pairs for each edge, for eg: ('000', 2) and ('100', 2), both mean the edge ('000', '100'). So this has size 2 x the no. of edges
        nonAdjacentPairs: pairs of non-adjacent vertices that need to be checked for the coloring rules, eg. ('000', '110').
        color: is an integer, with the default color of an edge 0.
        coloring: dictionary of edges and their colors.
        remainingEdges: those uncolored Edges that can potentially be assigned new colors.
        """
        self.n=n
        self.vertices = [] 
        self.edges={}
        self.edgeAsVertexDirection={}
        self.nonAdjacentPairs={}
        self.coloring={}
        self.numColors=0
        self.activeDirections=[False for k in range(n)] 
        self.anyMoreDirections=False
        self.remainingEdges=[]
        self.colors=[]
        
        def genVertices(self):
            """
            generates vertices as n bit strings
            """
            for i in range(2**self.n):
                vertex=''
                for k in range(self.n):
                    temp=(i/(2**(k)))%2
                    vertex=str(temp)+vertex
                self.vertices.append(vertex)
        
        genVertices(self)
        
        def genEdgeFromVertexDirection(self,vertex,direction):
            """
            creates an edge from vertex and direction
            """
            edge=[]
            targetVertex=list(vertex)
            if vertex[self.n-1-direction] == '0':
                targetVertex[self.n-1-direction]='1'
                edge=(vertex,"".join(targetVertex))
            else:
                targetVertex[self.n-1-direction]='0'
                edge=("".join(targetVertex),vertex)
            return edge   

                
        def genDirectionalEdges(self,direction):
            """
            creates all the edges in a given direction
            """
            directionalEdges=[]
            hypercubeOneLessDim=hypercube(self.n-1)
            VerticesOneLessDim=hypercubeOneLessDim.getVertices()
            for i in range(2**(self.n-1)):
                SourceVertex=list(VerticesOneLessDim[i])
                SourceVertex.insert(self.n-1-direction,'0')
                directionalEdges.append(genEdgeFromVertexDirection(self,"".join(SourceVertex),direction))
            return directionalEdges
    
        def genEdges(self):
            """
            generates all the  edges as  pair of vertices, and in  the (vertex, direction) forms, and initializes the 
            coloring table to 0 for each edge
            """
            for direction in range(self.n):
                directionalEdges=genDirectionalEdges(self,direction)
                self.edges.update(dict.fromkeys(directionalEdges,direction))
                self.coloring.update(dict.fromkeys(directionalEdges,0))
                self.edgeAsVertexDirection.update(dict(zip([(x[0],direction) for x in directionalEdges],directionalEdges)))
                self.edgeAsVertexDirection.update(dict(zip([(x[1],direction) for x in directionalEdges],directionalEdges)))


        
        genEdges(self)

        def genNonAdjacentPairs(self):
            """
            generates non-adjacent vertex pairs
            """
            vertices=self.vertices
            edges=self.edges.keys()

            for v1 in vertices:
                for v2 in vertices:
                    if v1<v2 and ((v1,v2) not in edges):
                        self.nonAdjacentPairs.update({(v1,v2):[n-1-i for i in range(n) if list(v1)[i]!=list(v2)[i]]})
                        
        genNonAdjacentPairs(self)

    
    def getVertices(self):
        """
        returns the list of vertices
        """
        return self.vertices
        
    def getEdges(self):
        """
        returns the list of edges and directions
        """
        return self.edges
        
    def getNonAdjacentPairs(self):
        """
        returns the list of non-adjacent vertices
        """
        return self.nonAdjacentPairs
        
    
    def getEdgeAsVertexDirection(self):
        """
        returns the list of edges as (vertex, direction) pairs (two such pairs for each edge)
        """
        return self.edgeAsVertexDirection

    def getColoring(self):
        """
        returns the current hypercube coloring 
        """
        return self.coloring

    def setPartialColoring(self,partialColoring):
        """
        returns the current hypercube coloring 
        coloring: a dictionary of vertices and directions with associated colors
        """
        for k in partialColoring.keys():
            self.coloring.update({self.edgeAsVertexDirection[k],partialColoring[k]})
        
 

    def resetColoring(self):
        """
        resets the current hypercube coloring to default
        """
        self.coloring = dict.fromkeys(self.coloring.iterkeys(), 0) 
            
    def setEdgeColor(self,edge,color):
        """
        sets the  coloring of a given edge
        """
        self.coloring.update({edge:color})

        
    def getEdgeColor(self,edge):
        """
        returns the edge color 
        """
        return self.coloring[edge]
        
    def setNumColors(self,numColors):
        """
        sets   numColors
        """
        self.numColors=numColors
        
    def getNumColors(self):
        """
        returns  numColors
        """
        return self.numColors
        
    def getColors(self):
        """
        returns  colors
        """
        return self.colors
        

        
        
    def ruleCheck(self,edge,color):
        """
        Given an edge, this function checks the coloring rule,  for all the non-adjacent pairs containing a vertex 
        from either end of the edge. It also colors edges that need to be colored with existent colors to  satisfy the coloring rule.
        Returns True if the rule is satisfied, or False if not. Coloring is unchanged if the rule is not satisfied.
        """
        ##print "NEW ROUND"
        colorcopy=self.coloring.copy()
        #self.color+=1
        self.coloring.update({edge:color})
        edgesToCheck=[]
        edgesToCheck.append(edge)  
        finalRuleSatisfaction=True
        while edgesToCheck:
            currentEdgeToCheck=edgesToCheck[0]
            del edgesToCheck[0]
            direction=self.edges[currentEdgeToCheck]
            sourceVertex=currentEdgeToCheck[0]
            targetVertex=currentEdgeToCheck[1]
            NonAdjacentPairsContainingSourceVertex=[p for p in self.nonAdjacentPairs.keys() if sourceVertex in p and direction in self.nonAdjacentPairs[p]]
            for p in NonAdjacentPairsContainingSourceVertex:
                directionsToCheck=self.nonAdjacentPairs[p]
                currentPairRuleSatisfaction=False
                numSharedNeutralDirections=0
                vertexPossiblyForcedToColorEdge=0
                for d in directionsToCheck:
                    if self.coloring[self.edgeAsVertexDirection[(p[0],d)]]==0:
                        numSharedNeutralDirections=numSharedNeutralDirections+1
                        vertexPossiblyForcedToColorEdge=0
                        savedDirection=d
                    if self.coloring[self.edgeAsVertexDirection[(p[1],d)]]==0:
                        numSharedNeutralDirections=numSharedNeutralDirections+1
                        vertexPossiblyForcedToColorEdge=1
                        savedDirection=d  
                    if numSharedNeutralDirections > 1 or self.coloring[self.edgeAsVertexDirection[(p[0],d)]]==self.coloring[self.edgeAsVertexDirection[(p[1],d)]]:
                        currentPairRuleSatisfaction=True
                if numSharedNeutralDirections==1  and not currentPairRuleSatisfaction:
                    #print "ADDING IN SOURCE"
                    if vertexPossiblyForcedToColorEdge==0:
                        self.coloring[self.edgeAsVertexDirection[(p[0],savedDirection)]]=self.coloring[self.edgeAsVertexDirection[(p[1],savedDirection)]]
                        edgesToCheck.append(self.edgeAsVertexDirection[(p[0],savedDirection)])
                    else:
                        self.coloring[self.edgeAsVertexDirection[(p[1],savedDirection)]]=self.coloring[self.edgeAsVertexDirection[(p[0],savedDirection)]]
                        edgesToCheck.append(self.edgeAsVertexDirection[(p[1],savedDirection)])
                    currentPairRuleSatisfaction=True
                #if not currentPairRuleSatisfaction:
                    #print ("Source pair", p)
                #print currentPairRuleSatisfaction
                finalRuleSatisfaction = finalRuleSatisfaction and currentPairRuleSatisfaction
                        
        
            NonAdjacentPairsContainingTargetVertex=[p for p in self.nonAdjacentPairs.keys() if targetVertex in p and direction in self.nonAdjacentPairs[p]]
            for p in NonAdjacentPairsContainingTargetVertex:
                directionsToCheck=self.nonAdjacentPairs[p]
                currentPairRuleSatisfaction=False
                numSharedNeutralDirections=0
                vertexPossiblyForcedToColorEdge=0
                for d in directionsToCheck:
                    if self.coloring[self.edgeAsVertexDirection[(p[0],d)]]==0:
                        numSharedNeutralDirections=numSharedNeutralDirections+1
                        vertexPossiblyForcedToColorEdge=0
                        savedDirection=d
                    if self.coloring[self.edgeAsVertexDirection[(p[1],d)]]==0:
                        numSharedNeutralDirections=numSharedNeutralDirections+1
                        vertexPossiblyForcedToColorEdge=1
                        savedDirection=d  
                    if numSharedNeutralDirections > 1 or self.coloring[self.edgeAsVertexDirection[(p[0],d)]]==self.coloring[self.edgeAsVertexDirection[(p[1],d)]]:
                        currentPairRuleSatisfaction=True
                if numSharedNeutralDirections==1 and not currentPairRuleSatisfaction:
                    #print "ADDING IN TARGET"
                    if vertexPossiblyForcedToColorEdge==0:
                        self.coloring[self.edgeAsVertexDirection[(p[0],savedDirection)]]=self.coloring[self.edgeAsVertexDirection[(p[1],savedDirection)]]
                        edgesToCheck.append(self.edgeAsVertexDirection[(p[0],savedDirection)])
                    else:
                        self.coloring[self.edgeAsVertexDirection[(p[1],savedDirection)]]=self.coloring[self.edgeAsVertexDirection[(p[0],savedDirection)]]
                        edgesToCheck.append(self.edgeAsVertexDirection[(p[1],savedDirection)])
                    currentPairRuleSatisfaction=True
                #if not currentPairRuleSatisfaction:
                    #print ("Target pair", p)
                finalRuleSatisfaction = finalRuleSatisfaction and currentPairRuleSatisfaction
                
                ##print currentPairRuleSatisfaction
 
            if not finalRuleSatisfaction:
                #print "FINAL RULE FAIL"
                self.coloring = colorcopy  #### IS IT OK TO JUST COPY OR HAVE TO BE CAREFUL AS FOLLOWS
                break
            #self.coloring.clear()
            #self.coloring.update(colorcopy)
                
        return finalRuleSatisfaction  
    

    
    def doColoring(self):
        """
        Starting with the current coloring, this function attempts to build up coloring consitent 
        with the minimum number of colors to be used in each direction.
        Returns True or False depending on success or failure of attempted coloring.
        """
        

        


        for direction in range(self.n):
            remainingEdgesinCurrentDirection=[e for e in self.coloring.keys() if self.coloring[e]==0 and self.edges[e]==direction]
            self.remainingEdges.append(remainingEdgesinCurrentDirection)
            if remainingEdgesinCurrentDirection:
                self.activeDirections[direction] = True
                self.anyMoreDirections = True
            else:
                pass

            self.colors.append(list(Set([self.coloring[e] for e in self.coloring.keys() if self.coloring[e]!=0 and self.edges[e]==direction])))
  
       
        
        while self.anyMoreDirections:
            for direction in range(self.n):
                #print self.colors
                #print direction
                #print self.remainingEdges
                ##print self.activeDirections
            

                if self.activeDirections[direction]:
                    randomEdgeInCurrentDirection=random.choice(self.remainingEdges[direction])
                    #print randomEdgeInCurrentDirection        
                    
                    if self.ruleCheck(randomEdgeInCurrentDirection,self.numColors+1):
                        self.numColors+=1
                    else: 
                        colorsCheckedFromExistingColorsInCurrentDirection=0
                        #print self.remainingEdges
                        while colorsCheckedFromExistingColorsInCurrentDirection<len(self.colors[direction]) and not self.ruleCheck(randomEdgeInCurrentDirection,self.colors[direction][colorsCheckedFromExistingColorsInCurrentDirection]):
                            colorsCheckedFromExistingColorsInCurrentDirection+=1
                        assert  colorsCheckedFromExistingColorsInCurrentDirection < len(self.colors[direction])
                            #print colorsCheckedFromExistingColorsInCurrentDirection
                            
                    #if len(self.colors[direction]) != 0:
                    #    assert  colorsCheckedFromExistingColorsInCurrentDirection < len(self.colors[direction])

                    self.colors=[]
                    self.activeDirections=[False for k in range(self.n)] 
                    self.anyMoreDirections=False
                    self.remainingEdges=[]
                    
 
                    for updateDirection in range(self.n):
                        remainingEdgesinCurrentDirection=[e for e in self.coloring.keys() if self.coloring[e]==0 and self.edges[e]==updateDirection]
                        self.remainingEdges.append(remainingEdgesinCurrentDirection)
                        if remainingEdgesinCurrentDirection:
                            self.activeDirections[updateDirection] = True
                            self.anyMoreDirections = True
                        else:
                            pass

                        self.colors.append(list(Set([self.coloring[e] for e in self.coloring.keys() if self.coloring[e]!=0 and self.edges[e]==updateDirection])))
    

    def findCrazyEdges(self):
    
        crazyEdges=[]
    
        for e in self.edges:
            sameColor=True
            edgeDirection=self.edges[e]
            for d in range(self.n):
                if d!=edgeDirection:
                    sameColor = sameColor and (self.coloring[self.edgeAsVertexDirection[(e[0],d)]] == self.coloring[self.edgeAsVertexDirection[(e[1],d)]])
                
            if sameColor:
                crazyEdges.append((e,self.coloring[e],len(filter(lambda x: self.coloring[x] == self.coloring[e],self.edges))))
        return crazyEdges
        
        
        
    
########################## EXAMPLE (3,1) coloring #########################    
"""
Create a cube. Assign colors to edges and check the coloring rule after each new color. 
The following example does the (3,1) coloring.
"""
    
        
#ch3=hypercube(3)
#print ch3.ruleCheck(('000', '001'),1)
#print ch3.ruleCheck(('010', '011'),1)
#print ch3.ruleCheck(('110', '111'),1)
#print ch3.ruleCheck(('100', '101'),2)
#ch3.setNumColors(2)
#ch3.doColoring()
#print "Number of colors used =" + str(ch3.getNumColors())
#print "Color distribution by directions = "+ str(ch3.getColors())
#print "Coloring by edges:"
#print ch3.getColoring()
#print "Edges with all colors the same at both ends, their color and  number of edges of that color= " + str(ch3.findCrazyEdges())

#ch4=hypercube(4)
#print ch4.ruleCheck(('0000', '0001'),1)
#print ch4.ruleCheck(('0010', '0011'),1)
#print ch4.ruleCheck(('0100', '0101'),1)
#print ch4.ruleCheck(('0110', '0111'),1)
#print ch4.ruleCheck(('1000', '1001'),1)
#print ch4.ruleCheck(('1010', '1011'),1)
#print ch4.ruleCheck(('1100', '1101'),1)
#print ch4.ruleCheck(('1110', '1111'),1)
#ch4.setNumColors(1)
#ch4.doColoring()
#print ch4.getColoring()
#print "Number of colors used =" + str(ch4.getNumColors())

ch4=hypercube(4)
print ch4.ruleCheck(('0000', '0001'),1)
print ch4.ruleCheck(('0010', '0011'),1)
print ch4.ruleCheck(('0100', '0101'),3)
print ch4.ruleCheck(('0110', '0111'),1)
print ch4.ruleCheck(('1000', '1001'),1)
print ch4.ruleCheck(('1010', '1011'),1)
print ch4.ruleCheck(('1100', '1101'),2)
print ch4.ruleCheck(('1110', '1111'),1)
ch4.setNumColors(3)
ch4.doColoring()
print "Number of colors used =" + str(ch4.getNumColors())
print "Color distribution by directions = "+ str(ch4.getColors())
print "Coloring by edges:"
print ch4.getColoring()
print "Edges with all colors the same at both ends, their color and  number of edges of that color= " + str(ch4.findCrazyEdges())


#ch4=hypercube(4)
#ch4.doColoring()
#print ch4.getColoring()
#print "Number of colors used =" + str(ch4.getNumColors())

#ch3=hypercube(3)
#ch3.doColoring()
#print ch3.getColoring()
#print "Number of colors used =" + str(ch3.getNumColors())