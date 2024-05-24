import _compression
import sys
import zlib
from _typeshed import ReadableBuffer, SizedBuffer, StrOrBytesPath
from io import FileIO
from typing import Literal, Protocol, TextIO, overload
from typing_extensions import TypeAlias

__all__ = ["BadGzipFile", "GzipFile", "open", "compress", "decompress"]

_ReadBinaryMode: TypeAlias = Literal["r", "rb"]
_WriteBinaryMode: TypeAlias = Literal["a", "ab", "w", "wb", "x", "xb"]
_OpenTextMode: TypeAlias = Literal["rt", "at", "wt", "xt"]

READ: object  # undocumented
WRITE: object  # undocumented

FTEXT: int  # actually Literal[1] # undocumented
FHCRC: int  # actually Literal[2] # undocumented
FEXTRA: int  # actually Literal[4] # undocumented
FNAME: int  # actually Literal[8] # undocumented
FCOMMENT: int  # actually Literal[16] # undocumented

class _ReadableFileobj(Protocol):
    def read(self, n: int, /) -> bytes: ...
    def seek(self, n: int, /) -> object: ...
    # The following attributes and methods are optional:
    # name: str
    # mode: str
    # def fileno() -> int: ...

class _WritableFileobj(Protocol):
    def write(self, b: bytes, /) -> object: ...
    def flush(self) -> object: ...
    # The following attributes and methods are optional:
    # name: str
    # mode: str
    # def fileno() -> int: ...

@overload
def open(
    filename: StrOrBytesPath | _ReadableFileobj,
    mode: _ReadBinaryMode = "rb",
    compresslevel: int = 9,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
) -> GzipFile: ...
@overload
def open(
    filename: StrOrBytesPath | _WritableFileobj,
    mode: _WriteBinaryMode,
    compresslevel: int = 9,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
) -> GzipFile: ...
@overload
def open(
    filename: StrOrBytesPath,
    mode: _OpenTextMode,
    compresslevel: int = 9,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
) -> TextIO: ...
@overload
def open(
    filename: StrOrBytesPath | _ReadableFileobj | _WritableFileobj,
    mode: str,
    compresslevel: int = 9,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
) -> GzipFile | TextIO: ...

class _PaddedFile:
    file: _ReadableFileobj
    def __init__(self, f: _ReadableFileobj, prepend: bytes = b"") -> None: ...
    def read(self, size: int) -> bytes: ...
    def prepend(self, prepend: bytes = b"") -> None: ...
    def seek(self, off: int) -> int: ...
    def seekable(self) -> bool: ...

class BadGzipFile(OSError): ...

class GzipFile(_compression.BaseStream):
    myfileobj: FileIO | None
    mode: object
    name: str
    compress: zlib._Compress
    fileobj: _ReadableFileobj | _WritableFileobj
    @overload
    def __init__(
        self,
        filename: StrOrBytesPath | None,
        mode: _ReadBinaryMode,
        compresslevel: int = 9,
        fileobj: _ReadableFileobj | None = None,
        mtime: float | int | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        mode: _ReadBinaryMode,
        compresslevel: int = 9,
        fileobj: _ReadableFileobj | None = None,
        mtime: float | int | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        filename: StrOrBytesPath | None,
        mode: _WriteBinaryMode,
        compresslevel: int = 9,
        fileobj: _WritableFileobj | None = None,
        mtime: float | int | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        mode: _WriteBinaryMode,
        compresslevel: int = 9,
        fileobj: _WritableFileobj | None = None,
        mtime: float | int | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        filename: StrOrBytesPath | None = None,
        mode: str | None = None,
        compresslevel: int = 9,
        fileobj: _ReadableFileobj | _WritableFileobj | None = None,
        mtime: float | int | None = None,
    ) -> None: ...
    if sys.version_info < (3, 12):
        @property
        def filename(self) -> str: ...

    @property
    def mtime(self) -> int | None: ...
    crc: int
    def write(self, data: ReadableBuffer) -> int: ...
    def read(self, size: int | None = -1) -> bytes: ...
    def read1(self, size: int = -1) -> bytes: ...
    def peek(self, n: int) -> bytes: ...
    def close(self) -> None: ...
    def flush(self, zlib_mode: int = 2) -> None: ...
    def fileno(self) -> int: ...
    def rewind(self) -> None: ...
    def seek(self, offset: int, whence: int = 0) -> int: ...
    def readline(self, size: int | None = -1) -> bytes: ...

class _GzipReader(_compression.DecompressReader):
    def __init__(self, fp: _ReadableFileobj) -> None: ...

def compress(data: SizedBuffer, compresslevel: int = 9, *, mtime: float | int | None = None) -> bytes: ...
def decompress(data: ReadableBuffer) -> bytes: ...
