"""
This submodule contains pipelines, i.e. functions incorporating data processing,
spectral modeling, and output of results. 
"""
__all__ = ["PAQSPipeline", "SDSSPipeline"]

from .paqs import PAQSPipeline
from .sdss import SDSSPipeline