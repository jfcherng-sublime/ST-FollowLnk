import struct
from struct import unpack
import warnings

from .extra.environment import Environment
from .extra.console import Console
from .extra.distributed_tracker import DistributedTracker
from .extra.code_page import CodePage
from .extra.special_folder import SpecialFolder
from .extra.darwin import Darwin
from .extra.icon import Icon
from .extra.shim_layer import ShimLayer
from .extra.metadata import Metadata
from .extra.known_folder import KnownFolder
from .extra.shell_item import ShellItem

"""
------------------------------------------------------------------
|     0-7b     |     8-15b     |     16-23b     |     24-31b     |
------------------------------------------------------------------
|              <u_int32> BlockSize == 0x00000314                 |
------------------------------------------------------------------
|            <u_int32> BlockSignature == 0xA0000001              |
------------------------------------------------------------------
"""


class ExtraFactory:
    EXTRA_SIGS = {
        "a0000001": Environment,
        "a0000002": Console,
        "a0000003": DistributedTracker,
        "a0000004": CodePage,
        "a0000005": SpecialFolder,
        "a0000006": Darwin,
        "a0000007": Icon,
        "a0000008": ShimLayer,
        "a0000009": Metadata,
        "a000000b": KnownFolder,
        "a000000c": ShellItem,
    }

    def __init__(self, indata):
        self._raw = indata

    def item_size(self):
        start, end = 0, 4
        size = unpack("<I", self._raw[start:end])[0]
        return size

    def _rsig(self):
        start, end = 4, 8
        rsig = unpack("<I", self._raw[start:end])[0]
        return rsig

    def extra_class(self):
        # Allow for no accompanying data for a reported size, observed in malicious files
        try:
            sig = str(hex(self._rsig()))[2:]  # huh?
            return self.EXTRA_SIGS.get(sig)
        except struct.error as e:
            warnings.warn(f"Error while parsing extra's signature {e}")
            return None
