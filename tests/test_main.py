#!/usr/bin/env python
"""Tests for `app` package."""
# pylint: disable=redefined-outer-name


import pytest
from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """


def test_app_creates_db():
    result = runner.invoke(app, ["create-db"])
    assert result.exit_code == 0
    assert "Database create complete" in result.stdout
