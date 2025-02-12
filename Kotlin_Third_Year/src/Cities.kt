// Data class to represent an intercity road between two cities with a specified distance
class Cities
{
    // Map to store city names and their corresponding unique identifiers
    private val cityNumbers: MutableMap<String, Int> = mutableMapOf()
    private val cityNames: MutableList<String> = mutableListOf()

    // Function to retrieve the unique identifier for a city name
    // If the city does not already have an identifier, it assigns a new one
    public fun getCityNumber(cityName: String): Int {
        // Retrieves the city identifier if it exists in the map
        val cityNumber: Int? = cityNumbers[cityName]
        val nextValue = cityNumbers.size

        // If the city does not have an identifier, adds it to the map
        if (cityNumber == null){
            cityNumbers[cityName] = nextValue
            cityNames.add(cityName)
            return nextValue
        }

        else {
            // Otherwise, returns the existing city identifier
            return cityNumber
        }
    }

    // Retrieves the name of a city given its unique identifier
    public fun getCityName (cityNumber: Int): String
        = cityNames[cityNumber]

    // Returns the total number of cities managed by this class
    public val size: Int
        get() = cityNumbers.size

}