from dagster import Definitions, sensor
from dagster._core.definitions.asset_spec import ObservableAsset
from dagster._core.definitions.events import AssetMaterialization, AssetObservation
from dagster._core.definitions.sensor_definition import SensorEvaluationContext

from external_lib import (
    report_asset_materialization,
    report_asset_observation,
)


@sensor()
def sensor_that_emits_materializations(context: SensorEvaluationContext):
    report_asset_materialization(
        instance=context.instance,
        asset_materialization=AssetMaterialization(
            asset_key="observable_asset_one", metadata={"source": "from_sensor"}
        ),
    )


@sensor()
def sensor_that_observes(context: SensorEvaluationContext):
    report_asset_observation(
        instance=context.instance,
        asset_observation=AssetObservation(
            asset_key="observable_asset_one", metadata={"source": "from_sensor"}
        ),
    )


# This code location defines metadata exclusively. It expects execution to happen elsewhere.
asset_one = ObservableAsset(asset_key="observable_asset_one")
asset_two = ObservableAsset(asset_key="observable_asset_two", deps=[asset_one])
defs = Definitions(assets=[asset_one, asset_two])


# sensors=[sensor_that_emits_materializations, sensor_that_observes],
