"""Data Loading Module - Load data from various sources"""

import logging
from io import StringIO
from typing import Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class DataLoader:
    """Load and manage data from multiple sources"""

    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """Load CSV file"""
        try:
            logger.info(f"Loading CSV: {file_path}")
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            raise

    @staticmethod
    def load_excel(file_path: str, sheet_name: str = 0) -> pd.DataFrame:
        """Load Excel file"""
        try:
            logger.info(f"Loading Excel: {file_path}")
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading Excel: {str(e)}")
            raise

    @staticmethod
    def load_json(file_path: str) -> pd.DataFrame:
        """Load JSON file"""
        try:
            logger.info(f"Loading JSON: {file_path}")
            df = pd.read_json(file_path)
            logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading JSON: {str(e)}")
            raise

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> bool:
        """Validate dataframe integrity"""
        if df is None or df.empty:
            logger.warning("DataFrame is empty")
            return False
        if len(df.columns) == 0:
            logger.warning("DataFrame has no columns")
            return False
        return True

    @staticmethod
    def get_data_info(df: pd.DataFrame) -> dict:
        """Get comprehensive data information"""
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "missing_count": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
            "memory_usage_mb": float(df.memory_usage(deep=True).sum() / 1024 / 1024),
        }
