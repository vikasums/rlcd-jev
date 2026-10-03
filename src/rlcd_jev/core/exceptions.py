"""
Custom exceptions hierarchy for Jev RLCD Compliance Firewall.
"""

class RLCDJevError(Exception):
    """Base exception for all RLCD Jev errors."""
    pass

class ConfigurationError(RLCDJevError):
    """Raised when configuration parameters are invalid or missing."""
    pass

class PrimitiveValidationError(RLCDJevError):
    """Raised when typed primitive evaluation fails validation."""
    pass

class FirewallPolicyError(RLCDJevError):
    """Raised when firewall policy gating encounters a fatal exception."""
    pass

class DatabaseAuditError(RLCDJevError):
    """Raised when database audit log persistence fails."""
    pass
