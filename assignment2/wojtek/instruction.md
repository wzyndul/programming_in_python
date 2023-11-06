The task in this assignment is to develop a simulation involving a wolf that tries to catch sheep scattered in a meadow, which uses text mode.

The simulation involves two animal species: a single wolf and a herd of sheep. These animals move around an infinite meadow with no terrain obstacles: the wolf
chases the sheep, trying to catch them and then eat them, while the sheep try (rather clumsily) to escape from the wolf. According to these stipulations,
the meadow is represented as an infinite two-dimensional space with the center located at the point (0.0; 0.0), thus using a Cartesian coordinate system,
whereas the position of each animal in the meadow is defined as a pair of floating-point numbers
(the coordinates can take on both positive and negative values).

At the beginning of the simulation, the initial positions of all animals are determined. The initial position of each sheep is chosen randomly,
with each coordinate being drawn from a range that extends symmetrically around 0 over positive and negative numbers, and where chosen values are
floating-point numbers, which need not be whole. Given that the range is symmetrical around 0, its specification is governed by a single predefined
value that is the absolute value of the limit imposed on the coordinates (hence the range spans from the negative of this value to this value).
The initial position of the wolf is the center of the meadow, that is the point (0.0; 0.0).

The simulation is advanced in rounds. In the first stage of every round, all alive sheep move one by one, and afterwards, in the second stage,
the wolf moves. During its movement, a sheep first randomly chooses one of the four directions: north (up), south (down), east (right), or west
(left), and then moves a predefined distance in the chosen direction. In turn, the wolf first determines which sheep is closest to it in terms
of the Euclidean distance, and subsequently checks whether this sheep is within the range of its attack, that is whether the Euclidean distance
to the sheep is not greater than the distance that the wolf moves when chasing a sheep; if this is the case, the wolf eats the sheep, which
means that the sheep disappears and the wolf takes its position, whereas if this is not the case, the wolf starts chasing the sheep,
 moving a predefined distance towards it (if there are more than one sheep within the same closest distance, the wolf takes its
  actions with respect only to the first one). The simulation ends either when all sheep have been eaten or when a predefined maximum
   number of rounds has been reached.



1.	Implement a simulation as described above. The code should be written in object-oriented manner and should comprise at least two classes: one encapsulating the behavior of a single sheep and the other encapsulating the behavior of the wolf. Create other classes as needed. Adopt the following values:
-	the maximum number of rounds: 50;
-	the number of sheep: 15;
-	the absolute value of the limit imposed on each coordinate of the initial positions of sheep: 10.0 (which implies that the respective range is [-10.0; 10.0]);
-	the distance of sheep movement: 0.5;
-	the distance of wolf movement: 1.0.

To generate random numbers, use the random module from the standard library. If more advanced mathematical calculations are necessary, use the math module from the standard library.
2.	Implement displaying basic information about the status of the simulation at the end of each round. The information should include:
-	the round number;
-	the position of the wolf (to the third decimal place of each coordinate);
-	the number of alive sheep;
-	if the wolf is chasing a sheep - a statement of this fact along with an indication which sheep is being chased (its sequence number);
-	if a sheep was eaten - a statement of this fact along with an indication which sheep it was (its sequence number).

Displaying the above information should not pause the simulation as no interaction with the user is necessary.
3.	Using the json package from the standard library, implement saving the position of every animal at the end of each round to a pos.json file. The file should contain a list of dictionaries, each of which should correspond to an individual round and comprise the following elements:
-	'round_no' - the round number (an integer);
-	'wolf_pos' - the position of the wolf (a pair of floating-point numbers);
-	'sheep_pos' - the positions of all sheep (a list containing as many elements as the number of sheep, with each element being either a pair of floating-point numbers in the case of an alive sheep or the null value, obtained owing to an automatic conversion from the None value, in the case of a sheep that has been eaten).

It is desirable for the content of the file to be nicely formatted, that is divided into successive lines that are appropriately indented. If a pos.json file already exists, it should be overwritten.
4.	Using the csv module from the standard library, implement saving the number of alive sheep at the end of each round to an alive.csv file. The file should contain two columns storing the following values:

    1.	the round number (an integer);
    2.	the number of alive sheep (an integer).
   Each row in the file should correspond to an individual round. If an alive.csv file already exists, it should be overwritten.

