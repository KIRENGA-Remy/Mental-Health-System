import pandas as pd

def fetch_appointments_as_dataframe(appointments):
    """
    Converts a list of appointments (e.g., QuerySet or list of dictionaries) to a pandas DataFrame.
    """
    data = [
        {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "status": appointment.status,
            "created_at": appointment.created_at,
        }
        for appointment in appointments
    ]
    df = pd.DataFrame(data)
    return df
