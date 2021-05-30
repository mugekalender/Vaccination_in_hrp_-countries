import pandas as pd
import folium
from folium import Map


def forecasted_vaccination(data_df):
    data_df['forecasted_vaccination'] = data_df['covax forecast total'] / data_df['population (undesa)'] * 100


def delivered_forecasted(data_df):
    data_df['delivered_forecasted'] = data_df['total delivered'] / data_df['covax forecast total'] * 100


def delivered_in_population(data_df):
    data_df['delivered_in_population'] = data_df['total delivered'] / data_df['population (undesa)'] * 100


# def country_breakdown():
#     #user's choice
#     selected_country = input("Please select a HRP participant country")


if __name__ == '__main__':
    data_fıle = "data/vaccine_in_hrp_countries.csv"
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

    data = pd.read_csv(data_fıle, dtype=col_types)
    data.columns = [cc.lower() for cc in data.columns]
    data.head(27)

    #joined_hrp = world_map.merge(data_file, on 'iso_a3')

    # create percentage columns
    forecasted_vaccination(data)
    delivered_forecasted(data)
    delivered_in_population(data)
    print(data[['iso_a3', 'population (undesa)', 'forecasted_vaccination', 'delivered_forecasted', 'delivered_in_population']].head())

    # Setup a folium map
    hrp_map: Map = folium.Map(location=[20, 80], zoom_start=2.5, min_zoom=2, max_bounds=True, tiles='cartodbpositron')
    world_map = "data/world_map.json"
    choropleth = folium.Choropleth(
        geo_data=world_map,
        data=data,
        columns=['iso_a3', 'delivered_in_population', 'population'],  # 'population (undesa)', 'forecasted_vaccination', 'delivered_forecasted',
        key_on='properties.iso_a3',
        fill_color='YlOrRd',
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name="Population Covered (One Dose)"
    ).add_to(hrp_map)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['iso_a3', ',' 'pop_est'], labels=False)
    )

    folium.LayerControl().add_to(hrp_map)
    hrp_map.save('out/hrp_map.html')









