# Data Converter
import pandas as pd
from utils.logger import app_logger
import os

def convert_format(df, output_path, format_type='csv'):
    """Converts a pandas DataFrame into various file formats."""
    try:
        if format_type.lower() == 'csv':
            if not output_path.endswith('.csv'):
                output_path += '.csv'
            df.to_csv(output_path, index=False)
            
        elif format_type.lower() == 'excel':
            if not output_path.endswith('.xlsx'):
                output_path += '.xlsx'
            # Using xlsxwriter engine
            df.to_excel(output_path, index=False, engine='xlsxwriter')
            
        elif format_type.lower() == 'sql':
            # Create a simple .sql insert statement file using basic iteration
            if not output_path.endswith('.sql'):
                output_path += '.sql'
            table_name = os.path.basename(output_path).replace('.sql', '')
            with open(output_path, 'w') as f:
                f.write(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(df.columns)});\n")
                for index, row in df.iterrows():
                    values = [f"'{str(v)}'" if isinstance(v, str) else str(v) for v in row.values]
                    f.write(f"INSERT INTO {table_name} VALUES ({', '.join(values)});\n")
            
        app_logger.info(f"Dataset successfully converted to {format_type} at {output_path}")
        return output_path
    
    except Exception as e:
        app_logger.error(f"Failed to convert dataset to {format_type}: {e}")
        return None
