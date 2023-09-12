from dagster import Definitions, sensor
from dagster._core.definitions.asset_spec import AssetSpec
from dagster._core.definitions.events import AssetMaterialization, AssetObservation
from dagster._core.definitions.sensor_definition import SensorEvaluationContext

from external_lib import (
    create_observable_asset,
    report_asset_materialization,
    report_asset_observation,
)

# This code location defines metadata exclusively. It expects execution to happen elsewhere.
unmanaged_asset_one_spec = AssetSpec(asset_key="unmanaged_asset_one")
unmanaged_asset_two_spec = AssetSpec(
    asset_key="unmanaged_asset_two", deps=[unmanaged_asset_one_spec]
)


@sensor()
def sensor_that_emits_materializations(context: SensorEvaluationContext):
    report_asset_materialization(
        instance=context.instance,
        asset_materialization=AssetMaterialization(
            asset_key="unmanaged_asset_one", metadata={"source": "from_sensor"}
        ),
    )


@sensor()
def sensor_that_observes(context: SensorEvaluationContext):
    report_asset_observation(
        instance=context.instance,
        asset_observation=AssetObservation(
            asset_key="unmanaged_asset_one", metadata={"source": "from_sensor"}
        ),
    )


defs = Definitions(
    assets=[
        create_observable_asset(unmanaged_asset_one_spec),
        create_observable_asset(unmanaged_asset_two_spec),
    ],
    sensors=[sensor_that_emits_materializations, sensor_that_observes],
)
