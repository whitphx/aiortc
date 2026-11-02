from abc import ABCMeta, abstractmethod

from av.frame import Frame
from av.packet import Packet

from ..jitterbuffer import JitterFrame

# The maximum size of a video RTP payload. It keeps RTP packets, including
# the header, its extensions and the RTX sequence number, within the 1200
# bytes libwebrtc uses, which fits the minimum IPv6 MTU (RFC 8200 section 5)
# once SRTP, UDP and IP overhead is added. See
# https://webrtc.googlesource.com/src/+/8290a27b8d720439e99762bcfa9b51afc9a9d613/media/base/media_constants.h#25
PACKET_MAX = 1150


class Decoder(metaclass=ABCMeta):
    @abstractmethod
    def decode(self, encoded_frame: JitterFrame) -> list[Frame]:
        pass  # pragma: no cover


class Encoder(metaclass=ABCMeta):
    @abstractmethod
    def encode(
        self, frame: Frame, force_keyframe: bool = False
    ) -> tuple[list[bytes], int]:
        pass  # pragma: no cover

    @abstractmethod
    def pack(self, packet: Packet) -> tuple[list[bytes], int]:
        pass  # pragma: no cover
