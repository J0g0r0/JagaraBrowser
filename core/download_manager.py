from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QProgressBar, QLabel, QPushButton, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem

class DownloadManager(QObject):
    _instance = None
    download_added = pyqtSignal(object)

    def __init__(self, parent=None):
        if DownloadManager._instance:
            raise Exception("Singleton")
        super().__init__(parent)
        from PyQt5.QtWebEngineWidgets import QWebEngineProfile
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.downloadRequested.connect(self.on_download_requested)
        DownloadManager._instance = self

    @staticmethod
    def instance():
        if not DownloadManager._instance:
            DownloadManager._instance = DownloadManager()
        return DownloadManager._instance

    def on_download_requested(self, download: QWebEngineDownloadItem):
        path, _ = QFileDialog.getSaveFileName(None, "Save Download", download.path())
        if path:
            download.setPath(path)
            download.accept()
            self.download_added.emit(download)
        else:
            download.cancel()

class DownloadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Downloads")
        self.resize(500, 300)
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        DownloadManager.instance().download_added.connect(self.add_download)

    def add_download(self, download):
        from PyQt5.QtWidgets import QListWidgetItem, QWidget, QHBoxLayout
        item = QListWidgetItem()
        widget = QWidget()
        hbox = QHBoxLayout(widget)
        label = QLabel(download.path().split('/')[-1])
        progress = QProgressBar()
        progress.setMaximum(100)
        hbox.addWidget(label)
        hbox.addWidget(progress)
        download.downloadProgress.connect(lambda recv, total: progress.setValue(int(recv/total*100)))
        download.finished.connect(lambda: progress.setValue(100))
        item.setSizeHint(widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)