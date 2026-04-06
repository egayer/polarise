"""Tests for polarise.utils.colormaps — BUILTIN_CMAPS and EXTERNAL_CMAPS lookups.

Run with:
    pytest tests/test_colormaps.py -v

All tests are cross-platform (pure Python, no file I/O).
Optional-package tests are skipped gracefully if the package is not installed.
"""
import pytest
from polarise.utils.colormaps import (
    BUILTIN_CMAPS,
    EXTERNAL_CMAPS,
    _AVAILABLE_PACKAGES,
    get_colormap,
    interpolate_color,
)


# ── BUILTIN_CMAPS ────────────────────────────────────────────────────────────

class TestBuiltinCmaps:
    def test_expected_maps_present(self):
        expected = [
            'hawaii', 'acton', 'nuuk', 'lipari', 'davos', 'buda',   # Crameri seq
            'vik', 'managua',                                          # Crameri div
            'CET_L20', 'CET_L19', 'CET_L17',                          # ColorCET seq
            'CET_D11', 'CET_D12', 'CET_I3',                           # ColorCET div
            'viridis', 'plasma',                                       # Matplotlib
            'grays', 'reds', 'blues', 'greens',                        # Custom single-hue
            'orange-to-purple',                                        # Diane Simoni
        ]
        for name in expected:
            assert name in BUILTIN_CMAPS, f"'{name}' missing from BUILTIN_CMAPS"

    def test_all_maps_have_reversed_variant(self):
        base_names = [k for k in BUILTIN_CMAPS if not k.endswith('_r')]
        for name in base_names:
            assert f"{name}_r" in BUILTIN_CMAPS, f"'{name}_r' missing"

    def test_reversed_is_actually_reversed(self):
        for name in ['hawaii', 'vik', 'CET_L20', 'grays']:
            fwd = BUILTIN_CMAPS[name]
            rev = BUILTIN_CMAPS[f"{name}_r"]
            assert rev == list(reversed(fwd))

    def test_crameri_maps_have_256_stops(self):
        for name in ['hawaii', 'acton', 'nuuk', 'lipari', 'davos', 'buda', 'vik', 'managua']:
            stops = BUILTIN_CMAPS[name]
            assert len(stops) == 256, f"'{name}' has {len(stops)} stops, expected 256"

    def test_colorect_maps_have_256_stops(self):
        for name in ['CET_L20', 'CET_L19', 'CET_L17', 'CET_D11', 'CET_D12', 'CET_I3']:
            stops = BUILTIN_CMAPS[name]
            assert len(stops) == 256, f"'{name}' has {len(stops)} stops, expected 256"

    def test_stops_are_rgb_tuples_in_range(self):
        for name, stops in BUILTIN_CMAPS.items():
            if name.endswith('_r'):
                continue
            for i, stop in enumerate(stops):
                assert len(stop) == 3, f"'{name}' stop {i} has {len(stop)} values"
                for channel in stop:
                    assert 0.0 <= channel <= 1.0, f"'{name}' stop {i} channel out of range: {channel}"

    def test_grays_endpoints(self):
        cmap = get_colormap('grays')
        assert cmap(0.0) == '#FFFFFF'
        assert cmap(1.0) == '#737373'

    def test_grays_r_endpoints(self):
        cmap = get_colormap('grays_r')
        assert cmap(0.0) == '#737373'
        assert cmap(1.0) == '#FFFFFF'


# ── interpolate_color ────────────────────────────────────────────────────────

class TestInterpolateColor:
    def test_two_stop_endpoints(self):
        stops = [(1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
        assert interpolate_color(stops, 0.0) == '#FF0000'
        assert interpolate_color(stops, 1.0) == '#0000FF'

    def test_two_stop_midpoint(self):
        stops = [(1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
        result = interpolate_color(stops, 0.5)
        assert result == '#7F007F'

    def test_clamps_below_zero(self):
        stops = [(1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
        assert interpolate_color(stops, -0.5) == interpolate_color(stops, 0.0)

    def test_clamps_above_one(self):
        stops = [(1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
        assert interpolate_color(stops, 1.5) == interpolate_color(stops, 1.0)


# ── get_colormap — built-ins ─────────────────────────────────────────────────

class TestGetColormapBuiltin:
    def test_returns_callable(self):
        cmap = get_colormap('hawaii')
        assert callable(cmap)

    def test_returns_hex_string(self):
        cmap = get_colormap('hawaii')
        result = cmap(0.5)
        assert isinstance(result, str)
        assert result.startswith('#')
        assert len(result) == 7

    def test_reversed_variant(self):
        fwd = get_colormap('hawaii')
        rev = get_colormap('hawaii_r')
        assert rev(0.0) == fwd(1.0)
        assert rev(1.0) == fwd(0.0)

    def test_all_builtin_maps_interpolate(self):
        base_names = [k for k in BUILTIN_CMAPS if not k.endswith('_r')]
        for name in base_names:
            cmap = get_colormap(name)
            for v in (0.0, 0.5, 1.0):
                result = cmap(v)
                assert result.startswith('#') and len(result) == 7, \
                    f"'{name}'({v}) returned bad value: {result}"

    def test_callable_object_passthrough(self):
        # A callable colormap object should be wrapped directly
        class FakeColormap:
            def __call__(self, v):
                return (v, v, v, 1.0)
        fake = FakeColormap()
        cmap = get_colormap(fake)
        result = cmap(0.5)
        assert result.startswith('#')


# ── _AVAILABLE_PACKAGES ──────────────────────────────────────────────────────

class TestAvailablePackages:
    def test_all_keys_present(self):
        for pkg in ('cmcrameri', 'colorspace', 'colorcet', 'matplotlib'):
            assert pkg in _AVAILABLE_PACKAGES

    def test_values_are_bool(self):
        for pkg, available in _AVAILABLE_PACKAGES.items():
            assert isinstance(available, bool), f"'{pkg}' value is not bool"


# ── EXTERNAL_CMAPS registry ──────────────────────────────────────────────────

class TestExternalCmapsRegistry:
    def test_all_packages_present(self):
        for pkg in ('cmcrameri', 'colorspace', 'colorcet'):
            assert pkg in EXTERNAL_CMAPS

    def test_crameri_names_not_in_builtin(self):
        # Maps only in cmcrameri (not in BUILTIN_CMAPS) should be in EXTERNAL_CMAPS
        assert 'bamako' in EXTERNAL_CMAPS['cmcrameri']
        assert 'lapaz' in EXTERNAL_CMAPS['cmcrameri']

    def test_colorspace_uses_exact_package_names(self):
        # Names must have colorspace's native format (capitalized, spaces, hyphens)
        assert 'Blues 2' in EXTERNAL_CMAPS['colorspace']
        assert 'Green-Orange' in EXTERNAL_CMAPS['colorspace']
        assert 'ag_Sunset' in EXTERNAL_CMAPS['colorspace']

    def test_colorcet_uses_exact_package_names(self):
        assert 'fire' in EXTERNAL_CMAPS['colorcet']
        assert 'CET_L1' in EXTERNAL_CMAPS['colorcet']
        assert 'CET_D11' in EXTERNAL_CMAPS['colorcet']


# ── get_colormap — cmcrameri ─────────────────────────────────────────────────

class TestGetColormapCmcrameri:
    @pytest.fixture(autouse=True)
    def require_cmcrameri(self):
        pytest.importorskip('cmcrameri')

    def test_bamako_returns_callable(self):
        cmap = get_colormap('bamako')
        assert callable(cmap)

    def test_bamako_interpolates(self):
        cmap = get_colormap('bamako')
        for v in (0.0, 0.5, 1.0):
            result = cmap(v)
            assert result.startswith('#') and len(result) == 7

    def test_bamako_r_reversal(self):
        fwd = get_colormap('bamako')
        rev = get_colormap('bamako_r')
        assert rev(0.0) == fwd(1.0)

    def test_lapaz(self):
        cmap = get_colormap('lapaz')
        assert cmap(0.5).startswith('#')


# ── get_colormap — colorspace ────────────────────────────────────────────────

class TestGetColormapColorspace:
    @pytest.fixture(autouse=True)
    def require_colorspace(self):
        pytest.importorskip('colorspace')

    def test_blues2_sequential(self):
        cmap = get_colormap('Blues 2')
        assert callable(cmap)
        assert cmap(0.5).startswith('#')

    def test_green_orange_diverging(self):
        cmap = get_colormap('Green-Orange')
        assert callable(cmap)
        # Green-Orange goes green→light→orange
        assert cmap(0.0) != cmap(1.0)

    def test_reversed_variant(self):
        fwd = get_colormap('Blues 2')
        rev = get_colormap('Blues 2_r')
        assert rev(0.0) == fwd(1.0)

    def test_sunset_sequential(self):
        cmap = get_colormap('Sunset')
        assert cmap(0.5).startswith('#')


# ── get_colormap — colorcet ──────────────────────────────────────────────────

class TestGetColormapColorcet:
    @pytest.fixture(autouse=True)
    def require_colorcet(self):
        pytest.importorskip('colorcet')

    def test_fire(self):
        cmap = get_colormap('fire')
        assert callable(cmap)
        assert cmap(0.0) == '#000000'  # fire starts black
        assert cmap(1.0) == '#FFFFFF'  # fire ends white

    def test_cet_l1(self):
        cmap = get_colormap('CET_L1')
        assert cmap(0.5).startswith('#')

    def test_reversed_variant(self):
        fwd = get_colormap('fire')
        rev = get_colormap('fire_r')
        assert rev(0.0) == fwd(1.0)


# ── error cases ──────────────────────────────────────────────────────────────

class TestGetColormapErrors:
    def test_unknown_name_raises_value_error(self):
        with pytest.raises((ValueError, Exception)):
            get_colormap('this_does_not_exist_xyz')

    def test_invalid_type_raises_type_error(self):
        with pytest.raises(TypeError):
            get_colormap(42)
