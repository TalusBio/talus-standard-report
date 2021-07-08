"""apps/streamlit_app.py"""
import streamlit as st

import talus_standard_report.data_loader as data_loader
from talus_standard_report.components import CustomProteinUploader
from talus_standard_report.report_figures import NuclearProteinOverlapFigure
from talus_standard_report.report_figures import NumPeptidesPerProtein
from talus_standard_report.report_figures import PeptideIntensitiesBoxPlotFigure
from talus_standard_report.report_figures import PeptideIntensitiesScatterMatrixFigure
from talus_standard_report.report_figures import ProteinIntensitiesHeatmap
from talus_standard_report.report_figures import SubcellularLocationEnrichmentFigure
from talus_standard_report.report_figures import UniquePeptidesProteinsFigure


st.set_page_config(
    page_title="Talus Standard Report",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    """Talus Standard Report."""
    st.write("Hello, Talus Standard Report!")

    dataset = "210308_MLLtx"

    peptide_proteins_result = data_loader.get_peptide_proteins_result(dataset=dataset)
    peptide_proteins_normalized = data_loader.get_peptide_proteins_normalized(
        dataset=dataset
    )
    unique_peptides_proteins = data_loader.get_unique_peptides_proteins(dataset=dataset)
    quant_proteins = data_loader.get_quant_proteins(dataset=dataset)
    # quant_peptides = data_loader.get_quant_peptides(dataset=dataset)

    custom_protein_uploader = CustomProteinUploader()

    figures = [
        UniquePeptidesProteinsFigure(
            title="Bar plot showing the number of unique peptides and proteins found in each sample",
            short_title="# Unique Peptides and Proteins",
            dataset_name=dataset,
            data=unique_peptides_proteins,
            description_placeholder="A bar plot showing the number of unique peptides and proteins found in each sample.",
        ),
        SubcellularLocationEnrichmentFigure(
            title="A heatmap showing the subcellular location enrichment",
            short_title="Subcellular Location Enrichment",
            dataset_name=dataset,
            data=peptide_proteins_normalized,
            description_placeholder="A heatmap plotting the enrichment scores for each subcellular location. Conceptually the enrichment factor metric is simply the measure of how many more protein we find within a given sample relative to a random distribution.",
        ),
        NuclearProteinOverlapFigure(
            title="A Venn Diagram showing the overlap between a list of nuclear proteins and the measured proteins",
            short_title="Nuclear Protein Overlap",
            dataset_name=dataset,
            data=peptide_proteins_result,
            description_placeholder="A Venn diagram showing the overlap between a list of nuclear proteins and the proteins that were measured during these sample runs.",
        ),
        PeptideIntensitiesScatterMatrixFigure(
            title="Scatter Matrix Plot of Peptide Intensities for each Sample",
            short_title="Peptide Intensities Scatter Matrix",
            dataset_name=dataset,
            data=peptide_proteins_result,
            description_placeholder="A scatter matrix plot containing the log10 protein intensities for each sample. The diagonal displays each sample mapped against itself which is why it is a straight line. Points falling far from x=y represent outliers. The farther a pair of samples (a point) falls from x=y, the more uncorrelated it is. In order to fit outliers the axes are sometimes adjusted and are not necessarily all the same.",
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
        ),
        NumPeptidesPerProtein(
            title="Histogram Plot mapping the Distribution of the Number of Peptides detected for each Protein",
            short_title="Number of Peptides per Protein",
            dataset_name=dataset,
            data=quant_proteins,
            description_placeholder="A histogram plotting the distribution of the number of peptides detected for each protein. It uses the data from the final report and therefore represents the data across all runs. The last bar to the right represents a catch-all and includes everything above this value. Ideally we should have more than two peptides for each protein but the more the better. The more peptides we have, the more confident we are in a detection. Having only one peptide could be due to randomness.",
        ),
        ProteinIntensitiesHeatmap(
            title="Heatmap Plot mapping the Protein Intensities",
            short_title="Protein Intensities Heatmap",
            dataset_name=dataset,
            data=quant_proteins,
            description_placeholder="A heatmap plotting the intensities of each detected Protein. The data is row normalized and sorted by the protein with the highest row-normalized intensity compared to the others.",
        ),
    ]
    for figure in figures:
        figure.toggle_active()

    custom_protein_uploader.display()

    for figure in figures:
        figure.display()


if __name__ == "__main__":
    main()
