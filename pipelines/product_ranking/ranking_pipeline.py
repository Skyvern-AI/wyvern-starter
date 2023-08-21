# -*- coding: utf-8 -*-
from wyvern.components.models.model_component import ModelComponent
from wyvern.components.ranking_pipeline import RankingPipeline, RankingResponse

from pipelines.product_ranking.models import RankingModel
from pipelines.product_ranking.schemas import MyRankingRequest, Product


class MyRankingPipeline(RankingPipeline[Product]):
    REQUEST_SCHEMA_CLASS = MyRankingRequest
    RESPONSE_SCHEMA_CLASS = RankingResponse

    def get_model(self) -> ModelComponent:
        return RankingModel()
