import os
from typing import Dict

from flask import redirect, url_for, render_template, request, Blueprint, current_app as app
from flask_user import login_required, current_user
from werkzeug.utils import secure_filename
from wtforms import Form, StringField, FileField

from nf_web.client import ProcessingClient, OddJobClient
from nf_web.users.models import Job, User
from nf_web.app import db

pr = ProcessingClient(os.getenv("PROCESSING_HOST"))
oj = OddJobClient(os.getenv("ODDJOB_HOST"))
main_blueprint = Blueprint('main', __name__)


class WorkflowForm(Form):

    @classmethod
    def get_form(cls, wf: Dict, formdata=None):
        setattr(cls, "wf", wf)
        for p in wf.get("parameters"):
            if p['type'] == 'array':
                setattr(cls, p['name'], FileField(p['name']))
            else:
                setattr(cls, p['name'], StringField(p['name']))
        return cls(formdata)

    def get_params(self) -> Dict:
        params = {}
        for p in self.wf.get("parameters"):
            param = getattr(self, p['name']).data
            params[p["name"]] = param
        return params


@main_blueprint.route('/')
def hello():
    return redirect(url_for('main.status'))


@main_blueprint.route('/status/')
@login_required
def status():
    template = "status.html"
    oj.trigger_task_job_check()
    workflows = pr.get_jobs()
    statuses = oj.check_job(list(wf['job_id'] for wf in workflows))
    print(statuses)
    for status, wf in zip(statuses, workflows):
        wf['status'] = status['status']
    print(workflows)
    return render_template(template, workflows=workflows, user=current_user)


@main_blueprint.route('/workflows/')
@login_required
def workflows():
    template = "workflows.html"
    workflows = pr.get_components()
    user = User.get_by_name(current_user)
    user_jobs = user.get_jobs()
    return render_template(template, workflows=workflows, user=current_user)


@main_blueprint.route('/workflow/<wf_id>/', methods=["GET", "POST"])
@login_required
def workflow(wf_id):
    template = "workflow.html"
    wf = pr.get_component(wf_id)
    if request.method == 'GET':
        form = WorkflowForm.get_form(wf)
        return render_template(template, wf=wf, form=form)
    elif request.method == 'POST':
        form = WorkflowForm.get_form(wf, request.form)
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        file = request.files.get('file', '')
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
        job_id = pr.post_components_groups(component_id=wf_id, group_id="", params=form.get_params())
        job = Job(id=int(job_id), user_id=User.get_by_name(current_user))
        db.session.add(job)
        db.session.commit()
        oj.trigger_task_job_submit()
        return redirect(url_for("main.status"))
