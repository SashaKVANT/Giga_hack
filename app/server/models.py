from pydantic import BaseModel

class AgentRequestModel(BaseModel):
    source_channel: str
    dest_channel: str 
    auditory_name: str