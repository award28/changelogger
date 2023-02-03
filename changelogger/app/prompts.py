from contextlib import contextmanager

from rich import print
from rich.markdown import Markdown

from changelogger.exceptions import RollbackException, UpgradeException
from changelogger.models.domain_models import ChangelogUpdate


def prompt_unreleased_changelog(update: ChangelogUpdate) -> ChangelogUpdate:
    for name, notes in update.release_notes.dict().items():
        done = False
        print(Markdown(f"## Updating **{name.title()}**"))
        while not done:
            print(f"Any further additions for [bold]{name.title()}[/bold]?")
            print(notes)
            if new_note := input("New note [Enter to continue]: "):
                notes.append(new_note)
            else:
                done = True
        update.release_notes[name] = notes
    return update


@contextmanager
def rollback_handler():
    try:
        yield
    except UpgradeException as e:
        print(f"[bold red]Failed to update.[/bold red] {str(e)}")
        if isinstance(e, RollbackException):
            note = "MANUAL INTERVENTION REQUIRED to fix versioned files."
            print(f"\n[bold red]{note}[/bold red]")
