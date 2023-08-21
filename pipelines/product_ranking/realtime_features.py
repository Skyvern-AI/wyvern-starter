# -*- coding: utf-8 -*-
import random
from typing import Any, Optional

from wyvern.components.features.realtime_features_component import (
    RealtimeFeatureComponent,
)
from wyvern.entities.feature_entities import FeatureData
from wyvern.entities.identifier import CompositeIdentifier
from wyvern.entities.identifier_entities import QueryEntity
from wyvern.wyvern_typing import WyvernFeature

from pipelines.product_ranking.schemas import Product


class RealtimeProductQueryFeature(
    RealtimeFeatureComponent[Product, QueryEntity, Any],
):
    def __init__(self):
        super().__init__(
            output_feature_names={
                "search_score",
                "query_category_similarity",
                "query_brand_similarity",
                "query_title_similarity",
                "query_description_similarity",
            },
        )

    async def compute_composite_features(
        self,
        primary_entity: Product,
        secondary_entity: QueryEntity,
        request: Any,
    ) -> Optional[FeatureData]:
        # compute the potential categories for the query.
        # In another word, given a query, what are the possible categories
        #   that the query is referring to with top 3 probability.
        # For example, if the query is "iphone", the top 3 categories could be "iphone", "iphone case", "iphone charger"

        features: dict[str, WyvernFeature] = {
            # need a model to do category similarity
            "query_category_similarity": random.random(),
            # need a model to do brand similarity
            "query_brand_similarity": random.random(),
            # need a model to do title similarity
            "query_title_similarity": random.random(),
            # need a model to do description similarity
            "query_description_similarity": random.random(),
        }

        return FeatureData(
            identifier=CompositeIdentifier(
                primary_entity.identifier,
                secondary_entity.identifier,
            ),
            features=features,
        )


class RealtimeProductFeature(RealtimeFeatureComponent[Product, Any, Any]):
    def __init__(self):
        super().__init__(
            output_feature_names={
                "search_score",
            },
        )

    async def compute_features(
        self,
        primary_entity: Product,
        request: Any,
    ) -> Optional[FeatureData]:
        features: dict[str, WyvernFeature] = {
            "search_score": primary_entity.search_score or 0.0,
        }

        return FeatureData(
            identifier=primary_entity.identifier,
            features=features,
        )
