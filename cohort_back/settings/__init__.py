from rest_framework.request import Request
from cohort_back.FhirAPi import FhirCountResponse, FhirCohortResponse, FhirValidateResponse


# called to format a json query stored in RequestQuerySnapshot to the format read by Fhir API
def format_json_request(json_req: str) -> str:
    raise NotImplementedError()


# called when a request is about to be made to external Fhir API
def get_fhir_authorization_header(request: Request) -> dict:
    raise NotImplementedError()

# called to retrieve care_site_ids (perimeters) from a Json request
def retrieve_perimeters(json_req: str) -> [str]:
    return None

# called to ask a Fhir API to compute the size of a cohort given the request in the json_file
def post_count_cohort(json_file: str, auth_headers) -> FhirCountResponse:
    raise NotImplementedError()


# called to ask a Fhir API to create a cohort given the request in the json_file
def post_create_cohort(json_file: str, auth_headers) -> FhirCohortResponse:
    raise NotImplementedError()


# called to ask a Fhir API to validate the format of the json_file
def post_validate_cohort(json_file: str, auth_headers) -> FhirValidateResponse:
    raise NotImplementedError()
