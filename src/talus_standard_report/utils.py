"""src/talus_standard_report/utils.py module."""
import base64
import os
import uuid

from pathlib import Path
from shutil import rmtree
from typing import Dict, Optional, Tuple

import dataframe_image as df_image
import inflection
import pandas as pd
import streamlit as st

from fpdf import FPDF

from talus_standard_report.figures.report_figure_abstract_class import (
    ReportFigureAbstractClass,
)


def streamlit_static_downloads_folder() -> Path:
    """Create a downloads directory within the streamlit static asset directory.
    HACK: This only works when we've installed streamlit with pipenv,
    so the permissions during install are the same as the running process.

    Returns
    -------
    Path
        The path to the downloads directory.
    """
    streamlit_static_path = Path(st.__path__[0]).joinpath("static")
    downloads_path = streamlit_static_path.joinpath("downloads")
    if downloads_path.exists():
        rmtree(downloads_path)
    downloads_path.mkdir()
    return downloads_path


def get_table_download_link(df: pd.DataFrame, downloads_path: Path) -> str:
    """Create a table download link for a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe to download.
    downloads_path : Path
        The path to the downloads directory.

    Returns
    -------
    str
        The download link for the data.
    """
    temp_file_path = downloads_path.joinpath(f"{str(uuid.uuid4())}.csv")
    df.to_csv(temp_file_path)
    return f"[Download as .csv file](downloads/{os.path.basename(temp_file_path)})"


class PDF(FPDF):
    """A PDF class that can be used to create a Streamlit PDF report."""

    def __init__(self, *args: str, **kwargs: str):
        """Create a PDF object."""
        super().__init__(*args, **kwargs)
        self._current_page = 1

    def header(self, width: Optional[int] = 210):
        """Create the header for the PDF."""
        self.set_font(family="Helvetica", style="B", size=15)
        self.set_fill_color(r=255, g=255, b=255)
        w = self.get_string_width(s=self.title) + 6
        self.set_x(x=(210 - w) / 2)
        self.cell(w=w, h=9, txt=self.title, border=0, ln=1, align="L", fill=1)
        self.ln(h=10)

    def footer(self):
        """Create the footer for the PDF."""
        self.set_y(y=-15)
        self.set_font(family="Helvetica", style="I", size=8)
        self.set_text_color(r=128)
        self.cell(
            w=0, h=10, txt="Page " + str(self.page_no()), border=0, ln=0, align="C"
        )

    def chapter_title(self, num: int, label: str):
        """Create a chapter title for the PDF.

        Parameters
        ----------
        num : int
            The chapter number.
        label : str
            The chapter label.
        """
        self.set_font(family="Helvetica", style="B", size=12)
        self.set_fill_color(r=200, g=220, b=255)
        self.multi_cell(w=0, h=6, txt="%d: %s" % (num, label), border=0, align="L")
        self.ln(h=4)

    def chapter_body(self, name: str, description: str, width: Optional[int] = 210):
        """Create the body of a chapter.

        Parameters
        ----------
        name : str
            The name of the object.
        description : str
            The description of the object.
        width : int
            The width of the object.
        """
        self.set_font(family="Helvetica", style="", size=12)
        self.multi_cell(w=0, h=5, txt=description)
        self.image(name=name, w=width)
        self.ln()

    def print_figure(
        self,
        figure: ReportFigureAbstractClass,
        width: Optional[int] = 210,
        write_directory_path: Optional[str] = "/tmp",
    ):
        """Print a figure to the PDF.

        Parameters
        ----------
        figure : ReportFigureAbstractClass
            The figure to print.
        width : int
            The width of the figure.
        height : int
            The height of the figure.
        """
        self.add_page()
        self.chapter_title(num=self._current_page, label=figure.title)
        # Create temporary directory to write the figure and add it to the PDF
        if isinstance(figure, Tuple):
            figures_data = []
            for i in range(len(figure)):
                figures_data.append(
                    {
                        "figure": figure[i].figure,
                        "data": figure[i].data,
                        "description": figure[i].description,
                    }
                )
        else:
            figures_data = [
                {
                    "figure": figure.figure,
                    "data": figure.data,
                    "description": figure.description,
                }
            ]
        for plot_data in figures_data:
            figure_path = os.path.join(
                write_directory_path, f"fig{self._current_page}.png"
            )
            if plot_data["figure"]:
                plot_data["figure"].write_image(figure_path)
            else:
                df_image.export(obj=plot_data["data"], filename=figure_path)
            self.chapter_body(
                name=figure_path,
                description=plot_data["description"],
                width=int(width * 0.8),
            )
            self._current_page += 1

    def get_html_download_link(self) -> str:
        """Create a html download link for an object (which will be base64 encoded).

        Returns
        -------
        str
            The download link for the object.
        """
        out_filename = (
            f"{inflection.parameterize(self.title, separator='_')}_report.pdf"
        )
        b64_encoded = base64.b64encode(
            self.output(out_filename, dest="S").encode("latin-1")
        )
        return f'<a href="data:application/octet-stream;base64,{b64_encoded.decode()}" download="{out_filename}">Download file</a>'


def get_file_to_condition_map(
    peptide_proteins_results: pd.DataFrame, metadata: pd.DataFrame
) -> Dict[str, str]:
    """Create a mapping from file name to condition.

    Parameters
    ----------
    peptide_proteins_results : pd.DataFrame
        The results of the peptide_proteins analysis.
    metadata : pd.DataFrame
        The metadata for the samples.

    Returns
    -------
    dict
        A mapping from file name to condition.
    """
    file_to_condition = {}
    if not metadata.empty:
        metadata = metadata.loc[metadata["Acquisition Type"] == "Wide DIA"]
        metadata["Sample No."] = metadata.groupby("Sample").cumcount() + 1
        metadata["Condition"] = metadata.apply(
            lambda row: f'{row["Working Compound"]}:{row["Working Cell Line"]}:{row["Sample No."]}',
            axis=1,
        )
        metadata_map = (
            metadata[["Run", "Condition"]].set_index("Run").to_dict()["Condition"]
        )
    else:
        metadata_map = (
            peptide_proteins_results[["Run", "Condition"]]
            .set_index("Run")
            .to_dict()["Condition"]
        )

    run_ids = list(peptide_proteins_results["Run"].unique())
    for run in run_ids:
        run_name = run.split(".")[0]
        file_to_condition[run_name] = metadata_map.get(run_name, run_name)

    return file_to_condition
