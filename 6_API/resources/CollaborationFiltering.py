# -*- coding: utf-8 -*-
import sys
import numpy as np

sys.path.append("..")
import config

from flask_restful import Resource

class RecommendClothes(Resource):
    def get(self):
        recommendRun()
        return {"message": "Success"}
    
    def post(self):
        recommendRun()
        return {"message": "Success"}


# %%
import datetime

from sqlalchemy import create_engine
from sqlalchemy import or_, and_, exists
from sqlalchemy.orm import sessionmaker
from resources.DbModels import MusinsaReview, MusinsaCustomer, BPCustomer, BPRating, RecommendGoods, GoodsOption, Calendar, WeatherCode, GoodsTag, Closet
from sklearn.metrics.pairwise import cosine_similarity

def getweatherDictTag(weatherObj, weatherTag): 
    return {"PR_21": round(weatherObj.snowRate, 2)
            , "PR_22": round(weatherObj.sunnyRate, 2)
            , "PR_23": round(weatherObj.cloudyRate, 2)
            , "PR_24": round(weatherObj.rainRate, 2)}[weatherTag]

# %% 추천 고객 확인 및 추천 진행
def recommendRun():
    # %% Create and engine and get the metadata
    engine = create_engine(
        config.SQLALCHEMY_DATABASE_URI,
        encoding='utf8',
        echo=False)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    conn = engine.connect()
    session = Session()
    
    weatherDict = {"PR_21":"snow", "PR_22":"sunny", "PR_23":"cloudy", "PR_24":"rain"}
    bottomCodeList = ["PR_1c", "PR_1d","PR_1h", "PR_1l"]
    topCodeList = ["PR_1a", "PR_1b","PR_1e", "PR_1f", "PR_1g", "PR_1i", "PR_1j", "PR_1k", "PR_1m"]
    if session.query(
        exists().where(
            and_(
                Calendar.recommendCode == "CD_1"))).scalar():
    
        # 추천을 진행할 고객 저장 & 중복 제거
        recm_sche_set = set(
            session.query(
                Calendar.calSerialNo).filter(
                Calendar.recommendCode == "CD_1").all())
    
        # 고객별로 추천 start
        for recm_sche in recm_sche_set:
            # 추천 고객 DB 확인
            recm_sche = session.query(Calendar).filter(
                Calendar.calSerialNo == recm_sche.calSerialNo).first()
            
            weatherObj = session.query(WeatherCode).filter(
                WeatherCode.weatherCodeId == recm_sche.weather).first()
    
            # %% 테스트용 고객 설정
    #        recm_cust = session.query(BPCustomer).filter(
    #            BPCustomer.bpCustomerId == 'test').first()
    
            # %% 옷장 변수 초기화
            # 고객 옷장 상품 List
            customer_goods_dict = dict()
            # 고객 옷장 상품특성 List
            customer_goods_tag_dict = dict()
            # 고객 옷장 예상값 합계 List
            customer_goods_sum_dict = dict()
            
            # %% 옷장 의상 일정 특성별 필터링
            for closet in session.query(Closet).filter(Closet.bpCustomerId == recm_sche.bpCustomerId).all():
               customer_goods_dict[closet.serialNo] = closet
               for goodsTag in session.query(GoodsTag).filter(and_(
                       closet.serialNo == GoodsTag.goodsId
                       , GoodsTag.malCf1Code == 'PV_1')).all():
                   secondKey = str(goodsTag.goodsId) + "," + goodsTag.predictCode
                   customer_goods_tag_dict[secondKey] = goodsTag
                   # 날씨 가중치
                   for weatherTag in weatherDict:
                       if weatherTag == goodsTag.predictCode:
                           weather_alpha = getweatherDictTag(weatherObj, weatherTag)
                           wa_prdictRate = round(customer_goods_tag_dict[secondKey].prdictRate, 2) + weather_alpha
                           customer_goods_tag_dict[secondKey].prdictRate =  wa_prdictRate
                   # 카테고리 가중치
                   if recm_sche.type == goodsTag.predictCode:
                       cate_alpha = 100
                       ca_prdictRate = round(customer_goods_tag_dict[secondKey].prdictRate, 2) + cate_alpha
                       customer_goods_tag_dict[secondKey].prdictRate =  ca_prdictRate
                   # 온도 가중치
                   if goodsTag.predictCode == 'PR_41' or goodsTag.predictCode == 'PR_42':
                       if goodsTag.prdictRate >= (int(recm_sche.mintemp) - 3) and goodsTag.prdictRate <= (int(recm_sche.maxtemp) + 3):
                           customer_goods_tag_dict[secondKey].prdictRate = 100
                       else:
                           customer_goods_tag_dict[secondKey].prdictRate = 0
            
            # 의상별 예상값 합계
            for key in customer_goods_tag_dict.keys():
                if key.split(',')[0] in customer_goods_sum_dict:
                    customer_goods_sum_dict[key.split(',')[0]] += customer_goods_tag_dict[key].prdictRate
                else:
                    customer_goods_sum_dict[key.split(',')[0]] = customer_goods_tag_dict[key].prdictRate
            
            customer_goods_sum_list = sorted(customer_goods_sum_dict, key=lambda x: customer_goods_sum_dict[x], reverse=True)
            
            topList = []
            bottomList = []
            for goodsid in customer_goods_sum_list:
                for key in customer_goods_tag_dict.keys():
                    if key.split(',')[0] == goodsid and key.split(',')[1] in bottomCodeList and customer_goods_tag_dict[key].bestYn == 'Y':
                        bottomList.append(goodsid)
                    elif key.split(',')[0] == goodsid and key.split(',')[1] in topCodeList and customer_goods_tag_dict[key].bestYn == 'Y':
                        topList.append(goodsid)
            
            # 옷장 추천의상 Add
            for i in range(min(len(topList), 2)):
                goodsid = topList[i]
                session.add(RecommendGoods(
                        calSerialNo = recm_sche.calSerialNo
                        , bpCustomerId = recm_sche.bpCustomerId
                        , recommendGoodsId = goodsid
                        , malCf1Code = 'PV_1'
                        , malCf1Name = 'top'
                        , recommendCoditionCode = 'CD_2'
                        , recommendCoditionCodeName = 'complete'
                        , createDate = datetime.datetime.now()))
            for i in range(min(len(bottomList), 2)):
                goodsid = bottomList[i]
                session.add(RecommendGoods(
                        calSerialNo = recm_sche.calSerialNo
                        , bpCustomerId = recm_sche.bpCustomerId
                        , recommendGoodsId = goodsid
                        , malCf1Code = 'PV_1'
                        , malCf1Name = 'bottom'
                        , recommendCoditionCode = 'CD_2'
                        , recommendCoditionCodeName = 'complete'
                        , createDate = datetime.datetime.now()))
            
            
            # %% 쇼핑몰 변수 초기화
            # 추천 고객이 구입한 상품 리스트
            recm_cust_bpRating_dict = dict()
            # 추천 고객과 유사한 고객 set
            similar_customer_set = set()
            # 유사한 고객들이 산 모든 상품 평점 dict
            all_goods_dict = dict()
            # 유사한 고객별 상품 dict
            all_customer_goods_dict = dict()
            # 쇼핑몰 GoodsList
            best_goods_list = set()
            
            # %% 쇼핑몰 의상 일정 특성별 필터링
            # 날씨 Goods
            for weatherTag in weatherDict:
                weather_alpha = getweatherDictTag(weatherObj, weatherTag)
                if weather_alpha > 10:
                    for goodsTag in session.query(GoodsTag).filter(and_(
                            GoodsTag.malCf1Code == 'RE_1'
                            , GoodsTag.predictCode == weatherTag
                            , GoodsTag.prdictRate >= (weather_alpha - 5))).all():
                        best_goods_list.add(goodsTag.goodsId)
            
            # 카테고리 Goods
            for goodsTag in session.query(GoodsTag).filter(and_(
                    GoodsTag.malCf1Code == 'RE_1'
                    , GoodsTag.predictCode == recm_sche.type
                    , GoodsTag.prdictRate >= 45)).all():
                best_goods_list.add(goodsTag.goodsId)
            
            # 온도 Goods
            for goodsTag in session.query(GoodsTag).filter(and_(
                    GoodsTag.malCf1Code == 'RE_1'
                    , or_(GoodsTag.predictCode == 'PR_41', goodsTag.predictCode == 'PR_42')
                    , GoodsTag.prdictRate <= (int(recm_sche.maxtemp) + 3)
                    , GoodsTag.prdictRate >= (int(recm_sche.mintemp) - 3))).all():
                best_goods_list.add(goodsTag.goodsId)
            
            # %% 유사 고객 리스트 만들기
            recm_cust = session.query(BPCustomer).filter(
                BPCustomer.bpCustomerId == recm_sche.bpCustomerId).first()
            # 키, 몸무게 비슷한 고객들 customerId 리스트에 저장
            for m_cust in session.query(MusinsaCustomer).filter(
                and_(
                    MusinsaCustomer.musinsaCustomerHeight >= recm_cust.bpCustomerHeight - 1,
                    MusinsaCustomer.musinsaCustomerHeight <= recm_cust.bpCustomerHeight + 1,
                    MusinsaCustomer.musinsaCustomerWeight >= recm_cust.bpCustomerWeight - 1,
                    MusinsaCustomer.musinsaCustomerWeight <= recm_cust.bpCustomerWeight + 1
                    )).all():
                similar_customer_set.add(m_cust.musinsaCustomerId)
    
            # 추천 고객과 같은 상품을 구입한 고객들 customerId 리스트에 저장
            for goods_rating in session.query(BPRating).filter(
                and_(
                    BPRating.bpCustomerId == recm_cust.bpCustomerId,
                    BPRating.malCf1Code == "RE_1")).all():
                # 추천 고객이 Rating을 매긴 무신사 상품(아이디, 평점) 저장
                recm_cust_bpRating_dict[goods_rating.goodsId] = goods_rating.bpReviewStars
                # 같은 상품을 구입한 고객 아이디 저장
                for m_review in session.query(MusinsaReview).filter(
                    MusinsaReview.musinsaGoodsId == goods_rating.goodsId).all():
                    similar_customer_set.add(m_review.musinsaCustomerId)
    
            # %% 유사한 고객들이 구입한 모든 상품(아이디, 평점) 저장
            for similar_cust_id in similar_customer_set:
                all_customer_goods_dict[similar_cust_id] = dict()
                for similar_cust_review in session.query(MusinsaReview).filter(
                        MusinsaReview.musinsaCustomerId == similar_cust_id).group_by(
                        MusinsaReview.musinsaGoodsId).all():
                    
                    #일정 특성별 필터링 의상군 제한
                    if similar_cust_review.musinsaGoodsId in best_goods_list:
                        # 고객별 상품 저장
                        all_customer_goods_dict[similar_cust_id][similar_cust_review.musinsaGoodsId] = similar_cust_review.musinsaReviewStars
    
                        # 상품별 평점 저장
                        if similar_cust_review.musinsaGoodsId in all_goods_dict:
                            all_goods_dict[similar_cust_review.musinsaGoodsId].append(
                                similar_cust_review.musinsaReviewStars)
                        else:
                            all_goods_dict[similar_cust_review.musinsaGoodsId] = [
                                similar_cust_review.musinsaReviewStars]
    
            # %% 추천 고객 평점 배열 만들기
            recm_cust_rating = []
    
            for goodsId in all_goods_dict.keys():
                # 평점이 있으면 저장, 없으면 평균 저장
                if goodsId in recm_cust_bpRating_dict:
                    recm_cust_rating.append(recm_cust_bpRating_dict[goodsId] * 10)
                else:
                    recm_cust_rating.append(
                        np.mean(np.array(all_goods_dict[goodsId])))
    
            recm_cust_rating_reshape = np.array(recm_cust_rating).reshape(1, -1)
    
            # %% 기존 고객들 배열 만들고 유사도 검증
            # 코사인 유사도 * 평점 리스트
            cos_mul_rate = [0] * len(similar_customer_set)
    
            # 유사 고객들이 매긴 점수가 있으면 저장, 없으면 평균 저장
            for index, similar_cust_id in enumerate(similar_customer_set):
                similar_cust_rating = []
                for goodsId in all_goods_dict.keys():
                    if goodsId in all_customer_goods_dict[similar_cust_id].keys():
                        similar_cust_rating.append(
                            all_customer_goods_dict[similar_cust_id][goodsId])
                    else:
                        similar_cust_rating.append(
                            np.mean(np.array(all_goods_dict[goodsId])))
                similar_cust_rating_np = np.array(similar_cust_rating)
                similar_cust_rating_reshape = similar_cust_rating_np.reshape(1, -1)
    
                # 기존 고객들과 신규 고객 사이 cosine 유사도 구하기
                cos_sm = cosine_similarity(
                    recm_cust_rating_reshape,
                    similar_cust_rating_reshape)
                cos_mul_rate[index] = similar_cust_rating_np * cos_sm
    
            # 상품별 유사도 평균 계산
            cos_mul_rate_np = np.array(cos_mul_rate)
            cos_mul_rate_np = np.sum(cos_mul_rate_np, axis=1)
            cos_mul_rate_np = np.sum(cos_mul_rate_np, axis=0)
            cos_mul_rate_result = cos_mul_rate_np / len(similar_customer_set)
            cos_mul_rate_result = cos_mul_rate_result.tolist()
    
            # %% 유사도가 높은 상품 추천
            topList = list()
            bottomList = list()
            for i in range(len(cos_mul_rate_result)):
                if len(topList) >= 2 and len(bottomList) >= 2:
                    break
                maxIndex = cos_mul_rate_result.index(max(cos_mul_rate_result))
                goodsid = list(all_goods_dict.keys())[maxIndex]
                goodsOption = session.query(GoodsOption).filter(GoodsOption.goodsId == goodsid).first()
                if goodsOption.codeId[3] == '3':
                    bottomList.append(goodsid)
                else:
                    topList.append(goodsid)
                cos_mul_rate_result.pop(maxIndex)
                all_goods_dict.pop(goodsid)
            
            #%%
            # 옷장 추천의상 Add
            for i in range(min(len(topList), 2)):
                goodsid = topList[i]
                session.add(RecommendGoods(
                        calSerialNo = recm_sche.calSerialNo
                        , bpCustomerId = recm_sche.bpCustomerId
                        , recommendGoodsId = goodsid
                        , malCf1Code = 'RE_1'
                        , malCf1Name = 'top'
                        , recommendCoditionCode = 'CD_2'
                        , recommendCoditionCodeName = 'complete'
                        , createDate = datetime.datetime.now()))
            for i in range(min(len(bottomList), 2)):
                goodsid = bottomList[i]
                session.add(RecommendGoods(
                        calSerialNo = recm_sche.calSerialNo
                        , bpCustomerId = recm_sche.bpCustomerId
                        , recommendGoodsId = goodsid
                        , malCf1Code = 'RE_1'
                        , malCf1Name = 'bottom'
                        , recommendCoditionCode = 'CD_2'
                        , recommendCoditionCodeName = 'complete'
                        , createDate = datetime.datetime.now()))

            recm_sche.recommendCode = 'CD_2'
            recm_sche.updateDate = datetime.datetime.now()
            session.add(recm_sche)
            session.commit()
    
    # %% 추천할 고객 없음
    else:
        print("no schedule")
    
    # %% 세션 종료
    session.close()
    conn.close()
    engine.dispose()
