from pydantic import BaseModel


class Persona(BaseModel):
    name: str
    domain: str


class AgentInitRequest(BaseModel):
    persona: Persona