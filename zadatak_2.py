import requests
import os
import geopandas as gpd

# Dohvat GeoJSON podataka s API-ja
url = "https://plovput.li-st.net/getObjekti/"
response = requests.get(url)
geojson_data = response.json()

# Učitavanje dohvaćenih podataka u GeoDataFrame objekt
gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

# Pridruživanje odgovarajućeg CRS-a GeoDataFrame objektu
if "crs" in geojson_data and geojson_data["crs"]["properties"]["name"]:
    crs_name = geojson_data["crs"]["properties"]["name"]
    gdf.set_crs(crs_name, inplace=True)

record_count = len(gdf)
print(f"Broj zapisa (objekata sigurnosti plovidbe): {record_count}")

# Filtriranje zapisa 
filtered_gdf = gdf.loc[gdf["tip_objekta"] == 16, :]

filtered_count = len(filtered_gdf)
print(f"Broj zapisa (objekata sigurnosti plovidbe) tipa objekta 16: {filtered_count}")

# Stvaranje izlazne direktorije za spremanje .geojson datoteke
if not os.path.exists(os.path.join(os.getcwd(), "zadatak_2_output")):
    os.mkdir(os.path.join(os.getcwd(), "zadatak_2_output"))

# Spremanje .geojson datoteke s filtriranim podatcima
filtered_data_path = os.path.join(os.getcwd(), "zadatak_2_output", "zapisi_tip_objekta_16.geojson")
filtered_gdf.to_file(filtered_data_path, driver="GeoJSON")
