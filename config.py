from datetime import datetime
import re
import json

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

DATABASE =  "wellconnect" #"adni" # ppmi2024 OR "ppmi" OR "wellconnect" OR "helius"
RAW_SDG = "meta-llama/llama-4-scout:free"#"deepseek/deepseek-r1-distill-qwen-14b:free"#"meta-llama/llama-4-maverick:free" #"google/gemini-2.5-flash-preview-05-20"#"meta-llama/llama-4-scout:free"#"deepseek/deepseek-prover-v2:free" #"meta-llama/llama-4-maverick:free"#"deepseek/deepseek-prover-v2:free" #"gpt-4-turbo" # gpt-4-turbo, ctgan, tvae, copula, mistral-large-largest, gpt-3.5-turbo
# Create a filesystem‐friendly version
SDG_MODEL = RAW_SDG
SDG_MODEL_FS = re.sub(r"[/:]", "_", SDG_MODEL)

RANDOM_STATE = 1
N_ROWS = 10
N_SAMPLE = 10
# name of prompt if GPT model OR name of database if standard SDG model
PROMPT_ID = "wellconnect_prompt" #"helius_prompt" #"adni_prompt" #"ppmi_prompt 
DATE = (
    datetime.today().strftime("%Y-%m-%d")
)
DATE_TIME = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")


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
FILE_SYNTHESIZED_DATA_PROMPT = f"{DATE_TIME}_{DATABASE}_synthesized_data_prompt.txt"
FILE_STATS_DATA_PROMPT = f"{DATE}_{DATABASE}_stats_data_prompt.txt"

# synthetic data
PATH_SYNTH_DATA = f"output_data/{SDG_MODEL_FS}/synthesized_data"
if PROMPT_ID:
    PATH_SYNTH_DATA += f"/{PROMPT_ID}"
FILE_SYNTHESIZED_DATA = f"{DATE_TIME}_{DATABASE}_synthesized_data.csv"

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

FILE_SYNTHESIZED_DATA_TIME = f"{DATE_TIME}_{DATABASE}_{SDG_MODEL_FS}_exec_time.txt"
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

# #list of features Helius
# LIST_FTR = [
# "questionnaire_completed",
# "physical_examination_completed",
# "date_physical_examination",
# "sex",
# "age",
# "migration_generation",
# "ethnicity",
# "ethnicity_surinamese_subgroups",
# "followup_time_helius1_helius2",
# "marital_status",
# "educational_level",
# "working_status",
# "occupational_level",
# "work_related_recovery_opportunities",
# "quality_of_life_sf12",
# "physical_activity_squash",
# "smoking_status",
# "smoking_packyears",
# "alcohol_use_past_12m_binary",
# "alcohol_use_past_12m_level",
# "body_weight_perception_scores",
# "health_literacy_sbs_scores",
# "health_literacy_realmd_scores",
# "perceived_discrimination",
# "cigarette_dependence_fagerstrom",
# "alcohol_dependence_audit",
# "lifetime_alcohol_dependence",
# "cannabis_dependence_cudit",
# "personality_extraversion_neo_ffi",
# "personality_neuroticism_neo_ffi",
# "dealing_with_everyday_problems_pearlin_schooler_mastery",
# "negative_life_events_nemesis",
# "psychological_stress_interheart",
# "childhood_experiences_nemesis",
# "ptss_problems_unpleasant_experiences",
# "depressive_symptoms_phq9",
# "lifetime_depression",
# "parental_psychological_history_nemesis",
# "social_support_ssq_satisfaction"]



#list of features WellConnect
LIST_FTR = [
    "PHQ9_q1",
    "PHQ9_q2",
    "PHQ9_q3",
    "PHQ9_q4",
    "PHQ9_q5",
    "PHQ9_q6",
    "PHQ9_q7",
    "PHQ9_q8",
    "PHQ9_q9",
    "PHQ9_Total",
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
    "TIPI_Extraversion",
    "TIPI_Agreeableness",
    "TIPI_Conscientiousness",
    "TIPI_Neuroticism",
    "TIPI_Openness",
    "PANCRS_Affirmation",
    "PANCRS_ProblemSolving",
    "PANCRS_EnhancingFriendship",
    "PANCRS_TotalPositive",
    "PANCRS_WorryAboutEvaluation",
    "PANCRS_InhibitingHappiness",
    "PANCRS_WorryAboutImpact",
    "PANCRS_Slack",
    "PANCRS_TotalNegative",
    "PANCRS_FrequencyPositive",
    "PANCRS_FrequencyNegative",
    "PANCRS_TotalFrequency",
]



# schema for enforcing json format
wellconnect_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "wellconnect_features",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "Age":                       { "type": "integer", "description": "Age" },
                "CountryOfBirth":            { "type": "string",  "description": "Country of birth" },
                "CountryOfBirthFather":      { "type": "string",  "description": "Country of birth of father" },
                "CountryOfBirthMother":      { "type": "string",  "description": "Country of birth of mother" },
                "EducationLevel":            { "type": "string",  "description": "Highest level of education achieved" },
                "EmploymentStatus":          { "type": "string",  "description": "Current employment status" },
                "Ethnicity":                 { "type": "string",  "description": "Self-reported ethnicity" },
                "Gender":                    { "type": "string",  "description": "Gender identity" },
                "Nationality":               { "type": "string",  "description": "Nationality" },
                "PANCRS_Affirmation":        { "type": "number",  "description": "PANCRS: Affirmation coping score" },
                "PANCRS_EnhancingFriendship":{ "type": "number",  "description": "PANCRS: Enhancing friendship coping score" },
                "PANCRS_FrequencyNegative":  { "type": "number",  "description": "PANCRS: Frequency of negative coping strategies" },
                "PANCRS_FrequencyPositive":  { "type": "number",  "description": "PANCRS: Frequency of positive coping strategies" },
                "PANCRS_InhibitingHappiness":{ "type": "number",  "description": "PANCRS: Inhibiting happiness coping score" },
                "PANCRS_ProblemSolving":     { "type": "number",  "description": "PANCRS: Problem solving coping score" },
                "PANCRS_Slack":              { "type": "number",  "description": "PANCRS: Slack coping score" },
                "PANCRS_TotalFrequency":     { "type": "number",  "description": "PANCRS: Total frequency of coping strategies" },
                "PANCRS_TotalPositive":      { "type": "number",  "description": "PANCRS: Total positive coping score" },
                "PANCRS_TotalNegative":      { "type": "number",  "description": "PANCRS: Total negative coping score" },
                "PHQ9_q1":                   { "type": "integer", "description": "PHQ-9 Q1: Little interest or pleasure" },
                "PHQ9_q2":                   { "type": "integer", "description": "PHQ-9 Q2: Feeling down or hopeless" },
                "PHQ9_q3":                   { "type": "integer", "description": "PHQ-9 Q3: Sleep issues" },
                "PHQ9_q4":                   { "type": "integer", "description": "PHQ-9 Q4: Tired or little energy" },
                "PHQ9_q5":                   { "type": "integer", "description": "PHQ-9 Q5: Appetite changes" },
                "PHQ9_q6":                   { "type": "integer", "description": "PHQ-9 Q6: Self-image issues" },
                "PHQ9_q7":                   { "type": "integer", "description": "PHQ-9 Q7: Concentration issues" },
                "PHQ9_q8":                   { "type": "integer", "description": "PHQ-9 Q8: Psychomotor changes" },
                "PHQ9_q9":                   { "type": "integer", "description": "PHQ-9 Q9: Suicidal thoughts" },
                "PHQ9_Total":                { "type": "integer", "description": "PHQ-9 total score" },
                "Postcode":                  { "type": "string",  "description": "Residential postcode" },
                "Religion":                  { "type": "string",  "description": "Religious affiliation" },
                "Sex":                       { "type": "string",  "description": "Sex assigned at birth" },
                "TIPI_Agreeableness":        { "type": "number",  "description": "TIPI: Agreeableness score" },
                "TIPI_Conscientiousness":    { "type": "number",  "description": "TIPI: Conscientiousness score" },
                "TIPI_Extraversion":         { "type": "number",  "description": "TIPI: Extraversion score" },
                "TIPI_Neuroticism":          { "type": "number",  "description": "TIPI: Neuroticism score" },
                "TIPI_Openness":             { "type": "number",  "description": "TIPI: Openness to experience score" }
            },
            "required": [
                "Age","CountryOfBirth","CountryOfBirthFather","CountryOfBirthMother",
                "EducationLevel","EmploymentStatus","Ethnicity","Gender","Nationality",
                "PANCRS_Affirmation","PANCRS_EnhancingFriendship","PANCRS_FrequencyNegative",
                "PANCRS_FrequencyPositive","PANCRS_InhibitingHappiness","PANCRS_ProblemSolving",
                "PANCRS_Slack","PANCRS_TotalFrequency","PANCRS_TotalPositive",
                "PANCRS_TotalNegative","PHQ9_q1","PHQ9_q2","PHQ9_q3","PHQ9_q4",
                "PHQ9_q5","PHQ9_q6","PHQ9_q7","PHQ9_q8","PHQ9_q9","PHQ9_Total",
                "Postcode","Religion","Sex","TIPI_Agreeableness","TIPI_Conscientiousness",
                "TIPI_Extraversion","TIPI_Neuroticism","TIPI_Openness"
            ],
            "additionalProperties": False
        }
    }
}

# =================================================
# Prompting
# =================================================
DATABASE_DESCRIPTION_DICT = {
    "mimic_iii": "",
    "ppmi": "PPMI Clinical database. The Parkinson's Progression Markers Initiative (PPMI) is an observational, international study designed to establish biomarker‐defined cohorts and identify clinical, imaging, genetic, and biospecimen Parkinson's disease (PD) progression markers to accelerate disease‐modifying therapeutic trials.",
    "ppmi2024": "PPMI Clinical database. The Parkinson's Progression Markers Initiative (PPMI) is an observational, international study designed to establish biomarker‐defined cohorts and identify clinical, imaging, genetic, and biospecimen Parkinson's disease (PD) progression markers to accelerate disease‐modifying therapeutic trials.",
    "adni": "ADNI data set. The Alzheimer's Disease Neuroimaging Initiative (ADNI) is an observational study designed to develop clinical, imaging, genetic, and biochemical biomarkers for the early detection and tracking of Alzheimer's disease (AD).",
    "wellconnect": "WellConnect cohort study dataset. WellConnect is a cohort study on depression patients from Amsterdam, the Netherlands. The cohort study aims to investigate how individual characteristics and group composition influence the formation and strength of social connections in ongoing group interventions for people with depressive symptoms. By collecting detailed data on participants' backgrounds and their social interactions during group sessions, the study will identify which personal trait dis(similarity) predicts social bonding. This information will be used to calibrate a computational model that will guide the formation of future intervention groups, with the goal of enhancing social cohesion (and, in turn, improving depression symptoms) while minimizing the risk of negative effects such as symptom contagion. According to the theory of homophily, we expect people who are more similar to be more likely to form social bonds. However, we also expect symptoms to spread through social interactions and have a negative effect due to the mechanism of co-rumination.",
    "helius": "HELIUS - – HEalthy Life In an Urban Setting – data set is a longitudinal study administered by the AMC and GGD Amsterdam in which a large spectrum of factors that could influence the health of the population of a multi-ethnic city is examined on a large scale. The study populations in HELIUS are Amsterdamers of Dutch, Surinamese, Turkish, Moroccan and Ghanaian descent. Thousands of people are being followed over time. The developments in health, healthcare use and wellbeing of the participants are being studied. Focal points are cardiovascular diseases, diabetes, psychological health and infectious diseases. More than one out of ten residents in our country is of non-Dutch descent and this number will increase. Large health differences exist between people from Dutch and non-western descent. "
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

# # row example Helius
# ROW_EXAMPLE = {
#     "0": {
#         "questionnaire_completed": "yes",
#         "physical_examination_completed": "yes",
#         "date_physical_examination": "2021-05-14",
#         "sex": "female",
#         "age": 52,
#         "migration_generation": "second",
#         "ethnicity": "Surinamese",
#         "ethnicity_surinamese_subgroups": "Creole",
#         "followup_time_helius1_helius2": 5.2,
#         "marital_status": "married",
#         "educational_level": "higher vocational",
#         "working_status": "employed",
#         "occupational_level": "skilled manual",
#         "work_related_recovery_opportunities": 3.8,
#         "quality_of_life_sf12": 48.7,
#         "physical_activity_squash": 1150,
#         "smoking_status": "ex-smoker",
#         "smoking_packyears": 12.5,
#         "alcohol_use_past_12m_binary": "yes",
#         "alcohol_use_past_12m_level": "moderate",
#         "body_weight_perception_scores": 2.4,
#         "health_literacy_sbs_scores": 28,
#         "health_literacy_realmd_scores": 62,
#         "perceived_discrimination": 7,
#         "cigarette_dependence_fagerstrom": 4,
#         "alcohol_dependence_audit": 5,
#         "lifetime_alcohol_dependence": "no",
#         "cannabis_dependence_cudit": 1,
#         "personality_extraversion_neo_ffi": 24,
#         "personality_neuroticism_neo_ffi": 18,
#         "dealing_with_everyday_problems_pearlin_schooler_mastery": 14,
#         "negative_life_events_nemesis": 3,
#         "psychological_stress_interheart": 2.1,
#         "childhood_experiences_nemesis": 4,
#         "ptss_problems_unpleasant_experiences": 1,
#         "depressive_symptoms_phq9": 6,
#         "lifetime_depression": "no",
#         "parental_psychological_history_nemesis": 1,
#         "social_support_ssq_satisfaction": 22
#     }
# }


#row example WellConnect
ROW_EXAMPLE = {
  "0": {
    "PHQ9_q1": 1,
    "PHQ9_q2": 2,
    "PHQ9_q3": 1,
    "PHQ9_q4": 2,
    "PHQ9_q5": 1,
    "PHQ9_q6": 2,
    "PHQ9_q7": 1,
    "PHQ9_q8": 1,
    "PHQ9_q9": 1,
    "PHQ9_Total": 12,
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
    "TIPI_Extraversion": 3.0,
    "TIPI_Agreeableness": 5.5,
    "TIPI_Conscientiousness": 4.0,
    "TIPI_Neuroticism": 2.5,
    "TIPI_Openness": 4.5,
    "PANCRS_Affirmation": 4.00,
    "PANCRS_ProblemSolving": 3.80,
    "PANCRS_EnhancingFriendship": 4.00,
    "PANCRS_TotalPositive": 3.80,
    "PANCRS_WorryAboutEvaluation": 3.20,
    "PANCRS_InhibitingHappiness": 3.00,
    "PANCRS_WorryAboutImpact": 2.80,
    "PANCRS_Slack": 2.40,
    "PANCRS_TotalNegative": 2.80,
    "PANCRS_FrequencyPositive": 3.00,
    "PANCRS_FrequencyNegative": 2.60,
    "PANCRS_TotalFrequency": 2.80,
  }
}

#encode to json to preserve formatting in the prompt (" instead of ')
ROW_EXAMPLE = json.dumps(ROW_EXAMPLE, ensure_ascii=False, indent=2)


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
        "prompt": f"""Give an example table of {N_ROWS} rows from {DATABASE_DESCRIPTION} Only consider patients with mild to moderate depression (so the overall PHQ-9 score must be between 5 and 15). The patients must be individuals from Amsterdam, the Netherlands, so consider the demographic composition of that area. 
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
    },
    "helius_prompt": { 
        "prompt": f"""Give an example table of {N_ROWS} rows from {DATABASE_DESCRIPTION} Only consider individuals from Amsterdam, the Netherlands. 
        The table must have one row by patient, no missing values and include all the following columns:
{COL_PTID}: patient unique identifier, string""" + """
{variables_description}
Return the table as a dictionary in JSON format with keys as index. JSON format strictly requires double quotes for strings. The column names need to be the same as those provided.
Only return the dictionary, do not repeat the question, introduce your answer or comment on it. Do not truncate the table, provide all the rows.

Here is an example for one patient with the associated key of the dictionary to output:
```json
{row_example}
```
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



