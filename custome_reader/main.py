from fastapi import FastAPI, HTTPException, Depends
from titiler.core.factory import TilerFactory 
from titiler.core.dependencies import DefaultDependency
from custome_reader.local_reader import LocalCOGReader
import os

app = FastAPI()

def validate_filepath(filepath: str):
    """Validate the local file path to prevent security issues."""
    allowed_directory = "data"
    if not os.path.abspath(filepath).startswith(os.path.abspath(allowed_directory)):
        raise HTTPException(status_code=403, detail="Access to this file is forbidden.")
    return filepath

# Create a custom dependency class for filepath parameter
class FilepathParams(DefaultDependency):
    filepath: str = Depends(validate_filepath)

# Create a TilerFactory instance using the LocalCOGReader
local_cog_tiler = TilerFactory(
    reader=LocalCOGReader,
    layer_dependency=FilepathParams  # Use layer_dependency instead of layer_params
)

# Include the router in your application
app.include_router(local_cog_tiler.router, prefix="/local", tags=["Local COG"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}