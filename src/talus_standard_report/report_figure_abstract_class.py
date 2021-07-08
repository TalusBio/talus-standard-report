"""src/talus_standard_report/report_figure.py"""
from abc import ABC
from abc import abstractmethod
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
import streamlit as st


class ReportFigureAbstractClass(ABC):
    """An abstract class for the ReportFigure classes.

    Args:
        ABC (class): The ABC class for abstract base classes.
    """

    @abstractmethod
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]],
        description_placeholder: Union[str, Tuple[str, str]],
        subheader: Union[Optional[str], Optional[Tuple[str, str]]] = None,
    ):
        """The init method for the ReportFigure abstract class.

        Args:
            title (str): The title of the figure.
            short_title (str): A short descriptive title for the sidebar.
            dataset_name (str): The dataset name of the dataset used.
            data (pd.DataFrame): The input dataset of the figure.
            description_placeholder (str): The description placeholder of the figure.
            subheader (str, optional): An optional subheader for the figure.
        """
        self._title = title
        self._short_title = short_title
        self._dataset_name = dataset_name
        self._data = data
        self._description_placeholder = description_placeholder
        self._subheader = subheader
        self._figure = None
        self._description = None
        self._is_active = False

    def toggle_active(self) -> None:
        """Toggles the activity of the figure via a checkbox on the sidebar."""
        self._is_active = st.sidebar.checkbox(self._short_title, key=self._title)

    @abstractmethod
    def display(self) -> None:
        """Displays the Streamlit components of the figure."""

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
    def figure(self):
        """Getter for figure."""
        return self._figure

    @property
    def subheader(self):
        """Getter for subheader."""
        return self._subheader
