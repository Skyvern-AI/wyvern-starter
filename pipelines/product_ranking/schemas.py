# -*- coding: utf-8 -*-
from wyvern.components.ranking_pipeline import RankingRequest
from wyvern.entities.identifier_entities import ProductEntity


class Product(ProductEntity):
    brand: str | None = None
    category: str | None = None
    categories: list[str] = []
    title: str | None = None
    description: str | None = None
    price: float | None = None
    number_in_stock: int | None = None
    search_score: float | None = None


class MyRankingRequest(RankingRequest[Product]):
    candidates: list[Product]
