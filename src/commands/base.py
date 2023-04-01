from abc import ABC, abstractmethod
from typing import Optional

from src.exceptions import CommandException


class BaseCommand(ABC):
	
	@abstractmethod
	def execute(self) -> None:
		raise NotImplementedError


class BaseMacroCommand(BaseCommand):
	
	def __init__(self, commands: Optional[list[BaseCommand]] = None) -> None:
		self._commands = [] if commands is None else commands
	
	def add_command(self, command: BaseCommand) -> None:
		self._commands.append(command)
	
	def execute(self) -> None:
		for command in self._commands:
			try:
				command.execute()
			except Exception as e:
				raise CommandException from e
