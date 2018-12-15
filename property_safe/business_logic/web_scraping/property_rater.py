from .image_rater import ImageRater

class PropertyRater():

    def __init__(self):
        self.customvision_predictor = ImageRater()


    # rates each image of the property and gets an overall rating that
    # is added to the property dictionary
    def rate_property(self, property):
        property_rating = 0

        for image in property['images']:

            image_url = image['url']
            image_rating = self.rate_image(image_url)

            image['rating'] = image_rating
            property_rating += image_rating

            print(image_url + ' ' + str(image_rating))

        property_rating /= len(property['images']) #average image rating

        print('PROPERTY RATING: {}'.format(property_rating))
        print()
        print()
        property['rating'] = property_rating

    # gets the rating for a single image
    def rate_image(self, img_url):

        # get models result
        result = self.customvision_predictor.rate_image(img_url)
        pred_label = result['label']
        confidence = result['confidence']

        # ignore if model not confident enough
        if(float(confidence) < 0.15):
            return 1

        # convert label name to a number for summing up ratings
        rating = self.convert_label_to_points(pred_label)
        return rating


    # very low = 0 point
    # low = 1 points
    # average = 3 points
    # high = 4 points
    # very high = 6 points
    def convert_label_to_points(self, label):
        if(label == 'very low'):
            return 0
        elif(label == 'low'):
            return 1
        elif(label == 'average'):
            return 3
        elif(label == 'high'):
            return 4
        elif(label == 'very high'):
            return 6
        else:
            print("Error in giving label points: "+str(label))
            return -9999
