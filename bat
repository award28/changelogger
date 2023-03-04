diff --git a/changelogger/app/__init__.py b/changelogger/app/__init__.py
index 3179778..3232bc2 100644
--- a/changelogger/app/__init__.py
+++ b/changelogger/app/__init__.py
@@ -8,7 +8,7 @@ from rich import print
 from changelogger.app._commands.init import init
 from changelogger.app.manage import app as manage_app
 from changelogger.app.manage._commands.check import check
-from changelogger.app.manage._commands.content import content
+from changelogger.app.manage._commands.notes import notes
 from changelogger.app.manage._commands.upgrade import upgrade
 from changelogger.app.manage._commands.versions import versions
 from changelogger.app.unreleased import app as unrealeased_app
@@ -28,7 +28,7 @@ app.command()(init)
 # Management Commands
 app.command()(upgrade)
 app.command()(check)
-app.command()(content)
+app.command()(notes)
 app.command()(versions)


diff --git a/changelogger/app/manage/__init__.py b/changelogger/app/manage/__init__.py
index ebf0d08..cb8686f 100644
--- a/changelogger/app/manage/__init__.py
+++ b/changelogger/app/manage/__init__.py
@@ -1,14 +1,14 @@
 import typer

 from changelogger.app.manage._commands.check import check
-from changelogger.app.manage._commands.content import content
+from changelogger.app.manage._commands.notes import notes
 from changelogger.app.manage._commands.upgrade import upgrade
 from changelogger.app.manage._commands.versions import versions

 app = typer.Typer()
 app.command()(upgrade)
 app.command()(check)
-app.command()(content)
+app.command()(notes)
 app.command()(versions)


diff --git a/changelogger/app/manage/_commands/check.py b/changelogger/app/manage/_commands/check.py
index 28b67b7..fd268ac 100644
--- a/changelogger/app/manage/_commands/check.py
+++ b/changelogger/app/manage/_commands/check.py
@@ -1,22 +1,28 @@
+import typer
 from rich import print

+
 from changelogger import changelog
 from changelogger.exceptions import ValidationException


 def check(
-    sys_exit: bool = False,
+    sys_exit: bool = typer.Option(
+        False,
+        "--sys-exit",
+        "--fail",
+        help="Exit with a status of 2 if any versioned files are invalid.",
+    ),
 ) -> None:
-    """Checks the Changelog file for any parts which do not meet changelogger's
-    expectations and reports them to the user. Can optionally system exit
-    for CI/CD failure.
+    """Checks the versioned files for any unparsable sections which do not match
+     the Changelogger configuration and reports them.
     """
     try:
         _check()
     except ValidationException as e:
         print(f"[bold red]Error:[/bold red] {str(e)}")
         if sys_exit:
-            exit(1)
+            raise typer.Exit(code=2)
     else:
         print(
             ":white_heavy_check_mark: [bold green]All versioned files are valid![/bold green]"
diff --git a/changelogger/app/manage/_commands/content.py b/changelogger/app/manage/_commands/content.py
deleted file mode 100644
index 772dd89..0000000
--- a/changelogger/app/manage/_commands/content.py
+++ /dev/null
@@ -1,27 +0,0 @@
-from rich import print
-from rich.markdown import Markdown
-
-from changelogger import changelog
-from changelogger.exceptions import CommandException
-from changelogger.models.domain_models import VersionInfo
-
-
-def content(
-    version: str,
-    pretty: bool = True,
-) -> None:
-    version_info = VersionInfo.parse(version)
-    """Retrieves the changelog content for the specified version."""
-    all_versions = changelog.get_all_versions()
-    if version_info not in all_versions:
-        raise CommandException(f"Could not find version {version}.")
-
-    i = all_versions.index(version_info)
-    prev_version = all_versions[i + 1] if i + 1 < len(all_versions) else None
-    release_notes = changelog.get_release_notes(version_info, prev_version)
-
-    md = release_notes.markdown()
-    if pretty:
-        print(Markdown(md))
-    else:
-        print(md)
