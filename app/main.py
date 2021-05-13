import multiprocessing

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .configs import config

from check_scheduler.utils.add_users import HandleData
from check_scheduler.run_checks import Scheduler
import check_scheduler.utils.loggers as lg

app = FastAPI(title="Vaccine Slot Availability",
              description="Get notifications about vaccination slot openings",
              version="0.0.1")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
data = HandleData(lg, config.settings)
workers = []

def run_scheduler():
	sch = Scheduler(config.settings)
	sch.run()

@app.on_event("startup")
async def run_schedulers():
	data.download_csv()
	lg.web.info("Starting scheduler for periodic checks..")
	process = multiprocessing.Process(target=run_scheduler, name="check_scheduler",daemon=True)
	workers.append(process)
	lg.web.info(f"{len(workers)} processes started...")
	process.start()
	lg.web.info("Startup tasks complete!")

@app.on_event("shutdown")
async def app_shutdown():
	lg.web.info("Performing shutdown activities...")
	data.shutdown_upload()
	lg.web.info("Killing processes...")
	for wk in workers:
		lg.web.info(f"Terminating process: '{wk.name}'")
		wk.terminate()
	lg.web.info("Done killing processes! App will shutdown now... :(")

@app.get("/", response_class=HTMLResponse)
async def submit(request: Request):
	response = {
		"user_info": "Add User Details"
	}
	return templates.TemplateResponse("index.html", {"request": request, "response": response})

@app.post("/", response_class=HTMLResponse)
async def submit(request: Request,
                 firstname: str = Form(...),
                 lastname: str = Form(...),
                 number: int = Form(...),
                 email: str = Form(...)):
	try:
		user_info = {
			"fname": firstname,
			"lname": lastname,
			"number": number,
			"email": email,
		}
		lg.web.info("Received user data: ", user_info)
		print("Received user data: ", user_info)
		data.add_user(user_info)

	except Exception as e:
		print(e)
	return templates.TemplateResponse("thank_you.html", {"request": request, "result": "Done"})
