"""
 * the regex code for the mac address was obtained from stackoverflow (https://stackoverflow.com/questions/4260467/what-is-a-regular-expression-for-a-mac-address)
 * the regex code for the private ip address was obtained from stackoverflow (https://stackoverflow.com/questions/2814002/private-ip-address-identifier-in-regular-expression)
"""
from pydantic import BaseModel, PositiveInt, IPvAnyAddress, constr, conint, confloat, root_validator
from typing import Optional, List
from datetime import datetime 
from typing import Dict


class AuditBase(BaseModel):
    timestamp: Optional[int]
    source_ip: Optional[int]
    api_name: Optional[str]
    payload: Dict[str, float] = None
    class Config:
        orm_mode = True
