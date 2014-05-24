import sys, os
import random
from PyQt4 import QtGui, QtCore
from PIL import ImageQt
from hexes import *


VERSION = '0.0.0'



def _show_image(image, widget):
    """Place the Image onto the QPushButton."""
    if image is not None:
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        bh, bw = (widget.iconSize().height() * .8,
                  widget.iconSize().width() * .8)
        if (image.size[0] < bw * 3 / 4 and
            image.size[1] < bh * 3 / 4):
            factor = bw / image.size[0]
            hfactor = bh / image.size[1]
            if hfactor < factor:
                factor = hfactor
            image = image.resize((int(image.size[0] * factor),
                                  int(image.size[1] * factor)))
        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(image))
        widget.setIcon(QtGui.QIcon(pixmap))
        

def CheckMark():
    """Create and return a simple green checkmark image."""
    image = Image.new("RGBA", (100, 100))
    draw = ImageDraw.Draw(image)
    draw.polygon([ 5, 45,  5, 50, 30, 90, 50, 90, 90, 15,
                    90, 10, 70, 10, 40, 70, 25, 45,  5, 45],
                    fill=(50, 255, 0, 255), outline=(0, 100, 0, 255))
    return image
CHECK_MARK = CheckMark()

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
TRASH_CAN = TrashCan()

def DropImage():
    """Create and return a "drop images here" invitation image."""
    image = Image.new("RGBA", (750, 500))

    # Text label
    font = ImageFont.truetype("gabriola.ttf", 48)
    text = "Drop creature images here!"
    size = font.getsize(text)
    offset = font.getoffset(text)
    textimage = Image.new("RGBA", (size[0] + offset[0], size[1] + offset[1]))
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0, 0), text, font=font, fill=(100, 100, 100, 255))
    textimage = textimage.rotate(35, expand=True)
    size = textimage.size
    image.paste(textimage, (225, 200))

    # Hex imagery
    draw = ImageDraw.Draw(image)
    hexer = HexDraw(draw, (200, 50, 350, 200))
    hexer.shade(fronts=(HexDraw.SOUTHWEST, HexDraw.NORTHWEST, HexDraw.NORTH),
                sides=(HexDraw.SOUTH, HexDraw.NORTHEAST),
                backs=(HexDraw.SOUTHEAST,),
                fill=False)
    hexer.shift(HexDraw.SOUTHEAST)
    hexer.shade(fronts=(HexDraw.NORTH, HexDraw.NORTHEAST, HexDraw.SOUTHEAST),
                sides=(HexDraw.SOUTH, HexDraw.NORTHWEST),
                fill=False)
    hexer.shift(HexDraw.SOUTHWEST)
    hexer.shade(sides=(HexDraw.NORTH, HexDraw.SOUTHEAST),
                backs=(HexDraw.NORTHWEST, HexDraw.SOUTHWEST, HexDraw.SOUTH),
                fill=False)
    return image
DROP_IMAGE = DropImage()


class HexifiedImageWidget(QtGui.QWidget):

    """Horizontal bar representing one hexified image and its actions."""

    ## Build the UI ##

    def __init__(self, parent, main, hexified_image):

        def make_button(size, layout, image, action=None):
            """Setup and return a button showing the image given."""
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

        # Previews
        def new_button(image, action=None):
            return make_button((100, 100), mbox, image, action)
        self._preview = new_button(self.hexed.preview,
                                   self.next_hex_configuration)
        self._image = new_button(self.hexed.image, self.select_image)
        self._fontpreview = new_button(self.hexed.fontpreview,
                                       self.randomize_letter)

        # Buttons to the right
        vbox = QtGui.QVBoxLayout()
        mbox.addLayout(vbox)
        def new_small(image, action=None):
            return make_button((43, 43), vbox, image, action)
        new_small(CHECK_MARK, self.toggle_confirm)
        new_small(TRASH_CAN, self.deleteLater)

        

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
        _show_image(self.hexed.preview, self._preview)
        self.main.update_page()

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
        _show_image(self.hexed.preview, self._preview)
        _show_image(self.hexed.fontpreview, self._fontpreview)
        self.main.update_page()

    def set_image(self, image):
        """Update the displayed image."""
        self.hexed.image = image
        _show_image(self.hexed.preview, self._preview)
        _show_image(self.hexed.image, self._image)
        self.main.update_page()

    def set_hex_detail(self, size, shape=HexDraw.SHAPE_LONG):
        """Update the hex configuration."""
        self.hexed.size = size
        self.hexed.shape = shape
        _show_image(self.hexed.preview, self._preview)
        self.main.update_page()

    def toggle_confirm(self):
        """Toggle disabling of future edits."""
        self._preview.setEnabled(self._confirmed)
        self._image.setEnabled(self._confirmed)
        self._fontpreview.setEnabled(self._confirmed)
        
        self._confirmed = not self._confirmed
        self.main.confirm(self, self._confirmed)
        

class HexifyWidget(QtGui.QWidget):

    """Primary application: display list of items and a page preview."""

    ## Build the UI ##

    def __init__(self):
        
        def new_button(name, layout, action=None):
            btn = QtGui.QPushButton(name, self)
            if action is not None:
                btn.clicked.connect(action)
            layout.addWidget(btn)
            
        QtGui.QWidget.__init__(self, None)
        self.setAcceptDrops(True)
        stack = QtGui.QStackedLayout(self)

        ## Special UI for accepting dropped files
        self.drop_UI = QtGui.QWidget(self)
        stack.addWidget(self.drop_UI)
        box = QtGui.QVBoxLayout()
        self.drop_UI.setLayout(box)
        landing_pad = QtGui.QPushButton(self.drop_UI)
        landing_pad.setIconSize(QtCore.QSize(750, 500))
        _show_image(DROP_IMAGE, landing_pad)
        box.addWidget(landing_pad)


        ## Main UI
        self.main_UI = QtGui.QWidget(self)
        stack.addWidget(self.main_UI)
        stack.setCurrentWidget(self.main_UI)
        mbox = QtGui.QHBoxLayout()
        self.main_UI.setLayout(mbox)

        # Header buttons
        lbox = QtGui.QVBoxLayout()
        mbox.addLayout(lbox)
        head = QtGui.QHBoxLayout()
        lbox.addLayout(head)
        new_button("Re-size All", head, self.resize_all)
        new_button("Randomize All", head, self.randomize_all)
        new_button("Confirm All", head, self.confirm_all)
        new_button("Delete All", head, self.delete_all)

        # List of HexifiedItems
        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        self.scroller = QtGui.QWidget(scrollArea)
        vbox = QtGui.QVBoxLayout()
        self.scroller.setLayout(vbox)
        scrollArea.setWidget(self.scroller)
        lbox.addWidget(scrollArea)
        vbox.addStretch()

        # Temporary HexifiedImageWidget for sizing
        temp = HexifiedImageWidget(self.scroller, self, HexifiedImage(None, " "))
        temp.deleteLater()
        vbox.addWidget(temp)

        # Control panel
        vbox = QtGui.QVBoxLayout()
        mbox.addLayout(vbox)
        new_button("Add Images", vbox, self.select_images)
        new_button("Save as PNG", vbox, self.export_PNG)
        new_button("Export to PDF", vbox, self.export_PDF)
        new_button("Print", vbox, self.print_dialog)

        # Page preview
        self._pagepreview = QtGui.QLabel(self)
        vbox.addWidget(self._pagepreview)
        self.update_page()
        
    def show(self):
        """Display this QWidget as the main window."""
        self.window_ = QtGui.QMainWindow()
        self.window_.setWindowTitle('Hexify v%s' % VERSION)
        self.window_.setCentralWidget(self)
        self.center()
        self.window_.show()

    def center(self):
        """Center this window on the screen."""
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.window_.geometry()
        width = min(size.width(), int(screen.width() * .9))
        height = min(size.height(), int(screen.height() * .9))
        if width != size.width() or height != size.height():
            self.window_.resize(width, height)
            size = self.window_.geometry()
        self.window_.move((screen.width() - size.width()) / 2,
                          (screen.height() - size.height()) / 2)


    ## Drag & Drop ##
        
    def dragEnterEvent(self, event):
        """Acknowledge files being dragged in."""
        if event.mimeData().hasUrls():
            self.layout().setCurrentWidget(self.drop_UI)
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """Revert UI to normal if dragging stops."""
        self.layout().setCurrentWidget(self.main_UI)

    def dropEvent(self, event):
        """Process dropped files."""
        self.layout().setCurrentWidget(self.main_UI)
        for url in event.mimeData().urls():
            file = url.toLocalFile()
            try:
                image = Image.open(file)
                image = image.convert("RGBA")
                self.add_image(HexifiedImage(image, os.path.basename(file)[0]))
            except:
                pass

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
                self.add_image(HexifiedImage(image, os.path.basename(file)[0]))

    def add_image(self, hexed):
        """Add a HexifiedImage to the displayed list."""
        widget = HexifiedImageWidget(self.scroller, self, hexed)
        widget.destroyed.connect(self.update_page)
        layout = self.scroller.layout()
        layout.insertWidget(layout.count() - 1, widget)
        self.update_page()

    def confirm(self, widget, confirm):
        """Update confirmation status of a HexifiedImageWidget."""
        layout = self.scroller.layout()
        if confirm:
            layout.insertWidget(layout.count() - 2, widget)
        else:
            layout.insertWidget(0, widget)
            self.scroller.parent().parent().ensureVisible(0, 0)


    ## Bulk actions ##

    def _get_items(self):
        """Get all HexifiedImageWidgets currently displayed."""
        items = []
        for widget in self.scroller.children():
            if "hexed" in widget.__dict__:
                items.append(widget)
        return items

    def resize_all(self):
        """Advance all (unconfirmed) items to the next hex size/shape."""
        for widget in self._get_items():
            if not widget._confirmed:
                widget.next_hex_configuration()

    def randomize_all(self):
        """Randomize all (unconfirmed) letter labels."""
        for widget in self._get_items():
            if not widget._confirmed:
                widget.randomize_letter()

    def confirm_all(self):
        """Confirm all unconfirmed items."""
        for widget in self._get_items():
            if not widget._confirmed:
                widget.toggle_confirm()

    def delete_all(self):
        """Remove all (unconfirmed) items."""
        for widget in self._get_items():
            if not widget._confirmed:
                widget.deleteLater()


    ## Exporting ##

    def _get_page(self, hexsize=(300, 300)):
        """Get and populate a page for printing."""
        page = HexPage(hexsize, (10, 10), blanks=True, background=(255, 255, 255, 255))
        page.arrange([i.hexed for i in self._get_items()])
        return page
        
    def update_page(self):
        """Update the page preview after a change."""
        page = self._get_page((32, 32))
        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(page.image))
        self._pagepreview.setPixmap(pixmap)

    def export_PNG(self):
        """Export the filled page to PNG format."""
        page = self._get_page()
        file = QtGui.QFileDialog.getSaveFileName(self, "Save As...",
                                                 self.cwd, "*.png")
        if file:
            page.image.save(file)

    def export_PDF(self):
        """Export the filled page to PDF format."""
        file = QtGui.QFileDialog.getSaveFileName(self, "Save As...",
                                                 self.cwd, "*.pdf")
        if file:
            printer = QtGui.QPrinter()
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOutputFileName(file)
            self._print(printer)

    def print_dialog(self):
        """Show the user a print dialog."""
        printer = QtGui.QPrinter()
        dialog = QtGui.QPrintDialog(printer, self)
        if dialog.exec() == QtGui.QDialog.Accepted:
            self._print(printer)

    def _print(self, printer):
        """Send a page to the printer."""
        page = self._get_page()
        printer.setResolution(300)
        printer.setFullPage(True)
        printer.setPageMargins(.25, .25, .5, .25, QtGui.QPrinter.Inch)
        painter = QtGui.QPainter()
        painter.begin(printer)
        painter.drawImage(QtCore.QPointF(0, 0),
                          ImageQt.ImageQt(page.image))
        painter.end()
            
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    HexifyWidget().show()
    sys.exit(app.exec_())

