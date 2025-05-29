from datetime import datetime
import re

# ===================================================
# PIPELINE STEPS
# ===================================================

# possible pipeline steps: preparing, tab_to_tab_sdg, text_to_tab_sdg_shuffle, text_to_tab_sdg
# evaluate_fidelity, evaluate_privacy, evaluate_utility, evaluate, evaluate_agg, describe_data
PIPELINE_STEPS_TO_PERFORM = [
    # "preparing",
    #"tab_to_tab_sdg",
    "text_to_tab_sdg_shuffle",
    # "describe_data",
    #"evaluate",
    # "evaluate_fidelity",
    # "evaluate_privacy"
]

DATABASE = "wellconnect" #"adni" # ppmi2024 OR ppmi OR wellconnect
RAW_SDG = "deepseek/deepseek-r1-0528:free" #"gpt-4-turbo" # gpt-4-turbo, ctgan, tvae, copula, mistral-large-largest, gpt-3.5-turbo
# Create a filesystem‐friendly version
SDG_MODEL = RAW_SDG
SDG_MODEL_FS = re.sub(r"[/:]", "_", SDG_MODEL)

RANDOM_STATE = 1
N_ROWS = 10
N_SAMPLE = 1000
# name of prompt if GPT model OR name of database if standard SDG model
PROMPT_ID = "wellconnect_prompt" #"adni_prompt" #"ppmi_prompt #"wellconnect_prompt"
DATE = (
    datetime.today().strftime("%Y-%m-%d")
)

# train test split: N_Splits with N_Synth generated at each split
train_test_splits = {"split1": {"split": 0.3, "random_state": 7, "n_runs": [1, 2, 3, 4, 5]},
"split2": {"split": 0.3, "random_state": 123, "n_runs": [1, 2, 3, 4, 5]},
"split3": {"split": 0.3,"random_state": 10, "n_runs": [1, 2, 3, 4, 5]},
"split4": {"split": 0.3, "random_state": 69, "n_runs": [1, 2, 3, 4, 5]},
"split5": {"split": 0.3, "random_state": 43, "n_runs": [1, 2, 3, 4, 5]}}


MLFLOW_URI = "file:mlruns/"
MLFLOW_EXPERIMENT_NAME = "main_exp_mt"

# ===================================================
# DATA PATHs
# ===================================================

BUCKET_NAME = "" #"s3-common-dev20231127224849095700000002"
PATH_RAW_DATA = f"raw_data/{DATABASE}/"
PATH_TEMP_DATA = f"temp_data/{SDG_MODEL_FS}/"

FILE_DB_DATA = {"ppmi": "PPMI_Original_Cohort_BL_to_Year_5_Dataset_Apr2020.csv",
                "ppmi2024": "PPMI_Curated_Data_Cut_Public_20240129.csv",
                "adni": "ADNIMERGE_15Oct2024.csv"}
FILE_PPMI_RAW_DATA = FILE_DB_DATA.get(DATABASE)


# ------------output data---------------
# metadata
PATH_METADATA = f"output_data/{SDG_MODEL_FS}/metadata/"
FILE_METADATA = f"metadata_{SDG_MODEL_FS}_{DATABASE}.txt"

# prepared data
PATH_PREPARED_DATA = f"output_data/prepared_data/{DATABASE}/"
FILE_PREPARED_DATA = f"{DATE}_{DATABASE}_prepared_data.csv"

# prompt
FILE_SYNTHESIZED_DATA_PROMPT = f"{DATE}_{DATABASE}_synthesized_data_prompt.txt"
FILE_STATS_DATA_PROMPT = f"{DATE}_{DATABASE}_stats_data_prompt.txt"

# synthetic data
PATH_SYNTH_DATA = f"output_data/{SDG_MODEL_FS}/synthesized_data"
if PROMPT_ID:
    PATH_SYNTH_DATA += f"/{PROMPT_ID}"
FILE_SYNTHESIZED_DATA = f"{DATE}_{DATABASE}_synthesized_data.csv"

# evaluation
PATH_EVALUATE = f"output_data/{SDG_MODEL_FS}/evaluate/train_test_splits"
if PROMPT_ID:
    PATH_EVALUATE += f"/{PROMPT_ID}"

# preprocessed data
PATH_PREPROC_DATA = f"output_data/{SDG_MODEL_FS}/preprocessed_data"
FILE_PREPROC_DATA = f"{DATE}_{DATABASE}_preprocessed_data.csv"

# model
PATH_OUTPUT_DATA = f"output_data/{SDG_MODEL_FS}/"
PATH_MODEL = PATH_OUTPUT_DATA + "models/"

FILE_SYNTHESIZED_DATA_TIME = f"{DATE}_{DATABASE}_{SDG_MODEL_FS}_exec_time.txt"
# Referentials #
PATH_CONF = "conf"

# Feature referential
FILENAME_FEATURE_REFERENTIAL = f"feature_referential_{DATABASE}.xlsx"

## Variable information sheet
REFERENTIAL_INFORMATION_SHEETNAME = "variable_information"
REFERENTIAL_VAR_NAME = "variable_name"
REFERENTIAL_VAR_DESC = "variable_description"
REFERENTIAL_VAR_CLASS = "variable_class"
REFERENTIAL_VAR_NATURE = "variable_nature"
REFERENTIAL_VAR_TYPE = "variable_type"
REFERENTIAL_VAR_CAT_MAPPING = "variable_category_map"

## Variable use sheet
REFERENTIAL_USAGE_SHEETNAME = "variable_use"
REFERENTIAL_USE_MODELLING = "to_use_for_modelling"

# =================================================
# Preparing
# =================================================

COL_PTID = "PTID" #PTID" #PATNO" 
# LIST_FTR_RM = ['DX_bl','VISCODE']#["COHORT", "EVENT_ID"]
LIST_FTR_RM = []

#Features of #PPMI2024
# LIST_FTR = ['PATNO',
#             'COHORT',
#             'EVENT_ID', 
#             'ageonset',
#             'duration',
#             'SEX',
#             'EDUCYRS',
#             'updrs3_score',
#             'updrs2_score',
#             'updrs1_score',
#             'updrs_totscore',
#             'moca',
#             'scopa',
#             'sym_tremor',
#             'sym_rigid',
#             'DATSCAN_PUTAMEN_R',
#             'DATSCAN_PUTAMEN_L']

#list of features ADNI
# LIST_FTR = ['PTID',
#             'DX_bl',
#             'VISCODE',
#             'AGE',
#             'PTGENDER',
#             'PTEDUCAT',
#             'APOE4',
#             'CDRSB',
#             'ADAS11',
#             'MMSE', 
#             'Ventricles_bl',
#             'WholeBrain_bl',
#             'ICV_bl'
#             ]
            
#list of features WellConnect
LIST_FTR = [
    "ParticipantID",
    "PHQ-9-q1",
    "PHQ-9-q2",
    "PHQ-9-q3",
    "PHQ-9-q4",
    "PHQ-9-q5",
    "PHQ-9-q6",
    "PHQ-9-q7",
    "PHQ-9-q8"
    ,"PHQ-9-q9",
    "PHQ-9-total",
    "Age",
    "Sex",
    "Gender",
    "EducationLevel",
    "CountryOfBirth",
    "Nationality",
    "CountryOfBirthMother",
    "CountryOfBirthFather",
    "Ethnicity",
    "Religion",
    "Postcode",
    "EmploymentStatus",
    "TIPI-Extraversion",
    "TIPI-Agreeableness",
    "TIPI-Conscientiousness",
    "TIPI-Neuroticism",
    "TIPI-Openness",
    "PANCRS-Affirmation",
    "PANCRS-ProblemSolving",
    "PANCRS-EnhancingFriendship",
    "PANCRS-TotalPositive",
    "PANCRS-WorryAboutEvaluation",
    "PANCRS-InhibitingHappiness",
    "PANCRS-WorryAboutImpact",
    "PANCRS-Slack",
    "PANCRS-TotalNegative",
    "PANCRS-FrequencyPositive",
    "PANCRS-FrequencyNegative",
    "PANCRS-TotalFrequency",
]



# =================================================
# Prompting
# =================================================
DATABASE_DESCRIPTION_DICT = {
    "mimic_iii": "",
    "ppmi": "PPMI Clinical database. The Parkinson's Progression Markers Initiative (PPMI) is an observational, international study designed to establish biomarker‐defined cohorts and identify clinical, imaging, genetic, and biospecimen Parkinson's disease (PD) progression markers to accelerate disease‐modifying therapeutic trials.",
    "ppmi2024": "PPMI Clinical database. The Parkinson's Progression Markers Initiative (PPMI) is an observational, international study designed to establish biomarker‐defined cohorts and identify clinical, imaging, genetic, and biospecimen Parkinson's disease (PD) progression markers to accelerate disease‐modifying therapeutic trials.",
    "adni": "ADNI data set. The Alzheimer's Disease Neuroimaging Initiative (ADNI) is an observational study designed to develop clinical, imaging, genetic, and biochemical biomarkers for the early detection and tracking of Alzheimer's disease (AD).",
    "wellconnect": "WellConnect data set. WellConnect is a cohort study designed to investigate the effects of social connection on mildly to moderatrely depressed patients (PHQ-9 within 5 to 15) living in Amsterdam, the Netherlands."
}

DATABASE_DESCRIPTION = DATABASE_DESCRIPTION_DICT[DATABASE]

# row example ADNI
# ROW_EXAMPLE = {
#   "0": {
#     "PATNO": "022_S_0004",
#     "AGE": 74,
#     "PTGENDER": 1,
#     "PTEDUCAT": 15.5 ,
#     "APOE4": 1,
#     "CDRSB": 4.3,
#     "ADAS11": 18.6,
#     "MMSE":23.3,
#     "Ventricles_bl": 39300,
#     "WholeBrain_bl": 1066000,
#     "ICV_bl":1500000
#   }
# }


# row example PPMI
# ROW_EXAMPLE = {
#   "0": {
#     "PATNO": 3000,
#     "scopa": 10,
#     "ageonset": 61.7,
#     "updrs_totscore": 33,
#     "DATSCAN_PUTAMEN_L": 0.69,
#     "EDUCYRS": 14,
#     "DATSCAN_PUTAMEN_R": 0.96,
#     "duration": 6.5,
#     "sym_tremor": 1,
#     "SEX": 1,
#     "updrs3_score": 21,
#     "updrs2_score": 6,
#     "moca": 27,
#     "sym_rigid": 1,
#     "updrs1_score": 6
#   }
# }

#row example WellConnect
ROW_EXAMPLE = {
  "0": {
    "ParticipantID": "01621127115",
    "PHQ-9-q1": 1,
    "PHQ-9-q2": 2,
    "PHQ-9-q3": 1,
    "PHQ-9-q4": 2,
    "PHQ-9-q5": 1,
    "PHQ-9-q6": 2,
    "PHQ-9-q7": 1,
    "PHQ-9-q8": 1
    ,"PHQ-9-q9": 1,
    "PHQ-9-total": 12,
    "Age": "18-24 jaar",
    "Sex": "Vrouw",
    "Gender": "Vrouw",
    "EducationLevel": "HBO" ,
    "CountryOfBirth": "Nederland",
    "Nationality": "Nederlands",
    "CountryOfBirthMother": "Marokko",
    "CountryOfBirthFather": "Marokko",
    "Ethnicity": "Marokkaans",
    "Religion": "Islam",
    "Postcode": "1104CA",
    "EmploymentStatus": "Betaalde baan (fulltime)",
    "TIPI-Extraversion": 3.0,
    "TIPI-Agreeableness": 5.5,
    "TIPI-Conscientiousness": 4.0,
    "TIPI-Neuroticism": 2.5,
    "TIPI-Openness": 4.5,
    "PANCRS-Affirmation": 4.00,
    "PANCRS-ProblemSolving": 3.80,
    "PANCRS-EnhancingFriendship": 4.00,
    "PANCRS-TotalPositive": 3.80,
    "PANCRS-WorryAboutEvaluation": 3.20,
    "PANCRS-InhibitingHappiness": 3.00,
    "PANCRS-WorryAboutImpact": 2.80,
    "PANCRS-Slack": 2.40,
    "PANCRS-TotalNegative": 2.80,
    "PANCRS-FrequencyPositive": 3.00,
    "PANCRS-FrequencyNegative": 2.60,
    "PANCRS-TotalFrequency": 2.80,
  }
}

# TEXT2TAB #
# mapping of {prompt_id: prompt info}
# with prompt info = {
# 'prompt': prompt text to use
# 'is_template': whether the prompt is a template on which to apply a .format()
# 'template_items': if the prompt is a template, list the variable names to be substituted using .format()
# 'enrichment_strategy': strategy of prompt enrichment to use. Default to None.
# }

TEXT2TAB_PROMPT_DICT = { 
    "ppmi_prompt": {
        "prompt": f"""Give an example table of {N_ROWS} rows of from the {DATABASE_DESCRIPTION} Only consider untreated PD patients. 
        The table must have one row by patient, no missing values and include all the following columns: 
{COL_PTID}: patient unique identifier, integer""" + """ 
{variables_description}
Return the table as a dictionary in JSON format with keys as index. JSON format strictly requires double quotes for strings. The column names need to be the same than those provided.
Only return the dictionary, do not repeat the question, introduce your answer or comment on it. Do not truncate the table, provide all the rows.

Here is an example for one patient with the associated key of the dictionary to output: 

{row_example}
""",
        "is_template": True,
        "template_items": ["variables_description", "row_example"], 
        "enrichment_strategy": None,
        "text2stats_prompt_id": None,
        "input_stats_prompt_id": None,
    }, 
    "adni_prompt": {
        "prompt": f"""Give an example table of {N_ROWS} rows from {DATABASE_DESCRIPTION} Only consider patients with Alzheimer's Disease diagnosis. 
        The table must have one row by patient, no missing values and include all the following columns: 
{COL_PTID}: patient unique identifier, integer""" + """ 
{variables_description}
Return the table as a dictionary in JSON format with keys as index. JSON format strictly requires double quotes for strings. The column names need to be the same than those provided.
Only return the dictionary, do not repeat the question, introduce your answer or comment on it. Do not truncate the table, provide all the rows.

Here is an example for one patient with the associated key of the dictionary to output: 

{row_example}
""",
        "is_template": True,
        "template_items": ["variables_description", "row_example"], 
        "enrichment_strategy": None,
        "text2stats_prompt_id": None,
        "input_stats_prompt_id": None,
    }, 
    "wellconnect_prompt": { 
        "prompt": f"""Give an example table of {N_ROWS} rows from {DATABASE_DESCRIPTION} Only consider patients with mild to moderate depression (PHQ-9 score between 5 and 15) and only individuals from Amsterdam, the Netherlands. 
        The table must have one row by patient, no missing values and include all the following columns:
{COL_PTID}: patient unique identifier, string""" + """
{variables_description}
Return the table as a dictionary in JSON format with keys as index. JSON format strictly requires double quotes for strings. The column names need to be the same as those provided.
Only return the dictionary, do not repeat the question, introduce your answer or comment on it. Do not truncate the table, provide all the rows.

Here is an example for one patient with the associated key of the dictionary to output:
{row_example}
""",
        "is_template": True,
        "template_items": ["variables_description", "row_example"], 
        "enrichment_strategy": None,
        "text2stats_prompt_id": None,
        "input_stats_prompt_id": None,
    }
}

VAR_DESC_PROMPT_DICT = { 
    "template": "{var_name}: {var_desc}|{var_class}|{var_mapping}| {var_stats}",
    'mapping': {
        "var_name": REFERENTIAL_VAR_NAME,
        "var_class": REFERENTIAL_VAR_CLASS,
        "var_mapping": REFERENTIAL_VAR_CAT_MAPPING,
        "var_desc": REFERENTIAL_VAR_DESC,
        "var_stats": "var_stats"
    }
}

# =================================================
# Evaluation
# =================================================

# ==== fidelity ====
FIDELITY_METRICS_TO_COMPUTE = [
        "KSComplement",
        "TVComplement",
        "CorrelationSimilarity",
        "ContingencySimilarity",
        "WD",
        "JSD",
        "LogisticDetection"
    ]

# ==== privacy ====
PRIVACY_METRICS_TO_COMPUTE = [
        "NewRowSynthesis",
        "DCR",
        "NNDR",
        "CategoricalCAP"
    ]

UTILITY_METRICS_TO_COMPUTE = [
    "BinaryAdaBoostClassifier"
]
# if PPMI database: LIST_KEY_FIELDS = ["SEX", "updrs3_score", "moca"]
# if ADNI database: LIST_KEY_FIELDS = ["PTGENDER", "MMSE", "APOE4"]
LIST_KEY_FIELDS = ["PTGENDER", "MMSE", "APOE4"]
#LIST_KEY_FIELDS = ["SEX", "updrs3_score", "moca"]

# if PPMI database: LIST_SENSITIVE_FIELDS =['EDUCYRS'] 
# if ADNI database: LIST_SENSITIVE_FIELDS = ["PTEDUCAT"]
LIST_SENSITIVE_FIELDS = ["PTEDUCAT"]#['EDUCYRS']
#LIST_SENSITIVE_FIELDS =['EDUCYRS'] 

# if PPMI database: COL_TARGET = "updrs3_score"
# if ADNI database: COL_TARGET = "MMSE"
COL_TARGET = "MMSE" #"updrs3_score"
#COL_TARGET = "updrs3_score"
# =================================================
# TAB2TAB
# =================================================

# tvae / ctgan
BATCH_SIZE = 50
EPOCHS = 300



