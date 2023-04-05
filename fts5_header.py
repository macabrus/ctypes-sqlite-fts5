import ctypes as ct

# typedef struct Fts5Tokenizer Fts5Tokenizer;
# typedef struct fts5_tokenizer fts5_tokenizer;
# struct fts5_tokenizer {
#   int (*xCreate)(void*, const char **azArg, int nArg, Fts5Tokenizer **ppOut);
#   void (*xDelete)(Fts5Tokenizer*);
#   int (*xTokenize)(Fts5Tokenizer*, 
#       void *pCtx,
#       int flags,            /* Mask of FTS5_TOKENIZE_* flags */
#       const char *pText, int nText, 
#       int (*xToken)(
#         void *pCtx,         /* Copy of 2nd argument to xTokenize() */
#         int tflags,         /* Mask of FTS5_TOKEN_* flags */
#         const char *pToken, /* Pointer to buffer containing token */
#         int nToken,         /* Size of token in bytes */
#         int iStart,         /* Byte offset of token within input text */
#         int iEnd            /* Byte offset of end of token within input text */
#       )
#   );
# };

import ctypes

def custom_tokenize(text):
    for word in text.split(' '):
        yield word

# Define Fts5Tokenizer struct
class Fts5Tokenizer(ctypes.Structure):
    pass

# Define fts5_tokenizer struct
class fts5_tokenizer(ctypes.Structure):
    _fields_ = [
        ("xCreate", ctypes.CFUNCTYPE(
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.c_int,
            ctypes.POINTER(ctypes.POINTER(Fts5Tokenizer))
        )),
        ("xDelete", ctypes.CFUNCTYPE(
            None,
            ctypes.POINTER(Fts5Tokenizer)
        )),
        ("xTokenize", ctypes.CFUNCTYPE(
            ctypes.c_int,
            ctypes.POINTER(Fts5Tokenizer),
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.CFUNCTYPE(
                ctypes.c_int,
                ctypes.c_void_p,
                ctypes.c_int,
                ctypes.c_char_p,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int
            )
        ))
    ]


# /* Flags that may be passed as the third argument to xTokenize() */
# #define FTS5_TOKENIZE_QUERY     0x0001
# #define FTS5_TOKENIZE_PREFIX    0x0002
# #define FTS5_TOKENIZE_DOCUMENT  0x0004
# #define FTS5_TOKENIZE_AUX       0x0008

# /* Flags that may be passed by the tokenizer implementation back to FTS5
# ** as the third argument to the supplied xToken callback. */
# #define FTS5_TOKEN_COLOCATED    0x0001      /* Same position as prev. token */

# /*
# ** END OF CUSTOM TOKENIZERS
# *************************************************************************/

# /*************************************************************************
# ** FTS5 EXTENSION REGISTRATION API
# */
# typedef struct fts5_api fts5_api;
# struct fts5_api {
#   int iVersion;                   /* Currently always set to 2 */

#   /* Create a new tokenizer */
#   int (*xCreateTokenizer)(
#     fts5_api *pApi,
#     const char *zName,
#     void *pContext,
#     fts5_tokenizer *pTokenizer,
#     void (*xDestroy)(void*)
#   );

#   /* Find an existing tokenizer */
#   int (*xFindTokenizer)(
#     fts5_api *pApi,
#     const char *zName,
#     void **ppContext,
#     fts5_tokenizer *pTokenizer
#   );

#   /* Create a new auxiliary function */
#   int (*xCreateFunction)(
#     fts5_api *pApi,
#     const char *zName,
#     void *pContext,
#     fts5_extension_function xFunction,
#     void (*xDestroy)(void*)
#   );
# };

import ctypes

# Define fts5_api struct
class fts5_api(ctypes.Structure):
    pass

fts5_api._fields_ = [
        ("iVersion", ctypes.c_int),
        ("xCreateTokenizer", ctypes.CFUNCTYPE(
            ctypes.c_int,
            ctypes.POINTER(fts5_api),
            ctypes.c_char_p,
            ctypes.c_void_p,
            ctypes.POINTER(fts5_tokenizer),
            ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p
            )
        )),
        ("xFindTokenizer", ctypes.CFUNCTYPE(
            ctypes.c_int,
            ctypes.POINTER(fts5_api),
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.POINTER(fts5_tokenizer)
        )),
        ("xCreateFunction", ctypes.CFUNCTYPE(
            ctypes.c_int,
            ctypes.POINTER(fts5_api),
            ctypes.c_char_p,
            ctypes.c_void_p,
            ctypes.c_void_p, # ctypes.POINTER(fts5_extension_function),
            ctypes.CFUNCTYPE(
                None,
                ctypes.c_void_p
            )
        ))
    ]


# We should write ctypes api for this and then 