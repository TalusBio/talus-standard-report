"""apps/streamlit_app.py component."""
from functools import reduce

import pandas as pd
import streamlit as st

from streamlit.script_runner import StopException

import talus_standard_report.data_loader as data_loader

from talus_standard_report.components.custom_protein_uploader import (
    CustomProteinUploader,
)
from talus_standard_report.components.dataset_choice import DatasetChoice
from talus_standard_report.constants import (
    ENCYCLOPEDIA_BUCKET,
    SELECTBOX_DEFAULT,
    STANDARD_REPORT_TITLE,
)
from talus_standard_report.figures.file_size_dataframe import FileSizeDataFrame
from talus_standard_report.figures.hit_selection_figure import HitSelectionFigure
from talus_standard_report.figures.nuclear_protein_overlap_figure import (
    NuclearProteinOverlapFigure,
)
from talus_standard_report.figures.num_peptides_per_protein_figure import (
    NumPeptidesPerProteinFigure,
)
from talus_standard_report.figures.peptide_intensities_box_plot_figure import (
    PeptideIntensitiesBoxPlotFigure,
)
from talus_standard_report.figures.peptide_intensities_clustergram import (
    PeptideIntensitiesClustergram,
)
from talus_standard_report.figures.peptide_intensities_pca_plot import (
    PeptideIntensitiesPCAPlot,
)
from talus_standard_report.figures.peptide_intensities_scatter_matrix_figure import (
    PeptideIntensitiesScatterMatrixFigure,
)
from talus_standard_report.figures.protein_intensities_heatmap import (
    ProteinIntensitiesHeatmap,
)
from talus_standard_report.figures.subcellular_location_enrichment_figure import (
    SubcellularLocationEnrichmentFigure,
)
from talus_standard_report.figures.unique_peptides_proteins_figure import (
    UniquePeptidesProteinsFigure,
)
from talus_standard_report.utils import (
    PDF,
    get_file_to_condition_map,
    streamlit_static_downloads_folder,
)


st.set_page_config(
    page_title=STANDARD_REPORT_TITLE,
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    """Talus Standard Report."""
    st.title(STANDARD_REPORT_TITLE)

    st.sidebar.header("Options")
    dataset_chooser = DatasetChoice(
        bucket=ENCYCLOPEDIA_BUCKET,
        key="wide",
        filename_filter="peptide_proteins_results",
        file_type="parquet",
    )
    dataset_chooser.display()

    dataset = dataset_chooser.dataset

    if dataset == SELECTBOX_DEFAULT:
        st.warning("Please select a dataset.")
        raise StopException

    downloads_path = streamlit_static_downloads_folder()

    metadata = data_loader.get_metadata(dataset=dataset)

    peptide_proteins_result = data_loader.get_peptide_proteins_result(dataset=dataset)
    file_to_condition = get_file_to_condition_map(
        peptide_proteins_results=peptide_proteins_result, metadata=metadata
    )

    peptide_proteins_normalized = data_loader.get_peptide_proteins_normalized(
        dataset=dataset
    )

    unique_peptides_proteins = data_loader.get_unique_peptides_proteins(dataset=dataset)
    quant_proteins = data_loader.get_quant_proteins(dataset=dataset)
    quant_peptides = data_loader.get_quant_peptides(dataset=dataset)
    quant_peptides_pca_reduced = data_loader.get_quant_peptides_pca_reduced(
        dataset=dataset
    )
    quant_peptides_pca = data_loader.get_quant_peptides_pca(dataset=dataset)

    nuclear_proteins = data_loader.get_nuclear_proteins()
    protein_locations = data_loader.get_protein_locations()
    expected_fractions_of_locations = data_loader.get_expected_fractions_of_locations()

    # Preprocess dataframes
    peptide_proteins_result["Condition"] = peptide_proteins_result["Condition"].apply(
        lambda name: file_to_condition.get(name.split(".")[0], name)
    )
    peptide_proteins_normalized["originalRUN"] = peptide_proteins_normalized[
        "originalRUN"
    ].apply(lambda name: file_to_condition.get(name.split(".")[0], name))
    unique_peptides_proteins["Sample Name"] = unique_peptides_proteins[
        "Sample Name"
    ].apply(lambda name: file_to_condition.get(name, name))
    quant_proteins.columns = [
        file_to_condition.get(name.split(".")[0], name)
        for name in quant_proteins.columns
    ]
    quant_peptides.columns = [
        file_to_condition.get(name.split(".")[0], name)
        for name in quant_peptides.columns
    ]
    quant_peptides_pca_reduced["index"] = quant_peptides_pca_reduced["index"].apply(
        lambda name: file_to_condition.get(name.split(".")[0], name)
    )

    custom_protein_uploader = CustomProteinUploader()

    conditional_figures = [
        (
            True,
            FileSizeDataFrame(
                title="Raw File Sizes",
                short_title="Raw File Sizes",
                dataset_name=dataset,
                data=pd.DataFrame(),
                description_placeholder="A DataFrame containing the .raw file sizes.",
                width=None,
                height=None,
                downloads_path=downloads_path,
            ),
        ),
        (
            not unique_peptides_proteins.empty,
            UniquePeptidesProteinsFigure(
                title="Bar plot showing the number of unique peptides and proteins found in each sample",
                short_title="# Unique Peptides and Proteins",
                dataset_name=dataset,
                data=unique_peptides_proteins,
                description_placeholder="A bar plot showing the number of unique peptides and proteins found in each sample.",
                width=900,
                height=750,
                downloads_path=downloads_path,
            ),
        ),
        (
            not (
                peptide_proteins_normalized.empty
                or protein_locations.empty
                or expected_fractions_of_locations.empty
            ),
            SubcellularLocationEnrichmentFigure(
                title="A heatmap showing the subcellular location enrichment",
                short_title="Subcellular Location Enrichment",
                dataset_name=dataset,
                data=peptide_proteins_normalized,
                description_placeholder="A heatmap plotting the enrichment scores for each subcellular location. Conceptually the enrichment factor metric is simply the measure of how many more protein we find within a given sample relative to a random distribution.",
                width=500,
                height=1000,
                protein_locations=protein_locations,
                expected_fractions_of_locations=expected_fractions_of_locations,
                downloads_path=downloads_path,
            ),
        ),
        (
            not (peptide_proteins_result.empty or nuclear_proteins.empty),
            NuclearProteinOverlapFigure(
                title="A Venn Diagram showing the overlap between a list of nuclear proteins and the measured proteins",
                short_title="Nuclear Protein Overlap",
                dataset_name=dataset,
                data=peptide_proteins_result,
                description_placeholder="A Venn diagram showing the overlap between a list of nuclear proteins and the proteins that were measured during these sample runs.",
                width=800,
                height=500,
                nuclear_proteins=nuclear_proteins,
                custom_protein_uploader=custom_protein_uploader,
                downloads_path=downloads_path,
            ),
        ),
        (
            not peptide_proteins_result.empty,
            PeptideIntensitiesScatterMatrixFigure(
                title="Scatter Matrix Plot of Peptide Intensities for each Sample",
                short_title="Peptide Intensities Scatter Matrix",
                dataset_name=dataset,
                data=peptide_proteins_result,
                description_placeholder="A scatter matrix plot containing the log10 protein intensities for each sample. The diagonal displays each sample mapped against itself which is why it is a straight line. Points falling far from x=y represent outliers. The farther a pair of samples (a point) falls from x=y, the more uncorrelated it is. In order to fit outliers the axes are sometimes adjusted and are not necessarily all the same.",
                width=900,
                height=900,
                downloads_path=downloads_path,
            ),
        ),
        (
            not (peptide_proteins_result.empty or peptide_proteins_normalized.empty),
            PeptideIntensitiesBoxPlotFigure(
                title="Box Plot of Raw/Normalized Peptide Intensities for each Sample",
                short_title="Peptide Intensities Box Plot",
                subheader=(
                    "Box Plot of Raw Peptide Intensities for each Sample",
                    "Box Plot of Normalized Peptide Intensities for each Sample",
                ),
                dataset_name=dataset,
                data=(peptide_proteins_result, peptide_proteins_normalized),
                description_placeholder=(
                    "A box plot showing the log2 peptide intensities for each sample/replicate. The outliers are filtered out and the ends of the box represent the lower (25th) and upper (75th) quartiles, while the median (second quartile) is marked by a line inside the box. If the distribution of one sample deviates from the others, that sample is an outlier.",
                    "A box plot showing the same data as above but the intensities have been log2 transformed and normalized.",
                ),
                width=750,
                height=900,
                downloads_path=downloads_path,
            ),
        ),
        (
            not quant_proteins.empty,
            NumPeptidesPerProteinFigure(
                title="Histogram Plot mapping the Distribution of the Number of Peptides detected for each Protein",
                short_title="Number of Peptides per Protein",
                dataset_name=dataset,
                data=quant_proteins,
                description_placeholder="A histogram plotting the distribution of the number of peptides detected for each protein. It uses the data from the final report and therefore represents the data across all runs. The last bar to the right represents a catch-all and includes everything above this value. Ideally we should have more than two peptides for each protein but the more the better. The more peptides we have, the more confident we are in a detection. Having only one peptide could be due to randomness.",
                width=900,
                height=750,
                downloads_path=downloads_path,
            ),
        ),
        (
            not quant_proteins.empty,
            ProteinIntensitiesHeatmap(
                title="Heatmap Plot mapping the Protein Intensities",
                short_title="Protein Intensities Heatmap",
                dataset_name=dataset,
                data=quant_proteins,
                description_placeholder="A heatmap plotting the intensities of each detected Protein. The data is row normalized and sorted by the protein with the highest row-normalized intensity compared to the others.",
                width=500,
                height=900,
                custom_protein_uploader=custom_protein_uploader,
                downloads_path=downloads_path,
            ),
        ),
        (
            not quant_peptides.empty,
            HitSelectionFigure(
                title="Hit Selection Mapping Protein Outliers",
                short_title="Hit Selection",
                dataset_name=dataset,
                data=quant_peptides,
                description_placeholder="A hit selection algorithm takes a peptide intensity dataframe and log scales as well as median normalizes it. It then calculcates how many peptides are 2 standard deviations above or below the mean and reports the associated protein. This plot shows all values above or below the mean.",
                width=500,
                height=900,
                custom_protein_uploader=custom_protein_uploader,
                file_to_condition=file_to_condition,
                downloads_path=downloads_path,
            ),
        ),
        (
            not quant_peptides_pca_reduced.empty,
            PeptideIntensitiesPCAPlot(
                title="PCA Plot mapping the Principal Components of the Peptide Intensities for each Sample",
                short_title="Peptide Intensities PCA",
                dataset_name=dataset,
                data=quant_peptides_pca_reduced,
                description_placeholder="A PCA (Principal Component Analysis) Plot where for each sample/bio replicate the peptide intensity was reduced to two principal components. Samples that are closer together are more similar, samples that are farther apart less so. Most ideally we'll see similar replicates/treatments clustered together. If not, there could have potentially been batch effects. The input data to the PCA algorithm were the raw, unnormalized intensities.",
                width=750,
                height=750,
                pca_model=quant_peptides_pca,
                downloads_path=downloads_path,
            ),
        ),
        (
            quant_peptides_pca != "",
            PeptideIntensitiesClustergram(
                title="Clustergram Plot mapping the log10 Peptide Intensities for each Sample",
                short_title="Peptide Intensities Clustergram",
                dataset_name=dataset,
                data=quant_peptides,
                description_placeholder="A clustergram showing the top {} log10 peptide intensities (y-axis) for each sample/bio replicate (x-axis) sorted by: {}. The dendrograms on each side cluster the data by peptides and sample similarity on the y- and x-axis respectively. The cluster method used is single linkage.",
                width=750,
                height=1000,
                pca_model=quant_peptides_pca,
                file_to_condition=file_to_condition,
                downloads_path=downloads_path,
            ),
        ),
    ]
    figures = reduce(
        lambda accum, cond_figure: accum + [cond_figure[1]]
        if cond_figure[0]
        else accum,
        conditional_figures,
        [],
    )
    for figure in figures:
        figure.toggle_active()

    custom_protein_uploader.display()

    for figure in figures:
        figure.display()

    if st.button("Export to PDF"):
        with st.spinner(text="Loading"):
            pdf = PDF()
            pdf.set_title(STANDARD_REPORT_TITLE)
            for figure in figures:
                if figure.is_active:
                    pdf.print_figure(figure=figure, write_directory_path=downloads_path)

            html = pdf.get_html_download_link()
            st.markdown(html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
