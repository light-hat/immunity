import json
import os

import pytest
from core.engine.vul_engine import VulEngine
from tests import MOCKDATA_DIR


@pytest.mark.unit
def test_search_method_pool():
    MOCKDATA_FILE = os.path.join(MOCKDATA_DIR, "method_pool_edge_out_of_index.json")
    with open(MOCKDATA_FILE) as fp:
        mock_method_pool_data = json.load(fp)
    engine = VulEngine()
    engine.method_pool = mock_method_pool_data
    try:
        engine.search(
            method_pool=mock_method_pool_data,
            vul_method_signature="java.lang.Class.forName",
        )
    except IndexError:
        self.fail(
            "engine.search show check method_pool data instead of raise IndexError."
        )


@pytest.mark.unit
def test_search_method_pool_ssrf_safe():
    MOCKDATA_FILE = os.path.join(MOCKDATA_DIR, "ssrf_in_cookie_safe.json")
    with open(MOCKDATA_FILE) as fp:
        mock_method_pool_data = json.load(fp)
    engine = VulEngine()
    engine.method_pool = mock_method_pool_data
    engine.search(
        method_pool=mock_method_pool_data,
        vul_method_signature="org.apache.http.impl.client.CloseableHttpClient.doExecute",
    )
    status, stack, source_sign, sink_sign, taint_value = engine.result()
    assert status == False


@pytest.mark.unit
def test_search_method_pool_ssrf_unsafe():
    MOCKDATA_FILE = os.path.join(MOCKDATA_DIR, "ssrf_in_cookie_unsafe.json")
    with open(MOCKDATA_FILE) as fp:
        mock_method_pool_data = json.load(fp)
    engine = VulEngine()
    engine.method_pool = mock_method_pool_data
    engine.search(
        method_pool=mock_method_pool_data,
        vul_method_signature="org.apache.http.impl.client.CloseableHttpClient.doExecute",
    )
    status, stack, source_sign, sink_sign, taint_value = engine.result()
    assert status == True


@pytest.mark.unit
def test_search_method_pool_ssrf_unsafe_v2():
    MOCKDATA_FILE = os.path.join(
        MOCKDATA_DIR, "ssrf_unsafe_java-net-url-connection.json"
    )
    with open(MOCKDATA_FILE) as fp:
        mock_method_pool_data = json.load(fp)
    engine = VulEngine()
    engine.method_pool = mock_method_pool_data
    engine.search(
        method_pool=mock_method_pool_data,
        vul_method_signature="sun.net.www.protocol.http.HttpURLConnection.connect",
    )
    status, stack, source_sign, sink_sign, taint_value = engine.result()
    assert status == True


@pytest.mark.unit
def test_search_method_pool_ssrf_safe_v2():
    MOCKDATA_FILE = os.path.join(
        MOCKDATA_DIR, "ssrf_safe_java-net-url-connection-param.json"
    )
    with open(MOCKDATA_FILE) as fp:
        mock_method_pool_data = json.load(fp)
    engine = VulEngine()
    engine.method_pool = mock_method_pool_data
    engine.search(
        method_pool=mock_method_pool_data,
        vul_method_signature="sun.net.www.protocol.http.HttpURLConnection.connect",
    )
    status, stack, source_sign, sink_sign, taint_value = engine.result()
    assert status == False


@pytest.mark.unit
def test_search_method_pool_range_unsafe():
    MOCKDATA_FILE = os.path.join(
        MOCKDATA_DIR, "propagator_range-remove_unsafe_string-builder-delete.json"
    )
    with open(MOCKDATA_FILE) as fp:
        mock_method_pool_data = json.load(fp)
    engine = VulEngine()
    engine.method_pool = mock_method_pool_data
    engine.search(
        method_pool=mock_method_pool_data, vul_method_signature="java.lang.Runtime.exec"
    )
    status, stack, source_sign, sink_sign, taint_value = engine.result()
    assert status == True


@pytest.mark.unit
def test_search_method_pool_range_safe():
    MOCKDATA_FILE = os.path.join(
        MOCKDATA_DIR, "range-subset_safe_string_builder_substring_start2.json"
    )
    with open(MOCKDATA_FILE) as fp:
        mock_method_pool_data = json.load(fp)
    engine = VulEngine()
    engine.method_pool = mock_method_pool_data
    engine.search(
        method_pool=mock_method_pool_data, vul_method_signature="java.lang.Runtime.exec"
    )
    status, stack, source_sign, sink_sign, taint_value = engine.result()
    assert status == False


@pytest.mark.unit
def test_search_method_pool_range_safe_v2():
    MOCKDATA_FILE = os.path.join(
        MOCKDATA_DIR, "reflection-injection_safe_for-name.json"
    )
    with open(MOCKDATA_FILE) as fp:
        mock_method_pool_data = json.load(fp)
    engine = VulEngine()
    engine.method_pool = mock_method_pool_data
    engine.search(
        method_pool=mock_method_pool_data,
        vul_method_signature="java.lang.Class.forName",
    )
    status, stack, source_sign, sink_sign, taint_value = engine.result()
    assert status == False
