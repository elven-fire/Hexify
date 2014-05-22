import math
from PIL import Image, ImageDraw, ImageFont


class HexPageOverlapError(Exception):
    pass

class InvalidHexShapeError(Exception):
    pass

class InvalidHexSizeError(Exception):
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

    Directional (static)S variables NORTH, NORTHEAST, SOUTHEAST, SOUTH, SOUTHWEST,
    and NORTHWEST available to refer to sides of the final hex.

    Static variables BACK_COLOR, FRONT_COLOR, SIDE_COLOR, BG_COLOR,
    and OUTLINE_COLOR available describing standard colors.

    Public methods:
      fill(color) -- fill the entire hex area with the given color
      outline(color) -- outline the entire hex in the given color
      side(side, fill, outline) -- color and/or outline one side of the hex
      shade(fronts, sides, backs) -- shade multiple sides at once
      shift(direction, distance) -- move on to an adjacent hex
      draw_multi(size, shape) -- draw a multi-hex area and return its placement

    """

    # Side enumeration
    NORTH = 0
    NORTHEAST = 1
    SOUTHEAST = 2
    SOUTH = 3
    SOUTHWEST = 4
    NORTHWEST = 5
    EAST = 6  #: directly right (two columns over)
    WEST = 7  #: directly left (two columns over)

    # Standard colors
    BACK_COLOR = (255, 100, 100, 100)
    FRONT_COLOR = (100, 255, 100, 100)
    SIDE_COLOR = (255, 255, 100, 100)
    BG_COLOR = (255, 255, 255, 0)
    OUTLINE_COLOR = (0, 0, 0, 0)

    # Multi-hex shape options
    SHAPE_LONG = 0
    SHAPE_ROUND = 1
    SHAPE_WAVY = 2
    SHAPE_CURLY = 3


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
            
    def shade(self, fronts=None, sides=None, backs=None, fill=True):
        """Shade and outline all desired sides at once.

        Arguments:
          fronts -- tuple of HexDraw sides to mark with FRONT_COLOR (optional)
          sides -- tuple of HexDraw sides to mark with SIDE_COLOR (optional)
          backs -- tuple of HexDraw sides to mark with BACK_COLOR (optional)
          fill -- boolean to include drawing the background (default: True)
        """
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

    def draw_multi(self, size, shape=0, **kwargs):
        """Draw a multi-hex area and return its HexImagePlacement.

        The area will be rooted at the current location of the HexDraw.

        Arguments:
          size -- number of hexes to place
          shape -- shape modifier (default: HexDraw.SHAPE_LONG)

        Additional keyword arguments will be passed to the shade function:
          fill -- whether to color the hex backdrop (default: True)

        This is a lazy function, and may move the HexDraw incidental to the
        draw operation.
        """
        
        if size == 1:
            """Draw a single hex, facing NORTH."""
            self.shade(fronts=(HexDraw.NORTHWEST, HexDraw.NORTH, HexDraw.NORTHEAST),
                       sides=(HexDraw.SOUTHEAST, HexDraw.SOUTHWEST),
                       backs=(HexDraw.SOUTH,),
                       **kwargs)
            return HexImagePlacement(self.NW + self.SE, 0, self._letterbox(),
                                     [(0,0)])

        elif size == 2:
            """Draw two vertical hexes, facing NORTH."""
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

    """Manages an Image consisting of a page of hex creatures."""

    BG_COLOR = (200, 200, 200, 255)

    def __init__(self, hexsize=(180, 180), pagesize=(11, 13), blanks=False):
        """Create a blank hex grid.

        Arguments:
          hexsize -- size of a single hex's bounding box in pixels (x, y)
          pagesize -- number of (rows, columns) on the page
          blanks -- if True, first fill page with empty hexes (default: False)
        """
        self.hexsize = hexsize
        self.size = pagesize
        self.image = Image.new(
                    "RGBA",
                    (int(hexsize[0] + hexsize[0] * (pagesize[0] - 1) * 3 / 4),
                     hexsize[1] * pagesize[1] + int(hexsize[1] / 2)),
                    HexPage.BG_COLOR)
        self.draw = ImageDraw.Draw(self.image)
        self.filled = [[False,] * pagesize[1] for i in range(pagesize[0])]
        if blanks:
            self._drawpage()

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

    def _mark(self, target, shift=(0,0)):
        """Mark the given grid location used."""
        try:
            if self.filled[target[0] + shift[0]][target[1] + shift[1]]:
                raise HexPageOverlapError
        except HexPageOverlapError:
            raise
        except IndexError:
            raise HexPageOverlapError
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
            fontsize = 14
            font = ImageFont.truetype("arial.ttf", fontsize)
            fontboxsize = self.draw.textsize(letter, font=font)
            target_width = loc.letter_rect[2] - loc.letter_rect[0]
            target_height = loc.letter_rect[3] - loc.letter_rect[1]
            while (fontboxsize[0] < target_width * 3 / 4 and
                   fontboxsize[1] < target_height * 3 / 4):
                fontsize += 1
                font = ImageFont.truetype("arial.ttf", fontsize)
                fontboxsize = self.draw.textsize(letter, font=font)
            while (fontboxsize[0] > target_width or
                   fontboxsize[1] > target_height):
                fontsize -= 1
                if fontsize < 6:
                    fontsize = 6
                    break
                font = ImageFont.truetype("arial.ttf", fontsize)
                fontboxsize = self.draw.textsize(letter, font=font)
            fontboxsize = (fontboxsize[0]+10, fontboxsize[1]+10)
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
        loc = _hex.draw_multi(size, shape)
        for shift in loc.offsets_used:
            self._mark(target, shift)
        self._place(loc, image, letter, letterfill)
