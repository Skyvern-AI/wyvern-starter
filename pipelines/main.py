# -*- coding: utf-8 -*-
from wyvern.service import WyvernService

from pipelines.product_ranking.ranking_pipeline import MyRankingPipeline
from pipelines.product_ranking.realtime_features import (
    RealtimeProductFeature,
    RealtimeProductQueryFeature,
)

app = WyvernService.generate_app(
    route_components=[MyRankingPipeline],
    realtime_feature_components=[RealtimeProductFeature, RealtimeProductQueryFeature],
)
