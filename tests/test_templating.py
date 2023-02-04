from unittest.mock import MagicMock, call, patch

import pytest
from freezegun import freeze_time

from changelogger import templating


class TestTemplating:
    @pytest.fixture
    def mock_jinja_environment(self):
        with patch(
            "changelogger.templating.Environment",
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_jinja_base_loader(self):
        with patch(
            "changelogger.templating.BaseLoader",
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_render_variables(self):
        with patch(
            "changelogger.templating._render_variables",
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_tmpl(self):
        with patch(
            "changelogger.templating._tmpl",
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_cached_compile(self):
        with patch(
            "changelogger.templating.cached_compile",
        ) as mock:
            yield mock

    def test_tmpl(
        self,
        mock_jinja_environment: MagicMock,
        mock_jinja_base_loader: MagicMock,
    ) -> None:
        jinja = "Some Template"
        templating._tmpl(jinja)
        mock_jinja_environment.assert_called_once_with(
            loader=mock_jinja_base_loader(),
        )
        mock_jinja_environment().from_string.assert_called_once_with(
            jinja,
        )

    FROZEN_DATE = "2012-01-14"

    @freeze_time(FROZEN_DATE)
    def test_render_variables(
        self,
    ):
        versioned_file = MagicMock()
        update = MagicMock()
        tmpl_variables = templating._render_variables(
            versioned_file=versioned_file,
            update=update,
        )
        assert tmpl_variables["new_version"] == update.new_version
        assert tmpl_variables["old_version"] == update.old_version
        assert str(tmpl_variables["today"]) == self.FROZEN_DATE
        assert tmpl_variables["sections"] == update.release_notes.dict()
        assert tmpl_variables["context"] == versioned_file.context

    def test_update_with_jinja_neither_jinja_raises(
        self,
    ):
        file = MagicMock()
        file.jinja = None
        file.jinja_rel_path = None

        with pytest.raises(AssertionError) as excinfo:
            templating.update_with_jinja(file)

        assert excinfo.value.args == ("No valid jinja template found.",)

    def test_update_with_jinja_from_jinja_string(
        self,
        mock_render_variables,
        mock_tmpl,
        mock_cached_compile,
    ):
        file = MagicMock()
        file.jinja = "jinja"
        file.jinja_rel_path = None

        update_fn = templating.update_with_jinja(file)

        content = "Some content"
        update = MagicMock()
        update_fn(content, update)

        mock_render_variables.assert_called_once_with(file, update)
        mock_tmpl.assert_has_calls(
            [
                call(file.pattern),
                call().render(),
                call(file.jinja),
                call().render(),
            ]
        )

        mock_tmpl().render.assert_has_calls(
            [call(**mock_render_variables())] * 2,
        )

        mock_cached_compile.assert_called_once_with(mock_tmpl().render())
        mock_cached_compile().sub.assert_called_once_with(
            mock_tmpl().render(),
            content,
        )

    def test_update_with_jinja_from_jinja_file(
        self,
        mock_render_variables,
        mock_tmpl,
        mock_cached_compile,
    ):
        file = MagicMock()
        file.jinja = None

        update_fn = templating.update_with_jinja(file)

        content = "Some content"
        update = MagicMock()
        update_fn(content, update)

        mock_render_variables.assert_called_once_with(file, update)
        mock_tmpl.assert_has_calls(
            [
                call(file.pattern),
                call().render(),
                call(file.jinja_rel_path.read_text()),
                call().render(),
            ]
        )

        mock_tmpl().render.assert_has_calls(
            [call(**mock_render_variables())] * 2,
        )

        mock_cached_compile.assert_called_once_with(mock_tmpl().render())
        mock_cached_compile().sub.assert_called_once_with(
            mock_tmpl().render(),
            content,
        )
