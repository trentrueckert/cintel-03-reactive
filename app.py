import plotly.express as px
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_plotly, render_widget
from palmerpenguins import load_penguins
import seaborn as sns

penguins = load_penguins()

ui.page_opts(title="Trent's Penguin Data", fillable=True)

with ui.sidebar(
    position="right",
    bg="#f8f8f8",
    open="open"
):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Selected Attribute",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

    ui.input_numeric("plotly_bin_count", "Plotly Bins", 1, min=1, max=10)
    ui.input_slider("seaborn_bin_count", "Seaborn Bins", 5, 50, 25)
    ui.input_checkbox_group("selected_species_list", "Selected Species", ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie", "Chinstrap"], inline=False)
    ui.hr()
    ui.a("Trent's GitHub Repo", "https://github.com/trentrueckert/cintel-02-data", target= "_blank")
    

# Plotly Histogram showing all species
with ui.layout_columns():
    with ui.card():
        ui.card_header("Plotly Histogram")
        
        @render_plotly
        def plotly_historgram():
            return px.histogram(
                filtered_data(), 
                x=input.selected_attribute(), 
                nbins=input.plotly_bin_count(),
                color="species",
            )
            
    # Data grid showing all data
    with ui.card():
        ui.card_header("Data Grid")
        @render.data_frame
        def data_grid():
            return render.DataGrid(filtered_data())
    
    # Data table showing all data        
    with ui.card():
        ui.card_header("Data Table")
        @render.data_frame
        def data_table():
            return render.DataTable(filtered_data())

# Plotly Scatterplot showing all species
with ui.layout_columns():
    with ui.card():
        ui.card_header("Plotly Scatterplot: Species")
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                data_frame=filtered_data(),
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                labels={
                    "bill_depth_mm": "Bill Depth (mm)",
                    "body_mass_g": "Body Mass (g)"})

    # Seaborn Histogram showing all species   
    with ui.card():
        ui.card_header("Seaborn Histogram")
        @render.plot
        def plot2():
            ax=sns.histplot(
                data=filtered_data(), 
                x=input.selected_attribute(), 
                bins=input.seaborn_bin_count())
            ax.set_title("Palmer Penguins")
            ax.set_xlabel(input.selected_attribute())
            ax.set_ylabel("Number")
            return ax


@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    if selected_species:
        return penguins[penguins['species'].isin(selected_species)]
    else:
        return penguins 
