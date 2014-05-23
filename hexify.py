import sys, os
import random
from PyQt4 import QtGui, QtCore
from PIL import ImageQt
from hexes import *


VERSION = '0.0.0'


class HexifiedImageWidget(QtGui.QWidget):

    """Horizontal bar representing one hexified image and its actions."""

    ## Build the UI ##

    def __init__(self, parent, main, hexified_image):

        def make_button(size, layout, image, action=None):
            btn = QtGui.QPushButton(self)
            btn.setIconSize(QtCore.QSize(size[0], size[1]))
            layout.addWidget(btn)
            self._show_image(image, btn)
            if action is not None:
                btn.clicked.connect(action)
            return btn
        
        QtGui.QWidget.__init__(self, parent)
        self.main = main
        self.hexed = hexified_image
        self._confirmed = False
        if (self.hexed.image is None):
            self.hexed.image = Image.new("RGBA", (100, 100))
        mbox = QtGui.QHBoxLayout()
        self.setLayout(mbox)

        def new_button(image, action=None):
            return make_button((100, 100), mbox, image, action)
        self._preview = new_button(self.hexed.preview,
                                   self.next_hex_configuration)
        self._image = new_button(self.hexed.image, self.select_image)
        self._fontpreview = new_button(self.hexed.fontpreview,
                                       self.randomize_letter)

        vbox = QtGui.QVBoxLayout()
        mbox.addLayout(vbox)

        def new_small(image, action=None):
            return make_button((43, 43), vbox, image, action)
        new_small(HexifiedImageWidget.CheckMark(), self.toggle_confirm)
        new_small(HexifiedImageWidget.TrashCan(), self.deleteLater)

        

    def _show_image(self, image, button):
        """Place the Image onto the QPushButton."""
        if image is not None:
            if image.mode != "RGBA":
                image = image.convert("RGBA")
            bh, bw = (button.iconSize().height() * .8,
                      button.iconSize().width() * .8)
            if (image.size[0] < bw * 3 / 4 and
                image.size[1] < bh * 3 / 4):
                factor = bw / image.size[0]
                hfactor = bh / image.size[1]
                if hfactor < factor:
                    factor = hfactor
                image = image.resize((int(image.size[0] * factor),
                                      int(image.size[1] * factor)))
            pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(image))
            button.setIcon(QtGui.QIcon(pixmap))


    ## Custom Images ##

    def CheckMark():
        """Create and return a simple green checkmark image."""
        image = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(image)
        draw.polygon([ 5, 45,  5, 50, 30, 90, 50, 90, 90, 15,
                      90, 10, 70, 10, 40, 70, 25, 45,  5, 45],
                     fill=(50, 255, 0, 255), outline=(0, 100, 0, 255))
        return image

    def TrashCan():
        """Create and return a simple red trash can image."""
        base = (200, 0, 0, 255)
        line = (100, 0, 0, 255)
        image = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(image)
        draw.polygon((10, 15, 90, 15, 80, 90, 20, 90, 10, 15), fill=base)
        draw.line((10, 15, 20, 90), fill=line)
        draw.line((90, 15, 80, 90), fill=line)
        draw.chord((20, 82, 80, 98), 0, 180, fill=base)
        draw.arc((20, 82, 80, 98), 0, 180, fill=line)
        draw.ellipse((10, 5, 90, 25), fill=base, outline=line)
        draw.arc((13, 11, 87, 29), 0, 180, fill=line)
        draw.line((45, 15, 55, 15), fill=line)
        draw.line((50, 29, 50, 98), fill=line)
        draw.line((30, 28, 35, 94), fill=line)
        draw.line((70, 28, 65, 94), fill=line)
        return image

        
    ## Actions & Updates ##

    def next_hex_configuration(self):
        """Move to the next shape (or size) of hexes."""
        shape = self.hexed.shape
        self.hexed.shape += 1
        self.hexed.preview
        if self.hexed.shape == 0:
            size = self.hexed.size
            self.hexed.size += 1
            self.hexed.preview
            if size == self.hexed.size:
                self.hexed.size = 1
                self.hexed.preview
        self._show_image(self.hexed.preview, self._preview)

    def select_image(self):
        """Allow the user to select an image."""
        file = QtGui.QFileDialog.getOpenFileName(self,
                                                 "Select An Image",
                                                 self.main.cwd,
                                                 "Images (*.png *.xpm *.jpg)")
        if os.path.isfile(file):
            self.main.cwd = os.path.dirname(file)
            image = Image.open(file)
            image = image.convert("RGBA")
            self.set_image(image)
            self.set_letter(os.path.basename(file)[0]) 

    def randomize_letter(self):
        """Choose a random upper-case letter."""
        self.set_letter(chr(random.randint(65, 90)))

    def set_letter(self, letter):
        """Update the displayed letter."""
        self.hexed.letter = letter
        self._show_image(self.hexed.preview, self._preview)
        self._show_image(self.hexed.fontpreview, self._fontpreview)

    def set_image(self, image):
        """Update the displayed image."""
        self.hexed.image = image
        self._show_image(self.hexed.preview, self._preview)
        self._show_image(self.hexed.image, self._image)

    def set_hex_detail(self, size, shape=HexDraw.SHAPE_LONG):
        """Update the hex configuration."""
        self.hexed.size = size
        self.hexed.shape = shape
        self._show_image(self.hexed.preview, self._preview)

    def toggle_confirm(self):
        """Toggle disabling of future edits."""
        self._preview.setEnabled(self._confirmed)
        self._image.setEnabled(self._confirmed)
        self._fontpreview.setEnabled(self._confirmed)
        
        self._confirmed = not self._confirmed
        self.main.confirm(self, self._confirmed)
        

class HexifyWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self, None)
        mbox = QtGui.QHBoxLayout()
        self.setLayout(mbox)

        # List of HexifiedItems
        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        self.scroller = QtGui.QWidget(scrollArea)
        vbox = QtGui.QVBoxLayout()
        self.scroller.setLayout(vbox)
        scrollArea.setWidget(self.scroller)
        mbox.addWidget(scrollArea)
        vbox.addStretch()

        # Control panel
        vbox = QtGui.QVBoxLayout()
        mbox.addLayout(vbox)
        def new_button(name, action=None):
            btn = QtGui.QPushButton(name, self)
            if action is not None:
                btn.clicked.connect(action)
            vbox.addWidget(btn)
        new_button("Add Images", self.select_images)
        #new_button("Print")
        #new_button("Clear All")

        # Page preview

        
    def show(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setWindowTitle('Hexifyv%s' % VERSION)
        self.window_.setCentralWidget(self)
        self.center()
        self.window_.show()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.window_.geometry()
        width = min(size.width(), int(screen.width() * .9))
        height = min(size.height(), int(screen.height() * .9))
        if width != size.width() or height != size.height():
            self.window_.resize(width, height)
            size = self.window_.geometry()
        self.window_.move((screen.width() - size.width()) / 2,
                          (screen.height() - size.height()) / 2)


    ## Actions & Updates ##

    def __getattr__(self, name):
        if name == "cwd":
            return os.getcwd()
        raise NameError

    def select_images(self):
        """Allow the user to select one or more images to add."""
        files = QtGui.QFileDialog.getOpenFileNames(self,
                                                   "Select Your Image(s)",
                                                   self.cwd,
                                                   "Images (*.png *.xpm *.jpg)")
        for file in files:
            if os.path.isfile(file):
                self.cwd = os.path.dirname(file)
                image = Image.open(file)
                image = image.convert("RGBA")
                self.add_image(HexifiedImage(image, os.path.basename(file)[0]) )

    def add_image(self, hexed):
        """Add a HexifiedImage to the displayed list."""
        widget = HexifiedImageWidget(self.scroller, self, hexed)
        layout = self.scroller.layout()
        layout.insertWidget(layout.count() - 1, widget)

    def confirm(self, widget, confirm):
        """Update confirmation status of a HexifiedImageWidget."""
        layout = self.scroller.layout()
        if confirm:
            layout.insertWidget(layout.count() - 2, widget)
        else:
            layout.insertWidget(0, widget)
            
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    HexifyWidget().show()
    sys.exit(app.exec_())

