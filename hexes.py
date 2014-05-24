import math
from PIL import Image, ImageDraw, ImageFont


class HexPageOverlapError(Exception):
    """Hexes placed here overlap existing hexes."""
    pass

class HexPageOverflowError(Exception):
    """Hexes placed here fall off the HexPage."""
    pass

class InvalidHexShapeError(Exception):
    """No known hex configuration for this shape at the current size."""
    pass

class InvalidHexSizeError(Exception):
    """No known hex configuration for this size."""
    pass


class HexImagePlacement:

    """Calculate and maintain proper placement for items within hex shape.

    Public attributes:
      image_rect -- rectangle (un-rotated) to hold creature image
      letter_rect -- rectangle (un-rotated) to hold letter
      rotation -- angle of rotation to apply (in degrees)
      offsets_used -- list of two-tuples showing offsets used from the start

    Note that moving horizontally along a row requires a SOUTHEAST move from
    an even column to an odd, and a NORTHEAST move from an odd to an even.
    The starting location is always considered to be an even column.
    """

    def __init__(self, image_rect, rotation, letter_rect, offsets_used):
        self.image_rect = image_rect
        self.rotation = rotation
        self.letter_rect = letter_rect
        self.offsets_used = offsets_used

    def __repr__(self):
        return self.__class__.__name__ + repr((self.image_rect, self.rotation, self.letter_rect))

    def __str__(self):
        return repr(self)


class HexDraw:
    
    """Used to draw hexes, one (color-shaded) side at a time.

    Directional class constants NORTH, NORTHEAST, SOUTHEAST, SOUTH, SOUTHWEST,
    and NORTHWEST available to refer to sides of the final hex.

    Class constants BACK_COLOR, FRONT_COLOR, SIDE_COLOR, BG_COLOR,
    and OUTLINE_COLOR available describing standard colors.

    Class constants SHAPE_LONG, SHAPE_ROUND, SHAPE_WAVY, and SHAPE_CURLY
    available to customize hex configuration.

    Public methods:
      fill(color) -- fill the entire hex area with the given color
      outline(color) -- outline the entire hex in the given color
      side(side, fill, outline) -- color and/or outline one side of the hex
      shade(fronts, sides, backs) -- shade multiple sides at once
      shift(direction, distance) -- move on to an adjacent hex
      measure(size, shape) -- measure a multi-hex area and return its placement
      draw_multi(size, shape) -- draw a multi-hex area and return its placement

    """

    # Side enumeration
    NORTH = 0                           #: directly up
    NORTHEAST = 1                       #: up and to the right
    SOUTHEAST = 2                       #: down and to the right
    SOUTH = 3                           #: directly down
    SOUTHWEST = 4                       #: down and to the left
    NORTHWEST = 5                       #: up and to the left
    EAST = 6                            #: directly right (two columns over)
    WEST = 7                            #: directly left (two columns over)

    # Standard colors
    BACK_COLOR = (255, 100, 100, 255)   #: red shading to a creature's rear
    FRONT_COLOR = (100, 255, 100, 255)  #: green shading in the front hexes
    SIDE_COLOR = (255, 255, 100, 255)   #: yellow shading at each side
    BG_COLOR = (255, 255, 255, 255)     #: solid background inside a hex
    OUTLINE_COLOR = (0, 0, 0, 255)      #: thin outline of the hex shape

    # Multi-hex shape options
    SHAPE_LONG = 0                      #: long and straight
    SHAPE_ROUND = 1                     #: circle-like
    SHAPE_WAVY = 2                      #: back and forth on a semi-line
    SHAPE_CURLY = 3                     #: curl around and up


    ## Basic Geometry Calculations ##

    def __init__(self, draw, rect, bgcolor=None):
        """Do initial geometry calculations, and fill the background.

        Arguments:
          draw -- ImageDraw.Draw object on the Image
          rect -- the rectangle to fill with a hexagon
          bgcolor -- the color (tuple) to fill in (optional)
        """
        self.draw = draw
        self.rect = rect
        self._findcorners()
        if bgcolor is not None:
            self.fill(bgcolor)

    def __repr__(self):
        return self.__class__.__name__ + repr((self.rect,))

    def __str__(self):
        return repr(self)

    def _findcorners(self):
        """Determine the coordinates of all geometric corners."""

        # outer corners
        left, top, right, bottom = self.rect
        width = right - left
        height = bottom - top
        self.NW = (left + int(width/4), top)
        self.NE = (right - int(width/4), top)
        self.W = (left, top + int(height/2))
        self.E = (right, top + int(height/2))
        self.SW = (left + int(width/4), bottom)
        self.SE = (right - int(width/4), bottom)
        self.outer_corners = (self.NW, self.NE, self.E, self.SE,
                              self.SW, self.W, self.NW)

        # inside the shaded rim
        thickness = height / 15
        shift = int(math.tan(math.pi/6) * thickness)
        thickness = int(thickness)
        NW_inner = (self.NW[0] + shift, self.NW[1] + thickness)
        NE_inner = (self.NE[0] - shift, self.NE[1] + thickness)
        SW_inner = (self.SW[0] + shift, self.SW[1] - thickness)
        SE_inner = (self.SE[0] - shift, self.SE[1] - thickness)
        W_inner = (self.W[0] + thickness, self.W[1])
        E_inner = (self.E[0] - thickness, self.E[1])
        self.inner_corners = (NW_inner, NE_inner, E_inner, SE_inner,
                              SW_inner, W_inner, NW_inner)


    ## Low-Level Draw Functions ##
        
    def fill(self, color):
        """Fill the background with the specified RGBA color."""
        self.draw.polygon(self.NW + self.NE + self.E + self.SE + self.SW
                          + self.W, fill=color)

    def outline(self, color):
        """Outline the hex with the specified RGBA color."""
        self.draw.polygon(self.NW + self.NE + self.E + self.SE + self.SW
                          + self.W, outline=color)

    def side(self, side, fill=None, outline=None):
        """Shade and outline a single side of the hex.

        Arguments:
          side -- HexDraw directional variable such as SOUTH or NORTHWEST
          fill -- RGBA color for the shaded border (default: None)
          outline -- RGBA color for the thin outline (default: None)
        """
        if fill is not None:
            self.draw.polygon(self.outer_corners[side]
                              + self.outer_corners[side + 1]
                              + self.inner_corners[side + 1]
                              + self.inner_corners[side],
                              fill=fill)
        if outline is not None:
            self.draw.line(self.outer_corners[side]
                           + self.outer_corners[side + 1],
                           fill=outline)


    ## High-Level Draw with Standard Colors ##
            
    def shade(self, fronts=None, sides=None, backs=None, fill=True, shadow=False):
        """Shade and outline all desired sides at once.

        Arguments:
          fronts -- tuple of HexDraw sides to mark with FRONT_COLOR (optional)
          sides -- tuple of HexDraw sides to mark with SIDE_COLOR (optional)
          backs -- tuple of HexDraw sides to mark with BACK_COLOR (optional)
          fill -- boolean to include drawing the background (default: True)
        """
        if shadow: return  # check once here rather than every call in draw_multi
        if fill:
            self.fill(HexDraw.BG_COLOR)
        if fronts is not None:
            for f in fronts:
                self.side(f, HexDraw.FRONT_COLOR, HexDraw.OUTLINE_COLOR)
        if sides is not None:
            for s in sides:
                self.side(s, HexDraw.SIDE_COLOR, HexDraw.OUTLINE_COLOR)
        if backs is not None:
            for b in backs:
                self.side(b, HexDraw.BACK_COLOR, HexDraw.OUTLINE_COLOR)


    ## Adjust Location for Connected Hexes ##
                
    def _move_down(self, distance):
        """Adjust self.rect down by distance."""
        self.rect = (self.rect[0], self.rect[1] + int(distance),
                     self.rect[2], self.rect[3] + int(distance))

    def _move_right(self, distance):
        """Adjust self.rect right by distance."""
        self.rect = (self.rect[0] + int(distance), self.rect[1],
                     self.rect[2] + int(distance), self.rect[3])
        
    def shift(self, direction, distance=1):
        """Shift to another hex in-pattern.

        Arguments:
          direction -- cardinal direction to shift (e.g. HexDraw.SOUTHWEST)
          distance -- number of hexes to shift (default: 1)
        """
        width, height = self.rect[2] - self.rect[0], self.rect[3] - self.rect[1]
        if direction == HexDraw.NORTH:
            self._move_down(-distance * height)
        elif direction == HexDraw.SOUTH:
            self._move_down(distance * height)
        elif direction == HexDraw.WEST:
            self._move_right(-distance * width * 3 / 2)
        elif direction == HexDraw.EAST:
            self._move_right(distance * width * 3 / 2)
        elif direction == HexDraw.NORTHWEST:
            self._move_down(-distance * height / 2)
            self._move_right(-distance * width * 3 / 4)
        elif direction == HexDraw.NORTHEAST:
            self._move_down(-distance * height / 2)
            self._move_right(distance * width * 3 / 4)
        elif direction == HexDraw.SOUTHWEST:
            self._move_down(distance * height / 2)
            self._move_right(-distance * width * 3 / 4)
        elif direction == HexDraw.SOUTHEAST:
            self._move_down(distance * height / 2)
            self._move_right(distance * width * 3 / 4)
        self._findcorners()


    ## Multi-Hex Draw Operations ##

    def _letterbox(self):
        """Return a suitable letter-box to the right of this hex."""
        left, top, right, bottom = self.rect
        width = right - left
        height = bottom - top
        return (left + int(width * 3 / 5),  # 3/5 across
                top + int(height / 3),      # 1/3 down
                right - int(width / 12),    # intersection w/hex
                bottom - int(height / 3))   # 2/3 down

    def measure(self, size, shape=0, **kwargs):
        """Measure a potential multi-hex here; return its HexImagePlacement."""
        return self.draw_multi(size, shape, shadow=True, **kwargs)

    def draw_multi(self, size, shape=0, **kwargs):
        """Draw a multi-hex area and return its HexImagePlacement.

        The area will be rooted at the current location of the HexDraw.

        Arguments:
          size -- number of hexes to place
          shape -- shape modifier (default: HexDraw.SHAPE_LONG)

        Additional keyword arguments will be passed to the shade function:
          fill -- whether to color the hex backdrop (default: True)
        """
        
        if size == 1:
            """Draw a single hex, facing NORTH."""
            if shape != HexDraw.SHAPE_LONG:
                raise InvalidHexShapeError
            self.shade(fronts=(HexDraw.NORTHWEST, HexDraw.NORTH, HexDraw.NORTHEAST),
                       sides=(HexDraw.SOUTHEAST, HexDraw.SOUTHWEST),
                       backs=(HexDraw.SOUTH,),
                       **kwargs)
            return HexImagePlacement(self.NW + self.SE, 0, self._letterbox(),
                                     [(0,0)])

        elif size == 2:
            """Draw two vertical hexes, facing NORTH."""
            if shape != HexDraw.SHAPE_LONG:
                raise InvalidHexShapeError
            self.shade(fronts=(HexDraw.NORTHWEST, HexDraw.NORTH,
                               HexDraw.NORTHEAST),
                       sides=(HexDraw.SOUTHEAST, HexDraw.SOUTHWEST),
                       backs=None,
                       **kwargs)
            self.shift(HexDraw.SOUTH)
            self.shade(fronts=None,
                       sides=(HexDraw.NORTHWEST, HexDraw.NORTHEAST),
                       backs=(HexDraw.SOUTHWEST, HexDraw.SOUTH,
                              HexDraw.SOUTHEAST),
                       **kwargs)
            bottomright = self.SE
            self.shift(HexDraw.NORTH)
            return HexImagePlacement(self.NW + bottomright, 0,
                                     self._letterbox(), [(0,0), (0,1)])

        elif size == 3:
            if shape == HexDraw.SHAPE_LONG:
                """Draw three vertical hexes, facing NORTH."""
                self.shade(fronts=(HexDraw.NORTHWEST, HexDraw.NORTH,
                                   HexDraw.NORTHEAST),
                           sides=(HexDraw.SOUTHEAST, HexDraw.SOUTHWEST),
                           **kwargs)
                self.shift(HexDraw.SOUTH)
                self.shade(sides=(HexDraw.NORTHWEST, HexDraw.NORTHEAST,
                                  HexDraw.SOUTHWEST, HexDraw.SOUTHEAST),
                           **kwargs)
                self.shift(HexDraw.SOUTH)
                self.shade(sides=(HexDraw.NORTHWEST, HexDraw.NORTHEAST),
                           backs=(HexDraw.SOUTHWEST, HexDraw.SOUTH,
                                  HexDraw.SOUTHEAST),
                           **kwargs)
                bottomright = self.SE
                self.shift(HexDraw.NORTH)
                self.shift(HexDraw.NORTH)
                return HexImagePlacement(self.NW + bottomright, 0,
                                         self._letterbox(),
                                         [(0,0), (0,1), (0,2)])
            elif shape == HexDraw.SHAPE_ROUND:
                """Draw three round hexes, facing NORTHWEST."""
                self.shade(fronts=(HexDraw.NORTHWEST, HexDraw.NORTH, HexDraw.NORTHEAST,
                                   HexDraw.SOUTHWEST),
                           **kwargs)
                self.shift(HexDraw.SOUTHEAST)
                self.shade(sides=(HexDraw.NORTH, HexDraw.NORTHEAST),
                           backs=(HexDraw.SOUTH, HexDraw.SOUTHEAST),
                           **kwargs)
                bottomright = self.SE
                letterbox = self._letterbox()
                self.shift(HexDraw.SOUTHWEST)
                self.shade(sides=(HexDraw.NORTHWEST, HexDraw.SOUTHWEST),
                           backs=(HexDraw.SOUTH, HexDraw.SOUTHEAST),
                           **kwargs)
                self.shift(HexDraw.NORTH)
                return HexImagePlacement(self.W + bottomright, 30, letterbox,
                                         [(0,0), (1,0), (0,1)])
            
            else:
                raise InvalidHexShapeError

        else:
            raise InvalidHexSizeError
                        
                        

class HexPage:

    """Manages an Image consisting of a page of hex creatures.

    Methods:
      used -- return a boolean: is there something here already?
      place -- place a hex shape at a specific location
      add -- place a hex shape at the next available location
      arrange -- place a list of HexifiedImages intelligently

    Attributes:
      image -- the page Image so far
      size -- number of (rows, columns) on the page
      hexsize -- number of pixels (x, y) in each hex's bounding box
    """

    BG_COLOR = (200, 200, 200, 0)
    """The background fill for the page."""

    def Arrange(items, *args, **kwargs):
        """Arrange HexifiedImage items on one or more pages.

        Arguments:
          items -- list of HexifiedImages to place
        Additional arguments will be passed to each HexPage instance.

        Return value:
          list of HexPages containing the items

        Raises HexPageOverflowError if there is an item that -- on its own --
        will not fit on a HexPage of the given size.
        """
        pages = []
        last_items = items
        while items:
            page = HexPage(*args, **kwargs)
            items = page.arrange(items)
            if items == last_items:
                raise HexPageOverflowError  # item(s) won't fit at all
            last_items = items
            pages.append(page)
        return pages

    def __init__(self, hexsize=(180, 180), pagesize=(11, 13), blanks=False, background=BG_COLOR):
        """Create a blank hex grid.

        Arguments:
          hexsize -- size of a single hex's bounding box in pixels (x, y)
          pagesize -- number of (rows, columns) on the page
          blanks -- if True, first fill page with empty hexes (default: False)
          background -- RGBA color to fill the page (default: HexPage.BG_COLOR)
        """
        self.hexsize = hexsize
        self.size = pagesize
        self.image = Image.new(
                    "RGBA",
                    (int(hexsize[0] + hexsize[0] * (pagesize[0] - 1) * 3 / 4),
                     hexsize[1] * pagesize[1] + int(hexsize[1] / 2)),
                    background)
        self.draw = ImageDraw.Draw(self.image)
        self.filled = [[False,] * pagesize[1] for i in range(pagesize[0])]
        if blanks:
            self._drawpage()
        self.next_hex = (0, 0)

    def __repr__(self):
        return self.__class__.__name__ + repr((self.hexsize, self.size))

    def __str__(self):
        return repr(self)

    def _drawpage(self):
        """Shade the entire grid in empty one-hex bits."""
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                self._gethexdraw((row,col)).draw_multi(1)

    def _gethexdraw(self, target):
        """Return a HexDraw instance at the given grid location."""
        left = int(self.hexsize[0] * target[0] * 3 / 4)
        top = self.hexsize[1] * target[1]
        if (target[0] % 2):
            top += int(self.hexsize[1] / 2)
        return HexDraw(self.draw,
                       (left, top,
                        left + self.hexsize[0], top + self.hexsize[1]))

    def used(self, target, shift=(0,0)):
        """Return boolean indicating if the target hex is occupied."""
        try:
            return self.filled[target[0] + shift[0]][target[1] + shift[1]]
        except IndexError:
            pass #raise HexPageOverflowError
        raise HexPageOverflowError

    def _mark(self, target, offsets=[(0,0)]):
        """Mark the given grid location used, atomically."""
        for shift in offsets:
            if self.used(target, shift):
                raise HexPageOverlapError
        for shift in offsets:
            self.filled[target[0] + shift[0]][target[1] + shift[1]] = True
        
    def _resize(self, image, imagesize, targetbox):
        """Return a copy of image, resized to fix into targetbox."""
        imagewidth = imagesize[0]
        imageheight = imagesize[1]
        targetwidth = targetbox[2] - targetbox[0]
        targetheight = targetbox[3] - targetbox[1]
        if imagewidth < targetwidth and imageheight < targetheight:
            factor = targetwidth / imagewidth
            hfactor = targetheight / imageheight
            if hfactor < factor:
                factor = hfactor
            imagewidth *= factor
            imageheight *= factor
        if imagewidth > targetwidth:
            factor = targetwidth / imagewidth
            imagewidth *= factor
            imageheight *= factor
        if imageheight > targetheight:
            factor = targetheight / imageheight
            imagewidth *= factor
            imageheight *= factor
        return image.resize((int(imagewidth), int(imageheight)))

    def _center(self, imagesize, targetbox):
        """Return a copy of targetbox, resized to fit imagesize centered within."""
        imagewidth = imagesize[0]
        imageheight = imagesize[1]
        targetwidth = targetbox[2] - targetbox[0]
        targetheight = targetbox[3] - targetbox[1]
        if targetwidth != imagewidth:
            left = targetbox[0] + int((targetwidth - imagewidth) / 2)
            targetbox = (left, targetbox[1], left + imagewidth, targetbox[3])
        if targetheight != imageheight:
            top = targetbox[1] + int((targetheight - imageheight) / 2)
            targetbox = (targetbox[0], top, targetbox[2], top + imageheight)
        return targetbox

    def _place(self, loc, image=None, letter=None, letterfill=(0, 0, 0, 255)):
        """Place the image and/or letter according to the HexImagePlacement."""
        if image is not None:
            if image.mode != "RGBA":
                image = image.convert("RGBA")
            imagebox = image.getbbox()
            if imagebox is not None:
                image = image.crop(imagebox)
                targetbox = loc.image_rect
                image = self._resize(image, image.size, targetbox)
                targetbox = self._center(image.size, targetbox)
                if (loc.rotation != 0):
                    image = image.rotate(loc.rotation, expand=True)
                    targetbox = self._center(image.size, targetbox)
                self.image.paste(image, targetbox, image)
        if letter is not None:
            def _fontsize(font, letter):
                size = font.getsize(letter)
                off = font.getoffset(letter)
                return (size[0] + off[0], size[1] + off[1])
            fontsize = 14
            font = ImageFont.truetype("arial.ttf", fontsize)
            fontboxsize = _fontsize(font, letter)
            target_width = loc.letter_rect[2] - loc.letter_rect[0]
            target_height = loc.letter_rect[3] - loc.letter_rect[1]
            while (fontboxsize[0] < target_width * 3 / 4 and
                   fontboxsize[1] < target_height * 3 / 4):
                fontsize += 1
                font = ImageFont.truetype("arial.ttf", fontsize)
                fontboxsize = _fontsize(font, letter)
            while (fontboxsize[0] > target_width or
                   fontboxsize[1] > target_height):
                fontsize -= 1
                if fontsize < 6:
                    fontsize = 6
                    break
                font = ImageFont.truetype("arial.ttf", fontsize)
                fontboxsize = _fontsize(font, letter)
            targetbox = self._center(fontboxsize, loc.letter_rect)
            if loc.rotation != 0:
                letterimage = Image.new("RGBA", fontboxsize, (0, 0, 0, 0))
                letterdraw = ImageDraw.Draw(letterimage)
                letterdraw.text((0,0), letter, font=font, fill=letterfill)
                letterimage = letterimage.rotate(loc.rotation, expand=True)
                targetbox = self._center(letterimage.size, targetbox)
                self.image.paste(letterimage, targetbox, letterimage)
            else:
                self.draw.text((targetbox[0], targetbox[1]), letter,
                               font=font, fill=letterfill)

    def place(self, target, size, shape=HexDraw.SHAPE_LONG,
              image=None, letter=None, letterfill=(0, 0, 0, 255)):
        """Place a multi-hex at the given location.

        Arguments:
          target -- (row, column) to place the root hex
          size -- number of total hexes to place
          shape -- special shape type (default: HexDraw.SHAPE_LONG)
          image -- character image to place on multi-hex (default: None)
          letter -- string to place over the character image (default: None)
          letterfill -- RGBA color of letter (default: black)
        """
        _hex = self._gethexdraw(target)
        loc = _hex.measure(size, shape)
        self._mark(target, loc.offsets_used)  # raises HexOver*Error
        _hex.draw_multi(size, shape)
        self._place(loc, image, letter, letterfill)

    def _increment(self, next_hex):
        next_hex = (next_hex[0] + 1, next_hex[1])
        if next_hex[0] >= self.size[0]:
            next_hex = (0, next_hex[1] + 1)
            if next_hex[1] >= self.size[1]:
                raise HexPageOverflowError
        return next_hex
                
    def _next_available(self, next_hex):
        while self.used(next_hex):
            next_hex = self._increment(next_hex)
        return next_hex

    def add(self, size, shape=HexDraw.SHAPE_LONG,
            image=None, letter=None, letterfill=(0, 0, 0, 255)):
        """Place a multi-hex at the next available location.

        Arguments:
          size -- number of total hexes to place
          shape -- special shape type (default: HexDraw.SHAPE_LONG)
          image -- character image to place on multi-hex (default: None)
          letter -- string to place over the character image (default: None)
          letterfill -- RGBA color of letter (default: black)

        Return value: chosen grid location for root hex

        Naive algorithm, uses a greedy approach to add shapes one at a time.
        """
        next_hex = self.next_hex
        while True:
            try:
                self.place(next_hex, size, shape, image, letter, letterfill)
            except (HexPageOverlapError, HexPageOverflowError):
                next_hex = self._next_available(self._increment(next_hex))
            else:
                try:
                    self.next_hex = self._next_available(self.next_hex)
                except HexPageOverflowError:
                    pass
                return next_hex

    def arrange(self, images):
        """Attempt to place a list of HexifiedImages on the page.
        Return a list of any images that didn't fit."""
        extras = []
        for i in sorted(images, reverse=True):
            try:
                self.add(i.size, i.shape, i.image, i.letter)
            except HexPageOverflowError:
                extras.append(i)
        return extras


class HexifiedImage:

    """A single hexified image, ready for placement on a page."""

    def __init__(self, image, letter, size=1, shape=HexDraw.SHAPE_LONG):
        self.image = image
        self.letter = letter
        self.size = size
        self.shape = shape
        self.preview  # validate

    def __lt__(self, other):
        """Sort by size (then by shape)."""
        if self.size == other.size:
            return self.shape < other.shape
        return self.size < other.size

    def __eq__(self, other):
        """Compare critical attributes."""
        try:
            return self._get_crits() == other._get_crits()
        except AttributeError:
            return False

    def __repr__(self):
        return self.__class__.__name__ + repr((self.image, self.letter, self.size, self.shape))

    def __str__(self):
        return repr(self)

    def _get_crits(self):
        """Return a tuple of all critical attributes."""
        image = self.image
        if image is not None:
            image = image.histogram()
        return (image, self.letter, self.size, self.shape)

    def __getattr__(self, name):
        """Re-generate preview with each access (if needed)."""
        if name == "preview":
            self.preview = self._create_preview()
            return self.preview
        elif name == "fontpreview":
            self.fontpreview = self._create_font_preview()
            return self.fontpreview
        raise NameError

    def __setattr__(self, name, value):
        """Mark the saved preview out of date when inputs change."""
        if (name in ["size", "shape", "image", "letter"]):
            try:
                del self.__dict__["preview"]
            except KeyError:
                pass
        if (name in ["letter"]):
            try:
                del self.__dict__["fontpreview"]
            except KeyError:
                pass
        object.__setattr__(self, name, value)

    def _create_preview(self):
        """Generate and return a preview image."""
        page = HexPage((64, 64), (self.size, self.size), background=(0,0,0,0))
        try:
            page.place((0,0), self.size, self.shape, self.image, self.letter)
        except InvalidHexSizeError:
            if self.size < 1:
                self.size = 1
            else:
                self.size -= 1
            return self._create_preview()
        except InvalidHexShapeError:
            self.shape += 1
            if self.shape > HexDraw.SHAPE_CURLY:
                self.shape = HexDraw.SHAPE_LONG
            return self._create_preview()
        return page.image.crop(page.image.getbbox())

    def _create_font_preview(self, fontsize=112, color=(0, 0, 0, 255)):
        """Generate and return a simple letter image."""
        font = ImageFont.truetype("arial.ttf", fontsize)
        size = font.getsize(self.letter)
        offset = font.getoffset(self.letter)
        image = Image.new("RGBA", (size[0] + offset[0], size[1] + offset[1]))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), self.letter, font=font, fill=color)
        return image.crop(image.getbbox())

