# -*- coding: utf-8 -*-
from wyvern.feature_store.feature_server import (
    generate_wyvern_store_app,
    start_wyvern_store,
)

from pipelines.main import app as wyvern_app  # noqa: F401

app = generate_wyvern_store_app(path=".")
