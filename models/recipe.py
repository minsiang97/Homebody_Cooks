from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property

class Recipe(BaseModel):
    recipe_name = pw.CharField(null=False)
    description = pw.TextField(null=True)
    image_url = pw.TextField(null=True)

    @hybrid_property
    def recipe_image_path(self):
        from app import app
        if not self.image_url:
            return app.config.get("S3_LOCATION") + "Untitled_Artwork.jpg"
        else:
            return app.config.get("S3_LOCATION") + self.image_url