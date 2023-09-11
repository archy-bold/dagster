from dagster import AssetMaterialization, DagsterInstance
from dagster._core.definitions.asset_spec import AssetSpec
from dagster._core.definitions.assets import AssetsDefinition
from dagster._core.definitions.decorators.asset_decorator import asset
from dagster._core.events import DagsterEvent, DagsterEventType, StepMaterializationData


def create_dummy_asset(asset_spec: AssetSpec) -> AssetsDefinition:
    @asset(key=asset_spec.asset_key, deps=[dep.asset_key for dep in asset_spec.deps])
    def _dummy_asset(_) -> None:
        raise Exception("illegal to materialize this asset")

    # this is not working
    # @multi_asset(specs=[asset_spec])
    # def _dummy_asset(_):
    #     raise Exception("illegal to materialize this asset")
    return _dummy_asset

def report_asset_materialization(asset_key: str, metadata: dict):
    instance = DagsterInstance.get()
    dagster_event = DagsterEvent.from_exteral(
        event_type=DagsterEventType.ASSET_MATERIALIZATION,
        event_specific_data=StepMaterializationData(
            AssetMaterialization(asset_key=asset_key, metadata=metadata)
        )
    )
    instance.report_dagster_event(dagster_event, run_id="dummy")
