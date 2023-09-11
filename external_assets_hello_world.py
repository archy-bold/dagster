from dagster import Definitions
from dagster._core.definitions.asset_spec import AssetSpec
from dagster._core.definitions.unresolved_asset_job_definition import define_asset_job

from external_lib import create_externally_computed_asset

# This code location defines metadata exclusively. It expects execution to happen elsewhere.

external_one_asset = AssetSpec(asset_key="external_one")
external_two_asset = AssetSpec(asset_key="external_two", deps=[external_one_asset])
external_job = define_asset_job("job_representing_external_compute")
defs = Definitions(assets=[create_externally_computed_asset(external_one_asset), create_externally_computed_asset(external_two_asset)], jobs=[external_job])
