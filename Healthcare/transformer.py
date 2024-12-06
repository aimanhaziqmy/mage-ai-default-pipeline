import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    #-- Convert all dates to datetime
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    # -- Rename the columns
    df.rename(columns={'Name':'name','Age':'age','Billing Amount': 'billing_amount','Blood Type': 'blood_type','Medical Condition': 'medical_condition','Date of Admission':'date_admission', 'Doctor': 'doctor_name', 'Insurance Provider': 'insurance_provider','Gender': 'gender'}, inplace=True)

    # Set patientID
    df = df.drop_duplicates().reset_index(drop=True)
    df['patient_id'] = df.index

    # Blood Type Dimensions
    blood_type_dim = df[['blood_type']].drop_duplicates().reset_index(drop=True)
    blood_type_dim['blood_type_id'] = blood_type_dim.index
    blood_type_dim = blood_type_dim[['blood_type_id','blood_type']]

    # Medical Condition Dimensions
    medical_condition_dim = df[['medical_condition']].drop_duplicates().reset_index(drop=True)
    medical_condition_dim['medical_condition_id'] = medical_condition_dim.index
    medical_condition_dim = medical_condition_dim[['medical_condition_id','medical_condition']]

    # DateTime Admission Dimensions
    date_admission_dim = df[['date_admission']].drop_duplicates().reset_index(drop=True)
    #--Extract Datetime
    date_admission_dim['date_admission_day'] = date_admission_dim['date_admission'].dt.day
    date_admission_dim['date_admission_month'] = date_admission_dim['date_admission'].dt.month
    date_admission_dim['date_admission_year'] = date_admission_dim['date_admission'].dt.year
    date_admission_dim['date_admission_id'] = date_admission_dim.index

    date_admission_dim = date_admission_dim[['date_admission_id', 'date_admission', 'date_admission_day', 'date_admission_month', 'date_admission_year']]

    # Doctor Dimensions
    doctor_dim = df[['doctor_name']].drop_duplicates().reset_index(drop=True)
    doctor_dim['doctor_id'] = doctor_dim.index
    doctor_dim = doctor_dim[['doctor_id','doctor_name']]

    # Insurance Provider Dimensions
    insurance_provider_dim = df[['insurance_provider']].drop_duplicates().reset_index(drop=True)
    insurance_provider_dim['insurance_provider_id'] = insurance_provider_dim.index
    insurance_provider_dim = insurance_provider_dim[['insurance_provider_id', 'insurance_provider']]

    # Gender Dimensions
    gender_dim = df[['gender']].drop_duplicates().reset_index(drop=True)
    gender_dim['gender_id'] = gender_dim.index
    gender_dim = gender_dim[['gender_id', 'gender']]

    fact_table = df.merge(blood_type_dim, on='blood_type') \
    .merge(medical_condition_dim, on='medical_condition') \
    .merge(date_admission_dim, on='date_admission') \
    .merge(doctor_dim, on='doctor_name') \
    .merge(insurance_provider_dim, on='insurance_provider') \
    .merge(gender_dim, on='gender') \
    [['patient_id', 'name', 'age', 'billing_amount', 
    'blood_type_id','medical_condition_id','date_admission_id','doctor_id', 
    'insurance_provider_id','gender_id']]
  
    return {
        'blood_type_dim': blood_type_dim,
        'medical_condition_dim' : medical_condition_dim,
        'date_admission_dim' : date_admission_dim,
        'doctor_dim' : doctor_dim,
        'insurance_provider_dim' : insurance_provider_dim,
        'gender_dim' : gender_dim,
        'fact_table' : fact_table
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
