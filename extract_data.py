import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import sys
import logging


def sample_analyze_all_image_file(image_data):
    # Acquire the logger for this client library. Use 'azure' to affect both
    logger = logging.getLogger("azure")

    # Set the desired logging level. logging.INFO or logging.DEBUG are good options.
    logger.setLevel(logging.INFO)

    # Direct logging output to stdout (the default):
    handler = logging.StreamHandler(stream=sys.stdout)
    # Or direct logging output to a file:
    logger.addHandler(handler)

    # Optional: change the default logging format. Here we add a timestamp.
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    handler.setFormatter(formatter)
    # [END logging]

    # Set the values of your computer vision endpoint and computer vision key as environment variables:
    try:
        endpoint = 'https://trojanarmy1.cognitiveservices.azure.com/'
        # key = '5748ca19bfe7450fb304427ade96592e'
        key = 'f0ec9afcf566497995cd690b2a18ddad'

    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
        print("Set them before running this sample.")
        exit()

    # Load image to analyze into a 'bytes' object
    
    # with open(path, "rb") as f:
    #     image_data = f.read()

    # Create an Image Analysis client with none redacted log
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        logging_enable=True
    )
    

    # Analyze all visual features from an image stream. This will be a synchronously (blocking) call.
    result = client.analyze(
        image_data=image_data,
        visual_features=[
            # VisualFeatures.TAGS,
            # VisualFeatures.OBJECTS,
            # VisualFeatures.CAPTION,
            # VisualFeatures.DENSE_CAPTIONS,
            VisualFeatures.READ,
            # VisualFeatures.SMART_CROPS,
            # VisualFeatures.PEOPLE,
        ],  
        smart_crops_aspect_ratios=[0.9, 1.33],  
        gender_neutral_caption=True,  
        language="en",  
        model_version="latest",  
    )

    if result.read is not None:
        data = []
        for line in result.read.blocks[0].lines:
            data.append({'text' : line.text , 'bounding_box' : line.bounding_polygon})
        return data

# if __name__ == "__main__":
#     print(sample_analyze_all_image_file('/Users/anantharaman/Documents/StandardChaterHackathon/flask/Cheque100832.jpg'))