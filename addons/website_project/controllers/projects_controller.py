import logging

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class ProjectsList(http.Controller):
    @http.route('/projects', type='http', auth='public', website=True)
    def get_list_of_projects(self):
        data = {'projects': []}

        projects = request.env['project.project'].search([('display_on_website', '=', True)])
        for project in projects:
            duration = f'{project.date_start if project.date_start else "???"} — {project.date if project.date else "Настоящее время"}'
            leader = f'Руководитель: {project.user_id.name}'
            project_href = f'/projects/{project.name}'
            tags = [{'name': tag.name, 'color': tag.color} for tag in project.tag_ids]

            data['projects'].append({'name': project.name,
                                     'number': project.x_project_number,
                                     'leader': leader,
                                     'duration': duration,
                                     'project_href': project_href,
                                     'tags': tags})

        return request.render("website_project.projects_list", data)

    @http.route('/projects/<string:project_name>', type='http', auth='public', website=True)
    def get_project_info(self, project_name: str):
        project = request.env['project.project'].search(['&',
                                                         ('name', '=', project_name),
                                                         ('display_on_website', '=', True)])
        if len(project) > 0:
            project = project[0]
        else:
            raise ValidationError('No such project!')

        data = {
            'name': project.name,
            'leader': project.user_id.name,
            'number': project.x_project_number,
            'description': project.description,
            'members': [member.name for member in project.x_project_members],
        }

        return request.render("website_project.project_page", data)
