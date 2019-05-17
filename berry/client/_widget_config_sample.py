# Berry-specific config
#
# Instructions: Copy this to _widget_config.py and then update line 10 to
# instantiate the right class.

from berry import berries


def get_widget(guid):
    return berries.BerryButton(live=True, guid=guid)

def get_selector(widget):
    from berry.selectors import LightSelect
    return LightSelect(widget)
