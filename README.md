**FF Bingo**

A script that generates a set of random bingo cards with statements taken from txt files.

The statements are taken from the txt files and overlayed on a background image. 
The background image can be changed as needed but offsets and cell dimensions will need to be changed in the script.
The script generalises to any rectangular board size, but the default uses a 5x5 board with a central free square.

The free square is by default taken randomly from a separate pool (separate txt file) but this can be turned off so all
statements are taken from the same pool if desired.

**Usage**

To use script make sure all packages in the `requirements.txt` are installed and run `main.py`. Bingo cards are saved to
the specified output folder in .png format. To edit the pool of random statements simply edit the txt files.

By default, the number of statements must be equal to or greater than the number of cells in your chosen grid. If you do
not have enough statements the `random.choice` functions can be changed to resample from the same pool, however this 
will cause duplicates in your card. To do this change `replace=False` in the `random.choice` functions to be `True`.