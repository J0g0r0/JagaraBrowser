"""
Ad blocker using URL interceptor with a careful blocklist.
"""
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

# Only block well-known ad/tracking domains (exact or subdomain)
AD_DOMAINS = [
    "doubleclick.net",
    "googlesyndication.com",
    "googleadservices.com",
    "ads.youtube.com",
    "pagead2.googlesyndication.com",
    "amazon-adsystem.com",
    "adnxs.com",
    "rubiconproject.com",
    "outbrain.com",
    "taboola.com",
    "criteo.com",
    "adsrvr.org",
    "pubmatic.com",
    "casalemedia.com",
    "openx.net",
    "moatads.com",
    "adservice.google.com",
]

class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self, profile):
        super().__init__()
        profile.setUrlRequestInterceptor(self)

    def interceptRequest(self, info):
        url = info.requestUrl().toString().lower()
        for domain in AD_DOMAINS:
            # Block if domain is exactly in the host or as a subdomain
            if f".{domain}" in url or url.startswith(f"{domain}/") or f"/{domain}" in url:
                info.block(True)
                return