import java.util.LinkedList

// Class to construct a Minimum Spanning Tree (MST) from the graph
class Mst {

    // Stores the list of intercity roads included in the MST
    var roads: MutableList<IntercityRoad> = mutableListOf()

    // Constructor that takes a graph and generates the MST
    public constructor(graph: Graph) {
        // List of cities not yet included in the MST
        val notAddedCities = LinkedList((1 ..<graph.size).toList())
        val possibleRoads = LinkedList<IntercityRoad>()
        var roadToAdd: IntercityRoad

        // Initialises possible roads from the starting city (0) to other cities
        for (nextCity in 1 ..<graph.size)
            possibleRoads.add(IntercityRoad(0,nextCity, graph[0, nextCity]))

        // Continues adding roads until all cities are included in the MST
        while (notAddedCities.isNotEmpty()) {
            // Finds the road with the shortest distance and adds it to the MST
            roadToAdd = possibleRoads.minBy { road -> road.distance }
            notAddedCities.remove(roadToAdd.secondCity)
            possibleRoads.removeIf { road -> road.secondCity == roadToAdd.secondCity }
            roads.add(roadToAdd)
            // Adds potential roads from the newly added city to the list of possible roads
            for (nextCity in notAddedCities)
                possibleRoads.add(IntercityRoad(
                    roadToAdd.secondCity,
                    nextCity,
                    graph[roadToAdd.secondCity, nextCity]))
        }
    }
}