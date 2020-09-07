import pytest
from source.data_collector.data_collector import DataCollector
from datetime import datetime, date

@pytest.fixture
def supply_data() -> dict:
    """
    Supply the energy_data list
    """
    energy = [
        {'ts': '2020-08-29 21:00', 'dem': 26342, 'eol': 11354, 'nuc': 6972, 'gf': 0, 'car': 437, 'cc': 4849, 'hid': 1725, 'aut': 0, 'inter': -3494, 'icb': -131, 'sol': 879, 'solFot': 68, 'solTer': 810, 'termRenov': 434, 'cogenResto': 3355},
        {'ts': '2020-08-29 21:10', 'dem': 27102, 'eol': 11198, 'nuc': 6971, 'gf': 0, 'car': 442, 'cc': 4628, 'hid': 2276, 'aut': 0, 'inter': -2916, 'icb': -131, 'sol': 740, 'solFot': 27, 'solTer': 713, 'termRenov': 460, 'cogenResto': 3399},
        {'ts': '2020-08-29 21:20', 'dem': 27142, 'eol': 11290, 'nuc': 6974, 'gf': 0, 'car': 442, 'cc': 4439, 'hid': 2210, 'aut': 0, 'inter': -2662, 'icb': -131, 'sol': 691, 'solFot': 18, 'solTer': 672, 'termRenov': 460, 'cogenResto': 3399},
        {'ts': '2020-08-29 21:30', 'dem': 27317, 'eol': 11219, 'nuc': 6971, 'gf': 0, 'car': 441, 'cc': 4593, 'hid': 2313, 'aut': 0, 'inter': -2643, 'icb': -131, 'sol': 667, 'solFot': 20, 'solTer': 647, 'termRenov': 460, 'cogenResto': 3399},
        {'ts': '2020-08-29 21:40', 'dem': 27039, 'eol': 11076, 'nuc': 6969, 'gf': 0, 'car': 439, 'cc': 4550, 'hid': 2214, 'aut': 0, 'inter': -2660, 'icb': -131, 'sol': 654, 'solFot': 18, 'solTer': 636, 'termRenov': 460, 'cogenResto': 3399},
        {'ts': '2020-08-29 21:50', 'dem': 27028, 'eol': 10917, 'nuc': 6974, 'gf': 0, 'car': 440, 'cc': 4686, 'hid': 2333, 'aut': 0, 'inter': -2649, 'icb': -131, 'sol': 652, 'solFot': 18, 'solTer': 634, 'termRenov': 460, 'cogenResto': 3399},
        {'ts': '2020-08-29 22:00', 'dem': 26574, 'eol': 10782, 'nuc': 6978, 'gf': 0, 'car': 443, 'cc': 4737, 'hid': 2133, 'aut': 0, 'inter': -2869, 'icb': -131, 'sol': 649, 'solFot': 20, 'solTer': 628, 'termRenov': 460, 'cogenResto': 3399},
        {'ts': '2020-08-29 22:10', 'dem': 26294, 'eol': 10687, 'nuc': 6971, 'gf': 0, 'car': 439, 'cc': 4768, 'hid': 2096, 'aut': 0, 'inter': -3031, 'icb': -131, 'sol': 641, 'solFot': 17, 'solTer': 624, 'termRenov': 461, 'cogenResto': 3390},
        {'ts': '2020-08-29 22:20', 'dem': 25900, 'eol': 10435, 'nuc': 6973, 'gf': 0, 'car': 438, 'cc': 4684, 'hid': 2094, 'aut': 0, 'inter': -3305, 'icb': 131, 'sol': 640, 'solFot': 17, 'solTer': 623, 'termRenov': 461, 'cogenResto': 3390},
        {'ts': '2020-08-29 22:30', 'dem': 25743, 'eol': 10328, 'nuc': 6975, 'gf': 0, 'car': 440, 'cc': 4590, 'hid': 2029, 'aut': 0, 'inter': -2951, 'icb': -131, 'sol': 637, 'solFot': 17, 'solTer': 620, 'termRenov': 461, 'cogenResto': 3390},
        {'ts': '2020-08-29 22:40', 'dem': 25341, 'eol': 10120, 'nuc': 6972, 'gf': 0, 'car': 441, 'cc': 4643, 'hid': 2025, 'aut': 0, 'inter': -3201, 'icb': -131, 'sol': 636, 'solFot': 17, 'solTer': 619, 'termRenov': 461, 'cogenResto': 3390},
        {'ts': '2020-08-29 22:50', 'dem': 24911, 'eol': 10139, 'nuc': 6979, 'gf': 0, 'car': 440, 'cc': 4375, 'hid': 1686, 'aut': 0, 'inter': -3120, 'icb': -131, 'sol': 637, 'solFot': 17, 'solTer': 620, 'termRenov': 461, 'cogenResto': 3390}
    ]

    emissions = {
        '2020-08-29 21:00': 3232.3099999999995,
        '2020-08-29 21:10': 3174.1899999999996,
        '2020-08-29 21:20': 3104.2599999999998,
        '2020-08-29 21:30': 3160.29,
        '2020-08-29 21:40': 3142.48,
        '2020-08-29 21:50': 3193.7499999999995,
        '2020-08-29 22:00': 3215.47,
        '2020-08-29 22:10': 3220.98,
        '2020-08-29 22:20': 3188.95,
        '2020-08-29 22:30': 3156.07, 
        '2020-08-29 22:40': 3176.63, 
        '2020-08-29 22:50': 3076.52
    }

    return (energy, emissions)

def test_retrieve_last_two_hours(mocker, supply_data):
    """
    Test the retrieve_last_two_hours method
    """
    collector = DataCollector()
    
    # Mocks the method to retrieve a certain date
    mocker.patch.object(collector, '_generate_previous_day_date', return_value='2020-08-30')
    # Mocks the method to avoid connecting to the API
    mocker.patch.object(collector, '_retrieve_energy_data', return_value=supply_data[0]) 

    result_doc = collector.retrieve_last_two_hours()

    assert isinstance(result_doc, dict)
    assert result_doc 
    assert result_doc == supply_data[1]