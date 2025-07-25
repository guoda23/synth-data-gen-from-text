import sys
import os
import logging
import pandas as pd
from tqdm import tqdm
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath("src/"))
sys.path.append(script_dir)

import config as conf
from src.parsers.pipeline_parser import pipeline_parser
from src.logger import init_logger
from src.loading import save_csv, save_text
from src.prompt_engineering.prompt_text_to_tab import prompt_synth_tab
from src.prompt_engineering.utils_prompt import parse_prompt
from src.utils import utils_df


def main():
   
    # Initiate parser
    parser = pipeline_parser()
    args = parser.parse_args()
    
    # Initiate logger
    init_logger(level=args.log_level, file=True, file_path="logs/logs.txt")
    logging.info("\n-----Text to tabular SDG with shuffling of columns-----")
    logging.info(f"Model: {conf.SDG_MODEL}")
    logging.info(f"Size of synthetic database: {conf.N_SAMPLE}")
    logging.info(f"Prompt ID: {conf.PROMPT_ID}")
    
    start_time = datetime.now()
    synth_data = []
    list_cols = conf.LIST_FTR
    
    # remove columns from original data not synthetisize
    for col in conf.LIST_FTR_RM:
        list_cols.remove(col)
    pbar = tqdm(total=conf.N_SAMPLE, desc="Synth data queries")
    
    # number of total rows in synthetic dataframe
    n_synth = 0
    while n_synth < conf.N_SAMPLE:
        logging.info(f"Currently {n_synth} rows synthesized out of {conf.N_SAMPLE}")
        # parse prompt by shuffling order of variables
        prompt = parse_prompt(prompt_dict=conf.TEXT2TAB_PROMPT_DICT[conf.PROMPT_ID],
                            prompt_example=conf.ROW_EXAMPLE,
                            var_desc_prompt_dict=conf.VAR_DESC_PROMPT_DICT,
                            ref_key=conf.REFERENTIAL_VAR_NAME,
                            shuffle=True)   
             
        # prompt a synthetic dataset of n_rows7

        df_synth_int = prompt_synth_tab(prompt=prompt,
                        model=conf.SDG_MODEL,
                        n_rows=conf.N_ROWS,
                        n_sample=conf.N_ROWS,
                        show_progress=False)
        
        # verify that the dataframe contains all expected columns 
        all_cols_in_list_bool = all(col in df_synth_int.columns for col in list_cols)
        
        if all_cols_in_list_bool:
            logging.info(f"All column names generated successfully!")
            # remove missing values if any 
            df_synth_int = utils_df.rm_null_rows(df=df_synth_int)
            
            # reorder columns of synthetic dataframe
            df_synth_int = df_synth_int[list_cols]
            synth_data.append(df_synth_int)
            n_synth += len(df_synth_int)
            pbar.update(n_synth)
        else:
            #get missing columns
            missing_cols = [col for col in list_cols if col not in df_synth_int.columns]
            logging.info(f"Not all columns in list. Missing columns: {missing_cols}. \nRetrying...")
            #print generated columns
            logging.info(f"Generated columns: {df_synth_int.columns.tolist()}")
            
    pbar.close()
   
    df_synth = pd.concat(synth_data, axis=0)
    
    # resample the desired size of sample if more
    df_synth = df_synth[:conf.N_SAMPLE]
    time = datetime.now() - start_time
    text_time = f"Execution time: {time}"
    logging.info(text_time)
    
    # saving data (locally)
    if args.save:
        # ensure the output directory exists
        os.makedirs(conf.PATH_SYNTH_DATA, exist_ok=True)

        # 1) save the synthesized CSV
        out_csv = os.path.join(conf.PATH_SYNTH_DATA, conf.FILE_SYNTHESIZED_DATA)
        df_synth.to_csv(out_csv, index=False)
        logging.info(f"Wrote synthetic data to {out_csv}")

        # 2) save the prompt you used
        out_prompt = os.path.join(conf.PATH_SYNTH_DATA, conf.FILE_SYNTHESIZED_DATA_PROMPT)
        with open(out_prompt, "w") as f:
            f.write(prompt)
        logging.info(f"Wrote prompt text to {out_prompt}")

        # 3) save the timing
        out_time = os.path.join(conf.PATH_SYNTH_DATA, conf.FILE_SYNTHESIZED_DATA_TIME)
        with open(out_time, "w") as f:
            f.write(text_time)
        logging.info(f"Wrote timing info to {out_time}")

if __name__ == "__main__":
    
    main()