import datetime

def get_latest_academicPeriod(self) -> dict:
    response = self.r.get(
        f"{self.base_url}/func-bm7-course-prod/AcademicPeriod/Student",
        headers=self.headers,
    )
    if response.status_code == 200:
        latest_academic_period = None
        current_date = datetime.datetime.now()
        for academic_period in response.json():
            term_end_date = datetime.datetime.strptime(academic_period["termEndDate"], "%Y-%m-%dT%H:%M:%S")
            if term_end_date > current_date:
                latest_academic_period = academic_period
                break
        return latest_academic_period
    raise Exception(response.text)

def get_latest_academic_start_end_date(self) -> tuple:
    academic_period = self.get_latest_academicPeriod()
    start_date = datetime.datetime.strptime(academic_period["termBeginDate"], "%Y-%m-%dT%H:%M:%S")
    end_date = datetime.datetime.strptime(academic_period["termEndDate"], "%Y-%m-%dT%H:%M:%S")
    return start_date, end_date