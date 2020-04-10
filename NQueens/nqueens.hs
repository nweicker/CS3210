-- CS 3210 - Principles of Programming Languages
-- Project 2
-- Authors:
--    Nicole Weickert
--    Myke Walker

type Seq = [Char]
type Board = [Seq]

--mainDiagIndices takes a board and a diagonal index and returns a sequence of tuples with the coordinates of the locations that are in the primary diagonal. 
mainDiagIndices :: Board -> Int -> [ (Int, Int) ]

--secDiagIndices takes a board and a diagonal index and returns a sequence of tuples with the coordinates of the locations that are in the secondary diagonal. 
secDiagIndices :: Board -> Int -> [ (Int, Int) ]

--setup takes an integer n >= 4 and creates an nxn board with all locations empty.  If n < 4 setup should return a 4x4 board
setup :: Int -> Board

--rows takes a board and returns its number of rows. 
rows :: Board -> Int

--cols takes a board and returns its number of columns if all rows have the same number of columns; it returns zero, otherwise. 
cols :: Board -> Int

--size takes a board and returns its size, which is the same as its number of rows (if it matches its number of columns), or zero, otherwise. 
size :: Board -> Int

--queensSeq takes a sequence and returns the number of queens found in it. 
queensSeq :: Seq -> Int

--queensBoard takes a board and returns the number of queens found in it. 
queensBoard :: Board -> Int 

--seqValid takes a sequence and returns true/false depending whether the sequence no more than 1 queen. 
seqValid :: Seq -> Bool

--rowsValid takes a board and returns true/false depending whether ALL of its rows correspond to valid sequences. 
rowsValid :: Board -> Bool

--colsValid takes a board and returns true/false depending whether ALL of its columns correspond to valid sequences. 
colsValid :: Board -> Bool

--diagonals takes a board and returns its number of primary (or secondary) diagonals. If a board has size n, its number of diagonals is given by the formula: 2 x n - 1.
diagonals :: Board -> Int

--allMainDiagIndices takes a board and returns a list of all primary diagonal indices.  
allMainDiagIndices :: Board -> [[ (Int, Int) ]]

--mainDiag takes a board and returns a list of all primary diagonal elements.  
mainDiag :: Board -> [Seq]

--allSecDiagIndices takes a board and returns a list of all secondary diagonal indices.  
allSecDiagIndices :: Board -> [[ (Int, Int) ]]

--secDiag takes a board and returns a list of all secondary diagonal elements.  
secDiag :: Board -> [Seq]

--diagsValid takes a board and returns true/false depending whether all of its primary and secondary diagonals are valid. 
diagsValid :: Board -> Bool

--valid takes a board and returns true/false depending whether the board configuration is valid (i.e., no queen is threatening another queen). 
valid :: Board -> Bool

--solved takes a board and returns true/false depending whether the board configuration is solved (i.e., the configuration is valid and also has the right amount of queens based on the board’s size). 
solved :: Board -> Bool

--setQueenAt takes a board and returns a list of new board configurations, each with a queen added at all of the possible columns of a given row index. 
setQueenAt :: Board -> Int -> [Board]

--nextRow takes a board and returns the first row index (from top to bottom) that does not have any queen.  
nextRow :: Board -> Int

--solve takes a board and returns ALL of the board configurations that solve the n-queens puzzle. 
solve :: Board -> [Board]

