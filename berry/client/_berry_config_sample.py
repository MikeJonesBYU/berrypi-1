# Berry-specific config
#
# Instructions: Copy this to _berry_config.py and then update line 10 to
# instantiate the right class.

from berry import berries


def get_berry(guid):
    return berries.BerryButton(live=True, guid=guid)
