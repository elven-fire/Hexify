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

        # Selection box
        self._selected = QtGui.QCheckBox(self)
        self._selected.setMaximumWidth(25)
        self._selected.stateChanged.connect(self.main.selection_changed)
        mbox.addWidget(self._selected)

        # Previews
        def new_button(image, action=None):
            return make_button((100, 100), mbox, image, action)
        self._preview = new_button(self.hexed.preview,
                                   self.next_hex_configuration)
        self._image = new_button(self.hexed.image, self.select_image)

        # Editable font preview
        self.stacker = QtGui.QStackedWidget(self)
        mbox.addWidget(self.stacker)
        self._fontpreview = new_button(self.hexed.fontpreview,
                                       self._edit_letter)
        self.stacker.addWidget(self._fontpreview)
        class DummyTextEdit(QtGui.QTextEdit):
            def focusOutEvent(s, e):
                self._editing_done()
                QtGui.QTextEdit.focusOutEvent(s, e)
            def keyPressEvent(s, e):
                if e.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return,
                             QtCore.Qt.Key_Escape]:
                    self._editing_done()
                    self._fontpreview.setFocus()
                else:
                    QtGui.QTextEdit.keyPressEvent(s, e)
        self._fonteditor = DummyTextEdit(self)
        self._fonteditor.setAcceptRichText(False)
        self._fonteditor.setTabChangesFocus(True)
        self._fonteditor.textChanged.connect(self._letter_edited)
        self.stacker.addWidget(self._fonteditor)
        self.stacker.setCurrentWidget(self._fontpreview)

        # Fix sizing issues with stacker
        square_size = self._fontpreview.sizeHint().height()
        self.stacker.setMaximumSize(QtCore.QSize(square_size, square_size))
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        
        # Buttons to the right
        vbox = QtGui.QVBoxLayout()
        mbox.addLayout(vbox)
        def new_small(image, action=None):
            return make_button((43, 43), vbox, image, action)
        new_small(CHECK_MARK, self.toggle_confirm)
        new_small(TRASH_CAN, self.deleteLater)

    @property
    def selected(self):
        return self._selected.isChecked()

    @selected.setter
    def selected(self, value):
        self._selected.setChecked(value)

    @property
    def confirmed(self):
        return self._confirmed

    @confirmed.setter
    def confirmed(self, value):
        if self._confirmed != value:
            self.toggle_confirm()
        

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
                                                 self.main.cwd_open,
                                                 "Images (*.png *.jpg)")
        if os.path.isfile(file):
            self.main.cwd_open = os.path.dirname(file)
            image = Image.open(file)
            image = image.convert("RGBA")
            self.set_image(image)
            self.set_letter(os.path.basename(file)[0])

    def _edit_letter(self):
        """Allow the user to edit the letter."""
        self._fonteditor.setText("")
        #self._fonteditor.textCursor().select(QtGui.QTextCursor.Document)
        self.stacker.setCurrentWidget(self._fonteditor)

    def _letter_edited(self):
        """Update the previews when the user types."""
        letter = self._fonteditor.toPlainText()
        if letter:
            self.set_letter(letter.strip())

    def _editing_done(self):
        """Return to the preview when editing is complete."""
        self.stacker.setCurrentWidget(self._fontpreview)

    def randomize_letter(self):
        """Choose a random upper-case letter."""
        current = self.hexed.letter
        while current == self.hexed.letter:
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
            return btn
            
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
        self._selected = QtGui.QCheckBox(self.main_UI)
        self._selected.setMaximumWidth(25)
        head.addWidget(self._selected)
        self._selected.setTristate()
        self._selected.stateChanged.connect(self._select_all)
        self._resize_btn = new_button("Resize Selected", head, self.resize_selected)
        self._random_btn = new_button("Randomize Selected", head, self.randomize_selected)
        self._confirm_btn = new_button("[Un]confirm Selected", head, self.confirm_selected)
        self._delete_btn = new_button("Delete Selected", head, self.delete_selected)
        self._pause_selection_watch = False

        # List of HexifiedItems
        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        self.scroller = QtGui.QWidget(scrollArea)
        vbox = QtGui.QVBoxLayout()
        self.scroller.setLayout(vbox)
        scrollArea.setWidget(self.scroller)
        lbox.addWidget(scrollArea)
        vbox.addStretch()
        self._confirmed_count = 0

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
        vbox.addWidget(self._pagepreview, alignment=QtCore.Qt.AlignBottom)
        hbox = QtGui.QHBoxLayout()
        vbox.addLayout(hbox)
        b = new_button("<", hbox, self.prev_preview_page)
        b.setMaximumWidth(25)
        self._pagepreviewlabel = QtGui.QLabel(self)
        self._pagepreviewlabel.setAlignment(QtCore.Qt.AlignCenter)
        hbox.addWidget(self._pagepreviewlabel)
        b = new_button(">", hbox, self.next_preview_page)
        b.setMaximumWidth(25)
        self._preview_page = 0
        self._pause_updates = False
        self.update_page()

    def pause_page_updates(f):
        """Decorator to temporarily pause preview page updates."""
        def paused_function(self, *args):
            self._pause_updates = True
            f(self, *args)
            self._pause_updates = False
            self.update_page()
        return paused_function
    
        
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

    @pause_page_updates
    def dropEvent(self, event):
        """Process dropped files."""
        self.layout().setCurrentWidget(self.main_UI)
        for url in event.mimeData().urls():
            file = url.toLocalFile()
            if os.path.isfile(file):
                self._add_file(file)
            elif os.path.isdir(file):
                for (path, dirs, files) in os.walk(file):
                    for filename in files:
                        self._add_file(os.path.join(path, filename))
                
    def _add_file(self, file):
        """Attempt to add a single file."""
        try:
            image = Image.open(file)
            image = image.convert("RGBA")
            self.add_image(HexifiedImage(image, os.path.basename(file)[0]))
        except:
            pass
        

    ## Actions & Updates ##

    def __getattr__(self, name):
        """Default separate cwd paths for opening and saving files."""
        if name in ["cwd_open", "cwd_save"]:
            return os.getcwd()
        raise NameError

    def select_images(self):
        """Allow the user to select one or more images to add."""
        files = QtGui.QFileDialog.getOpenFileNames(self,
                                                   "Select Your Image(s)",
                                                   self.cwd_open,
                                                   "Images (*.png *.jpg)")
        for file in files:
            if os.path.isfile(file):
                self.cwd_open = os.path.dirname(file)
                image = Image.open(file)
                image = image.convert("RGBA")
                self.add_image(HexifiedImage(image, os.path.basename(file)[0]))

    def add_image(self, hexed):
        """Add a HexifiedImage to the displayed list and return its widget."""
        widget = HexifiedImageWidget(self.scroller, self, hexed)
        widget.destroyed.connect(self.update_page)
        layout = self.scroller.layout()
        layout.insertWidget(layout.count() - self._confirmed_count - 1, widget)
        self.update_page()
        return widget

    def confirm(self, widget, confirm):
        """Update confirmation status of a HexifiedImageWidget."""
        layout = self.scroller.layout()
        if confirm:
            self._confirmed_count += 1
            layout.insertWidget(layout.count() - self._confirmed_count - 1,
                                widget)
            if self._selected.checkState() == QtCore.Qt.PartiallyChecked:
                widget.selected = False
        else:
            self._confirmed_count -= 1
            layout.insertWidget(0, widget)
            self.scroller.parent().parent().ensureVisible(0, 0)
            if self._selected.checkState() == QtCore.Qt.PartiallyChecked:
                widget.selected = True


    ## Bulk actions ##

    def _get_items(self):
        """Get all HexifiedImageWidgets currently displayed."""
        items = []
        for widget in self.scroller.children():
            if "hexed" in widget.__dict__:
                items.append(widget)
        return items

    def _set_selection_text(self, text):
        """Update button text suffix."""
        self._resize_btn.setText("Resize " + text)
        self._random_btn.setText("Randomize " + text)
        if text == "Selected":
            self._confirm_btn.setText("[Un]confirm " + text)
        else:
            self._confirm_btn.setText("Confirm " + text)
        self._delete_btn.setText("Delete " + text)

    def _select_all(self):
        """Handle a press to the "Select All" checkbox."""
        self._set_selection_text(("Selected", "Unconfirmed", "All")
                                 [self._selected.checkState()])
        if self._pause_selection_watch: return
        self._pause_selection_watch = True
        if self._selected.checkState() == QtCore.Qt.Unchecked:
            for widget in self._get_items():
                widget.selected = False
        elif self._selected.checkState() == QtCore.Qt.PartiallyChecked:
            for widget in self._get_items():
                widget.selected = not widget.confirmed
        else:  # QtCore.Qt.Checked
            for widget in self._get_items():
                widget.selected = True
        self._pause_selection_watch = False

    def selection_changed(self):
        """Note a widget selection change."""
        if self._pause_selection_watch: return
        if self._selected.checkState() != QtCore.Qt.Unchecked:
            self._pause_selection_watch = True
            self._selected.setCheckState(QtCore.Qt.Unchecked)
            self._pause_selection_watch = False

    @pause_page_updates
    def resize_selected(self, *args):
        """Advance each selected item to the next hex size/shape."""
        for widget in self._get_items():
            if widget.selected:
                widget.next_hex_configuration()

    @pause_page_updates
    def randomize_selected(self, *args):
        """Randomize all selected letter labels."""
        for widget in self._get_items():
            if widget.selected:
                widget.randomize_letter()

    @pause_page_updates
    def confirm_selected(self, *args):
        """Confirm all selected items."""
        self._pause_selection_watch = True
        for widget in self._get_items():
            if widget.selected:
                if self._confirm_btn.text() == "Confirm All":
                    if widget.confirmed: continue
                widget.toggle_confirm()
        self._pause_selection_watch = False
        if self._selected.checkState() == QtCore.Qt.PartiallyChecked:
            self._selected.setCheckState(QtCore.Qt.Checked)
        if self._selected.checkState() == QtCore.Qt.Checked:
            if self._confirm_btn.text() == "Unconfirm All":
                self._confirm_btn.setText("Confirm All")
            else:
                self._confirm_btn.setText("Unconfirm All")

    # no @pause_page_updates -- we are deleting LATER anyway
    def delete_selected(self, *args):
        """Remove all selected items."""
        for widget in self._get_items():
            if widget.selected:
                widget.deleteLater()
        self._selected.setCheckState(QtCore.Qt.Unchecked)


    ## Page Preview ##

    def _get_pages(self, hexsize=(300, 300)):
        """Get and populate one or more pages for printing."""
        pages = HexPage.Arrange([i.hexed for i in self._get_items()],
                                hexsize, (10, 10), blanks=True,
                                background=(255, 255, 255, 255))
        if pages == []:
            pages.append(HexPage(hexsize, (10, 10), blanks=True,
                                 background=(255, 255, 255, 255)))
        return pages

    def update_page(self):
        """Update the page preview after a change."""
        if self._pause_updates: return
        self._pages = self._get_pages((32, 32))
        if self._preview_page >= len(self._pages):
            self._preview_page = len(self._pages) - 1
        self._show_page_preview()

    def _show_page_preview(self):
        """Display the selected preview page."""
        image = self._pages[self._preview_page].image
        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(image))
        self._pagepreview.setPixmap(pixmap)
        self._pagepreviewlabel.setText("Page %s of %s"
                                       % (self._preview_page + 1, len(self._pages)))

    def next_preview_page(self):
        """Advance to the next page of the preview."""
        self._preview_page += 1
        if self._preview_page >= len(self._pages):
            self._preview_page = 0
        self._show_page_preview()

    def prev_preview_page(self):
        """Return to the previous page of the preview."""
        self._preview_page -= 1
        if self._preview_page < 0:
            self._preview_page = len(self._pages) - 1
        self._show_page_preview()


    ## Exporting ##

    def export_PNG(self):
        """Export the current page to PNG format."""
        page = self._get_pages()[self._preview_page]
        file = QtGui.QFileDialog.getSaveFileName(self,
                                                 "Save Current Page As...",
                                                 self.cwd_save,
                                                 "Images (*.png *.jpg)")
        if file:
            self.cwd_save = os.path.dirname(file)
            page.image.save(file)

    def export_PDF(self):
        """Export the filled pages to PDF format."""
        file = QtGui.QFileDialog.getSaveFileName(self, "Save All Pages As...",
                                                 self.cwd_save,
                                                 "PDFs (*.pdf)")
        if file:
            self.cwd_save = os.path.dirname(file)
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
        printer.setResolution(300)
        printer.setFullPage(True)
        printer.setPageMargins(.25, .25, .5, .25, QtGui.QPrinter.Inch)
        painter = QtGui.QPainter()
        painter.begin(printer)
        pages = self._get_pages()
        for page in pages[:-1]:
            painter.drawImage(QtCore.QPointF(0, 0),
                              ImageQt.ImageQt(page.image))
            printer.newPage()
        painter.drawImage(QtCore.QPointF(0, 0),
                              ImageQt.ImageQt(pages[-1].image))
        painter.end()
            
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    HexifyWidget().show()
    sys.exit(app.exec_())

