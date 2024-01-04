import geopandas
import geodatasets
import contextily as cx
import matplotlib.pyplot as plt

df = geopandas.read_file(geodatasets.get_path("nybb"))
ax = df.plot(figsize=(10, 10), alpha=0.5, edgecolor="k")

ax.plot()
plt.show()