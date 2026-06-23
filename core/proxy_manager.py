from PyQt5.QtNetwork import QNetworkProxy, QNetworkProxyFactory

class ProxyManager:
    @staticmethod
    def set_proxy(proxy_type: str, host: str, port: int, username='', password=''):
        proxy = QNetworkProxy()
        if proxy_type == 'http':
            proxy.setType(QNetworkProxy.HttpProxy)
        elif proxy_type == 'socks5':
            proxy.setType(QNetworkProxy.Socks5Proxy)
        else:
            proxy.setType(QNetworkProxy.NoProxy)

        proxy.setHostName(host)
        proxy.setPort(port)
        if username:
            proxy.setUser(username)
            proxy.setPassword(password)
        QNetworkProxy.setApplicationProxy(proxy)

    @staticmethod
    def disable_proxy():
        QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.NoProxy))