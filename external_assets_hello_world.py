from dagster import Definitions
from dagster._core.definitions.asset_spec import AssetSpec
from dagster._core.definitions.unresolved_asset_job_definition import define_asset_job

from external_lib import create_external_asset

# This code location defines metadata exclusively. It expects execution to happen elsewhere.

external_one_asset = AssetSpec(asset_key="external_one")
external_two_asset = AssetSpec(asset_key="external_two", deps=[external_one_asset])
my_job = define_asset_job("my_job")
defs = Definitions(assets=[create_external_asset(external_one_asset), create_external_asset(external_two_asset)], jobs=[my_job])
