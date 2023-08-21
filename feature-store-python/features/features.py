# -*- coding: utf-8 -*-
from datetime import timedelta

import yaml
from feast import Entity, FeatureView, Field, SnowflakeSource
from feast.types import Float64

# Define an entity for the product. You can think of an entity as a primary key used to
# fetch features.
product = Entity(name="product", join_keys=["IDENTIFIER"])

# Defines a data source from which feature values can be retrieved. Sources are queried when building training
# datasets or materializing features into an online store.
product_search_qif_source = SnowflakeSource(
    # The Snowflake table where features can be found
    database=yaml.safe_load(open("feature_store.yaml"))["offline_store"]["database"],
    table="YOUR_FEATURE_TABLE",
    # The event timestamp is used for point-in-time joins and for ensuring only
    # features within the TTL are returned
    timestamp_field="YOUR_TIMESTAMP_FIELD",
    schema="YOUR_SCHEMA",
)

# Feature views are a grouping based on how features are stored in either the
# online or offline store.
product_feature_view = FeatureView(
    # The unique name of this feature view. Two feature views in a single
    # project cannot have the same name
    name="product_feature_view",
    # The list of entities specifies the keys required for joining or looking
    # up features from this feature view. The reference provided in this field
    # correspond to the name of a defined entity (or entities)
    entities=[product],
    # The timedelta is the maximum age that each feature value may have
    # relative to its lookup time. For historical features (used in training),
    # TTL is relative to each timestamp provided in the entity dataframe.
    # TTL also allows for eviction of keys from online stores and limits the
    # amount of historical scanning required for historical feature values
    # during retrieval
    ttl=timedelta(weeks=1),
    # The list of features defined below act as a schema to both define features
    # for both materialization of features into a store, and are used as references
    # during retrieval for building a training dataset or serving features
    schema=[
        Field(name="PURCHASE_PAST_15_DAYS", dtype=Float64),
    ],
    source=product_search_qif_source,
    # Tags are user defined key/value pairs that are attached to each
    # feature view
    tags={"team": "team name"},
)
