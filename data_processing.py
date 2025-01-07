from rasterio.io import MemoryFile
from rasterio.mask import mask
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling
import numpy as np

def reproject_raster(input_raster, target_crs):
    """
    Reproject a raster image to a target CRS.

    Parameters:
        input_raster (rasterio.io.DatasetReader): Input raster image data.
        target_crs (CRS): Target coordinate reference system.

    Returns:
        dict: Contains the reprojected data array, transform information, and CRS.
    """
    if input_raster.crs != target_crs:

        # Calculate transform and new dimensions for the target CRS
        transform, width, height = calculate_default_transform(
            input_raster.crs, target_crs, input_raster.width, input_raster.height, *input_raster.bounds
        )

        # Create an array to store reprojected data
        destination = np.empty((height, width), dtype=input_raster.read(1).dtype)

        # Perform the reprojection
        reproject(
            source=input_raster.read(1),
            destination=destination,
            src_transform=input_raster.transform,
            src_crs=input_raster.crs,
            dst_transform=transform,
            dst_crs=target_crs,
            resampling=Resampling.nearest
        )

        return {
            "data": destination,
            "transform": transform,
            "crs": target_crs
        }
    else:
        return {
            "data": input_raster.read(1),
            "transform": input_raster.transform,
            "crs": input_raster.crs
        }


def clip_raster(input_raster, roi):
    """
    Clip a raster image to a specified ROI.

    Parameters:
        input_raster (dict): Dictionary containing data array, affine transform, and CRS.
        roi (GeoDataFrame): GeoDataFrame containing the ROI geometry.

    Returns:
        dict: Clipped raster data, including data array, affine transform, and CRS.
    """
    src_data = input_raster["data"]
    src_transform = input_raster["transform"]
    src_crs = input_raster["crs"]

    with MemoryFile() as memfile:
        with memfile.open(
            driver="GTiff",
            height=src_data.shape[0],
            width=src_data.shape[1],
            count=1,
            dtype=src_data.dtype,
            crs=src_crs,
            transform=src_transform,
        ) as dataset:
            dataset.write(src_data, 1)

            # Clip data using Rasterio's mask function
            out_image, out_transform = mask(
                dataset=dataset,
                shapes=roi.geometry,
                crop=True
            )

    return {
        "data": out_image[0],
        "transform": out_transform,  #
        "crs": src_crs
    }


def resample_raster(input_raster, new_resolution):
    """
    Resample a single band to the specified resolution.

    Parameters:
        input_raster (dict): Dictionary containing "data" (numpy.ndarray), "transform" (Affine), and "crs".
        new_resolution (tuple): Target resolution (x, y).

    Returns:
        dict: Contains resampled data array, affine transform, and CRS.
    """
    src_data = input_raster["data"]
    src_transform = input_raster["transform"]
    src_crs = input_raster["crs"]
    src_height, src_width = src_data.shape

    # Calculate target dimensions
    dst_width = int(src_width * (abs(src_transform[0]) / new_resolution[0]))
    dst_height = int(src_height * (abs(src_transform[4]) / new_resolution[1]))

    # Update target affine transform
    dst_transform = from_origin(
        src_transform.c,  # Top-left X coordinate
        src_transform.f,  # Top-left Y coordinate
        new_resolution[0],  # New pixel size X
        new_resolution[1]   # New pixel size Y
    )

    # Create empty array to store resampled data
    resampled_data = np.empty((dst_height, dst_width), dtype=src_data.dtype)

    # Perform resampling
    reproject(
        source=src_data,
        destination=resampled_data,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_transform=dst_transform,
        dst_crs=src_crs,
        resampling=Resampling.bilinear
    )

    return {
        "data": resampled_data,
        "transform": dst_transform,
        "crs": src_crs
    }




