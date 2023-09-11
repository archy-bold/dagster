from dagster import Definitions
from dagster._core.definitions.asset_spec import AssetSpec

from external_lib import create_unmanaged_asset

# This code location defines metadata exclusively. It expects execution to happen elsewhere.
unmanaged_asset_one_spec = AssetSpec(asset_key="unmanaged_asset_one")
unmanaged_asset_two_spec = AssetSpec(
    asset_key="unmanaged_asset_two", deps=[unmanaged_asset_one_spec]
)

defs = Definitions(
    assets=[
        create_unmanaged_asset(unmanaged_asset_one_spec),
        create_unmanaged_asset(unmanaged_asset_two_spec),
    ],
)
