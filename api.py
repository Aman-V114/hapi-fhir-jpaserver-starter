from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# HAPI FHIR Server Base URL (change if needed)
FHIR_SERVER_URL = "http://localhost:8080/fhir"

# Fetch a Patient by ID
@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    url = f"{FHIR_SERVER_URL}/Patient/{patient_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail="Patient not found")

# Create a New Patient
@app.post("/patients")
def create_patient(patient_data: dict):
    
    url = f"{FHIR_SERVER_URL}/Patient"
    response = requests.post(url, json=patient_data, headers={"Content-Type": "application/fhir+json"})
    

    if response.status_code in [200, 201]:
        return response.json()
    
    raise HTTPException(status_code=response.status_code, detail="Failed to create patient")



# Update an Existing Patient
@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient_data: dict):
    url = f"{FHIR_SERVER_URL}/Patient/{patient_id}"
    response = requests.put(url, json=patient_data, headers={"Content-Type": "application/fhir+json"})
    if response.status_code in [200, 201]:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail="Failed to update patient")

# Delete a Patient
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    url = f"{FHIR_SERVER_URL}/Patient/{patient_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        return {"message": "Patient deleted successfully"}
    raise HTTPException(status_code=response.status_code, detail="Failed to delete patient")

if __name__ == "__main__":
    
    import uvicorn

    uvicorn.run(app, host="127.0.0.1",port=8000)

#Showing sample requests

