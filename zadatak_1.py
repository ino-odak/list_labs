import rasterio
import numpy as np
import os

image_path = os.path.join(os.getcwd(), "data", "response_bands.tiff")
dataset = rasterio.open(image_path)

band_count = dataset.count
print(f"Satelitska snimka sadrži {band_count} kanala (bandova).\n")

# Dohvaćanje relevantnih bandova (kanala)
red = dataset.read(4) 
nir = dataset.read(8) 
swir = dataset.read(11)

# Ignoriranje "invalid value encountered in divide" upozorenja radi čistoće standardnog izlaza
with np.errstate(invalid="ignore"):
    # Izračun NDVI
    ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)
ndvi = np.nan_to_num(ndvi, nan=0)  # Rukovanje dijeljenjem s nula
ndvi = np.clip(ndvi, -1, 1)

# Ignoriranje "invalid value encountered in divide" upozorenja radi čistoće standardnog izlaza
with np.errstate(invalid="ignore"):
    # Izračun NDMI
    ndmi = (nir.astype(float) - swir.astype(float)) / (nir + swir)
ndmi = np.nan_to_num(ndmi, nan=0)  # Rukovanje dijeljenjem s nula
ndmi = np.clip(ndmi, -1, 1)

# Stvaranje izlazne direktorije za spremanje .tiff datoteka
if not os.path.exists(os.path.join(os.getcwd(), "zadatak_1_output")):
    os.mkdir(os.path.join(os.getcwd(), "zadatak_1_output"))

# Spremanje NDVI u .tiff datoteku
ndvi_path = os.path.join(os.getcwd(), "zadatak_1_output", "ndvi.tiff")
ndvi_meta = dataset.meta
ndvi_meta.update(dtype=rasterio.float32, count=1)
with rasterio.open(ndvi_path, 'w', **ndvi_meta) as f:
    f.write(ndvi.astype(rasterio.float32), 1)

# Spremanje NDMI u .tiff datoteku
ndmi_path = os.path.join(os.getcwd(), "zadatak_1_output", "ndmi.tiff")
ndmi_meta = dataset.meta
ndmi_meta.update(dtype=rasterio.float32, count=1)
with rasterio.open(ndmi_path, 'w', **ndmi_meta) as f:
    f.write(ndmi.astype(rasterio.float32), 1)

# Izračun i ispis prosječnih NDVI i NDMI vrijednosti
avg_ndvi = np.mean(ndvi)
avg_ndmi = np.mean(ndmi)
print(f"\nProsječni NDVI: {avg_ndvi:.5f}")
print(f"Prosječni NDMI: {avg_ndmi:.5f}")
