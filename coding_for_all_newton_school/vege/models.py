from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os

def get_image_path(instance, filename):
    """
    This function generates a new file name for the uploaded image.
    The file name includes the receipe_name, current date, and current time in (h:mm:ss a) format.
    """
    # Get the extension of the file
    ext = filename.split('.')[-1]
    # Get the current date and time
    now = timezone.now()
    # Generate a new filename using the receipe_name, current date, current time, and original extension
    filename = f"{instance.receipe_name}-{now.strftime('%d-%b-%Y-(%I:%M:%S %p)')}.{ext}"
    # Return the new file path
    return os.path.join('receipe/', filename)

# # Define a function to generate new image file names
# def get_image_path(instance, filename):
#     """
#     This function generates a new file name for the uploaded image.
#     The file name includes the receipe_name, current date, and current time in 24hrs format.
#     With this updated function, the receipe_image field in your Recipe model will generate filenames in the following format: 
    
#     {receipe_name}-{current_date}-{current_time}.{file_extension}.
    
#     For example, if the receipe_name is 'veg-pulao', the current date is 11-Apr-2023, the current time is 153024 (3:30:24 PM), and the original file extension is 'jpg', the resulting filename will be 'veg-pulao-11-Apr-2023-153024.jpg'.
#     """
#     # Get the extension of the file
#     ext = filename.split('.')[-1]
#     # Get the current date and time
#     now = timezone.now()
#     # Generate a new filename using the receipe_name, current date, current time, and original extension
#     filename = f"{instance.receipe_name}-{now.strftime('%d-%b-%Y-%H%M%S')}.{ext}"
#     # Return the new file path
#     return os.path.join('receipe/', filename)

# class Recipe(models.Model):
#     receipe_name = models.CharField(max_length=255)
#     receipe_description = models.TextField()
#     receipe_image = models.ImageField(upload_to='receipe')
    
#     def __str__(self):
#         return self.receipe_name
class Recipe(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,on_delete=models.SET_NULL)
    receipe_name = models.CharField(max_length=255)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to=get_image_path)

    def save(self, *args, **kwargs):
        """
        This method is called when the model is saved, and it allows us to modify the image file name before saving it.
        """
        # If the image field has changed and there is an existing image file, delete it
        if self.pk:
            old_image = Recipe.objects.get(pk=self.pk).receipe_image
            if self.receipe_image != old_image:
                old_image.delete(False)
        # Call the super save method to save the model
        super(Recipe, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.receipe_name
