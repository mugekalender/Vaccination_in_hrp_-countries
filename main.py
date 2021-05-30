import folium
import pandas as pd
from folium import Map
import geopandas as gpd


def forecasted_vaccination(data_df):
    data_df['forecasted_vaccination'] = round(data_df['covax forecast total'] / data_df['population (undesa)'] * 100, 2)


def delivered_forecasted(data_df):
    data_df['delivered_forecasted'] = round(data_df['covax delivered'] / data_df['covax forecast total'] * 100, 2)


def delivered_in_population(data_df):
    data_df['delivered_in_population'] = round(data_df['total delivered'] / data_df['population (undesa)'] * 100, 2)


if __name__ == '__main__':
    data_file = "data/vaccine_in_hrp_countries.csv"
    col_types = {
        "Country": str,
        "ISO_A3": str,
        "SFP/AMC": str,
        "Population (UNDESA)": int,
        "COVAX Forecast Total": int,
        "COVAX AstraZeneca/SII": int,
        "COVAX AstraZeneca/SKBio": int,
        "COVAX Pfizer/BioNTech": int,
        "COVAX Delivered": int,
        "Other Delivered": int,
        "Total Delivered": int,
        "Population Covered (One Dose)": str,
        "(DEPRECATAED) Other Delivered Source Country": str,
        "(DEPRECATAED) Other Delivered Source URLs": str
    }

    data = pd.read_csv(data_file, dtype=col_types)
    data.columns = [cc.lower() for cc in data.columns]
    data.head(27)

    # create percentage columns
    forecasted_vaccination(data)
    delivered_forecasted(data)
    delivered_in_population(data)

    print("")
    print("Data:")
    print(data[['iso_a3', 'population (undesa)', 'forecasted_vaccination', 'delivered_forecasted',
                'delivered_in_population']].head())

    world_map = "data/world_map.json"
    geo_data = gpd.read_file(world_map)
    print("")
    print("Geo data:")
    print(geo_data.head())

    final_data = geo_data.merge(data, on="iso_a3")
    print("")
    print("Final data:")
    print(final_data.head())

    # Setup a folium map
    hrp_map: Map = folium.Map(location=[20, 80], zoom_start=2.5, min_zoom=2, max_bounds=True, tiles='cartodbpositron')
    choropleth = folium.Choropleth(
        geo_data=final_data,
        data=final_data,
        columns=['iso_a3', 'delivered_in_population', 'population'],
        key_on='properties.iso_a3',
        fill_color='RdYlGn',
        bins=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name="Population Covered (One Dose) %"
    ).add_to(hrp_map)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ['iso_a3', 'population (undesa)', 'covax forecast total', 'forecasted_vaccination',
             'total delivered', 'delivered_forecasted'],
            aliases=['Country Code',
                     'UN Estimated Population',
                     'Forecasted COVAX Vaccine',
                     '% of Forecasted COVAX Vaccine per Total Population',
                     'Total Vaccines Delivered',
                     '% of Total Delivered Vaccine as part of COVAX per Forecasted Distribution'])
    )

    folium.LayerControl().add_to(hrp_map)
    hrp_map.save('out/hrp_map.html')

    data = data[['iso_a3', 'delivered_in_population']]
    data.head()
