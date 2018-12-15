from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from .secret_keys import *

class ImageRater():

    ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"
    project_id = get_projectid_customvision()

    def __init__(self):
        self.predictor = CustomVisionPredictionClient(get_customvision_predictionkey(), endpoint=self.ENDPOINT)

    def rate_image(self, img_url):

        results =  self.predictor.predict_image_url(self.project_id, url=img_url)


        prediction = results.predictions[0]
        probability = "{0:.2f} ".format(prediction.probability)
        label = prediction.tag_name

        friendly_results = dict()
        friendly_results['label'] = label
        friendly_results['confidence'] = probability

        return friendly_results
