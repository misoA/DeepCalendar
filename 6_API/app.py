from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.S3Image import S3ImageDownload
from resources.ImageDetector import DetectImage
from resources.ImageClassificator import ClassificateImage
from resources.CollaborationFiltering import RecommendClothes
from resources.ImageMatchRater import RatingMatchImage

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

#Route
api.add_resource(Hello, '/Hello')
api.add_resource(S3ImageDownload, '/S3download')
api.add_resource(DetectImage, '/detectImage')
api.add_resource(ClassificateImage, '/ClassificateImage')
api.add_resource(RecommendClothes, '/RecommendClothes')
api.add_resource(RatingMatchImage, '/matchImage')
