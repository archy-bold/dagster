from typing import Mapping, Optional

from dagster import AssetMaterialization, DagsterInstance
from dagster._core.definitions.asset_spec import AssetSpec
from dagster._core.definitions.assets import AssetsDefinition
from dagster._core.definitions.decorators.asset_decorator import asset
from dagster._core.definitions.events import CoercibleToAssetKey
from dagster._core.definitions.metadata import MetadataValue
from dagster._core.events import DagsterEvent, DagsterEventType, StepMaterializationData


# This creates an AssetsDefinition that contains an asset that is never
# meant to be materialized by Dagster. Presumably we would disable
# button in the UI (it would act more like a source asset). However
# this allows Dagster to act as a data observability tool and lineage
# tool for assets defined elsewhere
def create_unmanaged_asset(asset_spec: AssetSpec) -> AssetsDefinition:
    @asset(key=asset_spec.asset_key, deps=[dep.asset_key for dep in asset_spec.deps])
    def _unmanaged_asset(_) -> None:
        raise Exception("Illegal to materialize this asset")

    # this is not working
    # @multi_asset(specs=[asset_spec])
    # def _dummy_asset(_):
    #     raise Exception("illegal to materialize this asset")
    return _unmanaged_asset


# This is used by external computations to report materializations
# Right now this hits the DagsterInstance directly, but we would
# change this to hit the Dagster GraphQL API or some sort of ext-esque channel
def report_asset_materialization(
    asset_key: CoercibleToAssetKey,
    metadata: Optional[Mapping[str, MetadataValue]] = None,
    description: Optional[str] = None,
    partition: Optional[str] = None,
    tags: Optional[Mapping[str, str]] = None,
    instance: Optional[DagsterInstance] = None,
    run_id: Optional[str] = None,
    job_name: Optional[str] = None,
):
    instance = instance or DagsterInstance.get()
    dagster_event = DagsterEvent.from_external(
        event_type=DagsterEventType.ASSET_MATERIALIZATION,
        event_specific_data=StepMaterializationData(
            AssetMaterialization(
                asset_key=asset_key,
                metadata=metadata,
                description=description,
                tags=tags,
                partition=partition,
            ),
        ),
        job_name=job_name,
    )
    instance.report_dagster_event(dagster_event, run_id=run_id or "runless")
