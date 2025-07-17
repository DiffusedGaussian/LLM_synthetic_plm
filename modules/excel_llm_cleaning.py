import pandas as pd
import json
import random
import os


from openai import OpenAI


from typing import Dict, List
from pathlib import Path
from collections import Counter


def load_raw(path:Path) -> pd.DataFrame:
   '''Load an excel file with pandas and make sure that the correct header is choosen'''
   df = pd.read_excel(path, header=None, dtype=str)
   # guess header row: first row where ≥70 % cells are non-null & unique
   for i, row in df.iterrows():
       non_null = row.notna().sum()
       unique   = row.nunique(dropna=True)
       header_idx=0
       if non_null / len(row) > 0.7 and unique == non_null:
           header_idx = i
           break
   print(f"Using column-{header_idx} as header.")
   df = pd.read_excel(path, header=header_idx, dtype=str)
   # drop columns that are entirely null or duplicate
   df = df.dropna(axis=1, how="all")
   df = df.loc[:, ~df.columns.duplicated()]
   return df




def build_column_profile(df:pd.DataFrame, sample_rows=30) -> List[Dict]:
   """Extract statistical information about each column and store them in a dict for a sample of entries"""
   profile = []
   for col in df.columns:
       values = df[col].dropna().astype(str)
       sample = random.sample(list(values), min(len(values), sample_rows))
       freq   = Counter(sample).most_common(5)
       profile.append({
           "name":   col,
           "null_pct": 1 - len(values)/len(df),
           "sample": sample,
           "top_freq": freq
       })
   return profile




PLAN_SCHEMA = {
   "type": "object",
   "properties": {
       "columns": {
           "type": "object",
           "patternProperties": {
               ".*": {                      # each header
                   "type": "object",
                   "properties": {
                       "action":     {"enum":["keep","drop","rename"]},
                       "new_name":   {"type":["string","null"]},
                       "boolean_map":{"type":"object"},
                       "type":       {"enum":["int","float","date","str"]},
                       "reason":     {"type":"string"},
                       "confidence": {"type":"number", "minimum":0, "maximum":1},
                   },
                   "required": ["action","confidence"]
               }
           }
       }
   },
   "required": ["columns"]
}
PLAN_SCHEMA["properties"]["implementation_hint"] = {
   "type": "string",
   "description": "Concise Python/pandas pseudo-code that applies the plan"
}
PLAN_SCHEMA["required"].append("implementation_hint")




def llm_plan(profile: list[dict]) -> dict:
   """
   Ask the LLM for a cleaning plan. 
   Input  : column_profile from build_column_profile 
   Output : dict conforming to PLAN_SCHEMA
   """
   SYSTEM = (
   "You are an expert data engineer with deep knowledge of messy Excel exports "
   "from enterprise systems (e.g. SAP, PLM, BOM data). Your task is to produce a JSON cleaning plan. "
   "You analyze column profiles and infer semantic meaning from column names, sample values, and null ratios. "
   "You normalize values (e.g. for booleans like ['X', 'x', '-', null, 'no']), rename cryptic columns, drop useless ones, "
   "and ensure high-quality data for downstream systems. Return only valid JSON according to the given schema. "
   "Be opinionated. Don’t guess — use what you see."
   "Additionally return *implementation_hint*: a ≤20-line Python snippet "
   "(or bullet pseudo-code) showing how to execute the plan with python if applicable pandas."
)
   user_msg = json.dumps({
   "global_context": {
       "dataset_type": "SAP/BOM export",
       "goal": "clean for structured analysis and potential ML ingestion"
   },
   "columns": profile
}, ensure_ascii=False)[:8000]  # truncate safeguard
  
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


   client = OpenAI(api_key=OPENAI_API_KEY)
   resp = client.chat.completions.create(
       model="gpt-4o",
       messages=[
           {"role": "system", "content": SYSTEM},
           {"role": "user",   "content": user_msg}
       ],
       response_format={"type": "json_object"},
       #functions=[{"name": "return_plan", "parameters": PLAN_SCHEMA}],
   )


   return json.loads(resp.choices[0].message.content)
  





