import pytube, requests, os
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def main():
    class main_app(QMainWindow):
        def __init__(self, parent=None, *args):
            super(main_app, self).__init__(parent=parent)
            
            self.setWindowTitle('Py You Downloader')
            self.setFixedSize(700, 300)
            self.setWindowIcon(QIcon('ico.ico'))
            
            # --------  Url input  --------
            self.url = QLineEdit(self)
            self.url.setPlaceholderText('Url del Video')
            self.url.setGeometry(10, 10, 200, 30)
            self.url.setClearButtonEnabled(True)
            
            self.send = QPushButton('Buscar', self)
            self.send.setGeometry(220, 10, 50, 30)
            
            # --------  Error  --------
            self.error = QLabel(self)
            self.error.setHidden(True)
            self.error.setGeometry(10, 50, 260, 30)
            self.error.setStyleSheet('background: #ffbbbb')
            self.error.setAlignment(Qt.AlignCenter)
            
            self.downloaderror = QLabel('Ningún video con estas características', self)
            self.downloaderror.setHidden(True)
            self.downloaderror.setGeometry(10, 240, 260, 30)
            self.downloaderror.setStyleSheet('background: #ffbbbb')
            self.downloaderror.setAlignment(Qt.AlignCenter)
            
            self.connectionerror = QLabel('Error de conexión, vuelve a intentar', self)
            self.connectionerror.setHidden(True)
            self.connectionerror.setGeometry(10, 240, 260, 30)
            self.connectionerror.setStyleSheet('background: #ffbbbb')
            self.connectionerror.setAlignment(Qt.AlignCenter)
            
            # --------  Decorations  --------
            self.line_vertical = QLabel(self)
            self.line_vertical.setGeometry(280, 5, 2, 290)
            self.line_vertical.setStyleSheet('background: gray')
            
            self.filtertext = QLabel('<b>Filtros</b>', self)
            self.filtertext.setGeometry(10, 45, 260, 30)
            self.filtertext.setAlignment(Qt.AlignCenter)
            self.filtertext.setStyleSheet('color: gray')
            self.filtertext.setHidden(True)
            
            self.linefilter1 = QLabel(self)
            self.linefilter1.setGeometry(10, 60, 100, 2)
            self.linefilter1.setStyleSheet('background: gray')
            self.linefilter1.setHidden(True)
            
            self.linefilter2 = QLabel(self)
            self.linefilter2.setGeometry(170, 60, 100, 2)
            self.linefilter2.setStyleSheet('background: gray')
            self.linefilter2.setHidden(True)
            
            # --------  Video Info  --------
            
            self.lasturl = QLabel('', self)
            self.lasturl.setGeometry(10, 300, 300, 30)
            
            # Title
            self.title = QLabel(self)
            self.title.setGeometry(290, 220, 400, 30)
            self.title.setFont(QFont('calibri', 10))
            
            # Duration
            self.duration = QLabel(self)
            self.duration.setGeometry(290, 250, 260, 30)
            self.title.setFont(QFont('calibri', 10))
            
            # Image
            self.img = QLabel(self)
            self.img.setGeometry(290, 10, 400, 200)
            self.img.setAlignment(Qt.AlignCenter)
            
            
            # --------  Filter  --------
            # Video
            self.video = QRadioButton('Video', self)
            self.video.setGeometry(10, 70, 260, 30)
            self.video.setChecked(True)
            self.video.setHidden(True)
            
            # Audio
            self.audio = QRadioButton('Audio', self)
            self.audio.setGeometry(10, 90, 260, 30)
            self.audio.setHidden(True)
            
            # --------  Current Options  --------
            self.textlist = QLabel('Formato:', self)
            self.textlist.setGeometry(10, 117, 50, 30)
            self.textlist.setHidden(True)
            
            self.list = QComboBox(self)
            self.list.setHidden(True)
            self.list.setGeometry(60, 120, 210, 30)
            
            self.textquality = QLabel('Calidad:', self)
            self.textquality.setGeometry(10, 157, 50, 30)
            self.textquality.setHidden(True)
            
            self.quality = QComboBox(self)
            self.quality.setHidden(True)
            self.quality.setGeometry(60, 160, 210, 30)
            
            self.downloadbutton = QPushButton('Descargar', self)
            self.downloadbutton.setGeometry(10, 200, 260, 30)
            self.downloadbutton.setHidden(True)
            
            self.dir = QFile
            
            # --------  Triggers --------
            self.url.returnPressed.connect(self.search_url)
            self.send.clicked.connect(self.search_url)
            self.video.toggled.connect(self.videofilter)
            self.downloadbutton.clicked.connect(self.download)
        
        def videofilter(self):
            
            try:
                avariable_streams = pytube.YouTube(self.url.text()).streams
                self.list.clear()
                self.quality.clear()
                
                format = []
                quality = []
                
                for option in avariable_streams:
                    if option.audio_codec:
                        if self.video.isChecked(): # Type Video
                            if 'video' in option.mime_type:
                                if option.mime_type[6:] not in format:
                                    self.list.addItem(option.mime_type[6:])
                                    format.append(option.mime_type[6:])
                                if int(option.resolution.replace('p', '')) not in quality:
                                    quality.append(int(option.resolution.replace('p', '')))
                        
                        else:                      # Type Audio 
                            if 'audio' in option.mime_type:
                                if option.mime_type[6:] not in format:
                                    self.list.addItem(option.mime_type[6:])
                                    format.append(option.mime_type[6:])
                                if int(option.abr.replace('kbps', '')) not in quality:
                                    quality.append(int(option.abr.replace('kbps', '')))
                
                if self.video.isChecked():
                    for i in sorted(quality):
                        self.quality.addItem(str(i) + 'p')
                else:
                    for i in sorted(quality):
                        self.quality.addItem(str(i) + 'kbps')
                
            
            except pytube.exceptions.RegexMatchError:
                self.alert('⚠ No es un enlace de YouTube ⚠')
            
            except pytube.exceptions.VideoUnavailable:
                self.alert('⚠ Video no disponible ⚠')
            
            except:
                self.alert('⚠ Error de conexión, vuelve a intentar ⚠')
        
        def download(self):
            self.connectionerror.setHidden(True)
            self.downloaderror.setHidden(True)
            
            try:
                avariable_streams = pytube.YouTube(self.url.text()).streams
                
                options = {
                    'type'    : '',
                    'format'  : self.list.currentText(),
                    'quality' : self.quality.currentText()
                }
                
                if self.video.isChecked():
                    options['type'] = 'video'
                    avariable_streams = avariable_streams.filter(type=options['type'], mime_type='video/' + options['format'], resolution=options['quality'])
                else:
                    options['type'] = 'audio'
                    avariable_streams = avariable_streams.filter(type=options['type'], mime_type='audio/' + options['format'], abr=options['quality'])
                
                successs = False
                if avariable_streams:
                    for i in avariable_streams:
                        if i.audio_codec:
                            i.download()
                            successs =True
                            break
                    
                if not successs:
                    self.downloaderror.setHidden(False)
                
            except pytube.exceptions.RegexMatchError:
                self.alert('⚠ No es un enlace de YouTube ⚠')
                
            except pytube.exceptions.VideoUnavailable:
                self.alert('⚠ Video no disponible ⚠')
            except:
                self.connectionerror.setHidden(False)
        
        def search_url(self):
            
            try:
                video = pytube.YouTube(self.url.text())
                
                # --------  Hidden Elements  --------
                self.error.setHidden(True)
                self.img.setHidden(False)
                self.title.setHidden(False)
                self.duration.setHidden(False)
                self.filtertext.setHidden(False)
                self.linefilter2.setHidden(False)
                self.linefilter1.setHidden(False)
                self.video.setHidden(False)
                self.audio.setHidden(False)
                self.list.setHidden(False)
                self.textlist.setHidden(False)
                self.quality.setHidden(False)
                self.textquality.setHidden(False)
                self.downloadbutton.setHidden(False)
                
                # --------  Video Info  --------
                
                # Title
                self.title.setText('<b>Titulo: </b><br>' + video.title[0:60] + '...')
                
                # Duration
                duration = f'{str(video.length // 60)}:{video.length - (video.length // 60 * 60)}'
                self.duration.setText('<b>Duracion: </b>' + duration)
                
                # Image
                img = video.thumbnail_url
                
                with open('temp_img.jpg', 'wb') as f:
                    img = requests.get(img).content
                    f.write(img)
                
                with Image.open('temp_img.jpg') as img:
                    img = img.crop((0, 60, 640, 420))
                    img.save('temp_img.jpg')
                
                pixmap = QPixmap('temp_img.jpg').scaled(400, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.img.setPixmap(pixmap)
                
                # --------  Options  --------
                
                self.videofilter()
                
                
            except pytube.exceptions.RegexMatchError:
                self.alert('⚠ No es un enlace de YouTube ⚠')
                
            except pytube.exceptions.VideoUnavailable:
                self.alert('⚠ Video no disponible ⚠')
                
            except:
                self.alert('⚠ Error de conexión, vuelve a intentar ⚠')
            
            
        def alert(self, msg):
            self.error.setHidden(False)
            self.error.setText(msg)
            self.img.setHidden(True)
            self.title.setHidden(True)
            self.duration.setHidden(True)
            self.list.setHidden(True)
            self.filtertext.setHidden(True)
            self.linefilter2.setHidden(True)
            self.linefilter1.setHidden(True)
            self.video.setHidden(True)
            self.audio.setHidden(True)
            self.textlist.setHidden(True)
            self.quality.setHidden(True)
            self.textquality.setHidden(True)
            self.downloadbutton.setHidden(True)
        
        
    app = QApplication([])
    window = main_app()
    window.show()
    app.exec_()
    if os.path.exists('temp_img.jpg'):
        os.remove('temp_img.jpg')


if __name__ == '__main__':
    main()