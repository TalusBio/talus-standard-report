"""src/talus_standard_report/figures/report_figure_abstract_class.py module."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Tuple, Union

import inflection
import pandas as pd
import streamlit as st

from plotly.graph_objects import Figure


class ReportFigureAbstractClass(ABC):
    """Abstract base class for all report figures."""

    @abstractmethod
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]],
        description_placeholder: Union[str, Tuple[str, str]],
        width: int,
        height: int,
        downloads_path: Path,
        subheader: Union[Optional[str], Optional[Tuple[str, str]]] = None,
    ) -> None:
        """Initialize the ReportFigure abstract class.

        Parameters
        ----------
        title : str
            The title of the figure.
        short_title : str
            A short descriptive title for the sidebar.
        dataset_name : str
            The dataset name of the dataset used.
        data : Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]
            The input dataset of the figure.
        description_placeholder : Union[str, Tuple[str, str]]
            The description placeholder of the figure.
        width : int
            The figure width.
        height : int
            The figure height.
        downloads_path : Path
            The downloads path where data can be written.
        subheader : Union[Optional[str], Optional[Tuple[str, str]]], optional
            An optional subheader for the figure., by default None
        """
        self._title = title
        self._short_title = short_title
        self._dataset_name = dataset_name
        self._data = self.preprocess_data(data=data)
        self._description_placeholder = description_placeholder
        self._width = width
        self._height = height
        self._subheader = subheader
        self._figure = None
        self._description = None
        self._is_active = False
        self._downloads_path = downloads_path
        self._session_key = inflection.parameterize(self._short_title, separator="_")

    def toggle_active(self) -> None:
        """Toggle the activity of the figure via a checkbox on the sidebar."""
        self._is_active = st.sidebar.checkbox(self._short_title, key=self._title)

    @abstractmethod
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the data for the figure.

        Parameters
        ----------
        data : pd.DataFrame
            The input dataset.

        Returns
        -------
        pd.DataFrame
            The preprocessed dataset.
        """
        raise NotImplementedError

    @abstractmethod
    def get_figure(self, *args, **kwargs) -> Figure:
        """Get the figure object for the figure.

        Parameters
        ----------
        args
            Positional arguments for the figure.
        kwargs
            Keyword arguments for the figure.

        Returns
        -------
        Figure
            The figure object.
        """
        raise NotImplementedError

    @abstractmethod
    def display(self, *args, **kwargs) -> None:
        """Display the figure.

        Parameters
        ----------
        args
            Positional arguments for the figure.
        kwargs
            Keyword arguments for the figure.
        """
        raise NotImplementedError

    @property
    def title(self):
        """Getter for title."""
        return self._title

    @property
    def short_title(self):
        """Getter for short_title."""
        return self._short_title

    @property
    def description(self):
        """Getter for description."""
        return self._description

    @property
    def width(self):
        """Getter for width."""
        return self._width

    @property
    def height(self):
        """Getter for height."""
        return self._height

    @property
    def figure(self):
        """Getter for figure."""
        return self._figure

    @property
    def subheader(self):
        """Getter for subheader."""
        return self._subheader
