"""
@author: 'Marcel Siebes'
"""

# pydantic voor data validation
from pydantic import BaseModel

# Een class voor pydantic i.v.m. parameter controles 
class bankbiljet(BaseModel):
    variance: float
    skewness: float
    curtosis: float
    entropy: float