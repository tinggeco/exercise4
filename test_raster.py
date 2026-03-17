import numpy as np
import xarray as xr
import rioxarray

# Create a synthetic 10x10 DEM with a valley profile (elevation in meters)
elevation = np.array([
    [500, 450, 350, 200, 120,  80, 120, 200, 350, 500],
    [480, 430, 330, 180, 100,  60, 100, 180, 330, 480],
    [460, 410, 310, 160,  80,  40,  80, 160, 310, 460],
    [450, 400, 300, 150,  70,  30,  70, 150, 300, 450],
    [440, 390, 290, 140,  60,  20,  60, 140, 290, 440],
    [450, 400, 300, 150,  70,  30,  70, 150, 300, 450],
    [460, 410, 310, 160,  80,  40,  80, 160, 310, 460],
    [480, 430, 330, 180, 100,  60, 100, 180, 330, 480],
    [500, 450, 350, 200, 120,  80, 120, 200, 350, 500],
    [520, 470, 370, 220, 140, 100, 140, 220, 370, 520],
], dtype=np.float32)

# Wrap as xarray DataArray with spatial metadata
from rasterio.transform import from_bounds
transform = from_bounds(304000, 2637000, 304200, 2637200, 10, 10)

da = xr.DataArray(
    elevation[np.newaxis, :, :],
    dims=["band", "y", "x"],
    coords={
        "band": [1],
        "y": np.linspace(2637200, 2637000, 10),
        "x": np.linspace(304000, 304200, 10),
    },
)
# IMPORTANT: write_transform first, then write_crs last (order matters!)
da = da.rio.write_transform(transform)
da = da.rio.write_crs("EPSG:3826")

print("✅ rioxarray works!")
print(f"Shape: {da.shape}")
print(f"CRS: {da.rio.crs}")
print(f"Resolution: {da.rio.resolution()}")
print(f"Min elevation: {float(da.min()):.1f} m")
print(f"Max elevation: {float(da.max()):.1f} m")

# Test slope computation with numpy
dy, dx = np.gradient(elevation, 20)  # 20m resolution
slope_rad = np.arctan(np.sqrt(dx**2 + dy**2))
slope_deg = np.degrees(slope_rad)
print(f"\nSlope range: {slope_deg.min():.1f}° – {slope_deg.max():.1f}°")

print("\n✅ All checks passed! You are ready for Week 4.")
