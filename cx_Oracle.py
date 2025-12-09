# Lightweight cx_Oracle shim that forwards to python-oracledb (oracledb).
# Place this file at the repository root so "import cx_Oracle" picks it up.
# Requires the 'oracledb' package to be installed (ensure "oracledb" is in requirements.txt).

try:
    import oracledb as _oracledb
except Exception as _e:
    raise ImportError(
        "cx_Oracle shim requires the 'oracledb' package to be installed. "
        "Ensure 'oracledb' is present in requirements.txt and installed in the environment."
    ) from _e

# Forward commonly used names so existing cx_Oracle usage works.
# Export public attributes from oracledb under the cx_Oracle name.
for _name in dir(_oracledb):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_oracledb, _name)

# Common aliases to match legacy cx_Oracle code
connect = _oracledb.connect
makedsn = getattr(_oracledb, "makedsn", None)

__all__ = [n for n in dir(_oracledb) if not n.startswith("_")]
