from textwrap import dedent
from unittest.mock import MagicMock, patch

import pytest

from changelogger import changelog
from changelogger.exceptions import RollbackException, UpgradeException


class TestChangelog:
    @pytest.fixture
    def mock_settings(self):
        with patch("changelogger.changelog.settings") as mock:
            yield mock

    @pytest.fixture
    def mock_update_with_jinja(self):
        with patch("changelogger.changelog.update_with_jinja") as mock:
            yield mock

    @pytest.fixture
    def mock_rollback(self):
        with patch("changelogger.changelog._rollback") as mock:
            yield mock

    def test_get_all_links(
        self,
        mock_settings: MagicMock,
    ) -> None:
        v420 = "4.2.0"
        v410 = "4.1.0"
        v400 = "4.0.0"
        content = f"""
        [{v420}]: https://some-link.com/{v420}
        [{v410}]: https://some-link.com/{v410}
        [{v400}]: https://some-link.com/{v400}
        Not a link with a link
        """
        mock_settings.CHANGELOG_PATH.read_text.side_effect = (content,)
        links = changelog.get_all_links()
        versions = [v420, v410, v400]
        for v in versions:
            assert v in links
            assert links[v] == f"https://some-link.com/{v}"

        for key in links.keys():
            assert key in versions

    def test_get_all_versions(
        self,
        mock_settings: MagicMock,
    ) -> None:
        v420 = "4.2.0"
        v410 = "4.1.0"
        v400 = "4.0.0"
        content = f"""
        ### [{v420}]
        ### [{v410}]
        ### [{v400}]
        Not a version
        """
        mock_settings.CHANGELOG_PATH.read_text.side_effect = (content,)
        all_versions = changelog.get_all_versions()
        expected_versions = [v420, v410, v400]
        assert all_versions == expected_versions

    def test_get_sorted_versions(
        self,
        mock_settings: MagicMock,
    ) -> None:
        v420 = "4.2.0"
        v410 = "4.1.0"
        v400 = "4.0.0"
        content = f"""
        ### [{v420}]
        ### [{v410}]
        ### [{v400}]
        Not a version
        """
        mock_settings.CHANGELOG_PATH.read_text.side_effect = (content,)
        all_versions = changelog.get_sorted_versions()
        expected_versions = [v400, v410, v420]
        assert all_versions == expected_versions

    def test_get_latest_versions(
        self,
        mock_settings: MagicMock,
    ) -> None:
        v243 = "2.4.3"
        v420 = "4.2.0"
        v410 = "4.1.0"
        v400 = "4.0.0"
        content = f"""
        ### [{v243}]
        ### [{v420}]
        ### [{v410}]
        ### [{v400}]
        Not a version
        """
        mock_settings.CHANGELOG_PATH.read_text.side_effect = (content,)
        latest_version = changelog.get_latest_version()
        assert latest_version == v420

    def test_get_latest_versions_no_versions(
        self,
        mock_settings: MagicMock,
    ) -> None:
        content = f"""
        Not a version
        """
        mock_settings.CHANGELOG_PATH.read_text.side_effect = (content,)
        with pytest.raises(UpgradeException):
            changelog.get_latest_version()

    def test_get_release_notes_no_match_raises(
        self,
        mock_settings,
    ):
        content = ""
        mock_settings.CHANGELOG_PATH.read_text.side_effect = (content,)
        with pytest.raises(UpgradeException) as excinfo:
            changelog.get_release_notes("", "")

        assert excinfo.value.args == ("Could not extract release notes.",)

    def test_get_release_notes(
        self,
        mock_settings,
    ):
        v420 = "4.2.0"
        v410 = "4.1.0"
        v400 = "4.0.0"

        note1 = "some note"
        note2 = "some other note"
        content = dedent(
            f"""
        ### [{v420}]

        #### Added
        - {note1}
        - {note2}

        ### [{v410}]

        #### Deprecated
        - it's a me, deprecated

        ### [{v400}]
        """
        )
        mock_settings.CHANGELOG_PATH.read_text.side_effect = (content,)
        release_notes = changelog.get_release_notes(v420, v410)
        assert not release_notes.deprecated
        assert note1 in release_notes.added
        assert note2 in release_notes.added

    def test_rollback(
        self,
    ):
        path = MagicMock()
        content = "Some content"
        changelog._rollback([(path, content)])

        path.write_text.assert_called_once_with(content)

    def test_upgrade_versioned_files_raises_upgrade_exc(
        self,
        mock_update_with_jinja,
    ):
        update_fn = mock_update_with_jinja()
        update_fn.side_effect = Exception("oops")

        update = MagicMock()
        versioned_file = MagicMock()

        with pytest.raises(UpgradeException):
            changelog.update_versioned_files(
                update=update, versioned_files=[versioned_file]
            )

    def test_upgrade_versioned_files_raises_rollback_exc(
        self,
        mock_update_with_jinja,
        mock_rollback,
    ):
        update_fn = mock_update_with_jinja()
        update_fn.side_effect = Exception("oops")
        mock_rollback.side_effect = Exception("double oops")

        update = MagicMock()
        versioned_file = MagicMock()

        with pytest.raises(RollbackException):
            changelog.update_versioned_files(
                update=update, versioned_files=[versioned_file]
            )

    def test_upgrade_versioned_files(
        self,
        mock_update_with_jinja,
        mock_rollback,
    ):
        update = MagicMock()
        versioned_file = MagicMock()

        changelog.update_versioned_files(
            update=update, versioned_files=[versioned_file]
        )

        mock_update_with_jinja.assert_called_once_with(versioned_file)
        mock_rollback.assert_not_called()
