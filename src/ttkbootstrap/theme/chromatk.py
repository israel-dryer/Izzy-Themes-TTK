from PIL import Image
from PIL.ImageTk import PhotoImage
from ttkbootstrap.theme.engine import ThemeEngine, image_draw, image_resize
from ttkbootstrap.constants import *
from ttkbootstrap.style.element import ElementLayout as Element
from tkinter.font import Font

# TODO standardize focus effects on elements
# TODO define and create chevron element once in setup script
# TODO remove builder methods from Style class and implement in Engine
# TODO vertical scrollbar sizing is slower than desired
# TODO create both inline and compact spinbox styles, inline only currently

"""
    Making smooth edges using pillow is know problem. The only way to do
    this currently is to make the image large and then resize using anti-
    aliasing. This is a bit awkward, but it works for now until they can
    improve the api in this regard.  
"""


MINIMUM_WIDTH = 140  # pixels

# button style constants
BTN_BUILD_SIZE = 1000, 1000
BTN_FINAL_SIZE = 500, 500
BTN_OUTLINE_WIDTH = 2
BTN_BUILD_RADIUS = 4
BTN_BORDER_RECT = (1, 1, BTN_BUILD_SIZE[0]-2, BTN_BUILD_SIZE[0]-2)
BTN_PADDING = 12, 4

# radiobutton and checkbutton style constants
CB_BUILD_SIZE = 640, 640
CB_FINAL_SIZE = 28, 28
CB_BORDER_WIDTH = 24
CB_BUILD_RADIUS = 76
CB_OUTLINE_WIDTH = 24
CB_LINE_WIDTH = 40
CB_CHECK_RECT = 190, 330, 293, 433, 516, 210
CB_DASH_RECT = 213, 320, 427, 320
CB_BORDER_RECT = (1, 1, CB_BUILD_SIZE[0]-2, CB_BUILD_SIZE[0]-2)
RB_OUTER_WIDTH = 3
RB_INNER_WIDTH_1 = 140
RB_INNER_WIDTH_2 = 110

# switch style constants
SW_BUILD_SIZE = 1200, 600
SW_FINAL_SIZE = 56, 28
SW_INNER_WIDTH_N = 80
SW_INNER_WIDTH_H = 60
SW_INNER_RADIUS = 290
SW_INNER_RECT = 622, 34, 1166, 566
SW_OUTER_WIDTH_1 = 24
SW_OUTER_WIDTH_2 = 6
SW_OUTER_RADIUS = 300
SW_OUTER_RECT = 10, 10, 1190, 590
SW_PRESS_RECT = 500, 34, 1100, 566

# scrollbar sizes
SB_BUILD_SIZE = 2000, 500
SB_FINAL_SIZE = 1000, 250
SB_BUILD_RADIUS = 10
SB_LINE_RECT = 8, 249, 1991, 249
SB_THUMB_RECT = (1, 1, SB_BUILD_SIZE[0]-2, SB_BUILD_SIZE[1]-2)
SB_TROUGH_OUTLINE_WIDTH = 2
SB_TROUGH_RECT = (1, 1, SB_BUILD_SIZE[0]-2, SB_BUILD_SIZE[1]-2)
SB_RESTING_WIDTH = 485
SB_TROUGH_PAD = 5

# entry sizes
ENTRY_BUILD_SIZE = 1000, 1000
ENTRY_FINAL_SIZE = 500, 500
ENTRY_OUTLINE_WIDTH = 2
ENTRY_BUILD_RADIUS = 6
ENTRY_LINE_RECT = 4, 996, 995, 996
ENTRY_UNDERLINE_WIDTH = 1
ENTRY_UNDERLINE_HOVER_WIDTH = 1
ENTRY_UNDERLINE_FOCUS_WIDTH = 4
ENTRY_PADDING = 12, 4
ENTRY_BORDER_RECT = (1, 1, ENTRY_BUILD_SIZE[0]-2, ENTRY_BUILD_SIZE[0]-2)

# chevron sizes
CHEVRON_BUILD_SIZE = 1400, 755
CHEVRON_FINAL_SIZE = 18, 9
CHEVRON_LINE_WIDTH = 100
CHEVRON_LINE_PRESSED_WIDTH = 200
CHEVRON_LINE_RECT = 20, 20, 735, 735, 700, 700, 1380, 20

# paned window sizes
PW_SASH_THICKNESS = 2

# separator sizes
SEP_BUILD_SIZE = 1000, 1
SEP_LINE_WIDTH = 1


class ChromatkEngine(ThemeEngine):

    def __init__(self, style):
        super().__init__('chromatk', 'default', style)
        self.use_rgba = False
        self.create_named_fonts()
        self.register_keywords()
        self.miscellaneous_setup()

    def miscellaneous_setup(self):
        # set default font for all widgets that are not style configurable
        self.style.tk.call('option', 'add', '*font', 'TkBody')
        # set default font for all style configurable widgets
        self.configure(".", font="TkBody")

    def register_keywords(self):
        self.handler_set('button', self.create_button_style)
        self.handler_set('outline-button', self.create_outline_button_style)
        self.handler_set('link-button', self.create_link_button_style)
        self.handler_set('frame', self.create_frame_style)
        self.handler_set('label', self.create_label_style)
        self.handler_set('inverse-label', self.create_inverse_label_style)
        self.handler_set('labelframe', self.create_labelframe_style)
        self.handler_set('separator', self.create_separator_style)
        self.handler_set('entry', self.create_entry_style)
        self.handler_set('combobox', self.create_combobox_style)
        self.handler_set('spinbox', self.create_spinbox_style)
        self.handler_set('menubutton', self.create_menubutton_style)
        self.handler_set('notebook', self.create_notebook_style)
        self.handler_set('panedwindow', self.create_panedwindow_style)
        self.handler_set('progressbar', self.create_progressbar_style)
        self.handler_set('scale', self.create_scale_style)
        self.handler_set('sizegrip', self.create_sizegrip_style)
        self.handler_set('checkbutton', self.create_checkbutton_style)
        self.handler_set('radiobutton', self.create_radiobutton_style)
        self.handler_set('switch', self.create_switch_style)
        self.handler_set('scrollbar', self.create_scrollbar_style)
        self.handler_set('tk-tk', self.create_window_style)
        self.handler_set('tk-combobox-popdown',
                         self.create_combobox_popdown_style)
        self.handler_set('outline-menubutton',
                         self.create_outline_menubutton_style)

    def create_named_fonts(self):
        """Create the named fonts used by this theme engine
        The font size is measured in pixels and is scaled to fit the
        screen so that the proportions are similar from computer to computer.
        https://learn.microsoft.com/en-us/windows/apps/design/style/xaml-theme-resources#the-xaml-type-ramp
        """
        scaling_factor = 1.4

        def s(x):
            return self.scale_size(-x * scaling_factor)

        self.register_assets(
            'fonts',
            Font(name='TkCaption', family='Segoe UI', size=10),
            Font(name='TkBody', family='Segoe UI', size=12),
            Font(name='TkBodyStrong', family='Segoe UI Semibold', size=12),
            Font(name='TkBodyLarge', family='Segoe UI', size=16),
            Font(name='TkSubtitle', family='Segoe UI Semibold', size=18),
            Font(name='TkTitle', family='Segoe UI Semibold', size=26),
            Font(name='TkTitleLarge', family='Segoe UI Semibold', size=36),
            Font(name='TkDisplay', family='Segoe UI Semibold', size=60))

    def create_window_style(self, options):
        """Style the application main window"""
        scheme = options['scheme']
        colorname = 'background'
        background = scheme.get_color(colorname)

        # set the application window style
        window = options['widget']
        window.configure(background=background)

        # default global ttk styles for theme
        self.configure('.', font='TkBody', background=background,
                       darkcolor=background, foreground=scheme.foreground,
                       troughcolor=background, selectbg=scheme.info,
                       selectfg=background, fieldbg=background, borderwidth=1)

    def create_button_style(self, options):
        """Create the default button style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        foreground = scheme.get_foreground(colorname)
        background = accents.accent
        hover = accents.light1 if scheme.is_light else accents.dark1
        pressed = accents.light2 if scheme.is_light else accents.dark1
        disabled = accents.light2

        # create style assets
        common = {'xy': BTN_BORDER_RECT, 'radius': BTN_BUILD_RADIUS,
                  'outline': accents.dark1, 'width': BTN_OUTLINE_WIDTH}

        if self.use_rgba:
            draw_settings = (BTN_BUILD_SIZE,)
        else:
            draw_settings = (BTN_BUILD_SIZE, 'RGB', scheme.background)

        # normal image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, fill=background)
        img_norm = image_resize(im, BTN_FINAL_SIZE)

        # hover image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, fill=hover)
        img_hover = image_resize(im, BTN_FINAL_SIZE)

        # pressed image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, fill=pressed)
        img_pressed = image_resize(im, BTN_FINAL_SIZE)

        self.register_assets(scheme.name, img_norm, img_hover, img_pressed)

        # element image
        e_name = f'{ttkstyle}.button'
        elem = self.element_builder(e_name, img_norm, sticky=NSEW,
                                    width=MINIMUM_WIDTH, height=0,
                                    border=BTN_BUILD_RADIUS)
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # widget layout
        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element(e_name), [
                Element('Button.padding'), [
                    Element('Button.label', side=LEFT, expand=True)]]])

        # widget properties
        self.configure(ttkstyle, foreground=foreground, focuscolor=foreground,
                       relief=RAISED, anchor=CENTER, padding=BTN_PADDING)

        # widget state properties
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])
        self.map(ttkstyle, 'shiftrelief', [('pressed !disabled', -1)])

    def create_outline_button_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_lt = scheme.accents(LIGHT)
        accents_bg = scheme.accents('background')
        disabled = accents_lt.dark1 if scheme.is_light else accents_lt.dark4
        background = foreground = accents.accent
        hover_bg = accents_bg.light1 if scheme.is_dark else accents_lt.accent

        # create style assets
        common = {'xy': BTN_BORDER_RECT, 'radius': BTN_BUILD_RADIUS}

        if self.use_rgba:
            draw_settings = (BTN_BUILD_SIZE,)
        else:
            draw_settings = (BTN_BUILD_SIZE, 'RGB', scheme.background)

        # normal image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background, width=2)
        img_norm = image_resize(im, BTN_FINAL_SIZE)

        # hover image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background, width=3,
                               fill=hover_bg)
        img_hover = image_resize(im, BTN_FINAL_SIZE)

        # pressed image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background, width=3,
                               fill=hover_bg)
        img_pressed = image_resize(im, BTN_FINAL_SIZE)

        # disable image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=disabled, width=2)
        img_disabled = image_resize(im, BTN_FINAL_SIZE)

        self.register_assets(scheme.name, img_norm, img_hover, img_pressed,
                             img_disabled)

        # button image element
        e_name = f'{ttkstyle}.button'
        elem = self.element_builder(e_name, img_norm, sticky=NSEW, height=0,
                                    width=MINIMUM_WIDTH,
                                    border=BTN_BUILD_RADIUS)
        elem.map('disabled', img_disabled)
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # button layout
        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element(e_name, sticky=NSEW), [
                Element('Button.padding'), [
                    Element('Button.label', side=LEFT, expand=True)]]])

        # normal state
        self.configure(ttkstyle, foreground=foreground, anchor=CENTER,
                       padding=BTN_PADDING)

        # state map
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])
        self.map(ttkstyle, 'shiftrelief', [('pressed !disabled', -1)])

    def create_link_button_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents_lt = scheme.accents(LIGHT)
        disabled = accents_lt.dark1 if scheme.is_light else accents_lt.dark4
        foreground = scheme.get_color(colorname)
        hover = scheme.info

        # normal state
        self.configure(ttkstyle, relief=RAISED, foreground=foreground,
                       borderwidth=0, anchor=CENTER, padding=BTN_PADDING)

        # button layout
        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element('Label.border'), [
                Element('Label.padding'), [
                    Element('Button.label', side=LEFT, expand=True)]]])

        # state style maps
        self.map(ttkstyle, 'foreground', [('disabled', disabled),
                                          ('hover !disabled', hover)])
        self.map(ttkstyle, 'shiftrelief', [('pressed !disabled', '-2')])
        self.map(ttkstyle, 'focuscolor', [('hover', hover)])

    def create_checkbutton_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_lt = scheme.accents(LIGHT)
        accents_bg = scheme.accents('background')
        foreground = scheme.background
        background = accents.accent
        app_bg = scheme.background
        disabled = accents_lt.dark1 if scheme.is_light else accents_lt.dark4
        outline = accents_lt.dark3 if scheme.is_dark else accents_lt.dark3
        hover_on = accents.light1 if scheme.is_light else accents.dark1
        hover_off = accents_bg.light1 if scheme.is_dark else accents_lt.accent
        pressed_off = accents_bg.light2 if scheme.is_dark else accents_lt.dark1
        pressed_on = accents.light2 if scheme.is_light else accents.dark1

        # create style assets
        off_common = {'xy': CB_BORDER_RECT, 'radius': CB_BUILD_RADIUS,
                      'width': CB_BORDER_WIDTH, 'outline': outline}

        on_common = {'xy': CB_BORDER_RECT, 'radius': CB_BUILD_RADIUS,
                     'width': 3, 'outline': accents_bg.dark1}

        on_line_common = {'xy': CB_CHECK_RECT, 'width': CB_LINE_WIDTH,
                          'fill': foreground, 'joint': 'curve'}

        alt_line_common = {'xy': CB_DASH_RECT, 'width': CB_LINE_WIDTH,
                           'fill': foreground}

        if self.use_rgba:
            draw_settings = (CB_BUILD_SIZE,)
        else:
            draw_settings = (CB_BUILD_SIZE, 'RGB', scheme.background)

        # off image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**off_common, fill=app_bg)
        img_off = image_resize(im, CB_FINAL_SIZE)

        # off/hover image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**off_common, fill=hover_off)
        img_off_hover = image_resize(im, CB_FINAL_SIZE)

        # off/pressed image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**off_common, fill=pressed_off)
        img_off_pressed = image_resize(im, CB_FINAL_SIZE)

        # on image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**on_common, fill=background)
        draw.line(**on_line_common)
        img_on = image_resize(im, CB_FINAL_SIZE)

        # on/hover
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**on_common, fill=hover_on)
        draw.line(**on_line_common)
        img_on_hover = image_resize(im, CB_FINAL_SIZE)

        # on/pressed
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**on_common, fill=pressed_on)
        draw.line(**on_line_common)
        img_on_pressed = image_resize(im, CB_FINAL_SIZE)

        # on/disabled
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**on_common, fill=background)
        draw.line(CB_CHECK_RECT, disabled, CB_LINE_WIDTH, 'curve')
        img_on_dis = image_resize(im, CB_FINAL_SIZE)

        # alt normal
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**on_common, fill=background)
        draw.line(**alt_line_common)
        img_alt = image_resize(im, CB_FINAL_SIZE)

        # alt pressed
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**on_common, fill=pressed_on)
        draw.line(**alt_line_common)
        img_alt_pressed = image_resize(im, CB_FINAL_SIZE)

        # alt hover
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**on_common, fill=hover_on)
        draw.line(**alt_line_common)
        img_alt_hover = image_resize(im, CB_FINAL_SIZE)

        # alt/disabled
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(CB_BORDER_RECT, radius=CB_BUILD_RADIUS,
                               outline=disabled, fill=background, width=3)
        draw.line(CB_DASH_RECT, width=CB_LINE_WIDTH, fill=disabled)
        img_alt_dis = image_resize(im, CB_FINAL_SIZE)

        # disabled
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(CB_BORDER_RECT, radius=CB_BUILD_RADIUS,
                               outline=disabled, fill=foreground, width=12)
        img_dis = image_resize(im, CB_FINAL_SIZE)

        # create image element
        indicator = ttkstyle.replace('.TC', '.C') + '.indicator'
        elem = self.element_builder(indicator, img_on, width=34, sticky=W)
        elem.map('disabled selected', img_on_dis)
        elem.map('disabled alternate', img_alt_dis)
        elem.map('disabled', img_dis)
        elem.map('pressed alternate !disabled', img_alt_pressed)
        elem.map('pressed !selected !disabled', img_off_pressed)
        elem.map('pressed selected !disabled', img_on_pressed)
        elem.map('hover alternate !disabled', img_alt_hover)
        elem.map('hover !selected !disabled', img_off_hover)
        elem.map('hover selected !disabled', img_on_hover)
        elem.map('alternate', img_alt)
        elem.map('!selected', img_off)
        elem.build()

        # register theme assets to prevent GC
        self.register_assets(scheme.name, img_on, img_on_dis, img_alt_dis,
                             img_dis, img_alt_pressed, img_off_pressed,
                             img_on_pressed, img_alt_hover, img_off_hover,
                             img_on_hover, img_alt, img_off)

        # normal state style
        self.configure(ttkstyle, foreground=scheme.foreground,
                       background=scheme.background, focuscolor='',
                       padding=BTN_PADDING)

        # state mapping
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])

        # style layout
        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element('Checkbutton.button'), [
                Element('Checkbutton.padding'), [
                    Element(indicator, side=LEFT, sticky=''),
                    Element('Checkbutton.label', side=RIGHT, expand=True)]]])

    def create_radiobutton_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_lt = scheme.accents(LIGHT)
        accents_bg = scheme.accents('background')
        app_bg = scheme.background
        background = accents.accent
        disabled = accents_lt.dark1 if scheme.is_light else accents_lt.dark4
        outline = accents_lt.dark3
        hover_on = accents.light1 if scheme.is_light else accents.dark1
        hover_off = accents_bg.light1 if scheme.is_dark else accents_lt.accent
        pressed_on = accents.light2 if scheme.is_light else accents.dark1

        # create radiobutton assets
        if self.use_rgba:
            draw_settings = (CB_BUILD_SIZE,)
        else:
            draw_settings = (CB_BUILD_SIZE, 'RGB', scheme.background)

        off_common = {'xy': CB_BORDER_RECT, 'outline': outline}

        # off image
        im, draw = image_draw(*draw_settings)
        draw.ellipse(**off_common, fill=app_bg, width=CB_OUTLINE_WIDTH)
        img_off = image_resize(im, CB_FINAL_SIZE)

        # off/hover
        im, draw = image_draw(*draw_settings)
        draw.ellipse(**off_common, fill=hover_off, width=CB_OUTLINE_WIDTH)
        img_off_hover = image_resize(im, CB_FINAL_SIZE)

        # off/pressed
        im, draw = image_draw(*draw_settings)
        draw.ellipse(**off_common, fill=app_bg, width=RB_INNER_WIDTH_1)
        draw.ellipse(**off_common, width=CB_OUTLINE_WIDTH)
        img_off_pressed = image_resize(im, CB_FINAL_SIZE)

        # on
        im, draw = image_draw(*draw_settings)
        draw.ellipse(CB_BORDER_RECT, outline=background, fill=app_bg,
                     width=RB_INNER_WIDTH_1)
        draw.ellipse(CB_BORDER_RECT, outline=accents.dark1,
                     width=RB_OUTER_WIDTH)
        img_on = image_resize(im, CB_FINAL_SIZE)

        # on/hover
        im, draw = image_draw(*draw_settings)
        draw.ellipse(CB_BORDER_RECT, outline=hover_on, fill=app_bg,
                     width=RB_INNER_WIDTH_2)
        draw.ellipse(CB_BORDER_RECT, outline=accents.dark1,
                     width=RB_OUTER_WIDTH)
        img_on_hover = image_resize(im, CB_FINAL_SIZE)

        # on/pressed
        im, draw = image_draw(*draw_settings)
        draw.ellipse(CB_BORDER_RECT, outline=pressed_on, fill=app_bg,
                     width=RB_INNER_WIDTH_1)
        draw.ellipse(CB_BORDER_RECT, outline=accents.dark1,
                     width=RB_OUTER_WIDTH)
        img_on_pressed = image_resize(im, CB_FINAL_SIZE)

        # radio on/disabled
        im, draw = image_draw(*draw_settings)
        draw.ellipse(CB_BORDER_RECT, outline=disabled, fill=app_bg,
                     width=RB_INNER_WIDTH_1)
        draw.ellipse(CB_BORDER_RECT, outline=outline, width=RB_OUTER_WIDTH)
        img_on_dis = image_resize(im, CB_FINAL_SIZE)

        # radio disabled
        im, draw = image_draw(*draw_settings)
        draw.ellipse(CB_BORDER_RECT, outline=disabled, fill=app_bg,
                     width=CB_BORDER_WIDTH)
        img_dis = image_resize(im, CB_FINAL_SIZE)

        # create image elements
        #   A small amount is added to the width to allow for padding between
        #   the button and the text.
        e_name = f'{ttkstyle}.indicator'
        elem = self.element_builder(e_name, img_on, width=CB_BORDER_WIDTH + 6,
                                    sticky=W)
        elem.map('disabled selected', img_on_dis)
        elem.map('disabled', img_dis)
        elem.map('pressed !selected !disabled', img_off_pressed)
        elem.map('pressed selected !disabled', img_on_pressed)
        elem.map('hover !selected !disabled', img_off_hover)
        elem.map('hover selected !disabled', img_on_hover)
        elem.map('!selected', img_off)
        elem.build()

        # register assets to prevent GC
        self.register_assets(scheme.name, img_on, img_on_dis, img_dis,
                             img_off_pressed, img_on_pressed, img_off_hover,
                             img_on_hover, img_off)

        # normal style
        self.configure(ttkstyle, foreground=scheme.foreground, focuscolor='',
                       background=scheme.background, padding=BTN_PADDING)

        # state mapping
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])

        # style layout
        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element('Radiobutton.padding'), [
                Element(e_name, side=LEFT),
                Element('Radiobutton.label', side=RIGHT, expand=True)]])

    def create_switch_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_lt = scheme.accents(LIGHT)
        background = accents.accent
        app_bg = scheme.background
        disabled = accents_lt.dark1 if scheme.is_light else accents_lt.dark4
        outline = accents_lt.dark3
        hover_on = accents.light1 if scheme.is_light else accents[5]
        pressed_on = accents[2] if scheme.is_light else accents.dark1

        # create style assets
        if self.use_rgba:
            draw_settings = (SW_BUILD_SIZE,)
        else:
            draw_settings = (SW_BUILD_SIZE, 'RGB', scheme.background)

        # off - normal
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(SW_OUTER_RECT, outline=outline,
                               width=SW_OUTER_WIDTH_1, fill=app_bg,
                               radius=SW_OUTER_RADIUS)
        draw.rounded_rectangle(SW_INNER_RECT, outline=app_bg,
                               width=SW_INNER_WIDTH_N, fill=outline,
                               radius=SW_INNER_RADIUS)
        img_off = image_resize(im.rotate(180), SW_FINAL_SIZE)

        # off - hover
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(SW_OUTER_RECT, outline=outline,
                               width=SW_OUTER_WIDTH_1, fill=app_bg,
                               radius=SW_OUTER_RADIUS)
        draw.rounded_rectangle(SW_INNER_RECT, outline=app_bg,
                               width=SW_INNER_WIDTH_H,
                               fill=outline, radius=SW_INNER_RADIUS)
        img_off_hover = image_resize(im.rotate(180), SW_FINAL_SIZE)

        # off - pressed
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(SW_OUTER_RECT, outline=outline,
                               width=SW_OUTER_WIDTH_1, fill=app_bg,
                               radius=SW_OUTER_RADIUS)
        draw.rounded_rectangle(SW_PRESS_RECT, outline=app_bg,
                               width=SW_INNER_WIDTH_H, fill=outline,
                               radius=SW_INNER_RADIUS)
        img_off_pressed = image_resize(im.rotate(180), SW_FINAL_SIZE)

        # on - normal
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(SW_OUTER_RECT, outline=accents.dark1,
                               width=SW_OUTER_WIDTH_2, fill=background,
                               radius=SW_OUTER_RADIUS)
        draw.rounded_rectangle(SW_INNER_RECT, outline=background,
                               width=SW_INNER_WIDTH_N, fill=app_bg,
                               radius=SW_INNER_RADIUS)
        img_on = image_resize(im, SW_FINAL_SIZE)

        # on - hover
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(SW_OUTER_RECT, outline=accents.dark1,
                               width=SW_OUTER_WIDTH_2, fill=hover_on,
                               radius=SW_OUTER_RADIUS)
        draw.rounded_rectangle(SW_INNER_RECT, outline=hover_on, fill=app_bg,
                               width=SW_INNER_WIDTH_H, radius=SW_INNER_RADIUS)
        img_on_hover = image_resize(im, SW_FINAL_SIZE)

        # on - pressed
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(SW_OUTER_RECT, fill=pressed_on,
                               radius=SW_OUTER_RADIUS)
        draw.rounded_rectangle(SW_PRESS_RECT, outline=pressed_on,
                               width=SW_INNER_WIDTH_H, fill=app_bg,
                               radius=SW_INNER_RADIUS)
        img_on_pressed = image_resize(im, SW_FINAL_SIZE)

        # off - disabled
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(SW_OUTER_RECT, outline=disabled,
                               width=SW_OUTER_WIDTH_1, fill=app_bg,
                               radius=SW_OUTER_RADIUS)
        draw.rounded_rectangle(SW_INNER_RECT, outline=app_bg,
                               width=SW_INNER_WIDTH_N, fill=disabled,
                               radius=SW_INNER_RADIUS)
        img_off_dis = image_resize(im.rotate(180), SW_FINAL_SIZE)

        # on - disabled
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(SW_OUTER_RECT, outline=outline, width=6,
                               fill=disabled, radius=SW_OUTER_RADIUS)
        draw.rounded_rectangle(SW_INNER_RECT, outline=disabled,
                               width=SW_INNER_WIDTH_N, fill=app_bg,
                               radius=SW_INNER_RADIUS)
        img_on_dis = image_resize(im, SW_FINAL_SIZE)

        # style element
        #   add small amount to width to add padding between indicator and text
        e_name = f'{ttkstyle}.indicator'
        elem = self.element_builder(e_name, img_on, sticky=W,
                                    width=SW_FINAL_SIZE[0] + 6)
        elem.map('disabled !selected', img_off_dis)
        elem.map('disabled selected', img_on_dis)
        elem.map('!selected pressed', img_off_pressed)
        elem.map('!selected hover', img_off_hover)
        elem.map('!selected', img_off)
        elem.map('selected pressed', img_on_pressed)
        elem.map('selected hover', img_on_hover)
        elem.build()

        # register assets to prevent GC
        self.register_assets(scheme.name, img_on, img_off_dis, img_on_dis,
                             img_off_pressed, img_off_hover, img_off,
                             img_on_pressed, img_on_hover)

        # style layout
        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element('Toolbutton.border'), [
                Element('Toolbutton.padding'), [
                    Element(e_name, side=LEFT),
                    Element('Toolbutton.label', side=RIGHT, expand=True)]]])

        # normal style
        self.configure(ttkstyle, foreground=scheme.foreground,
                       background=scheme.background, padding=BTN_PADDING)

        # state map
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])

    def create_scrollbar_style(self, options):
        """Create a progressbar style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        orient = options['orient']
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_bg = scheme.accents('background')
        background = accents.accent
        outline = accents_bg.dark1
        troughcolor = accents_bg.light2 if scheme.is_dark else accents_bg.dark1

        # create style assets
        thumb_common = {'xy': SB_THUMB_RECT, 'radius': SB_BUILD_RADIUS}
        trough_common = {'xy': SB_TROUGH_RECT, 'radius': SB_BUILD_RADIUS}

        # thumb normal
        im, draw = image_draw(SB_BUILD_SIZE, 'RGB', scheme.background)
        draw.line(SB_LINE_RECT, width=SB_RESTING_WIDTH, fill=background)
        img_thumb_norm = image_resize(im, SB_FINAL_SIZE)
        im.resize(SB_FINAL_SIZE, Image.LANCZOS).save('thumb_normal.png')

        # thumb hover
        im, draw = image_draw(SB_BUILD_SIZE, 'RGB', troughcolor)
        draw.rounded_rectangle(**thumb_common, fill=background)
        img_thumb_hover = image_resize(im, SB_FINAL_SIZE, orient)
        im.resize(SB_FINAL_SIZE, Image.LANCZOS).save('thumb_hover.png')

        # trough norm
        im, draw = image_draw(SB_BUILD_SIZE, 'RGB', scheme.background)
        img_trough_norm = image_resize(im, SB_FINAL_SIZE, orient)

        # trough hover
        im, draw = image_draw(SB_BUILD_SIZE, 'RGB', scheme.background)
        draw.rounded_rectangle(**trough_common, fill=troughcolor,
                               outline=outline, width=SB_TROUGH_OUTLINE_WIDTH)
        img_trough_hover = image_resize(im, SB_FINAL_SIZE, orient)

        self.register_assets(scheme.name, img_thumb_norm, img_thumb_hover,
                             img_trough_norm, img_trough_hover)

        # create elements
        if orient == HORIZONTAL:
            side = LEFT
            width, height = MINIMUM_WIDTH, 0
        else:
            side = BOTTOM
            width, height = 0, MINIMUM_WIDTH

        thumb_name = f'{ttkstyle}.thumb'
        elem = self.element_builder(thumb_name, img_thumb_norm, width=width,
                                    height=height, border=SB_BUILD_RADIUS-4)
        elem.map('hover', img_thumb_hover)
        elem.build()

        trough_name = f'{ttkstyle}.trough'
        elem = self.element_builder(trough_name, img_trough_norm, width=width,
                                    height=height, border=SB_BUILD_RADIUS,
                                    padding=SB_TROUGH_PAD)
        elem.map('hover', img_trough_hover)
        elem.build()

        # create progressbar layout
        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element(trough_name, side=side, expand=True), [
                Element(thumb_name, side=side, expand=True)]])

    def create_spinbox_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or LIGHT
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_bg = scheme.accents('background')
        accents_lt = scheme.accents(LIGHT)
        disabled = accents_lt.dark1 if scheme.is_light else accents_lt.dark4
        background = accents.dark1
        foreground = scheme.foreground
        focus_color = scheme.primary if colorname == LIGHT else accents.accent
        hover_bg = accents_bg.light1 if scheme.is_dark else accents_lt.accent

        common = {'xy': ENTRY_BORDER_RECT, 'radius': ENTRY_BUILD_RADIUS,
                  'width': ENTRY_OUTLINE_WIDTH}

        if self.use_rgba:
            draw_settings = (ENTRY_BUILD_SIZE,)
        else:
            draw_settings = (ENTRY_BUILD_SIZE, 'RGB', scheme.background)

        # field
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ENTRY_LINE_RECT, fill=accents.dark3,
                  width=ENTRY_UNDERLINE_WIDTH)
        img_field = image_resize(im, ENTRY_FINAL_SIZE)

        # field hover
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background, fill=hover_bg)
        draw.line(ENTRY_LINE_RECT, fill=accents.dark3,
                  width=ENTRY_UNDERLINE_HOVER_WIDTH)
        img_hover = image_resize(im, ENTRY_FINAL_SIZE)

        # field focus
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ENTRY_LINE_RECT, fill=focus_color,
                  width=ENTRY_UNDERLINE_FOCUS_WIDTH)
        img_focus = image_resize(im, ENTRY_FINAL_SIZE)

        # field disabled
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=disabled)
        img_disabled = image_resize(im, ENTRY_FINAL_SIZE)

        # field element
        field_name = f'{ttkstyle}.field'
        elem = self.element_builder(field_name, img_field, sticky=NSEW,
                                    height=0, width=MINIMUM_WIDTH,
                                    border=ENTRY_BUILD_RADIUS)
        elem.map('disabled', img_disabled)
        elem.map('focus !readonly', img_focus)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # chevron normal
        im, draw = image_draw(CHEVRON_BUILD_SIZE)
        draw.line(CHEVRON_LINE_RECT, fill=foreground, width=CHEVRON_LINE_WIDTH)
        img_chev_dw = image_resize(im, CHEVRON_FINAL_SIZE)
        img_chev_up = image_resize(im.rotate(180), CHEVRON_FINAL_SIZE)

        # chevron pressed
        #   The field bubbles up the hover event and causes the button to light
        #   up when it shouldn't, so there is only a pressed state effect.
        im, draw = image_draw(CHEVRON_BUILD_SIZE)
        draw.line(CHEVRON_LINE_RECT, fill=focus_color,
                  width=CHEVRON_LINE_PRESSED_WIDTH)
        img_chev_dwp = image_resize(im, CHEVRON_FINAL_SIZE)
        img_chev_upp = image_resize(im.rotate(180), CHEVRON_FINAL_SIZE)

        # chevron disabled
        im, draw = image_draw(CHEVRON_BUILD_SIZE)
        draw.line(CHEVRON_LINE_RECT, fill=disabled, width=CHEVRON_LINE_WIDTH)
        img_chev_dw_dis = image_resize(im, CHEVRON_FINAL_SIZE)
        img_chev_up_dis = image_resize(im.rotate(180), CHEVRON_FINAL_SIZE)

        self.register_assets(scheme.name, img_chev_dw, img_chev_up,
                             img_chev_dwp, img_chev_upp, img_chev_dw_dis,
                             img_chev_up_dis, img_field, img_hover, img_focus,
                             img_disabled)

        chev_up_name = f'{ttkstyle}.uparrow'
        elem = self.element_builder(chev_up_name, img_chev_up, sticky='',
                                    padding='24 4')
        elem.map('disabled', img_chev_up_dis)
        elem.map('pressed !disabled', img_chev_upp)
        elem.build()

        chev_down_name = f'{ttkstyle}.downarrow'
        elem = self.element_builder(chev_down_name, img_chev_dw, sticky='',
                                    padding='4')
        elem.map('disabled', img_chev_dw_dis)
        elem.map('pressed !disabled', img_chev_dwp)
        elem.build()

        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element(field_name, expand=True), [
                Element('Spinbox.padding', sticky=NSEW), [
                    Element(chev_down_name, side=RIGHT, sticky=NS),
                    Element(chev_up_name, side=RIGHT, sticky=NS),
                    Element('Spinbox.textarea', side=LEFT)]]])

        # normal style
        self.configure(ttkstyle, foreground=foreground, insertcolor=foreground,
                       selectbackground=accents_bg.accent,
                       selectforeground=foreground, padding=ENTRY_PADDING)

        # state style map
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])
        self.map(ttkstyle, 'selectbackground', [('hover !disabled', hover_bg)])

    def create_frame_style(self, options):
        """Create a frame style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'background'
        self.register_style(options['ttkstyle'], scheme)

        # normal state
        background = scheme.get_color(colorname)
        self.configure(ttkstyle, background=background)

    def create_outline_frame_style(self, options):
        # TODO
        pass

    def create_label_style(self, options):
        """Create a label style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'foreground'
        self.register_style(options['ttkstyle'], scheme)

        # normal state
        foreground = scheme.get_color(colorname)
        self.configure(ttkstyle, foreground=foreground,
                       background=scheme.background)

    def create_inverse_label_style(self, options):
        """Create an inverse label style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'background'
        self.register_style(options['ttkstyle'], scheme)

        # normal state
        background = scheme.get_color(colorname)
        self.configure(ttkstyle, foreground=scheme.background,
                       background=background)

    def create_labelframe_style(self, options):
        """Create an labelframe style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or LIGHT
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        background = scheme.background
        foreground = scheme.foreground
        bordercolor = accents.dark3

        im_size = ss(1600, 1600)
        final_size = ss(64, 64)
        im, draw = image_draw(im_size, 'RGB', scheme.background)
        draw.rounded_rectangle((10, 10, 1590, 1590), radius=ss(1600 * 0.12),
                               outline=bordercolor, width=ss(24))
        img = image_resize(im, final_size)
        self.register_assets(scheme.name, img)

        self.style.element_image_builder(
            f'{ttkstyle}.border', img, sticky=NSEW, border=12).build()

        self.style.element_layout_builder(ttkstyle).build([
            Element(f'{ttkstyle}.border')])

        # widget label
        self.style.configure(style=f'{ttkstyle}.Label', foreground=foreground,
                             background=background)

        # widget frame
        self.style.configure(style=ttkstyle, borderwidth=2, relief=RAISED,
                             bordercolor=bordercolor, lightcolor=background,
                             darkcolor=background, background=background)

    def create_separator_style(self, options):
        """Create a separator style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or LIGHT
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        background = accents.dark3 if colorname == LIGHT else accents.accent

        # create style assets
        if options['orient'] == HORIZONTAL:
            build_size = SEP_BUILD_SIZE
            width = MINIMUM_WIDTH
            height = 0
            side = LEFT
        else:
            build_size = tuple(reversed(SEP_BUILD_SIZE))
            height = MINIMUM_WIDTH
            width = 0
            side = BOTTOM

        img = PhotoImage(image=Image.new('RGB', build_size, background))
        self.register_assets(scheme.name, img)
        separator_name = f'{ttkstyle}.separator'

        # style elements and layout
        self.element_create(separator_name, 'image', img, width=width,
                            height=height, border=SEP_LINE_WIDTH)
        self.layout_builder(ttkstyle).build([
            Element(separator_name, side=side, expand=True)])

    def create_entry_style(self, options):
        """Create an entry style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or LIGHT
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_bg = scheme.accents('background')
        accents_lt = scheme.accents(LIGHT)
        disabled = accents_lt.dark1 if scheme.is_light else accents_lt.dark4
        background = accents.dark1
        foreground = scheme.foreground
        select_fg = scheme.get_foreground(PRIMARY)
        focus_color = scheme.primary if colorname == LIGHT else accents.accent
        hover_bg = accents_bg.light1 if scheme.is_dark else accents_lt.accent

        common = {'xy': ENTRY_BORDER_RECT, 'radius': ENTRY_BUILD_RADIUS,
                  'width': ENTRY_OUTLINE_WIDTH}

        if self.use_rgba:
            draw_settings = (ENTRY_BUILD_SIZE,)
        else:
            draw_settings = (ENTRY_BUILD_SIZE, 'RGB', scheme.background)

        # entry field
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ENTRY_LINE_RECT, fill=accents.dark3,
                  width=ENTRY_UNDERLINE_WIDTH)
        img_field = image_resize(im, ENTRY_FINAL_SIZE)

        # entry hover
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background, fill=hover_bg)
        draw.line(ENTRY_LINE_RECT, fill=accents.dark3,
                  width=ENTRY_UNDERLINE_HOVER_WIDTH)
        img_hover = image_resize(im, ENTRY_FINAL_SIZE)

        # entry field focus
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ENTRY_LINE_RECT, fill=focus_color,
                  width=ENTRY_UNDERLINE_FOCUS_WIDTH)
        img_focus = image_resize(im, ENTRY_FINAL_SIZE)

        # entry field disabled
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=disabled)
        draw.line(ENTRY_LINE_RECT, fill=disabled, width=ENTRY_UNDERLINE_WIDTH)
        img_disabled = image_resize(im, ENTRY_FINAL_SIZE)

        self.register_assets(scheme.name, img_field, img_hover, img_focus,
                             img_disabled)

        field_name = f'{ttkstyle}.field'
        elem = self.element_builder(field_name, img_field, sticky=NSEW,
                                    border=ENTRY_BUILD_RADIUS,
                                    width=MINIMUM_WIDTH, height=0)
        elem.map('disabled', img_disabled)
        elem.map('focus', img_focus)
        elem.map('hover', img_hover)
        elem.build()

        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element(field_name), [
                Element('Entry.padding', sticky=NSEW), [
                    Element('Entry.textarea', sticky=NSEW)]]])

        # normal style
        self.configure(ttkstyle, foreground=foreground, insertcolor=foreground,
                       selectbackground=scheme.primary, padding=ENTRY_PADDING,
                       selectforeground=select_fg)

        # state style map
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])

    def create_combobox_style(self, options):
        """Create a combobox style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or LIGHT
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_bg = scheme.accents('background')
        accents_lt = scheme.accents(LIGHT)
        disabled = accents_lt.dark3 if scheme.is_light else accents_lt.dark4
        background = accents.dark1
        foreground = scheme.foreground
        focus_color = scheme.primary if colorname == LIGHT else accents.accent
        hover_bg = accents_bg.light1 if scheme.is_dark else accents_lt.accent

        common = {'xy': ENTRY_BORDER_RECT, 'radius': ENTRY_BUILD_RADIUS,
                  'width': ENTRY_OUTLINE_WIDTH}

        if self.use_rgba:
            draw_settings = (ENTRY_BUILD_SIZE,)
        else:
            draw_settings = (ENTRY_BUILD_SIZE, 'RGB', scheme.background)

        # combo field
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ENTRY_LINE_RECT, fill=accents.dark3,
                  width=ENTRY_UNDERLINE_WIDTH)
        img_field = image_resize(im, ENTRY_FINAL_SIZE)

        # combo hover
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background, fill=hover_bg)
        draw.line(ENTRY_LINE_RECT, fill=accents.dark3,
                  width=ENTRY_UNDERLINE_HOVER_WIDTH)
        img_hover = image_resize(im, ENTRY_FINAL_SIZE)

        # combo focus
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ENTRY_LINE_RECT, fill=focus_color,
                  width=ENTRY_UNDERLINE_FOCUS_WIDTH)
        img_focus = image_resize(im, ENTRY_FINAL_SIZE)

        # combo disabled
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=disabled)
        img_disabled = image_resize(im, ENTRY_FINAL_SIZE)

        # create field element
        field_name = f'{ttkstyle}.field'
        elem = self.element_builder(field_name, img_field, sticky=NSEW,
                                    border=ENTRY_BUILD_RADIUS,
                                    width=MINIMUM_WIDTH, height=0)
        elem.map('disabled', img_disabled)
        elem.map('focus !readonly', img_focus)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # chevron normal
        im, draw = image_draw(CHEVRON_BUILD_SIZE)
        draw.line(CHEVRON_LINE_RECT, fill=foreground, width=CHEVRON_LINE_WIDTH)
        img_chevron = image_resize(im, CHEVRON_FINAL_SIZE)

        # chevron disabled
        im, draw = image_draw(CHEVRON_BUILD_SIZE)
        draw.line(CHEVRON_LINE_RECT,
                  fill=disabled, width=CHEVRON_LINE_WIDTH)
        img_chev_dis = image_resize(im, CHEVRON_FINAL_SIZE)

        chevron_name = f'{ttkstyle}.chevron'
        elem = self.element_builder(chevron_name, img_chevron, sticky='',
                                    padding='12 4 4 4')
        elem.map('disabled', img_chev_dis)
        elem.build()

        self.register_assets(scheme.name, img_field, img_hover, img_focus,
                             img_disabled, img_chevron, img_chev_dis)

        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element(field_name, expand=True), [
                Element('Combobox.padding', sticky=NSEW), [
                    Element(chevron_name, side=RIGHT, sticky=''),
                    Element('Combobox.textarea', side=LEFT, sticky='')]]])

        # normal style
        self.configure(style=ttkstyle, foreground=foreground,
                       insertcolor=foreground,
                       selectbackground=accents_bg.accent,
                       selectforeground=foreground,
                       padding=ENTRY_PADDING)

        # state style map
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])
        self.map(ttkstyle, 'selectbackground', [('hover !disabled', hover_bg)])

        # setup options for scrollbar
        opt = options.copy()
        opt['orient'] = VERTICAL
        opt['ttkstyle'] = 'TCombobox.Vertical.TScrollbar'
        self.create_scrollbar_style(opt)

    @staticmethod
    def create_combobox_popdown_style(options):
        """Style the embedded popdown window within the combobox"""
        scheme = options['scheme']

        # style colors
        accents_bg = scheme.accents('background')
        accents_lt = scheme.accents(LIGHT)
        foreground = scheme.foreground
        selectbackground = scheme.info
        selectforeground = scheme.get_foreground('info')
        background = accents_bg.light1 if scheme.is_dark else accents_lt.accent

        # set the application window style
        widget = options['widget']

        tk_settings = []
        tk_settings.extend(["-borderwidth", 0])
        tk_settings.extend(["-background", background])
        tk_settings.extend(["-foreground", foreground])
        tk_settings.extend(["-selectbackground", selectbackground])
        tk_settings.extend(["-selectforeground", selectforeground])

        # set popdown style
        popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {str(widget)}")
        widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

        # set scrollbar style
        sb_style = "TCombobox.Vertical.TScrollbar"
        widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)

    def create_menubutton_style(self, options):
        """Create the default menubutton style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        foreground = scheme.get_foreground(colorname)
        background = accents.accent
        hover = accents.light1 if scheme.is_light else accents.dark1
        disabled = accents.light2

        # create style assets
        common = {'xy': BTN_BORDER_RECT, 'radius': BTN_BUILD_RADIUS,
                  'outline': accents.dark1, 'width': BTN_OUTLINE_WIDTH}

        if self.use_rgba:
            draw_settings = (BTN_BUILD_SIZE,)
        else:
            draw_settings = (BTN_BUILD_SIZE, 'RGB', scheme.background)

        # normal image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, fill=background)
        img_norm = image_resize(im, BTN_FINAL_SIZE)

        # hover image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, fill=hover)
        img_hover = image_resize(im, BTN_FINAL_SIZE)

        # button image element
        button_name = f'{ttkstyle}.button'
        elem = self.element_builder(button_name, img_norm, sticky=NSEW,
                                    height=0, width=MINIMUM_WIDTH,
                                    border=BTN_BUILD_RADIUS)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # chevron normal
        im, draw = image_draw(CHEVRON_BUILD_SIZE)
        draw.line(CHEVRON_LINE_RECT, fill=foreground, width=CHEVRON_LINE_WIDTH)
        img_chev_norm = image_resize(im, CHEVRON_FINAL_SIZE)

        # chevron disabled
        im, draw = image_draw(CHEVRON_BUILD_SIZE)
        draw.line(CHEVRON_LINE_RECT, fill=disabled, width=CHEVRON_LINE_WIDTH)
        img_chev_dis = image_resize(im, CHEVRON_FINAL_SIZE)

        # chevron element
        chevron_name = f'{ttkstyle}.chevron'
        elem = self.element_builder(chevron_name, img_chev_norm, sticky='')
        elem.map('disabled', img_chev_dis)
        elem.build()

        self.register_assets(scheme.name, img_norm, img_hover, img_chev_norm,
                             img_chev_dis)

        # button layout
        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element(button_name, sticky=NSEW), [
                Element('Menubutton.focus', sticky=NSEW), [
                    Element('Menubutton.padding', expand=True), [
                        Element(chevron_name, side=RIGHT, sticky=''),
                        Element('Menubutton.label', side=LEFT, expand=True)]]]]
        )

        # normal state
        self.configure(ttkstyle, foreground=foreground, padding=BTN_PADDING)

        # state map
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])

    def create_outline_menubutton_style(self, options):
        """Create an outline menubutton style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_lt = scheme.accents(LIGHT)
        accents_bg = scheme.accents('background')
        disabled = accents_lt.dark1 if scheme.is_light else accents_lt.dark4
        background = foreground = accents.accent
        hover_bg = accents_bg.light2 if scheme.is_dark else accents_lt.accent

        # create style assets
        common = {'xy': BTN_BORDER_RECT, 'radius': BTN_BUILD_RADIUS}

        if self.use_rgba:
            draw_settings = (BTN_BUILD_SIZE,)
        else:
            draw_settings = (BTN_BUILD_SIZE, 'RGB', scheme.background)

        # normal image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background, width=2)
        img_norm = image_resize(im, BTN_FINAL_SIZE)

        # hover image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background, width=3,
                               fill=hover_bg)
        img_hover = image_resize(im, BTN_FINAL_SIZE)

        # pressed image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=background, width=3,
                               fill=hover_bg)
        img_pressed = image_resize(im, BTN_FINAL_SIZE)

        # disable image
        im, draw = image_draw(*draw_settings)
        draw.rounded_rectangle(**common, outline=disabled, width=2)
        img_disabled = image_resize(im, BTN_FINAL_SIZE)

        # button image element
        button_name = f'{ttkstyle}.button'
        elem = self.element_builder(button_name, image=img_norm, sticky=NSEW,
                                    height=0, width=MINIMUM_WIDTH,
                                    border=BTN_BUILD_RADIUS)
        elem.map('disabled', img_disabled)
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # chevron normal
        im, draw = image_draw(CHEVRON_BUILD_SIZE)
        draw.line(CHEVRON_LINE_RECT, fill=foreground, width=CHEVRON_LINE_WIDTH)
        img_chev_norm = image_resize(im, CHEVRON_FINAL_SIZE)

        # chevron disabled
        im, draw = image_draw(CHEVRON_BUILD_SIZE)
        draw.line(CHEVRON_LINE_RECT, fill=disabled, width=CHEVRON_LINE_WIDTH)
        img_chev_dis = image_resize(im, CHEVRON_FINAL_SIZE)

        # chevron element
        chevron_name = f'{ttkstyle}.chevron'
        elem = self.element_builder(chevron_name, img_chev_norm, sticky='')
        elem.map('disabled', img_chev_dis)
        elem.build()

        self.register_assets(scheme.name, img_norm, img_hover, img_pressed,
                             img_disabled, img_chev_norm, img_chev_dis)

        # button layout
        layout = self.layout_builder(ttkstyle)
        layout.build([
            Element(button_name, sticky=NSEW), [
                Element('Menubutton.focus', sticky=NSEW), [
                    Element('Menubutton.padding', expand=True), [
                        Element(chevron_name, side=RIGHT, sticky=''),
                        Element('Menubutton.label', side=LEFT, expand=True)]]]]
        )

        # normal state
        self.configure(ttkstyle, foreground=foreground, focuscolor=foreground,
                       padding=BTN_PADDING)

        # state map
        self.map(ttkstyle, 'foreground', [('disabled', disabled)])

    def create_notebook_style(self, options):
        """Create the notebook style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        colorname = options['color'] or LIGHT
        accents = scheme.accents(colorname)
        background = scheme.background
        inactive_bg = accents.dark1 if scheme.is_light else accents.dark4
        bordercolor = accents.dark1 if scheme.is_light else accents.dark4

        # notebook tab
        img_size = ss(64, 64)
        end_size = ss(32, 32)
        common = {'xy': ss(1, 1, 63, 80), 'radius': ss(12), 'width': ss(1)}

        # notebook tab active
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=bordercolor, fill=background)
        img_tab_on = image_resize(im, end_size)

        # notebook tab inactive
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=inactive_bg, fill=inactive_bg)
        img_tab_off = image_resize(im, end_size)

        # notebook tab element
        e_name = ttkstyle.replace('TN', 'N')
        elem = self.style.element_image_builder(
            f'{e_name}.tab', image=img_tab_on, border=ss(6, 6, 6, 0),
            padding=ss(16, 14, 14, 6), height=ss(end_size[0]))
        elem.map('!selected', img_tab_off)
        elem.build()

        # notebook border
        im_size = ss(1600, 1600)
        final_size = ss(64, 64)
        im, draw = image_draw(im_size)
        draw.rounded_rectangle((10, 10, 1590, 1800), radius=ss(1600 * 0.12),
                               outline=bordercolor, width=ss(24),
                               fill=inactive_bg)
        img_border = image_resize(im, final_size)
        im.resize(end_size, Image.LANCZOS).save('.notebook-border.png')

        self.register_assets(scheme.name, img_tab_on, img_tab_off, img_border)

        # notebook border element
        self.style.element_create(f'{e_name}.border', 'image', img_border,
                                  sticky=NSEW, border=ss(6, 6, 6, 0),
                                  width=ss(64), height=ss(64))

        # notebook layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{e_name}.border'), [
                Element(f'{ttkstyle}.Tab', expand=True)]])

        self.style.configure(ttkstyle, padding='1')
        self.style.configure(f'{ttkstyle}.Tab', focuscolor='')
        self.style.state_map(f'{ttkstyle}.Tab', 'background', [
            ('selected', background)])

    def create_panedwindow_style(self, options):
        """Create a panedwindow style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or LIGHT
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        background = accents.dark3 if colorname == LIGHT else accents.accent

        # normal state
        self.configure(ttkstyle, background=background)
        self.configure('Sash', gripcount=0, sashthickness=PW_SASH_THICKNESS)

    def create_progressbar_style(self, options):
        """Create a progressbar style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        orient = options['orient']
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_bg = scheme.accents('background')
        accents_lt = scheme.accents(LIGHT)
        background = accents.accent
        outline = accents_bg.dark1
        troughcolor = accents_lt.dark3 if scheme.is_dark else accents_bg.dark1

        final_size = 20, 10
        img_size = 1000, 500
        common = {'xy': (10, 10, 990, 490), 'radius': ss(250)}

        # progressbar
        im, draw = image_draw(img_size, 'RGB', troughcolor)
        draw.rounded_rectangle(**common, fill=background)
        img_pbar = image_resize(im, final_size)

        # trough
        im, draw = image_draw(img_size, 'RGB', scheme.background)
        draw.rounded_rectangle(**common, fill=troughcolor, outline=outline,
                               width=6)
        img_trough = image_resize(im, final_size)

        self.register_assets(scheme.name, img_pbar, img_trough)

        # create elements
        self.style.element_create(f'{ttkstyle}.pbar', 'image', img_pbar,
                                  border='4 0')
        self.style.element_create(f'{ttkstyle}.trough', 'image', img_trough,
                                  border='4 0', padding=0)

        # create progressbar layout
        sticky = EW if orient == HORIZONTAL else NS
        side = LEFT if orient == HORIZONTAL else BOTTOM
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.trough', sticky=EW), [
                Element(f'{ttkstyle}.pbar', side=side, sticky=sticky)]])

    def create_scale_style(self, options):
        """Create a scale style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        orient = options['orient']
        colorname = options['color'] or PRIMARY
        accents = scheme.accents(colorname)
        accents_bg = scheme.accents('background')
        accents_lt = scheme.accents(LIGHT)
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        background = accents.accent
        app_bg = scheme.background
        outline = accents_lt.dark3
        disabled = accents_lt.dark1 if scheme.is_light else accents_lt.dark4
        pressed = accents.dark1 if scheme.is_dark else accents.light2
        hover = accents.dark1 if scheme.is_dark else accents.light1
        troughcolor = accents_lt.dark3 if scheme.is_dark else accents_bg.dark1
        hover_bg = accents_bg.light1 if scheme.is_dark else accents_lt.accent

        # create scale assets
        size = ss(32)
        img_size = ss(640, 640)
        rect = ss(20, 20, 620, 620)
        radius = ss(310)
        common = {'xy': rect, 'radius': radius}

        # handle normal
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, width=150, outline=app_bg,
                               fill=background)
        draw.rounded_rectangle(**common, width=20, outline=outline)
        img_normal = PhotoImage(image=im.resize((size, size), Image.LANCZOS))

        # pressed state image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, width=180, outline=hover_bg,
                               fill=pressed)
        draw.rounded_rectangle(**common, width=20, outline=outline)
        img_pressed = image_resize(im, (size, size))

        # hover state image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, width=120, outline=hover_bg,
                               fill=hover)
        draw.rounded_rectangle(**common, width=20, outline=outline)
        img_hover = image_resize(im, (size, size))

        # disabled state image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, width=150, outline=app_bg,
                               fill=disabled)
        draw.rounded_rectangle(**common, width=20, outline=disabled)
        img_disabled = image_resize(im, (size, size))

        # create slider element
        slider_name = f'{ttkstyle}.slider'
        elem = self.style.element_image_builder(slider_name, img_normal)
        elem.map('disabled', img_disabled)
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # track image
        if orient == VERTICAL:
            track_size = self.scale_size(5, 40)
        else:
            track_size = self.scale_size(40, 5)

        img_track = PhotoImage(image=Image.new('RGB', track_size, troughcolor))

        self.register_assets(scheme.name, img_normal, img_pressed, img_hover,
                             img_disabled, img_track)

        # create track element
        track_name = f'{ttkstyle}.track'
        self.style.element_create(track_name, 'image', img_track)

        # slider layout
        side = LEFT if orient == HORIZONTAL else TOP
        sticky = EW if orient == HORIZONTAL else NS

        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.focus', expand=True, sticky=NSEW), [
                Element(track_name, sticky=sticky),
                Element(slider_name, side=side)]])

    def create_sizegrip_style(self, options):
        """Create a sizegrip style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or LIGHT
        self.register_style(options['ttkstyle'], scheme)

        # style colors
        accents = scheme.accents(colorname)
        accents_bg = scheme.accents('background')

        if colorname == LIGHT:
            fill = accents.dark3 if scheme.is_dark else accents_bg.dark1
        else:
            fill = accents.accent

        # create sizegrip assets
        box = self.scale_size(1)
        pad = box * 1
        chunk = box + pad  # 4
        w = chunk * 3 + pad  # 14
        h = chunk * 3 + pad  # 14
        size = w, h

        im, draw = image_draw(size)
        draw.rectangle((chunk * 2 + pad, pad, chunk * 3, chunk), fill=fill)
        draw.rectangle((chunk * 2 + pad, chunk + pad, chunk * 3, chunk * 2),
                       fill=fill)
        draw.rectangle(
            (chunk * 2 + pad, chunk * 2 + pad, chunk * 3, chunk * 3),
            fill=fill)
        draw.rectangle((chunk + pad, chunk + pad, chunk * 2, chunk * 2),
                       fill=fill)
        draw.rectangle((chunk + pad, chunk * 2 + pad, chunk * 2, chunk * 3),
                       fill=fill)
        draw.rectangle((pad, chunk * 2 + pad, chunk, chunk * 3), fill=fill)

        img_grip = PhotoImage(image=im)
        self.register_assets(scheme.name, img_grip)

        # widget element
        element_name = f'{ttkstyle}.sizegrip'
        self.element_create(element_name, 'image', img_grip)

        # widget layout
        self.layout_builder(ttkstyle).build([
            Element(element_name, side=BOTTOM, sticky=SE)])
