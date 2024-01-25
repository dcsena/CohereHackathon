class JobDescription:
    def __init__(self, job_id, role, department, location,
                 work_type, location_type, role_description):
        self.job_id = job_id
        self.role = role
        self.department = department
        self.location = location
        self.work_type = work_type
        self.location_type = location_type
        self.role_description = role_description

    def to_dict(self):
        return {
            "jobId": self.job_id,
            "role": self.role,
            "department": self.department,
            "location": self.location,
            "workType": self.work_type,
            "locationType": self.location_type,
            "roleDescription": self.role_description
        }
