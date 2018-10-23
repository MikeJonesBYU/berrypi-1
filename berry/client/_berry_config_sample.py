# Berry-specific config
#
# Instructions: update this to import the right class, then instantiate that
# class inside get_berry().
#
# Copy this to _berry_config.py

from berry.berries import BerryButton


def get_berry(guid):
    # Test berry
    berry = BerryButton(
        berry_type='button',
        live=True,
        guid=guid,
    )

    return berry
