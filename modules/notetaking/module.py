import logging
import os
import re
from fastapi import APIRouter, HTTPException, Request
from core.module import LifeLogModule

class NoteTaking(LifeLogModule):
    def __init__(self):
        self.router = APIRouter(prefix="/notetaking", tags=["notetaking"])
        self.templates = self._load_templates()
        self._setup_routes()

    def initialize(self, config: dict) -> bool:
        # Optionally load config for notes
        return True

    def get_name(self) -> str:
        return "notetaking"

    def get_router(self) -> APIRouter:
        return self.router

    def _parse_markdown_template(self, filepath):
        """
        Parse a markdown template file for group and section tags.
        Returns: {"groups": {group: [sections]}, "sections": {section: content}}
        """
        groups = {}
        sections = {}
        current_group = None
        current_section = None
        section_lines = []
        with open(filepath, 'r') as f:
            for line in f:
                group_match = re.match(r'<!--\s*@group:\s*(.+?)\s*-->', line)
                section_match = re.match(r'<!--\s*@section:\s*(.+?)\s*-->', line)
                if group_match:
                    current_group = group_match.group(1).strip()
                    if current_group not in groups:
                        groups[current_group] = []
                elif section_match:
                    # Save previous section
                    if current_section:
                        sections[current_section] = ''.join(section_lines).strip()
                        section_lines = []
                    current_section = section_match.group(1).strip()
                    if current_group:
                        groups[current_group].append(current_section)
                elif current_section:
                    section_lines.append(line)
            # Save last section
            if current_section:
                sections[current_section] = ''.join(section_lines).strip()
        return {"groups": groups, "sections": sections}

    def _load_templates(self):
        """
        Load all .md templates in the templates directory and parse them.
        Returns: {template_name: {groups, sections}}
        """
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        templates = {}
        for fname in os.listdir(templates_dir):
            if fname.endswith('.md'):
                template_name = fname.replace('_notes.md', '').replace('.md', '')
                path = os.path.join(templates_dir, fname)
                templates[template_name] = self._parse_markdown_template(path)
        return templates

    def _setup_routes(self):
        @self.router.get("/templates")
        async def list_templates():
            return self.templates

        @self.router.post("/generate-log")
        async def generate_log(request: Request):
            data = await request.json()
            template = data.get("template")
            sections = data.get("sections", [])
            groups = data.get("groups", [])
            # Combine selected sections/groups into a log
            if template not in self.templates:
                raise HTTPException(status_code=404, detail="Template not found")
            tpl = self.templates[template]
            selected_sections = set(sections)
            for group in groups:
                selected_sections.update(tpl["groups"].get(group, []))
            log_content = '\n\n'.join([tpl["sections"][s] for s in tpl["sections"] if s in selected_sections])
            return {"log": log_content} 