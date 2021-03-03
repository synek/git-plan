"""List command

@author Rory Byrne <rory@rory.bio>
"""
from git_plan.cli.commands.command import Command
from git_plan.model.project import Project
from git_plan.service.plan import PlanService
from git_plan.service.ui import UIService


class List(Command):
    """List commits."""

    subcommand = 'list'

    def __init__(self, plan_service: PlanService, ui_service: UIService, working_dir: str):
        assert plan_service, "Plan service not injected"
        assert working_dir, "Working dir not injected"
        self._plan_service = plan_service
        self._ui_service = ui_service
        self._project = Project.from_working_dir(working_dir)

        super().__init__()

    def pre_command(self):
        """Check whether a plan already exists?"""
        pass

    def command(self):
        """Use the PlanService to create the plan in the local .git/ directory

        1. Present a VIM editor with the PLAN_MSG template
        2. Save the result to a stable location
        3. Launch an observer to watch the development environment
            3a. When does the observer terminate?
        """
        commits = self._plan_service.get_commits(self._project)
        return self._ui_service.render_commits(commits, headline_only=False)
