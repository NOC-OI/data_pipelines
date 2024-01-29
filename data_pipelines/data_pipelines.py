"""DataFormatConverter: convert data formats from diferents data sources"""
import geopandas as gpd
import rioxarray as rio

from access_bucket.access_bucket import AccessBucket


class DataFormatConverter:
    """DataFormatConverter: convert data formats from diferents data sources"""

    def __init__(self, input_file: str = None, input_format: str = None) -> None:
        """_summary_

        Args:
            input_file (str): File that you want to open. Defaults to None.
            input_format (str): Format of the file that you want to open. Defaults to None.
        """
        self.input_file = input_file
        self.input_format = input_format
        self.input_data = self.open_file()

    def open_file(self):
        """open_file: open the file depending on the file format
        Returns:
            geopandas/xarray: file opened on python
        """
        if self.input_format == "geojson":
            return gpd.read_file(self.input_file)
        if self.input_format == "tif":
            return rio.open_rasterio(self.input_file)
        if self.input_format == "nc":
            return rio.open_rasterio(self.input_file)
        return None

    # def clip_data(self):
    #     """clip data
    #     """
    #     pass

    def convert_format(
        self,
        output_filename: str,
        output_filepath: str,
        output_format: str = "cog",
        upload_file: bool = False,
        bucket_name: str = "haig-fras",
        bucket_folder: str = "layers/bathymetry/gebco",
    ):
        """_summary_

        Args:
            output_filename (str): name of the output file
            output_filepath (str): path of the output
            output_format (str, optional): format of the output. Defaults to "cog".
            upload_file (bool, optional): Boolean that represents if you are going
        to upload the file on the bucket. Defaults to False.
            bucket_name (str, optional): Name of the bucket. Defaults to "haig-fras".
            bucket_folder (str, optional): Path on the bucket. Defaults to
        "layers/bathymetry/gebco".
        """
        self.input_data = self.input_data.rio.write_crs(4326)
        self.input_data = self.input_data.rio.reproject(3857)

        if output_format == "cog":
            # dataset_rio = rio.open_rasterio(str(file))
            # dataset_rio["elevation"].rio.to_raster(output_tif_file)
            # output_cog_file = f'{output_path}/{file.stem}_cog.tif'
            # #input_file = gdal.Open(str(file))

            # gdal.Translate(
            #     output_cog_file,
            #     output_tif_file,
            #     format="COG",
            #     creationOptions=["COMPRESS=LZW", "BIGTIFF=YES"],
            #     callback=progress_callback
            # )
            self.input_data.rio.to_raster(
                raster_path=f"{output_filepath}{output_filename}",
                driver="COG",
                BIGTIFF="YES",
                COMPRESS="LZW",
            )

        print(f"Saved {output_filename} file")
        if upload_file:
            upload_bucket = AccessBucket(bucket=bucket_name)
            upload_bucket.upload(
                file_names=[output_filename],
                path=output_filepath,
                bucket_folder=bucket_folder,
                verbose=1,
            )
