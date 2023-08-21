# -*- coding: utf-8 -*-
import asyncio
from functools import cached_property
from typing import List, Set

from wyvern.components.models.model_component import (
    ModelComponent,
    ModelInput,
    ModelOutput,
)
from wyvern.components.ranking_pipeline import RankingRequest
from wyvern.entities.identifier import CompositeIdentifier

from pipelines.product_ranking.schemas import Product


class RankingModel(
    ModelComponent[
        ModelInput[
            Product,
            RankingRequest[Product],
        ],
        ModelOutput[float],
    ],
):
    @cached_property
    def manifest_feature_names(self) -> Set[str]:
        return {
            "RealtimeProductFeature:search_score",
            "RealtimeProductQueryFeature:query_category_similarity",
            "RealtimeProductQueryFeature:query_brand_similarity",
            "RealtimeProductQueryFeature:query_title_similarity",
            "RealtimeProductQueryFeature:query_description_similarity",
        }

    async def batch_inference(
        self,
        request: RankingRequest[Product],
        entities: List[Product],
        **kwargs,
    ) -> List[float]:
        return await asyncio.gather(
            *[self._inference_helper(request, entity) for entity in entities]
        )

    async def _inference_helper(
        self,
        request: RankingRequest[Product],
        entity: Product,
    ) -> float:
        score = 0.0
        composite_identifier = CompositeIdentifier(
            primary_identifier=entity.identifier,
            secondary_identifier=request.query.identifier,
        )
        search_score = self.get_feature(
            entity.identifier,
            "RealtimeProductFeature:search_score",
        )
        query_category_similarity = self.get_feature(
            composite_identifier,
            "RealtimeProductQueryFeature:query_category_similarity",
        )
        query_brand_similarity = self.get_feature(
            composite_identifier,
            "RealtimeProductQueryFeature:query_brand_similarity",
        )
        query_title_similarity = self.get_feature(
            composite_identifier,
            "RealtimeProductQueryFeature:query_title_similarity",
        )
        query_description_similarity = self.get_feature(
            composite_identifier,
            "RealtimeProductQueryFeature:query_description_similarity",
        )
        if search_score:
            score += 2 * search_score
        if query_category_similarity:
            score += 10 * query_category_similarity
        if query_brand_similarity:
            score += 20 * query_brand_similarity
        if query_title_similarity:
            score += 22 * query_title_similarity
        if query_description_similarity:
            score += 13 * query_description_similarity

        return score
