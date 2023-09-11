from dagster import Definitions
from dagster._core.definitions.asset_spec import AssetSpec
from dagster._core.definitions.unresolved_asset_job_definition import define_asset_job

from external_lib import create_unmanaged_asset

# This code location defines metadata exclusively. It expects execution to happen elsewhere.

unmanaged_asset_one_asset = AssetSpec(asset_key="unmanaged_asset_one")
unmanaged_asset_two_asset = AssetSpec(asset_key="unmanaged_asset_two", deps=[unmanaged_asset_one_asset])
external_job = define_asset_job("job_representing_external_compute")
defs = Definitions(
    assets=[
        create_unmanaged_asset(unmanaged_asset_one_asset),
        create_unmanaged_asset(unmanaged_asset_two_asset)
    ],
    jobs=[external_job],
)
