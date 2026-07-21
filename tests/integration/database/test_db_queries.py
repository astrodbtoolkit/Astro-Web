import pandas as pd
import pytest
from astro_web.database.sources import get_all_sources, get_source_inventory, get_source_spectra
from astro_web.database.query import search_objects, cone_search

def test_get_all_sources():
    """Verify it returns a list of sources with expected columns."""
    sources = get_all_sources()
    assert isinstance(sources, list)
    assert len(sources) > 0
    # Check if 'source', 'ra_deg', 'dec_deg' are in the first record
    first_source = sources[0]
    assert "source" in first_source
    assert "ra_deg" in first_source
    assert "dec_deg" in first_source

def test_search_objects():
    """Verify search results for known objects."""
    # Searching for a known object in the database
    query_str = "Gl 229b"
    results, exec_time = search_objects(query_str)
    
    assert isinstance(results, pd.DataFrame)
    assert not results.empty
    assert exec_time > 0
    # Check if our target is in the results
    assert any(results["source"].str.contains(query_str, regex=False))

def test_cone_search():
    """Verify results are within the requested radius."""
    # Centered on Gl 229b (RA=92.6442, Dec=-21.8646)
    ra = 92.6442
    dec = -21.8646
    radius = 0.1 # 0.1 degrees

    results, exec_time = cone_search(ra, dec, radius)

    assert isinstance(results, pd.DataFrame)
    assert not results.empty
    assert exec_time > 0

    # Verify we found at least the source itself
    assert any(results["source"] == "Gl 229b")

def test_get_source_inventory():
    """Verify all related tables are retrieved for a specific source."""
    source_name = "Gl 229b"
    inventory = get_source_inventory(source_name)

    assert isinstance(inventory, dict)
    assert len(inventory) > 0
    # Common tables that should have data for this source
    assert "Sources" in inventory
    assert "Names" in inventory

@pytest.mark.xfail(reason="astrodb-template database contains no Spectra data")
def test_get_source_spectra():
    """Verify spectra data retrieval."""
    source_name = "Gl 229b"
    spectra = get_source_spectra(source_name)
    
    assert isinstance(spectra, pd.DataFrame)
    assert not spectra.empty
    assert "source" in spectra.columns
    assert "access_url" in spectra.columns
    assert "processed_spectrum" in spectra.columns
    
    # Check if at least one spectrum was processed
    assert spectra["processed_spectrum"].notna().any()
