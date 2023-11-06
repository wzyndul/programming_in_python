# the position of each animal in the meadow is defined as a pair of floating-point numbers
from simulation import Simulation

# The initial position of each sheep is chosen randomly at the start

# The initial position of the wolf is the center of the meadow, that is the point (0.0; 0.0).

# SHEEP MOVE
# The simulation is advanced in rounds. In the first stage of every round, all alive sheep move one by one,
# a sheep first randomly chooses one of the four directions: north (up), south (down), east (right), or west (left),
# and then moves a predefined distance in the chosen direction

# WOLF MOVE
# the wolf first determines which sheep is closest to it in terms of the Euclidean distance,
# and subsequently checks whether this sheep is within the range of its attack, that is whether
# the Euclidean distance to the sheep is not greater than the distance that the wolf moves when
# chasing a sheep; if this is the case, the wolf eats the sheep, which means that the sheep disappears
# and the wolf takes its position, whereas if this is not the case, the wolf starts chasing the sheep,
# moving a predefined distance towards it (if there are more than one sheep within the same closest distance,
# the wolf takes its actions with respect only to the first one)


#  The simulation ends either when all sheep have been eaten or when a predefined maximum number of rounds has been reached.

simulation = Simulation(round_nr=50, sheep_nr=15, limit=10, sheep_move=0.5,
                        wolf_move=1.0)
simulation.start()
