---
title: 'Extra credit: Asset metadata as Markdown'
module: 'dagster_essentials'
lesson: 'extra-credit'
---

# Asset metadata as Markdown

In Lesson 9, you created the `adhoc_request` asset. During materialization, the asset generates and saves a bar graph to storage. This setup is great for referring to the chart at a later time, but what about what’s generated right after a materialization? By using metadata, you can view the chart right in the Dagster UI!

---

## Adding the metadata to the asset

1. Navigate to and open `assets/requests.py`.
2. At this point in the course, the `adhoc_request` asset should look like this:

   ```python
   from dagster import Config, asset
   from dagster_duckdb import DuckDBResource

   import plotly.express as px
   import plotly.io as pio

   from . import constants

   class AdhocRequestConfig(Config):
     filename: str
     borough: str
     start_date: str
     end_date: str

   @asset
   def adhoc_request(config: AdhocRequestConfig, taxi_zones, taxi_trips, database: DuckDBResource):
     """
       The response to an request made in the `requests` directory.
       See `requests/README.md` for more information.
     """

     # strip the file extension from the filename, and use it as the output filename
     file_path = constants.REQUEST_DESTINATION_TEMPLATE_FILE_PATH.format(config.filename.split('.')[0])

     # count the number of trips that picked up in a given borough, aggregated by time of day and hour of day
     query = f"""
         select
           date_part('hour', pickup_datetime) as hour_of_day,
           date_part('dayofweek', pickup_datetime) as day_of_week_num,
           case date_part('dayofweek', pickup_datetime)
             when 0 then 'Sunday'
             when 1 then 'Monday'
             when 2 then 'Tuesday'
             when 3 then 'Wednesday'
             when 4 then 'Thursday'
             when 5 then 'Friday'
             when 6 then 'Saturday'
           end as day_of_week,
           count(*) as num_trips
         from trips
         left join zones on trips.pickup_zone_id = zones.zone_id
         where pickup_datetime >= '{config.start_date}'
         and pickup_datetime < '{config.end_date}'
         and pickup_zone_id in (
           select zone_id
           from zones
           where borough = '{config.borough}'
         )
         group by 1, 2
         order by 1, 2 asc
     """

     with database.get_connection() as conn:
       results = conn.execute(query).fetch_df()

     fig = px.bar(
           results,
           x="hour_of_day",
           y="num_trips",
           color="day_of_week",
           barmode="stack",
           title=f"Number of trips by hour of day in {config.borough}, from {config.start_date} to {config.end_date}",
           labels={
               "hour_of_day": "Hour of Day",
               "day_of_week": "Day of Week",
               "num_trips": "Number of Trips"
         }
     )

     pio.write_image(fig, file_path)
   ```

3. Add the following to the import to the top of the file:

   ```python
   import base64
   ```

4. Because you need to use the `context` object, you’ll need to add it to the asset function’s argument as the first argument:

   ```python
   @asset
   def adhoc_request(context, config: AdhocRequestConfig, taxi_zones, taxi_trips, database: DuckDBResource):
   ```

5. After the last line in the asset, add the following code:

   ```python
   with open(file_path, 'rb') as file:
     image_data = file.read()
   ```

6. Next, we’ll use base64 encoding to convert the chart to Markdown. After the `image_data` line, add the following code:

   ```python
   base64_data = base64.b64encode(image_data).decode('utf-8')
     md_content = f"![Image](data:image/jpeg;base64,{base64_data})"

    context.add_output_metadata({
      "preview": MetadataValue.md(md_content)
    })
   ```

   Let’s break down what’s happening here:

   1. A variable named `base64_data` is created.
   2. `base64.b64encode` encodes the image’s binary data (`image_data`) into base64 format.
   3. Next, the encoded image data is converted to a UTF-8 encoded string using the `decode` function.
   4. Next, a variable named `md_content` is created. The value of this variable is a Markdown-formatted string containing a JPEG image, where the base64 representation of the image is inserted.
   5. Using `context.add_output_metadata`, the image is passed in as metadata. The metadata will have a `preview` label in the Dagster UI.
   6. Using `MetadataValue.md`, the `md_content` is typed as Markdown. This ensures Dagster will correctly render the chart.

At this point, the code for the `adhoc_request` asset should look like this:

```python
from dagster import Config, asset, MetadataValue, get_dagster_logger
from dagster_duckdb import DuckDBResource

import plotly.express as px
import plotly.io as pio
import base64

from . import constants

class AdhocRequestConfig(Config):
  filename: str
  borough: str
  start_date: str
  end_date: str

@asset
def adhoc_request(context**,** config: AdhocRequestConfig, taxi_zones, taxi_trips, database: DuckDBResource):
  """
    The response to an request made in the `requests` directory.
    See `requests/README.md` for more information.
  """

  # strip the file extension from the filename, and use it as the output filename
  file_path = constants.REQUEST_DESTINATION_TEMPLATE_FILE_PATH.format(config.filename.split('.')[0])

  # count the number of trips that picked up in a given borough, aggregated by time of day and hour of day
  query = f"""
      select
        date_part('hour', pickup_datetime) as hour_of_day,
        date_part('dayofweek', pickup_datetime) as day_of_week_num,
        case date_part('dayofweek', pickup_datetime)
          when 0 then 'Sunday'
          when 1 then 'Monday'
          when 2 then 'Tuesday'
          when 3 then 'Wednesday'
          when 4 then 'Thursday'
          when 5 then 'Friday'
          when 6 then 'Saturday'
        end as day_of_week,
        count(*) as num_trips
      from trips
      left join zones on trips.pickup_zone_id = zones.zone_id
      where pickup_datetime >= '{config.start_date}'
      and pickup_datetime < '{config.end_date}'
      and pickup_zone_id in (
        select zone_id
        from zones
        where borough = '{config.borough}'
      )
      group by 1, 2
      order by 1, 2 asc
  """

  with database.get_connection() as conn:
    results = conn.execute(query).fetch_df()

  fig = px.bar(
        results,
        x="hour_of_day",
        y="num_trips",
        color="day_of_week",
        barmode="stack",
        title=f"Number of trips by hour of day in {config.borough}, from {config.start_date} to {config.end_date}",
        labels={
          "hour_of_day": "Hour of Day",
          "day_of_week": "Day of Week",
          "num_trips": "Number of Trips"
      }
  )

  pio.write_image(fig, file_path)

  with open(file_path, 'rb') as file:
    image_data = file.read()

  base64_data = base64.b64encode(image_data).decode('utf-8')
  md_content = f"![Image](data:image/jpeg;base64,{base64_data})"

  context.add_output_metadata({
    "preview": MetadataValue.md(md_content)
  })
```

---

## Viewing the metadata in the Dagster UI

After all that work, let’s check out what this looks like in the UI!

1. Navigate to the **Global Asset Lineage** page.
2. Click **Reload definitions.**
3. After the metadata code is updated, simulate a tick of the sensor.
<!-- TODO: Add link to Thinkific sensors lesson here? -->

On the right-hand side of the screen, you’ll see `preview`, which was the label given to the Markdown plot value:

![The Global Asset Lineage page with the adhoc_request asset selected](/images/dagster-essentials/extra-credit/ui-selected-adhoc-request-asset.png)

To display the chart, click **[Show Markdown]** :

![The chart rendered as a result of materializing the adhoc_request asset](/images/dagster-essentials/extra-credit/ui-markdown-chart.png)

You can also click **View in Asset Catalog** to view the chart:

![The adhoc_request asset in the Asset Catalog page in the Dagster UI](/images/dagster-essentials/extra-credit/ui-asset-catalog.png)
