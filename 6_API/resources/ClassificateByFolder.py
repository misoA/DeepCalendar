import os, sys
sys.path.append("..")
import config

import numpy as np
import ImageClassificator
import S3Image

from sqlalchemy import create_engine, and_, exists
from sqlalchemy.orm import sessionmaker    
from DbModels import Code, GoodsTag
import urllib.request
import datetime

# Create and engine and get the metadata
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, encoding='utf8', echo=False)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
conn = engine.connect()
session = Session()

sys.path.append("..")

detect_path = 'PUT_YOUR_PATH'
predictList = ['schedule', 'weather', 'temperature', 'category']


for bigCatedir in os.listdir(detect_path):
    for smallCatedir in os.listdir(os.path.join(detect_path, bigCatedir)):
        for imageFile in os.listdir(os.path.join(detect_path, bigCatedir, smallCatedir)):
            print("start predict : ", smallCatedir)
            goodsId = imageFile.split('_')[1]
            malCf1Code = ""
            if imageFile.split('_')[0] == 'M':
                malCf1Code = 'RE_1'
                
            for preCode in predictList:
                bestPredict = None
                codeList = session.query(Code).filter(
                        and_(Code.preCodeName == preCode, Code.codeCf == 'clo-cf2'))
                for code in codeList:
                    bestYn = 'N'
                    print("code : "  ,preCode, code.codeName)
                    if not session.query(
                            exists().where(and_(
                                    GoodsTag.goodsId == goodsId
                                    , GoodsTag.malCf1Code == malCf1Code
                                    , GoodsTag.predictCode == code.codeId))).scalar():
                        imageJson = ImageClassificator.anaylsis_with_folder(
                                imageFile
                                , os.path.join(detect_path, bigCatedir, smallCatedir))
                                                
                        if preCode != 'temperature' and imageJson[preCode]['predict'] == code.codeName:
                            bestYn = 'Y'
                        
                        predictRate = ""
                        if preCode == 'temperature':
                            predictRate= imageJson[preCode][code.codeName]
                        else:
                            predictRate = imageJson[preCode]['total'][code.codeName]
                            
                        goods = GoodsTag(goodsId = goodsId
                                         , malCf1Code = malCf1Code
                                         , predictCode = code.codeId
                                         , predictParentsCode = code.preCodeId
                                         , prdictRate = predictRate
                                         , bestYn = bestYn
                                         , createDate = datetime.datetime.now())
                        session.add(goods)
                        session.commit()

session.close()
conn.close()
engine.dispose()
