import os
import time
import pandas as pd
import numpy as np
from openai import OpenAI
import pdfplumber
import markdown2
import logging
from itertools import product
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class VCSimulator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        logging.basicConfig(level=logging.INFO)
        
    def load_vc_context(self, file_path: str) -> str:
        try:
            if file_path.endswith('.pdf'):
                with pdfplumber.open(file_path) as pdf:
                    return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            elif file_path.endswith('.md'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return markdown2.markdown(f.read())
        except Exception as e:
            logging.error(f"File reading error: {e}")
            return ""

    def generate_startup_descriptions(self, design_grid_path: str) -> pd.DataFrame:
        df = pd.read_csv(design_grid_path)
        for i in range(1, 11):
            df[f'Response_{i}'] = None

        for row in range(len(df)):
            prompt = df['Prompt'][row].replace("(e.g. hardware, life sciences)", "")
            completion = self.client.chat.completions.create(
                model="gpt-4",
                temperature=1,
                n=10,
                messages=[
                    {"role": "system", "content": "Generate detailed startup descriptions."},
                    {"role": "user", "content": prompt}
                ]
            )
            for i, response in enumerate(completion.choices):
                df.loc[row, f'Response_{i+1}'] = response.message.content
            
        return df

    def compute_embeddings(self, df: pd.DataFrame) -> tuple:
        indicator = list(range(1, len(df) + 1))
        company = list(range(1, 11))
        custom_index = [f"{i}.{j}" for i, j in product(indicator, company)]
        
        embedding_df = pd.DataFrame(index=custom_index, columns=['embedding'])
        
        for row in range(len(df)):
            for i in range(1, 11):
                index = f'{row + 1}.{i}'
                response = self.client.embeddings.create(
                    input=df.loc[row, f'Response_{i}'],
                    model="text-embedding-3-large"
                )
                embedding_df.loc[index, 'embedding'] = response.data[0].embedding

        embeddings = np.array(embedding_df['embedding'].tolist())
        cosine_sim = cosine_similarity(embeddings)
        cosine_df = pd.DataFrame(cosine_sim, index=custom_index, columns=custom_index)
        
        return embedding_df, cosine_df

    def get_vc_responses(self, df: pd.DataFrame, vc_context: str, vc_name: str) -> pd.DataFrame:
        responses = []
        
        for row in range(len(df)):
            for company in range(1, 11):
                desc = df.loc[row, f'Response_{company}']
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": f"You are {vc_name}. Use this context for decisions:\n{vc_context}"},
                        {"role": "user", "content": f"Evaluate this startup:\n{desc}"}
                    ],
                    response_format={"type": "json_object"}
                )
                result = response.choices[0].message.content
                responses.append({
                    'scenario_id': row + 1,
                    'company_id': company,
                    **eval(result)
                })
                time.sleep(1)
                
        return pd.DataFrame(responses)

def main():
    simulator = VCSimulator(os.getenv("OPENAI_API_KEY"))
    
    # Generate startup descriptions
    startups_df = simulator.generate_startup_descriptions('VC Design Grid.csv')
    
    # Generate embeddings and similarities
    embedding_df, cosine_df = simulator.compute_embeddings(startups_df)
    
    # Get VC responses
    
    marc_context = simulator.load_vc_context('decode(venturing)/Pmarca Blog Archives.pdf')
    marc_responses = simulator.get_vc_responses(startups_df, marc_context, "Marc Andreessen")
    
    bill_context = simulator.load_vc_context('decode(venturing)/bill gurley.md')
    bill_responses = simulator.get_vc_responses(startups_df, bill_context, "Bill Gurley")
    
    # Save outputs
    embedding_df.to_csv('embeddings.csv')
    cosine_df.to_csv('cosine_similarity.csv')
    pd.concat([marc_responses, bill_responses]).to_csv('vc_investor_responses.csv', index=False)

if __name__ == "__main__":
    main()