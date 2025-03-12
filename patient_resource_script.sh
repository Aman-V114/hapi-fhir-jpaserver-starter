#!/bin/bash

# URL of the FHIR server metadata endpoint
FHIR_METADATA_URL="http://localhost:8080/fhir/metadata"

# Send a GET request to the FHIR server metadata endpoint
response=$(curl -s -X GET "$FHIR_METADATA_URL" -H "Accept: application/fhir+json")

# Check if the response contains the Patient resource information
if echo "$response" | grep -q '"type": "Patient"'; then
  echo "Patient resource information found:"
  echo "$response" | jq '.rest[].resource[] | select(.type == "Patient")'
else
  echo "Patient resource information not found."
fi

