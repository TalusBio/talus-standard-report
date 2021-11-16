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
    EXPERIMENT_BUCKET,
    SELECTBOX_DEFAULT,
    STANDARD_REPORT_TITLE,
)
from talus_standard_report.figures.file_size_dataframe import FileSizeDataFrame
from talus_standard_report.figures.nuclear_protein_overlap_figure import (
    NuclearProteinOverlapFigure,
)
from talus_standard_report.figures.num_peptides_per_protein_figure import (
    NumPeptidesPerProteinFigure,
)
from talus_standard_report.figures.go_enrichment_figure import GOEnrichmentFigure
from talus_standard_report.figures.peptide_intensities_pca_plot import (
    PeptideIntensitiesPCAPlot,
)
from talus_standard_report.figures.peptide_intensities_scatter_matrix_figure import (
    PeptideIntensitiesScatterMatrixFigure,
)
from talus_standard_report.figures.protein_intensities_heatmap import (
    ProteinIntensitiesHeatmap,
)
from talus_standard_report.figures.peptide_intensities_box_plot_figure import PeptideIntensitiesBoxPlotFigure
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
        bucket=EXPERIMENT_BUCKET,
        key="",
        filename_filter="result-quant.elib.proteins.txt",
        file_type="txt",
    )
    dataset_chooser.display()

    dataset = dataset_chooser.dataset

    if dataset == SELECTBOX_DEFAULT:
        st.warning("Please select a dataset.")
        raise StopException

    tool_choice = st.sidebar.selectbox("Tool", options=["Encyclopedia"])

    downloads_path = streamlit_static_downloads_folder()

    metadata = data_loader.get_metadata(dataset=dataset, tool=tool_choice.lower())

    file_to_condition = get_file_to_condition_map(
        metadata=metadata
    )

    unique_peptides_proteins = data_loader.get_unique_peptides_proteins(dataset=dataset, tool=tool_choice.lower())
    quant_proteins = data_loader.get_quant_proteins(dataset=dataset, tool=tool_choice.lower())
    quant_peptides = data_loader.get_quant_peptides(dataset=dataset, tool=tool_choice.lower())

    nuclear_proteins = data_loader.get_nuclear_proteins()

    unique_peptides_proteins["Sample Name"] = unique_peptides_proteins[
        "Sample Name"
    ].apply(lambda name: file_to_condition.get(name, name))
    quant_proteins.columns = [
        file_to_condition.get(col, col)
        for col in quant_proteins.columns
    ]
    quant_peptides.columns = [
        file_to_condition.get(col, col)
        for col in quant_peptides.columns
    ]

    custom_protein_uploader = CustomProteinUploader()

    conditional_figures = [
        (
            True,
            FileSizeDataFrame(
                title="Raw File Sizes",
                short_title="Raw File Sizes",
                dataset_name=dataset,
                data=metadata,
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
            not (quant_proteins.empty or nuclear_proteins.empty),
            NuclearProteinOverlapFigure(
                title="A Venn Diagram showing the overlap between a list of nuclear proteins and the measured proteins",
                short_title="Nuclear Protein Overlap",
                dataset_name=dataset,
                data=quant_proteins,
                description_placeholder="A Venn diagram showing the overlap between a list of nuclear proteins and the proteins that were measured during these sample runs.",
                width=800,
                height=500,
                nuclear_proteins=nuclear_proteins,
                custom_protein_uploader=custom_protein_uploader,
                downloads_path=downloads_path,
            ),
        ),
        (
            not quant_proteins.empty,
            GOEnrichmentFigure(
                title="Bar Plot mapping GO Enrichment",
                short_title="GO Enrichment",
                dataset_name=dataset,
                data=quant_proteins,
                description_placeholder="A bar plot showing the go enrichment values for a subset of terms.",
                width=900,
                height=700,
                downloads_path=downloads_path,
                metadata=metadata
            ),
        ),
        (
            not quant_peptides.empty,
            PeptideIntensitiesBoxPlotFigure(
                title="Box Plot of Peptide Intensities for each Sample",
                short_title="Peptide Intensities Box Plot",
                subheader="Box Plot of Peptide Intensities for each Sample",
                dataset_name=dataset,
                data=quant_peptides,
                description_placeholder="A box plot showing the log2 peptide intensities for each sample/replicate. The outliers are filtered out and the ends of the box represent the lower (25th) and upper (75th) quartiles, while the median (second quartile) is marked by a line inside the box. If the distribution of one sample deviates from the others, that sample is an outlier.",
                width=750,
                height=900,
                downloads_path=downloads_path,
            ),
        ),
        (
            not quant_peptides.empty,
            PeptideIntensitiesScatterMatrixFigure(
                title="Scatter Matrix Plot of Peptide Intensities for each Sample",
                short_title="Peptide Intensities Scatter Matrix",
                dataset_name=dataset,
                data=quant_peptides,
                description_placeholder="A scatter matrix plot containing the log10 protein intensities for each sample. The diagonal displays each sample mapped against itself which is why it is a straight line. Points falling far from x=y represent outliers. The farther a pair of samples (a point) falls from x=y, the more uncorrelated it is. In order to fit outliers the axes are sometimes adjusted and are not necessarily all the same.",
                width=900,
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
                height=1000,
                custom_protein_uploader=custom_protein_uploader,
                downloads_path=downloads_path,
            ),
        ),
        (
            not quant_peptides.empty,
            PeptideIntensitiesPCAPlot(
                title="PCA Plot mapping the Principal Components of the Peptide Intensities for each Sample",
                short_title="Peptide Intensities PCA",
                dataset_name=dataset,
                data=quant_peptides,
                description_placeholder="A PCA (Principal Component Analysis) Plot where for each sample/bio replicate the peptide intensity was reduced to two principal components. Samples that are closer together are more similar, samples that are farther apart less so. Most ideally we'll see similar replicates/treatments clustered together. If not, there could have potentially been batch effects. The input data to the PCA algorithm were the raw, unnormalized intensities.",
                width=750,
                height=750,
                downloads_path=downloads_path,
                metadata=metadata
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
