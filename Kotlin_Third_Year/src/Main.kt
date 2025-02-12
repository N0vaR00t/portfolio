import java.io.File


fun main() {
    val cities = Cities()

    // Path to the file containing capital city data
    print("Enter path to the file: ")
    var filePath: String = readln()

    // Read all lines from the file into a list of strings
    val roads = File(filePath).useLines {
        it.map { line ->
            // Splits each line by comma to extract city names and distance
            val splitline = line.split(", ")
            IntercityRoad(
                cities.getCityNumber(splitline[0]),
                cities.getCityNumber(splitline[1]),
                splitline[2].toInt()
            )
        }.toList()
    }

    // Creates a graph structure with the size based on the number of cities
    val graph = Graph(cities.size)

    // Populates the graph with distances between cities based on the data read from the file
    for (road in roads)
        graph[road.firstCity, road.secondCity] = road.distance

    // Calculates the minimum spanning tree (MST) for the graph
    val mst = Mst(graph)

    // Outputs each road in the MST with city names and distances
    for (road in mst.roads)
        println("${cities.getCityName(road.firstCity)}, ${cities.getCityName(road.secondCity)}, ${road.distance}")
}


