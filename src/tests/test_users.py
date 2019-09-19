from nf_web.users.models import User, Job


def test_create_user(db, app):
    email = "pupkin@kremlin.ru"
    _ = User.create_user(app, db, email, "pup")
    db_user = db.session.query(User).filter(User.email==email).all()[0]
    assert db_user.email == email


def test_get_user_jobs(db, app):
    email = "pupkin@kremlin.ru"
    # user1 = User.create_user(app, db, email, "pup")
    user1 = db.session.query(User).filter(User.email == email).all()[0]
    user2 = User.create_user(app, db, email.replace("p", "d"), "pup")
    jobname1 = "kj32"
    jobname2 = "jk34"
    job1 = Job(job_id=jobname1, user_id=user1.id)
    job2 = Job(job_id="kj33", user_id=user1.id)
    job3 = Job(job_id=jobname2, user_id=user2.id)
    db.session.add(job1)
    db.session.add(job2)
    db.session.add(job3)
    db.session.commit()
    for job in db.session.query(Job).all():
        print(job.job_id)
    assert len(user1.jobs) == 2
    assert user1.jobs[0].job_id == jobname1
    assert user2.jobs[0].job_id == jobname2
