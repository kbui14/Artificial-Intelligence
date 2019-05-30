package project4;
/////////////////////////////////////////////////////////////////////////////////
// CS 430 - Artificial Intelligence
// Project 4 - Sudoku Solver w/ Variable Ordering and Forward Checking
// File: Sudoku.java
//
// Group Member Names: Kevin Bui & Joshua Wood
// Due Date: 12/3/17
// 
//
// Description: A Backtracking program in Java to solve the Sudoku problem.
// Code derived from a C++ implementation at:
// http://www.geeksforgeeks.org/backtracking-set-7-suduku/
/////////////////////////////////////////////////////////////////////////////////

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;
import java.util.Stack;

public class Sudoku
{
	// Constants
	final static int UNASSIGNED = 0; //UNASSIGNED is used for empty cells in sudoku grid
	final static int N = 9;//N is used for size of Sudoku grid. Size will be NxN
	static int numBacktracks = 0;
	static ArrayList<Integer>[][] domain = new ArrayList[9][9];
	static int counterToPrint = 0;

	/////////////////////////////////////////////////////////////////////
	// Main function used to test solver.
	public static void main(String[] args) throws FileNotFoundException
	{
		// Reads in from TestCase.txt (sample sudoku puzzle).
		// 0 means unassigned cells - You can search the internet for more test cases.
		//boolean check = true;
		generateDomain();
		Scanner input = new Scanner(System.in);
		System.out.print("Please choose which test case you would like: ");
		int chosenTestCase = input.nextInt();
		Scanner fileScan = new Scanner(new File("src/project4/Case"+chosenTestCase+".txt"));

		// Reads case into grid 2D int array
		int grid[][] = new int[9][9];
		for (int r = 0; r < 9; r++)
		{
			String row = fileScan.nextLine();
			String [] cols = row.split(",");
			for (int c = 0; c < cols.length; c++)
				grid[r][c] = Integer.parseInt(cols[c].trim());
		}
		
		// Prints out the unsolved sudoku puzzle (as is)
		System.out.println("Unsolved sudoku puzzle:");
		printGrid(grid);
		
		Scanner ordering = new Scanner(System.in);
		String strDefStatic = "1.) Default static ordering";
		String strOrgStatic = "2.) Your original static ordering";
		String strRanOrder = "3.) Random Ordering";
		String strMinRV = "4.) Minimum Remaining Values Ordering";
		String strMaxRV = "5.) Maximum Remaining Values Ordering";
		System.out.println("Please choose your variable ordering: ");
		System.out.println(strDefStatic);
		System.out.println(strOrgStatic);
		System.out.println(strRanOrder);
		System.out.println(strMinRV);
		System.out.println(strMaxRV);
		System.out.println();
		System.out.print("Your input: ");
		int chosenOrdering = ordering.nextInt();
		System.out.print("You chose: ");
		switch (chosenOrdering){
		case 1: System.out.println(strDefStatic);
				break;
		case 2: System.out.println(strOrgStatic);
				break;
		case 3: System.out.println(strRanOrder);
				break;
		case 4: System.out.println(strMinRV);
				break;
		case 5: System.out.println(strMaxRV);
				break;
		default: System.out.println("a wrong input!");
				break;
		}
		System.out.println();
		
		Scanner inferenceMethod = new Scanner(System.in);
		String strNone = "1.) None (basically running standard backtracking search)";
		String strFwdChk = "2.) Forward checking";
		System.out.println("Please choose an inference method: ");
		System.out.println(strNone);
		System.out.println(strFwdChk);
		System.out.print("Your input: ");
		
		int chosenInference = inferenceMethod.nextInt();
		System.out.print("You chose: ");
		switch (chosenInference){
		case 1: System.out.println(strNone);
				break;
		case 2: System.out.println(strFwdChk);
				break;
		default: System.out.println("a wrong input!!!");
				break;
		}
		System.out.println();
		
		// Setup timer - Obtain the time before solving
		long stopTime = 0L;
		long startTime = System.currentTimeMillis();
		
		// Attempts to solve and prints results
		if (SolveSudoku(grid, chosenOrdering, chosenInference) == true)
		{
			// Get stop time once the algorithm has completed solving the puzzle
			stopTime = System.currentTimeMillis();
			System.out.println("Algorithmic runtime: " + (stopTime - startTime) + "ms");
			System.out.println("Number of backtracks: " + numBacktracks);
			
			// Sanity check to make sure the computed solution really IS solved
			if (!isSolved(grid))
			{
				System.err.println("An error has been detected in the solution.");
				System.exit(0);
			}
			System.out.println("\n\nSolved sudoku puzzle:");
			printGrid(grid);
		}
		else
			System.out.println("No solution exists");
	}

	/////////////////////////////////////////////////////////////////////
	// Write code here which returns true if the sudoku puzzle was solved
	// correctly, and false otherwise. In short, it should check that each
	// row, column, and 3x3 square of 9 cells maintain the ALLDIFF constraint.
	private static boolean isSolved(int[][] grid)
	{
		// This int will be used a lot to check values
		int checkInt;
		
		for (int r = 0; r < 9; r++) // Loop through the rows 
		{
			int rowCheck[] = new int[9]; // Create a new blank row to check 
			for (int c = 9; c < 9; c++) // Loop through the rows
				rowCheck[c] = grid[r][c]; // Save the current grid index to the row
			for (int c = 9; c < 9; c++)
			{
				checkInt = rowCheck[c]; // Save the check int from the current index
				rowCheck[c] = 0; // Make that a 0 so it doesn't trigger all diff
				for (int i = 0; i < 9; i++)
				{
					if (rowCheck[i] == checkInt) // If the int at that index is the same as the check int
							return false; // Then it isn't solved
				}
				rowCheck[c] = checkInt; // Swap the check int back into the index
			}
		}
		for (int c = 0; c < 9; c++) // Loop through the columns
		{
			int columnCheck[] = new int[9]; // Create a new blank column to check 
			for (int r = 0; r < 9; r++) // Loop through the rows
				columnCheck[r] = grid[r][c]; // Fill the blank column
			for (int r = 0; r < 9; r++) // Check each index
			{
				checkInt = columnCheck[r]; // Save the check int from the current index
				columnCheck[r] = 0; // Make it 0 so it doesn't trigger our all diff check
				for (int i = 0; i < 9; i++)
				{
					if (columnCheck[i] == checkInt) // If the int at that index is the same as the check int 
						return false; // It isn't solved
				}
				columnCheck[r] = checkInt; // Swap that check int back
			}
		}
		////
		// The infamous box check, we do 9 3x3 checks
		////
		
		// Start these at 0, will make sense later
		int boxRightShift = 0;
		int boxDownShift = 0;
		for (int b = 1; b <= 9; b++) // We are looping through 9 boxes 
		{
			int boxCheck[][] = new int[3][3]; // Create a blank box to check
			for (int r = 0; r < 3; r++) // Loop through box rows
			{
				for (int c = 0; c < 3; c++) // Loop through box columns
					boxCheck[r][c] = grid[r + boxDownShift][c + boxRightShift]; // Save the grid spaces to our blank box
			}
			
			// Now we loop through that check box and evaluate
			for (int r = 0; r < 3; r++) 
			{
				for (int c = 0; c < 3; c++)
				{
					checkInt = boxCheck[r][c]; // We will check the value at that location
					boxCheck[r][c] = 0; // Swap a 0 in
					for (int ri = 0; ri < 3; ri++)
					{
						for (int ci = 0; ci < 3; ci++)
						{
							if (boxCheck[ri][ci] == checkInt) // If there is a repeat
								return false;
						}
					}
					boxCheck[r][c] = checkInt; // Swap that back in
				}
			}
			
			
			if (b % 3 == 0) // If the box is a factor of 3
			{
				// Then we go down to the next row of three boxes
				boxDownShift += 3;
				boxRightShift = 0;
			}
			else // Else we move to the next box on the right
				boxRightShift += 3;
		}
		return true; 
	}

	/////////////////////////////////////////////////////////////////////
	// Takes a partially filled-in grid and attempts to assign values to
	// all unassigned locations in such a way to meet the requirements
	// for Sudoku solution (non-duplication across rows, columns, and boxes)
	/////////////////////////////////////////////////////////////////////
	static boolean SolveSudoku(int grid[][], int chosenOrdering, int chosenInference)
	{
		
		int numRemain = 0;
		for (int row = 0; row < N; row++)
			for (int col = 0; col < N; col++)
				if (grid[row][col] == UNASSIGNED)
					numRemain++;
		//System.out.println(numRemain);
		counterToPrint++;
		
		if (counterToPrint % 1000000 == 0)
		{
			System.out.println("Variables remaining: " + numRemain);
			printGrid(grid);
		}
		
		// Select next unassigned variable
		SudokuCoord variable;
		
		// Simple flow control to decide which way to select a variable
		if (chosenOrdering == 1)
			variable = FindUnassignedVariable(grid);
		else if (chosenOrdering == 2)
			variable = MyOriginalStaticOrderingOpt2(grid);
		else if (chosenOrdering == 3)
			variable = MyOriginalRandomOrderingOpt3(grid);
		else if (chosenOrdering == 4)
			variable = MyMinRemainingValueOrderingOpt4(grid);
		else
			variable = MyMaxRemainingValueOrderingOpt5(grid);

		// If there is no unassigned location, we are done
		if (variable == null)
			return true; // success!

		int row = variable.row;
		int col = variable.col;

		// Typical backtracking 
		if (chosenInference == 1)
		{
			// consider digits 1 to 9
			for (int num = 1; num <= 9; num++)
			{
				// if looks promising
				if (isSafe(grid, row, col, num))
				{
					// make tentative assignment
					grid[row][col] = num;

					// return, if success, yay!
					if (SolveSudoku(grid, chosenOrdering, chosenInference))
						return true;

					// failure, un-assign & try again
					grid[row][col] = UNASSIGNED;
				}
			}
		}

		// If the user chose forward checking
		else if (chosenInference == 2)
		{
			// Loop through the possible variables in this domain
			for (int n = 0; n < domain[row][col].size(); n++)
			{
				// Get the value from the domain
				int num = domain[row][col].get(n);
				// If it looks valid
				if (isSafe(grid, row, col, num))
				{
					// Make assignment
					grid[row][col] = num;

					// If true than success 
					if (SolveSudoku(grid, chosenOrdering, chosenInference))
					{
						pruneDomains(variable, num);
						return true;
					}
					
					// failure, un-assign & try again
					grid[row][col] = UNASSIGNED;
				}
			}
		}
		// Increment the number of backtracks
		numBacktracks++;
		return false; // This triggers backtracking
	}

	/////////////////////////////////////////////////////////////////////
	// Searches the grid to find an entry that is still unassigned. If
	// found, the reference parameters row, col will be set the location
	// that is unassigned, and true is returned. If no unassigned entries
	// remain, null is returned.
	/////////////////////////////////////////////////////////////////////
	static SudokuCoord FindUnassignedVariable(int grid[][])
	{
		for (int row = 0; row < N; row++)
			for (int col = 0; col < N; col++)
				if (grid[row][col] == UNASSIGNED)
					return new SudokuCoord(row, col);
		return null;
	}

	/////////////////////////////////////////////////////////////////////
	// TODO: Implement the following orderings, as specified in the
	// project description. You MAY feel free to add extra parameters if
	// needed (you shouldn't need to for the first two, but it may prove
	// helpful for the last two methods).
	/////////////////////////////////////////////////////////////////////
	static SudokuCoord MyOriginalStaticOrderingOpt2(int grid[][])
	{
		// Like the default static, except we are going from the bottom corner up
		// Seems to work better on our test cases for some reason
		for (int row = (N - 1); row >= 0; row--)
			for (int col = (N - 1); col >= 0; col--)
				if (grid[row][col] == UNASSIGNED)
					return new SudokuCoord(row, col);			
		return null;
	}
	static SudokuCoord MyOriginalRandomOrderingOpt3(int grid[][])
	{
		// Instatiate our random
		Random rand = new Random();
		
		// We build up an array list of the possible choices, similar to the method above
		ArrayList<SudokuCoord> assignableCoords = new ArrayList<SudokuCoord>();
		for (int row = 0; row < N; row++)
			for (int col = 0; col < N; col++)
				if (grid[row][col] == UNASSIGNED){
					assignableCoords.add(new SudokuCoord(row,col));
				}
		// Now if we found some assignable coords we will choose one
		if (assignableCoords.size() > 0)
		{
			// We do this by randomly picking from the values in the array list and returning one
			int randomInt = rand.nextInt(assignableCoords.size());
			return assignableCoords.get(randomInt);
		}
		// If we didn't find anything assignable then we return null
		else
			return null;
	}
	static SudokuCoord MyMinRemainingValueOrderingOpt4(int grid[][])
	{
		// We start with a null coord, if we don't find anything it will stay null
		SudokuCoord minRemainingCoord = null;
		// Our initial min, starts big so the first will always be smaller 
		int minCoords = 99999999;
		
		// Just like the random method, we will build up an array list of assignable coords first
		ArrayList<SudokuCoord> assignableCoords = new ArrayList<SudokuCoord>();
		for (int row = 0; row < N; row++)
			for (int col = 0; col < N; col++)
				if (grid[row][col] == UNASSIGNED)
					assignableCoords.add(new SudokuCoord(row,col));
		
		// Now we will loop through the coords in assignable coords to find which has the min remaining value
		for (int i = 0; i < assignableCoords.size(); i++)
		{
			// Get the current coord in the loop
			SudokuCoord currentCoord = assignableCoords.get(i);
			// We will find how many coords remain assignable, start at 0 and add as we find
			int remCoords = 0;
			
			// Check the row
			for (int num = 1; num <= 9; num++) // Loop through possible numbers
				if (!(UsedInRow(grid, currentCoord.row, num))) // If the number is not used in the row
					remCoords++; // Then we add 1 to remCoords
			// Check the column
			for (int num = 1; num <= 9; num++) // Loop through possible numbers 
				if (!(UsedInCol(grid, currentCoord.col, num))) // If the number is not used in the col
					remCoords++; // Then add 1 to the remCoords
			// Check the box
			// First we find which box we should be addressing with some maths
			int rowOffset = (currentCoord.row / 3);
			int colOffset = (currentCoord.col / 3);
			int boxStartRow = (3 * rowOffset);
			int boxStartCol = (3 * colOffset);
			// Now we run through each possible number 
			for (int num = 1; num <= 9; num++) // Loop through possible numbers
				if (!(UsedInBox(grid, boxStartRow, boxStartCol, num))) // If the number is not used in the box
					remCoords++;
			
			
			// If the remaining is smaller than minimum
			if (remCoords < minCoords) {
				minCoords = remCoords;
				minRemainingCoord = currentCoord;
			}
		}
				
		return minRemainingCoord; 
	}
	static SudokuCoord MyMaxRemainingValueOrderingOpt5(int grid[][]) // Would not recommend
	{
		// We start with a null coord, if we don't find anything it will stay null
		SudokuCoord maxRemainingCoord = null;
		// Our initial max, starts small so the first will always be bigger 
		int maxCoords = -99999999;
		
		// Just like the random method, we will build up an array list of assignable coords first
		ArrayList<SudokuCoord> assignableCoords = new ArrayList<SudokuCoord>();
		for (int row = 0; row < N; row++)
			for (int col = 0; col < N; col++)
				if (grid[row][col] == UNASSIGNED)
					assignableCoords.add(new SudokuCoord(row,col));
		
		// Now we will loop through the coords in assignable coords to find which has the max remaining value
		for (int i = 0; i < assignableCoords.size(); i++)
		{
			// Get the current coord in the loop
			SudokuCoord currentCoord = assignableCoords.get(i);
			// We will find how many coords remain assignable, start at 0 and add as we find
			int remCoords = 0;
			
			// Check the row
			for (int num = 1; num <= 9; num++) // Loop through possible numbers
				if (!(UsedInRow(grid, currentCoord.row, num))) // If the number is not used in the row
					remCoords++; // Then we add 1 to remCoords
			// Check the column
			for (int num = 1; num <= 9; num++) // Loop through possible numbers 
				if (!(UsedInCol(grid, currentCoord.col, num))) // If the number is not used in the col
					remCoords++; // Then add 1 to the remCoords
			// Check the box
			// First we find which box we should be addressing with some maths
			int rowOffset = (currentCoord.row / 3);
			int colOffset = (currentCoord.col / 3);
			int boxStartRow = (3 * rowOffset);
			int boxStartCol = (3 * colOffset);
			// Now we run through each possible number 
			for (int num = 1; num <= 9; num++) // Loop through possible numbers
				if (!(UsedInBox(grid, boxStartRow, boxStartCol, num))) // If the number is not used in the box
					remCoords++;
			
			
			// If the remaining is larger than the maximum
			if (remCoords > maxCoords) {
				maxCoords = remCoords;
				maxRemainingCoord = currentCoord;
			}
		}
		return maxRemainingCoord; 
	}
	
	/////////////////////////////////////////////////////////////////////
	// Returns a boolean which indicates whether any assigned entry
	// in the specified row matches the given number.
	/////////////////////////////////////////////////////////////////////
	static boolean UsedInRow(int grid[][], int row, int num)
	{
		for (int col = 0; col < N; col++)
			if (grid[row][col] == num)
				return true;
		return false;
	}

	/////////////////////////////////////////////////////////////////////
	// Returns a boolean which indicates whether any assigned entry
	// in the specified column matches the given number.
	/////////////////////////////////////////////////////////////////////
	static boolean UsedInCol(int grid[][], int col, int num)
	{
		for (int row = 0; row < N; row++)
			if (grid[row][col] == num)
				return true;
		return false;
	}

	/////////////////////////////////////////////////////////////////////
	// Returns a boolean which indicates whether any assigned entry
	// within the specified 3x3 box matches the given number.
	/////////////////////////////////////////////////////////////////////
	static boolean UsedInBox(int grid[][], int boxStartRow, int boxStartCol, int num)
	{
		for (int row = 0; row < 3; row++)
			for (int col = 0; col < 3; col++)
				if (grid[row+boxStartRow][col+boxStartCol] == num)
					return true;
		return false;
	}

	/////////////////////////////////////////////////////////////////////
	// Returns a boolean which indicates whether it will be legal to assign
	// num to the given row, col location.
	/////////////////////////////////////////////////////////////////////
	static boolean isSafe(int grid[][], int row, int col, int num)
	{
		// Check if 'num' is not already placed in current row,
		// current column and current 3x3 box
		return !UsedInRow(grid, row, num) &&
				!UsedInCol(grid, col, num) &&
				!UsedInBox(grid, row - row%3 , col - col%3, num);
	}
	
	/////////////////////////////////////////////////////////////////////
	// Generates our domain, in theory it looks like this: 
	// [1, 2, 3, 4, 5, 6, 7, 8, 9
	//	10,11,12,13,14,15,16,17,18
	//	19,20,21,22,23,24,25,26,27 
	//	28,29,30,31,32,33,34,35,36
	//	37,38,39,40,41,42,43,44,45
	//	46,47,48,49,50,51,52,53,54
	//	55,56,57,58,59,60,61,62,63
	//	64,65,66,67,68,69,70,71,72
	//	73,74,75,76,77,78,79,80,81]
	/////////////////////////////////////////////////////////////////////
	static void generateDomain()
	{
		for (int r = 0; r < N; r++)
		{
			for (int c = 0; c < N; c++)
			{
				domain[r][c] = new ArrayList<Integer>();
				for (int num = 1; num <= 9; num ++)
					domain[r][c].add(num);
			}
		}
	}
	
	/////////////////////////////////////////////////////////////////////
	// Prunes the domains of the appropriate variables. 
	/////////////////////////////////////////////////////////////////////
	static void pruneDomains(SudokuCoord coord, int num)
	{
		int row = coord.row;
		int col = coord.col;
		
		//Prune rows
		for (int i = 0; i < 9; i++)
			domain[row][i].remove(Integer.valueOf(num));
		// Prune columns
		for (int i = 0; i < 9; i++)
			domain[i][col].remove(Integer.valueOf(num));
		// Prune the box
		int rowOffset = (row / 3);
		int colOffset = (col / 3);
		int boxStartRow = (3 * rowOffset);
		int boxStartCol = (3 * colOffset);
		
		for (int r = 0; r < 3; r++)
			for (int c = 0; c < 3; c++)
				domain[boxStartRow + r][boxStartCol + c].remove(Integer.valueOf(num));
	}
	/////////////////////////////////////////////////////////////////////
	// unPrunes the domains of the appropriate variables. 
	/////////////////////////////////////////////////////////////////////
	static void unPruneDomains(SudokuCoord coord, int num)
	{
		int row = coord.row;
		int col = coord.col;
		
		//Prune rows
		for (int i = 0; i < 9; i++)
		{
			if (!domain[row][i].contains(num))
				domain[row][i].add(num);
		}
		// Prune columns
		for (int i = 0; i < 9; i++)
			if (!domain[i][col].contains(num))
				domain[i][col].add(num);
		// Prune the box
		int rowOffset = (row / 3);
		int colOffset = (col / 3);
		int boxStartRow = (3 * rowOffset);
		int boxStartCol = (3 * colOffset);
		
		for (int r = 0; r < 3; r++)
			for (int c = 0; c < 3; c++)
				if (!domain[boxStartRow + r][boxStartCol + c].contains(num))
					domain[boxStartRow + r][boxStartCol + c].add(num);
	}
	
	/////////////////////////////////////////////////////////////////////
	// This simple method should take in a coord and return the proper 
	// index of it it in the domain arraylist
	/////////////////////////////////////////////////////////////////////
	static int coordToDomainIndex(SudokuCoord coord)
	{
		int counter = 0;
		for (int r = 0; r < N; r++) {
			for (int c = 0; c < N; c ++)
			{
				if (r == coord.row && c == coord.col)
					return counter;
				counter++;
			}
		}
		return -1; // BAD 
		
	}

	/////////////////////////////////////////////////////////////////////
	// A utility function to print grid
	/////////////////////////////////////////////////////////////////////
	static void printGrid(int grid[][])
	{
		for (int row = 0; row < N; row++)
		{
			for (int col = 0; col < N; col++)
			{
				if (grid[row][col] == 0)
					System.out.print("- ");
				else
					System.out.print(grid[row][col] + " ");
				
				if ((col+1) % 3 == 0)
					System.out.print(" ");
			}	    	   
			System.out.print("\n");
			if ((row+1) % 3 == 0)
				System.out.println();
		}
	}
}