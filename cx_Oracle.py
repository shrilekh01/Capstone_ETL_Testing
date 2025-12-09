# Lightweight cx_Oracle shim that forwards attributes to python-oracledb (oracledb)
# Place this file at the repository root so "import cx_Oracle" picks it up
# Requires 'oracledb' to be installed (already in your requirements.txt).

try:
    import oracledb as _oracledb
except Exception as _e:
    raise ImportError("cx_Oracle shim requires the 'oracledb' package to be installed. "
                      "Please ensure 'oracledb' is in requirements.txt and installed.") from _e

# Export all public attributes from oracledb under the cx_Oracle module name.
# This covers common uses such as cx_Oracle.connect, DatabaseError, makedsn, etc.
for _name in dir(_oracledb):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_oracledb, _name)

# Provide a helpful __all__ for introspection
__all__ = [n for n in dir(_oracledb) if not n.startswith("_")]
