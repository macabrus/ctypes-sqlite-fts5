import ctypes
import fts5_header

# Load the SQLite library
sqlite = ctypes.cdll.LoadLibrary('./sqlite3.dylib')

# Define the function arguments and return value
sqlite3_prepare_v2 = sqlite.sqlite3_prepare_v2
sqlite3_prepare_v2.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_char_p)]
sqlite3_prepare_v2.restype = ctypes.c_int

sqlite3_bind_pointer = sqlite.sqlite3_bind_pointer
sqlite3_bind_pointer.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]

sqlite3_step = sqlite.sqlite3_step
sqlite3_step.argtypes = [ctypes.c_void_p]
sqlite3_step.restype = ctypes.c_int

sqlite3_finalize = sqlite.sqlite3_finalize
sqlite3_finalize.argtypes = [ctypes.c_void_p]
sqlite3_finalize.restype = ctypes.c_int

# Open a SQLite database connection
db = ctypes.c_void_p()
sqlite.sqlite3_open(b":memory:", ctypes.byref(db))

# Prepare the statement to get the fts5_api struct
pStmt = ctypes.c_void_p()
zSql = b"SELECT fts5(?1)"
rc = sqlite3_prepare_v2(db, zSql, len(zSql), ctypes.byref(pStmt), None)

# Bind the fts5 argument to the statement
pApi = ctypes.c_void_p()
sqlite3_bind_pointer(pStmt, 1, ctypes.byref(pApi), b"fts5_api_ptr", None)

# Execute the statement to obtain the fts5_api struct
rc = sqlite3_step(pStmt)
# print(rc)
# if rc != 101:  # SQLITE_ROW
#     print("Error: Failed to obtain fts5_api struct")
# else:
fts5_api = ctypes.cast(pApi.value, ctypes.POINTER(fts5_header.fts5_api)).contents
print("fts5_api version:", fts5_api.iVersion)

# TODO
# tok = fts5_header.fts5_tokenizer()
# tok.xTokenize

# Register custom tokenizer
# fts5_api.xCreateTokenizer(fts5_api, "test", 0, ctypes.byref(tok), 0)

# Clean up
sqlite3_finalize(pStmt)
sqlite.sqlite3_close(db)
