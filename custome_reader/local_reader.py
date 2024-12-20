from rio_tiler.io import COGReader
from typing import Any, Dict, Union
from rio_tiler.models import ImageData
import rasterio
import numpy as np
import logging

logger = logging.getLogger(__name__)

class LocalCOGReader(COGReader):
    def __init__(self, filepath: str, *args: Any, **kwargs: Any):
        """Initialize with a local file path."""
        super().__init__(filepath, *args, **kwargs)

    def preview(
        self,
        max_size: int = 1024,
        height: int = None,
        width: int = None,
        **kwargs: Any,
    ) -> ImageData:
        """Read preview from local COG."""
        # Log input parameters
        logger.debug(f"Preview parameters: {kwargs}")
        
        # Convert bidx to indexes parameter
        if "bidx" in kwargs:
            kwargs["indexes"] = kwargs.pop("bidx")
            if isinstance(kwargs["indexes"], (list, tuple)) and len(kwargs["indexes"]) > 4:
                kwargs["indexes"] = kwargs["indexes"][:3]
        else:
            kwargs["indexes"] = [1, 2, 3]  # Default RGB
            
        # Force single band for colormap
        if "colormap_name" in kwargs or "colormap" in kwargs:
            kwargs["indexes"] = kwargs["indexes"][0] if isinstance(kwargs["indexes"], (list, tuple)) else 1
        
        # Get image data
        data = super().preview(
            max_size=max_size,
            height=height,
            width=width,
            **kwargs
        )
        
        logger.debug(f"Data shape: {data.data.shape}")
        return data