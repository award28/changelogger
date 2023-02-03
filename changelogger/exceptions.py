class CommandException(Exception):
    ...


class UpgradeException(CommandException):
    ...


class RollbackException(UpgradeException):
    ...


class ValidationException(Exception):
    ...
