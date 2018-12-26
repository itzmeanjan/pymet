# pymet
A simple to use Python Interface for fetching MET Norway Weather Data.


## Example Usage ::

  #### pymet.extremes_wwc.fetch() :
   
   - No mandatory to provide parameter.
   - Don't change base_url parameter.
   - dt_2_local is set to True, which converts ISO date-time strings to users local timezone representation.
   - Feel free to set dt_2_local to False, if you want to keep date-time strings in ISO format.
   - parse parameter is by default set to True, which leads to parsing of XML document and returns python dict, which can be converted to JSON, by using json.dumps().
   - If you need to work on XML document, try setting parse to False, which returns unparsed XML document.
   - Returns the WWC-data for the two last periods of time in Norway ( 6-18 and 18-6 UTC ). WWC means Warmest, Wettest and  Coldest.
   
  ```
    import pymet
    print(pymet.extremes_wwc.fetch())
  ```
 
 
  #### pymet.forecast.fetch() :
  
   - Latitude and Longitude parameters are mandatory. Needs to be in decimal numeric form.
   - There's one MSL, Meters above Sea Level, parameter, which is set to None by default. May be set to integer value.
   - MSL value will be used only for places outside Norway.
   - Returns a forecast with several parameters for a nine-day period.
   - Here also, you can request to get XML document, instead of getting parsed python dict, by setting parse=False while invoking this function.
   - UTC date time string can be kept in response by setting dt_2_local = False.
   - Don't need to make any changes in base_url parameter.
   
  ```
    import pymet
    print(pymet.forecast.fetch(latitude, longitude, msl=meters_above_sea_level))
  ```
  
### Important Points ::
  
  - Weather Data fetched by [pymet](https://github.com/itzmeanjan/pymet/), is provided by [MET Norway](https://api.met.no/).
  - Condition of Usage of this Service can be found [here](https://api.met.no/conditions_service.html).
  - Better you subscribe to [API users mailing list](http://lists.met.no/mailman/listinfo/api-users) for staying updated.
  - [pymet]((https://github.com/itzmeanjan/pymet/)) is based on MET Norway API v3, documentation can be read [here](https://api.met.no/weatherapi/documentation).
  - **pymet.forecast** fetches data using [this](https://api.met.no/weatherapi/locationforecast/1.9/documentation) API.
  - **pymet.extremes_wwc** uses [this](https://api.met.no/weatherapi/extremeswwc/1.2/documentation) one.
  - If you're using this module in your application, make sure you cache the data you received.
  

Hope it was helpful :)
