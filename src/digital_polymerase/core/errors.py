"""Custom exceptions for Digital Polymerase core."""
class DigitalPolymeraseError(Exception): pass
class PDBParseError(DigitalPolymeraseError): pass
class TemplateError(DigitalPolymeraseError): pass
class RegistryError(DigitalPolymeraseError): pass
class ValidationError(DigitalPolymeraseError): pass
class UnsupportedResidueError(DigitalPolymeraseError): pass
