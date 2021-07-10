"""
axes package.
Usefull extensions of the OpenCV and PIL Image extract

Package Structure
=================

Modules:

* __init__.py: API imports

"""
__author__ = 'hernani'
__version__ = 'ffmpeglib-0.0.1'
__apply__ = 'console - OpenVC with GUI python'
__version__ = '1'

try:
    from .flowlayout import Flowlayout
    from .imagetrans import Imagetrans
    from .spritepane import SpritePane
    from .ToolTip import ToolTip, createToolTip
    from .tooltipmenu import ToolTipMenu, createToolTipMenu
    from .windialog import LabelEntryButton, FrameButtons
    from .windialog import WindowCopyTo, CustomEntry, OpenDialogRename, ToolFile
except ImportError:
    from flowlayout import Flowlayout
    from imagetrans import Imagetrans
    from spritepane import SpritePane
    from ToolTip import ToolTip, createToolTip
    from tooltipmenu import ToolTipMenu, createToolTipMenu
    from windialog import LabelEntryButton, FrameButtons
    from windialog import WindowCopyTo, CustomEntry, OpenDialogRename, ToolFile


