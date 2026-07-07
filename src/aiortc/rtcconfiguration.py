import enum
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class RTCIceServer:
    """
    The :class:`RTCIceServer` dictionary defines how to connect to a single
    STUN or TURN server. It includes both the URL and the necessary credentials,
    if any, to connect to the server.
    """

    urls: Union[str, list[str]]
    """
    This required property is either a single string or a list of strings,
    each specifying a URL which can be used to connect to the server.
    """
    username: Optional[str] = None
    "The username to use during authentication (for TURN only)."
    credential: Optional[str] = None
    "The credential to use during authentication (for TURN only)."
    credentialType: str = "password"


class RTCBundlePolicy(enum.Enum):
    """
    The :class:`RTCBundlePolicy` affects which media tracks are negotiated if
    the remote endpoint is not bundle-aware, and what ICE candidates are
    gathered.

    See https://w3c.github.io/webrtc-pc/#rtcbundlepolicy-enum
    """

    BALANCED = "balanced"
    """
    Gather ICE candidates for each media type in use (audio, video, and data).
    If the remote endpoint is not bundle-aware, negotiate only one audio and
    video track on separate transports.
    """

    MAX_COMPAT = "max-compat"
    """
    Gather ICE candidates for each track. If the remote endpoint is not
    bundle-aware, negotiate all media tracks on separate transports.
    """

    MAX_BUNDLE = "max-bundle"
    """
    Gather ICE candidates for only one track. If the remote endpoint is not
    bundle-aware, negotiate only one media track.
    """


@dataclass
class RTCConfiguration:
    """
    The :class:`RTCConfiguration` dictionary is used to provide configuration
    options for an :class:`RTCPeerConnection`.
    """

    iceServers: Optional[list[RTCIceServer]] = None
    "A list of :class:`RTCIceServer` objects to configure STUN / TURN servers."

    bundlePolicy: RTCBundlePolicy = RTCBundlePolicy.BALANCED
    "The media-bundling policy to use when gathering ICE candidates."

    alwaysNegotiateDataChannels: bool = False
    "Whether to always negotiate data channels in the SDP."

    trickleIce: bool = False
    """
    Whether to trickle ICE candidates.

    When enabled, :meth:`RTCPeerConnection.setLocalDescription` does not wait
    for ICE gathering to complete. Instead, each candidate is emitted through
    the :class:`RTCPeerConnection` `"icecandidate"` event as it is discovered,
    and should be sent to the remote party over the signaling channel. Once
    gathering completes, the event is emitted with `None`.

    This is an aiortc-specific extension: the W3C specification always
    trickles, but aiortc's historical behaviour is to wait for gathering.

    Note that per RFC 8838 an answerer should only trickle if the offerer
    indicated support for it (e.g. with an `a=ice-options:trickle` SDP
    attribute); checking this is the application's responsibility.
    """
