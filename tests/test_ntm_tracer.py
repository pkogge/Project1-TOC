from pathlib import Path
import pytest

from src.ntm_tracer import NTM_Tracer

# Resolve project root correctly (Project1-TOC)
ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "input"


def test_aplus_aaa():
    tracer = NTM_Tracer(str(INPUT / "aplus.tm"))
    assert tracer.run("aaa") is True


def test_composite_111111():
    tracer = NTM_Tracer(str(INPUT / "composite.tm"))
    assert tracer.run("111111") is True


def test_third_machine():
    tracer = NTM_Tracer(str(INPUT / "third.tm"))
    assert tracer.run("101") is True
