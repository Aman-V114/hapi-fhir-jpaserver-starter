from fastapi import FastAPI, HTTPException
import requests
import logging
import json

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.ERROR)

# HAPI FHIR Server Base URL (change if needed)
FHIR_SERVER_URL = "http://localhost:8080/fhir"


# Fetch a Patient by ID
@app.get("/patients/{patient_id}/_history/{version_id}")
def get_patient_version(patient_id: str, version_id: str):
    try:
        url = f"{FHIR_SERVER_URL}/Patient/{patient_id}/_history/{version_id}?_pretty=true"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail="Patient version not found")
    except Exception as e:
        logging.error(f"Error fetching patient version: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
	

# Create a New Patient
@app.post("/patients")
def create_patient(patient_data: dict):
    try:
        url = f"{FHIR_SERVER_URL}/Patient?_format=json&_pretty=true"
        patient_data_json = json.dumps(patient_data)
        response = requests.post(url, data=patient_data_json, headers={"Content-Type": "application/fhir+json"})
        if response.status_code in [200, 201]:
            patient_id = response.json().get("id")
            print(f"Created patient with ID: {patient_id}")
            return response.json()
        raise HTTPException(status_code=response.status_code, detail="Failed to create patient")
    except Exception as e:
        logging.error(f"Error creating patient: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Update an Existing Patient
@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient_data: dict):
    try:
        print(patient_data)
        url = f"{FHIR_SERVER_URL}/Patient/{patient_id}?_format=json&_pretty=true"
        response = requests.put(url, json=patient_data, headers={"Content-Type": "application/fhir+json"})
        if response.status_code in [200, 201]:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail="Failed to update patient")
    
    except Exception as e:
        logging.error(f"Error updating patient: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Delete a Patienst
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    try:
        url = f"{FHIR_SERVER_URL}/Patient/{patient_id}"
        response = requests.delete(url)
        if response.status_code == 200:
            return {"message": "Patient deleted successfully"}
        raise HTTPException(status_code=response.status_code, detail="Failed to delete patient")
    except Exception as e:
        logging.error(f"Error deleting patient: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




# # Fetch an Organization by ID
# @app.get("/organizations/{organization_id}")
# def get_organization(organization_id: str):
#     try:
#         url = f"{FHIR_SERVER_URL}/Organization/{organization_id}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()
#         raise HTTPException(status_code=response.status_code, detail="Organization not found")
#     except Exception as e:
#         logging.error(f"Error fetching organization: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


# # Create a New Organization
# @app.post("/organizations")
# def create_organization(organization_data: dict):
#     try:

#         url = f"{FHIR_SERVER_URL}/Organization"
#         organization_data_json = json.dumps(organization_data)
#         response = requests.post(url, data=organization_data_json, headers={"Content-Type": "application/fhir+json"})

#         if response.status_code in [200, 201]:
#             return response.json()
#         raise HTTPException(status_code=response.status_code, detail="Failed to create organization")

#     except Exception as e:
#         logging.error(f"Error creating organization: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")



# # Update an Existing Organization
# @app.put("/organizations/{organization_id}")
# def update_organization(organization_id: str, organization_data: dict):
#     try:
#         url = f"{FHIR_SERVER_URL}/Organization/{organization_id}"
#         response = requests.put(url, json=organization_data, headers={"Content-Type": "application/fhir+json"})
#         if response.status_code in [200, 201]:
#             return response.json()
#         raise HTTPException(status_code=response.status_code, detail="Failed to update organization")
#     except Exception as e:
#         logging.error(f"Error updating organization: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


# # Delete an Organization
# @app.delete("/organizations/{organization_id}")
# def delete_organization(organization_id: str):
#     try:
#         url = f"{FHIR_SERVER_URL}/Organization/{organization_id}"
#         response = requests.delete(url)
#         if response.status_code == 200:
#             return {"message": "Organization deleted successfully"}
#         raise HTTPException(status_code=response.status_code, detail="Failed to delete organization")
#     except Exception as e:
#         logging.error(f"Error deleting organization: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


def start():
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    start()