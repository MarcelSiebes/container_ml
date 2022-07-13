"""
@author: 'Marcel Siebes'
"""

from pydantic import BaseModel

# Een class voor pydantic i.v.m. parameter controles 
class bankbiljet(BaseModel):
    variance: float
    skewness: float
    curtosis: float
    entropy: float