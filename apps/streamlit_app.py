"""apps/streamlit_app.py"""
import streamlit as st

from numpy.lib.function_base import place

import talus_standard_report.data_loader as data_loader

from talus_standard_report.components import CustomProteinUploader
from talus_standard_report.constants import PRIMARY_COLOR, SECONDARY_COLOR
from talus_standard_report.report_figures import (
    HitSelectionFigure,
    NuclearProteinOverlapFigure,
    NumPeptidesPerProtein,
    PeptideIntensitiesBoxPlotFigure,
    PeptideIntensitiesClustergram,
    PeptideIntensitiesPCAPlot,
    PeptideIntensitiesScatterMatrixFigure,
    ProteinIntensitiesHeatmap,
    SubcellularLocationEnrichmentFigure,
    UniquePeptidesProteinsFigure,
)


st.set_page_config(
    page_title="Talus Standard Report",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    """Talus Standard Report."""
    st.title("Talus Standard Report")

    dataset = "210308_MLLtx"

    peptide_proteins_result = data_loader.get_peptide_proteins_result(dataset=dataset)
    peptide_proteins_normalized = data_loader.get_peptide_proteins_normalized(
        dataset=dataset
    )
    unique_peptides_proteins = data_loader.get_unique_peptides_proteins(dataset=dataset)
    quant_proteins = data_loader.get_quant_proteins(dataset=dataset)
    quant_peptides = data_loader.get_quant_peptides(dataset=dataset)
    quant_peptides_pca_reduced = data_loader.get_quant_peptides_pca_reduced(
        dataset=dataset
    )
    quant_peptides_pca_components = data_loader.get_quant_peptides_pca_components(
        dataset=dataset
    )

    custom_protein_uploader = CustomProteinUploader()

    figures = [
        UniquePeptidesProteinsFigure(
            title="Bar plot showing the number of unique peptides and proteins found in each sample",
            short_title="# Unique Peptides and Proteins",
            dataset_name=dataset,
            data=unique_peptides_proteins,
            description_placeholder="A bar plot showing the number of unique peptides and proteins found in each sample.",
            width=900,
            height=750,
        ),
        SubcellularLocationEnrichmentFigure(
            title="A heatmap showing the subcellular location enrichment",
            short_title="Subcellular Location Enrichment",
            dataset_name=dataset,
            data=peptide_proteins_normalized,
            description_placeholder="A heatmap plotting the enrichment scores for each subcellular location. Conceptually the enrichment factor metric is simply the measure of how many more protein we find within a given sample relative to a random distribution.",
            width=500,
            height=1000,
        ),
        NuclearProteinOverlapFigure(
            title="A Venn Diagram showing the overlap between a list of nuclear proteins and the measured proteins",
            short_title="Nuclear Protein Overlap",
            dataset_name=dataset,
            data=peptide_proteins_result,
            description_placeholder="A Venn diagram showing the overlap between a list of nuclear proteins and the proteins that were measured during these sample runs.",
            width=800,
            height=500,
        ),
        PeptideIntensitiesScatterMatrixFigure(
            title="Scatter Matrix Plot of Peptide Intensities for each Sample",
            short_title="Peptide Intensities Scatter Matrix",
            dataset_name=dataset,
            data=peptide_proteins_result,
            description_placeholder="A scatter matrix plot containing the log10 protein intensities for each sample. The diagonal displays each sample mapped against itself which is why it is a straight line. Points falling far from x=y represent outliers. The farther a pair of samples (a point) falls from x=y, the more uncorrelated it is. In order to fit outliers the axes are sometimes adjusted and are not necessarily all the same.",
            width=900,
            height=900,
        ),
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
        ),
        NumPeptidesPerProtein(
            title="Histogram Plot mapping the Distribution of the Number of Peptides detected for each Protein",
            short_title="Number of Peptides per Protein",
            dataset_name=dataset,
            data=quant_proteins,
            description_placeholder="A histogram plotting the distribution of the number of peptides detected for each protein. It uses the data from the final report and therefore represents the data across all runs. The last bar to the right represents a catch-all and includes everything above this value. Ideally we should have more than two peptides for each protein but the more the better. The more peptides we have, the more confident we are in a detection. Having only one peptide could be due to randomness.",
            width=900,
            height=750,
        ),
        ProteinIntensitiesHeatmap(
            title="Heatmap Plot mapping the Protein Intensities",
            short_title="Protein Intensities Heatmap",
            dataset_name=dataset,
            data=quant_proteins,
            description_placeholder="A heatmap plotting the intensities of each detected Protein. The data is row normalized and sorted by the protein with the highest row-normalized intensity compared to the others.",
            width=500,
            height=900,
            custom_protein_uploader=custom_protein_uploader,
        ),
        HitSelectionFigure(
            title="Hit Selection Mapping Protein Outliers",
            short_title="Hit Selection",
            dataset_name=dataset,
            data=quant_peptides,
            description_placeholder="A hit selection algorithm takes a peptide intensity dataframe and log scales as well as median normalizes it. It then calculcates how many peptides are 2 standard deviations above or below the mean and reports the associated protein. This plot shows all values above or below the mean.",
            width=500,
            height=900,
            custom_protein_uploader=custom_protein_uploader,
        ),
        PeptideIntensitiesPCAPlot(
            title="PCA Plot mapping the Principal Components of the Peptide Intensities for each Sample",
            short_title="Peptide Intensities PCA",
            dataset_name=dataset,
            data=quant_peptides_pca_reduced,
            description_placeholder="A PCA (Principal Component Analysis) Plot where for each sample/bio replicate the peptide intensity was reduced to two principal components. Samples that are closer together are more similar, samples that are farther apart less so. Most ideally we'll see similar replicates/treatments clustered together. If not, there could have potentially been batch effects. The input data to the PCA algorithm were the raw, unnormalized intensities.",
            width=750,
            height=750,
        ),
        PeptideIntensitiesClustergram(
            title="Clustergram Plot mapping the log10 Peptide Intensities for each Sample",
            short_title="Peptide Intensities Clustergram",
            dataset_name=dataset,
            data=quant_peptides,
            description_placeholder="A clustergram showing the top {} log10 peptide intensities (y-axis) for each sample/bio replicate (x-axis) sorted by: {}. The dendrograms on each side cluster the data by peptides and sample similarity on the y- and x-axis respectively. The cluster method used is single linkage.",
            width=750,
            height=1000,
            pca_components=quant_peptides_pca_components,
        ),
    ]
    st.sidebar.header("Options")
    primary_color = st.sidebar.color_picker("Primary Color", PRIMARY_COLOR)
    secondary_color = st.sidebar.color_picker("Secondary Color", SECONDARY_COLOR)
    for figure in figures:
        figure.toggle_active()

    custom_protein_uploader.display()

    for figure in figures:
        figure.display()


if __name__ == "__main__":
    main()
