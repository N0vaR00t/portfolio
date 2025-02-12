import java.awt.BorderLayout                                          // for layout
import java.awt.event.ActionEvent                                     // clicks
import java.io.File                                                   // for working with files
import javax.swing.*                                                  // swing components

fun main() {                                                          // main function to run the GUI

    val frame = JFrame("Telecoms Application")                        // creating the main window
    frame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE                // to close the application
    frame.setSize(400, 300)

    val outputArea = JTextArea()                                      // creating text area
    outputArea.isEditable = false

    val scrollPane = JScrollPane(outputArea)                          // making it scrollable

    val loadFileButton = JButton("Open File")                         // to open files

    loadFileButton.addActionListener { _: ActionEvent ->              // to detect buttons clicks
        val fileChooser = JFileChooser()

        val result = fileChooser.showOpenDialog(frame)

        if (result == JFileChooser.APPROVE_OPTION) {
            val selectedFile: File = fileChooser.selectedFile
            try {
                val cities = Cities()

                val roads = selectedFile.readLines().map {line ->      // to read each line
                    val splitLine = line.split(", ")                   // to split each line into:

                    IntercityRoad(
                        cities.getCityNumber(splitLine[0]),            // city1
                        cities.getCityNumber(splitLine[1]),            // city2
                        splitLine[2].toInt()                           // distance
                    )
                }

                val graph = Graph(cities.size)                         // creating a graph

                roads.forEach { road ->                                // adding each road
                    graph[road.firstCity,
                        road.secondCity] = road.distance
                }

                val mst = Mst(graph)                                   // calling to compute the Minimum Spanning Tree

                val resultText =
                    StringBuilder(
                        "Minimum Spanning Tree (MST):\n\n")

                mst.roads.forEach { road ->
                    resultText.append(
                        "${cities.getCityName(road.firstCity)}, " +
                                "${cities.getCityName(
                                    road.secondCity)}, " +
                                "${road.distance} km\n"
                    )
                }
                outputArea.text = resultText.toString()
            } catch (e: Exception) {                                   // to display an error message
                outputArea.text = "Error Loading File: ${e.message}"
            }
        } else {
            outputArea.text = "No File Selected"                       // if no file was selected
        }
    }

    val panel = JPanel()                                               // creating a panel for outout
    panel.layout = BorderLayout()
    panel.add(loadFileButton,
        BorderLayout.NORTH)
    panel.add(scrollPane,
        BorderLayout.CENTER)

    frame.add(panel)
    frame.isVisible = true
}

