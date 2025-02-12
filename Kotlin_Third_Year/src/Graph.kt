// Class representing a graph structure, with distance information between cities
class Graph (public  val size: Int) {
    private val elements: IntArray = IntArray(size*size) { Int.MAX_VALUE }

    // Retrieves the distance between two cities in the graph
    public operator fun get(city1: Int, city2: Int): Int
        = elements[city1 * size + city2]

    // Sets the distance between two cities in both directions
    public operator fun set(city1: Int, city2: Int, distance: Int) {
        elements[city1 * size + city2] = distance
        elements[city1 + city2 * size] = distance
    }
}
