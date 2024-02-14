import requests

# Example SPARQL query
sparql_query = """
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
#DECLAREER PREFIXES
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix geo: <http://www.opengis.net/ont/geosparql#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ceo: <https://linkeddata.cultureelerfgoed.nl/def/ceo#>
prefix overheid: <http://standaarden.overheid.nl/owms/terms/> 
PREFIX bif: <http://www.openlinksw.com/schemas/bif#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX uom: <http://www.opengis.net/def/uom/OGC/1.0/>

SELECT *

 {

  ?rm a ceo:Rijksmonument .
  ?rm ceo:rijksmonumentnummer ?rm_n . 
  ?rm ceo:heeftMonumentAard ?aard .
  ?rm ceo:heeftGeometrie/geo:asWKT ?shape_rm.
  ?rm ceo:heeftBasisregistratieRelatie/ceo:heeftProvincie <http://standaarden.overheid.nl/owms/terms/Groningen_(provincie)> .
  ?rm ceo:heeftLocatieAanduiding/ceo:locatienaam ?locatieNaam_ab .


    bind("purple" as ?shape_rmColor)
  BIND(<https://haleconnect.com/ows/services/org.874.7e01e60c-8887-425c-af9b-e2cf6af9181b_wms?SERVICE=WMS&Request=GetCapabilities> as ?mapEndpoint)

}
LIMIT 250
"""

# Example LOD SPARQL endpoint
endpoint = "https://api.linkeddata.cultureelerfgoed.nl/datasets/rce/cho/services/cho/sparql"

# Send SPARQL query to the endpoint
response = requests.get(endpoint, params={"query": sparql_query, "format": "json"})

# Parse the JSON response
data = response.json()
print(data)
# Process the data and generate HTML with Leaflet map
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Leaflet Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
</head>
<body>
    <div id="map" style="height: 1000px;"></div>
    <script>

        
    var map = L.map('map').setView([51.9, 4.5], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    
    // Check if data.results is defined
    if (data.results && data.results.bindings) {
        // Add markers from the SPARQL query results
        data.results.bindings.forEach(function(item) {
            var lat = parseFloat(item.lat.value);
            var long = parseFloat(item.long.value);
            L.marker([lat, long]).addTo(map)
                .bindPopup(item.label.value);
        });
    } else {
        console.error("No results found or unexpected data structure.");
    }


    </script>
</body>
</html>
"""

# Write HTML content to a file
with open("leaflet_map.html", "w") as file:
    file.write(html_content)
