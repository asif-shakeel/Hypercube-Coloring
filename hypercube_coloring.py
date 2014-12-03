import numpy
import random
import pylab


class hypercube(object):

    def __init__(self, n):
        """ 
        initializes a hypercube object 
        n: dimensions of the hypercube.
        vertices: 0 ... 2^n - 1, as an n bit binary string.
        direction: 0 ... n-1, the bit that flips from a vertex to an adjacent vertex connected to it by an edge.
        edge: an ordered pair (ordered by lex) of adjacent vertices (differing only in one bit), for instance ('000', '001').
        edges: a dictionary indexed by edges whose  values are the directions of the edges.
        color: is an integer, with the default color of an edge 0.
        coloring: dictionary of edges and their colors.
        remainingEdges: those uncolored Edges that can potentially be assigned new colors.
        """
        self.n=n
        self.vertices = [] 
        self.edges={}
        self.coloring={}
        
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
        

    def getColoring(self):
        """
        returns the current hypercube coloring 
        """
        return self.coloring

 

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
        

        
